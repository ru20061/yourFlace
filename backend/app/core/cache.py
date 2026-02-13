from typing import Optional, Any
import json
from redis.asyncio import Redis
from app.config import settings

class RedisClient:
    def __init__(self):
        self.redis: Optional[Redis] = None
        self._pubsub_redis: Optional[Redis] = None

    async def initialize(self):
        self.redis = await Redis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True,
            max_connections=settings.REDIS_MAX_CONNECTIONS
        )
        # Pub/Sub 전용 연결 (구독 중 블로킹되므로 별도 연결 필요)
        self._pubsub_redis = await Redis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True,
        )

    async def close(self):
        if self._pubsub_redis:
            await self._pubsub_redis.close()
        if self.redis:
            await self.redis.close()

    # --- Pub/Sub ---

    async def publish(self, channel: str, message: dict) -> int:
        """채널에 메시지 발행"""
        return await self.redis.publish(channel, json.dumps(message))

    def subscriber(self):
        """Pub/Sub 구독자 반환 (전용 연결 사용)"""
        return self._pubsub_redis.pubsub()
    
    async def get(self, key: str) -> Optional[Any]:
        value = await self.redis.get(key)
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
        return None
    
    async def set(
        self, 
        key: str, 
        value: Any, 
        expire: Optional[int] = None
    ) -> bool:
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        return await self.redis.set(key, value, ex=expire)
    
    async def delete(self, key: str) -> int:
        return await self.redis.delete(key)
    
    async def exists(self, key: str) -> bool:
        return await self.redis.exists(key)
    
    async def incr(self, key: str) -> int:
        return await self.redis.incr(key)
    
    async def expire(self, key: str, seconds: int) -> bool:
        return await self.redis.expire(key, seconds)
    
    async def keys(self, pattern: str) -> list:
        return await self.redis.keys(pattern)
    
    async def delete_pattern(self, pattern: str) -> int:
        keys = await self.keys(pattern)
        if keys:
            return await self.redis.delete(*keys)
        return 0

redis_client = RedisClient()
