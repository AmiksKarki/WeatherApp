from fastapi import Depends, Request

from app.services.redis_service import RedisService
from app.services.weather_service import WeatherService

async def get_redis_service(request: Request) -> RedisService:
    """
    Dependency to get Redis service.
    
    Uses the service stored in application state
    """
    return request.app.state.redis

async def get_weather_service(
    redis_service: RedisService = Depends(get_redis_service)
) -> WeatherService:
    """
    Dependency to get Weather service.
    
    Creates a new Weather service using the Redis service
    """
    return WeatherService(redis_service=redis_service)
