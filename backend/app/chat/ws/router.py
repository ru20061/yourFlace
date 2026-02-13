import json
import logging
from datetime import datetime
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from sqlalchemy import update

from app.database import AsyncSessionLocal
from app.core.security import verify_token
from app.core.cache import redis_client
from app.core.ws_manager import ws_manager
from app.auth.users.crud import user_crud
from app.chat.chat_rooms.crud import chat_room_crud
from app.chat.chat_messages.crud import chat_message_crud
from app.chat.chat_messages.schemas import ChatMessageCreate
from app.chat.chat_read_receipts.crud import chat_read_receipt_crud
from app.chat.chat_read_receipts.schemas import ChatReadReceiptCreate
from app.chat.chat_rooms.models import ChatRoom

logger = logging.getLogger(__name__)

router = APIRouter()


async def _authenticate(token: str) -> dict | None:
    """JWT 토큰 검증 후 유저 조회"""
    try:
        payload = verify_token(token, "access")
    except Exception:
        return None

    user_id = payload.get("sub")
    if not user_id:
        return None

    async with AsyncSessionLocal() as db:
        user = await user_crud.get(db, int(user_id))
        if not user or user.status != "active":
            return None
        return {"id": user.id, "status": user.status}


@router.websocket("/{chat_room_id}")
async def websocket_chat(
    websocket: WebSocket,
    chat_room_id: int,
    token: str = Query(...),
):
    """
    실시간 채팅 WebSocket 엔드포인트

    연결: ws://host/yourflace/chat/ws/{chat_room_id}?token=JWT_ACCESS_TOKEN

    클라이언트 → 서버 메시지 타입:
      - {"type": "chat.send", "content": "...", "message_type": "text"}
      - {"type": "typing.start"} / {"type": "typing.stop"}
      - {"type": "read", "message_id": 123}
    """

    # 1) 인증
    user = await _authenticate(token)
    if not user:
        await websocket.close(code=4001, reason="Unauthorized")
        return

    user_id: int = user["id"]

    # 2) 채팅방 존재 확인
    async with AsyncSessionLocal() as db:
        room = await chat_room_crud.get(db, chat_room_id)
        if not room:
            await websocket.close(code=4004, reason="Chat room not found")
            return

    # 3) 연결 등록
    await ws_manager.connect(chat_room_id, user_id, websocket)

    # 4) 온라인 유저 목록을 본인에게 전송
    online_users = await ws_manager.get_online_users(chat_room_id)
    await ws_manager.send_to_user(chat_room_id, user_id, {
        "type": "presence",
        "user_id": user_id,
        "status": "online",
        "online_users": online_users,
    })

    # 5) 메시지 수신 루프
    try:
        while True:
            raw = await websocket.receive_text()
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                await ws_manager.send_to_user(chat_room_id, user_id, {
                    "type": "error",
                    "message": "Invalid JSON",
                })
                continue

            msg_type = data.get("type")

            if msg_type == "chat.send":
                await _handle_chat_send(chat_room_id, user_id, data)

            elif msg_type in ("typing.start", "typing.stop"):
                await _handle_typing(chat_room_id, user_id, msg_type)

            elif msg_type == "read":
                await _handle_read(chat_room_id, user_id, data)

            else:
                await ws_manager.send_to_user(chat_room_id, user_id, {
                    "type": "error",
                    "message": f"Unknown message type: {msg_type}",
                })

    except WebSocketDisconnect:
        pass
    except Exception as e:
        logger.error(f"WebSocket 오류 (room={chat_room_id}, user={user_id}): {e}")
    finally:
        await ws_manager.disconnect(chat_room_id, user_id)


# --- 메시지 핸들러 ---

async def _handle_chat_send(chat_room_id: int, sender_id: int, data: dict):
    """채팅 메시지: DB 저장 → Redis Pub/Sub 발행"""
    content = data.get("content", "").strip()
    message_type = data.get("message_type", "text")

    if not content:
        await ws_manager.send_to_user(chat_room_id, sender_id, {
            "type": "error",
            "message": "Empty content",
        })
        return

    async with AsyncSessionLocal() as db:
        try:
            # 메시지 저장
            msg = await chat_message_crud.create(db, ChatMessageCreate(
                chat_room_id=chat_room_id,
                sender_id=sender_id,
                sender_type="fan",  # TODO: 유저 역할에 따라 동적 설정
                message_type=message_type,
                content=content,
            ))

            # chat_rooms.last_message_at 업데이트
            await db.execute(
                update(ChatRoom)
                .where(ChatRoom.id == chat_room_id)
                .values(last_message_at=datetime.utcnow())
            )
            await db.commit()

            # Redis Pub/Sub으로 발행
            await redis_client.publish(f"chat:room:{chat_room_id}", {
                "type": "chat.message",
                "id": msg.id,
                "chat_room_id": chat_room_id,
                "sender_id": sender_id,
                "sender_type": msg.sender_type,
                "content": msg.content,
                "message_type": msg.message_type,
                "created_at": msg.created_at.isoformat(),
            })

        except Exception as e:
            await db.rollback()
            logger.error(f"메시지 저장 실패: {e}")
            await ws_manager.send_to_user(chat_room_id, sender_id, {
                "type": "error",
                "message": "Failed to save message",
            })


async def _handle_typing(chat_room_id: int, user_id: int, msg_type: str):
    """타이핑 표시: DB 저장 없이 Redis Pub/Sub만 발행"""
    await redis_client.publish(f"chat:room:{chat_room_id}", {
        "type": msg_type,
        "user_id": user_id,
    })


async def _handle_read(chat_room_id: int, user_id: int, data: dict):
    """읽음 처리: DB 저장 → Redis Pub/Sub 발행"""
    message_id = data.get("message_id")
    if not message_id:
        await ws_manager.send_to_user(chat_room_id, user_id, {
            "type": "error",
            "message": "message_id required",
        })
        return

    async with AsyncSessionLocal() as db:
        try:
            receipt = await chat_read_receipt_crud.create(db, ChatReadReceiptCreate(
                chat_message_id=message_id,
                user_id=user_id,
            ))
            await db.commit()

            await redis_client.publish(f"chat:room:{chat_room_id}", {
                "type": "read",
                "message_id": message_id,
                "user_id": user_id,
                "read_at": receipt.read_at.isoformat(),
            })

        except Exception as e:
            await db.rollback()
            logger.error(f"읽음 처리 실패: {e}")
