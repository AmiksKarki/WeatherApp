import logging
from typing import Dict, Any, Optional

import httpx

from app.core.config import settings
from app.services.redis_service import RedisService

logger = logging.getLogger("weatherpy")

class WeatherService:
    """Service for retrieving weather data from OpenWeatherMap API"""
    
    def __init__(self, redis_service: RedisService):
        """Initialize weather service with Redis cache"""
        self.api_key = settings.OPENWEATHER_API_KEY
        self.api_url = settings.OPENWEATHER_API_URL
        self.redis_service = redis_service
    
    async def get_current_weather(self, city: str, country_code: Optional[str] = None) -> Dict[str, Any]:
        """Get current weather for a city"""
        # Create cache key
        query = city
        if country_code:
            query = f"{city},{country_code}"
        
        cache_key = f"weather:{query}"
        
        # Try to get from cache first
        cached_data = await self.redis_service.get(cache_key)
        if cached_data:
            logger.info(f"Retrieved weather for {query} from cache")
            return cached_data
        
        # Not in cache, fetch from API
        logger.info(f"Fetching current weather for {query} from OpenWeatherMap")
        
        params = {
            "q": query,
            "appid": self.api_key,
            "units": "metric"  # Use metric units (Celsius)
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.api_url}/weather", params=params)
            
            if response.status_code != 200:
                logger.error(f"OpenWeatherMap API error: {response.text}")
                error_data = response.json()
                return {
                    "success": False,
                    "error": error_data.get("message", "Unknown error"),
                    "status_code": response.status_code
                }
            
            data = response.json()
            
            # Process/transform the data
            result = {
                "success": True,
                "city": data["name"],
                "country": data["sys"]["country"],
                "weather": {
                    "description": data["weather"][0]["description"],
                    "icon": data["weather"][0]["icon"],
                    "temperature": data["main"]["temp"],
                    "feels_like": data["main"]["feels_like"],
                    "humidity": data["main"]["humidity"],
                    "pressure": data["main"]["pressure"],
                    "wind_speed": data["wind"]["speed"],
                    "clouds": data["clouds"]["all"],
                },
                "timestamp": data["dt"],
                "timezone": data["timezone"]
            }
            
            # Store in cache
            await self.redis_service.set(cache_key, result)
            return result
    
    async def get_forecast(self, city: str, country_code: Optional[str] = None) -> Dict[str, Any]:
        """Get 5-day weather forecast for a city"""
        # Create cache key
        query = city
        if country_code:
            query = f"{city},{country_code}"
        
        cache_key = f"forecast:{query}"
        
        # Try to get from cache first
        cached_data = await self.redis_service.get(cache_key)
        if cached_data:
            logger.info(f"Retrieved forecast for {query} from cache")
            return cached_data
        
        # Not in cache, fetch from API
        logger.info(f"Fetching forecast for {query} from OpenWeatherMap")
        
        params = {
            "q": query,
            "appid": self.api_key,
            "units": "metric"  # Use metric units (Celsius)
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.api_url}/forecast", params=params)
            
            if response.status_code != 200:
                logger.error(f"OpenWeatherMap API error: {response.text}")
                error_data = response.json()
                return {
                    "success": False,
                    "error": error_data.get("message", "Unknown error"),
                    "status_code": response.status_code
                }
            
            data = response.json()
            
            # Process the data to group by days and simplify
            result = {
                "success": True,
                "city": data["city"]["name"],
                "country": data["city"]["country"],
                "forecast": self._process_forecast(data["list"]),
                "timezone": data["city"]["timezone"]
            }
            
            # Store in cache
            await self.redis_service.set(cache_key, result)
            return result
    
    def _process_forecast(self, forecast_data: list) -> list:
        """Process the raw forecast data into a more usable format"""
        results = []
        
        for item in forecast_data:
            # Extract date (YYYY-MM-DD) from dt_txt
            date = item["dt_txt"].split(" ")[0]
            
            # Extract time (HH:MM:SS) from dt_txt
            time = item["dt_txt"].split(" ")[1]
            
            forecast_item = {
                "date": date,
                "time": time,
                "timestamp": item["dt"],
                "temperature": item["main"]["temp"],
                "feels_like": item["main"]["feels_like"],
                "humidity": item["main"]["humidity"],
                "pressure": item["main"]["pressure"],
                "description": item["weather"][0]["description"],
                "icon": item["weather"][0]["icon"],
                "wind_speed": item["wind"]["speed"],
                "clouds": item["clouds"]["all"],
            }
            
            results.append(forecast_item)
        
        return results
