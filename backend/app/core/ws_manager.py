import asyncio
import json
import logging
from typing import Optional
from fastapi import WebSocket
from app.core.cache import redis_client

logger = logging.getLogger(__name__)


class ConnectionManager:
    def __init__(self):
        # chat_room_id -> {user_id: WebSocket}
        self.room_connections: dict[int, dict[int, WebSocket]] = {}
        # chat_room_id -> asyncio.Task (Redis 구독 리스너)
        self._listeners: dict[int, asyncio.Task] = {}

    # --- 연결 관리 ---

    async def connect(self, chat_room_id: int, user_id: int, websocket: WebSocket):
        """WebSocket 연결 등록 + 온라인 상태 저장"""
        await websocket.accept()

        if chat_room_id not in self.room_connections:
            self.room_connections[chat_room_id] = {}

        self.room_connections[chat_room_id][user_id] = websocket

        # Redis Set에 온라인 유저 추가
        await redis_client.redis.sadd(f"chat:online:{chat_room_id}", str(user_id))

        # 해당 방의 첫 연결이면 Redis Pub/Sub 리스너 시작
        if chat_room_id not in self._listeners:
            self._listeners[chat_room_id] = asyncio.create_task(
                self._listen(chat_room_id)
            )

        # 접속 알림 발행
        await redis_client.publish(f"chat:room:{chat_room_id}", {
            "type": "presence",
            "user_id": user_id,
            "status": "online",
        })

    async def disconnect(self, chat_room_id: int, user_id: int):
        """WebSocket 연결 해제 + 온라인 상태 제거"""
        # 로컬 연결 제거
        if chat_room_id in self.room_connections:
            self.room_connections[chat_room_id].pop(user_id, None)

            # 방에 아무도 없으면 리스너 정리
            if not self.room_connections[chat_room_id]:
                del self.room_connections[chat_room_id]
                await self._stop_listener(chat_room_id)

        # Redis Set에서 온라인 유저 제거
        await redis_client.redis.srem(f"chat:online:{chat_room_id}", str(user_id))

        # 오프라인 알림 발행
        await redis_client.publish(f"chat:room:{chat_room_id}", {
            "type": "presence",
            "user_id": user_id,
            "status": "offline",
        })

    # --- 메시지 브로드캐스트 ---

    async def broadcast_to_room(self, chat_room_id: int, message: dict, exclude_user_id: Optional[int] = None):
        """로컬 서버의 해당 방 접속자에게 메시지 전송"""
        connections = self.room_connections.get(chat_room_id, {})
        dead_connections = []

        for user_id, ws in connections.items():
            if user_id == exclude_user_id:
                continue
            try:
                await ws.send_json(message)
            except Exception:
                dead_connections.append(user_id)

        # 끊어진 연결 정리
        for user_id in dead_connections:
            await self.disconnect(chat_room_id, user_id)

    async def send_to_user(self, chat_room_id: int, user_id: int, message: dict):
        """특정 유저에게 메시지 전송"""
        ws = self.room_connections.get(chat_room_id, {}).get(user_id)
        if ws:
            try:
                await ws.send_json(message)
            except Exception:
                await self.disconnect(chat_room_id, user_id)

    # --- Redis Pub/Sub 리스너 ---

    async def _listen(self, chat_room_id: int):
        """Redis 채널을 구독하고 수신된 메시지를 로컬 클라이언트에 브로드캐스트"""
        pubsub = redis_client.subscriber()
        channel = f"chat:room:{chat_room_id}"

        try:
            await pubsub.subscribe(channel)
            async for raw_message in pubsub.listen():
                if raw_message["type"] != "message":
                    continue
                try:
                    data = json.loads(raw_message["data"])
                    await self.broadcast_to_room(chat_room_id, data)
                except (json.JSONDecodeError, Exception) as e:
                    logger.error(f"Pub/Sub 메시지 처리 오류 (room={chat_room_id}): {e}")
        except asyncio.CancelledError:
            pass
        finally:
            await pubsub.unsubscribe(channel)
            await pubsub.close()

    async def _stop_listener(self, chat_room_id: int):
        """방의 Pub/Sub 리스너 중지"""
        task = self._listeners.pop(chat_room_id, None)
        if task and not task.done():
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass

    # --- 온라인 유저 조회 ---

    async def get_online_users(self, chat_room_id: int) -> list[int]:
        """Redis Set에서 해당 방의 온라인 유저 목록 조회"""
        members = await redis_client.redis.smembers(f"chat:online:{chat_room_id}")
        return [int(uid) for uid in members]

    # --- 정리 ---

    async def close(self):
        """모든 리스너 종료"""
        for chat_room_id in list(self._listeners.keys()):
            await self._stop_listener(chat_room_id)


ws_manager = ConnectionManager()
