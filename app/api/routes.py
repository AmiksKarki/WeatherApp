from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional

from app.models.weather import WeatherResponse, ForecastResponse, ErrorResponse
from app.services.weather_service import WeatherService
from app.api.dependencies import get_weather_service

router = APIRouter()

@router.get(
    "/weather",
    response_model=WeatherResponse,
    responses={404: {"model": ErrorResponse}, 400: {"model": ErrorResponse}},
    summary="Get current weather",
    description="Retrieve current weather data for a specified city"
)
async def get_weather(
    city: str = Query(..., description="City name"),
    country_code: Optional[str] = Query(None, description="Country code (ISO 3166-1 alpha-2)"),
    weather_service: WeatherService = Depends(get_weather_service)
):
    """
    Get current weather for a city.
    
    - **city**: Name of the city
    - **country_code**: Optional ISO 3166-1 alpha-2 country code
    """
    result = await weather_service.get_current_weather(city, country_code)
    
    if not result.get("success", True):
        status_code = result.get("status_code", 400)
        raise HTTPException(
            status_code=status_code,
            detail=result.get("error", "Failed to retrieve weather data")
        )
    
    return result

@router.get(
    "/forecast",
    response_model=ForecastResponse,
    responses={404: {"model": ErrorResponse}, 400: {"model": ErrorResponse}},
    summary="Get 5-day forecast",
    description="Retrieve 5-day forecast data for a specified city"
)
async def get_forecast(
    city: str = Query(..., description="City name"),
    country_code: Optional[str] = Query(None, description="Country code (ISO 3166-1 alpha-2)"),
    weather_service: WeatherService = Depends(get_weather_service)
):
    """
    Get 5-day weather forecast for a city.
    
    - **city**: Name of the city
    - **country_code**: Optional ISO 3166-1 alpha-2 country code
    """
    result = await weather_service.get_forecast(city, country_code)
    
    if not result.get("success", True):
        status_code = result.get("status_code", 400)
        raise HTTPException(
            status_code=status_code,
            detail=result.get("error", "Failed to retrieve forecast data")
        )
    
    return result
