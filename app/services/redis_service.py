import json
import logging
from typing import Any, Optional

import redis.asyncio as redis

from app.core.config import settings

logger = logging.getLogger("weatherpy")

class RedisService:
    """Service for interacting with Redis cache"""
    
    def __init__(self):
        """Initialize Redis connection"""
        self.redis_client = None
        self.host = settings.REDIS_HOST
        self.port = settings.REDIS_PORT
        self.password = settings.REDIS_PASSWORD
        self.db = settings.REDIS_DB
        self.ttl = settings.REDIS_CACHE_TTL
    
    async def connect(self) -> None:
        """Connect to Redis server"""
        try:
            logger.info(f"Connecting to Redis at {self.host}:{self.port}")
            self.redis_client = redis.Redis(
                host=self.host,
                port=self.port,
                password=self.password,
                db=self.db,
                decode_responses=True,
            )
            # Test connection
            await self.redis_client.ping()
            logger.info("Successfully connected to Redis")
        except redis.ConnectionError as e:
            logger.error(f"Failed to connect to Redis: {e}")
            # Don't raise here - service should work without cache
    
    async def close(self) -> None:
        """Close Redis connection"""
        if self.redis_client:
            await self.redis_client.close()
            logger.info("Redis connection closed")
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from Redis cache"""
        if not self.redis_client:
            return None
        
        try:
            value = await self.redis_client.get(key)
            if value:
                logger.debug(f"Cache hit for key: {key}")
                return json.loads(value)
            logger.debug(f"Cache miss for key: {key}")
            return None
        except Exception as e:
            logger.error(f"Error getting from Redis cache: {e}")
            return None
    
    async def set(self, key: str, value: Any) -> bool:
        """Set value in Redis cache with TTL"""
        if not self.redis_client:
            return False
        
        try:
            serialized_value = json.dumps(value)
            await self.redis_client.set(key, serialized_value, ex=self.ttl)
            logger.debug(f"Cached key: {key} with TTL: {self.ttl}s")
            return True
        except Exception as e:
            logger.error(f"Error setting Redis cache: {e}")
            return False
