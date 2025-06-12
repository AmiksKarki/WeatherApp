from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field


class WeatherDetail(BaseModel):
    """Weather details model"""
    description: str = Field(..., description="Weather description")
    icon: str = Field(..., description="Weather icon code")
    temperature: float = Field(..., description="Temperature in Celsius")
    feels_like: float = Field(..., description="Feels like temperature in Celsius")
    humidity: int = Field(..., description="Humidity percentage")
    pressure: int = Field(..., description="Atmospheric pressure in hPa")
    wind_speed: float = Field(..., description="Wind speed in m/s")
    clouds: int = Field(..., description="Cloudiness percentage")


class WeatherResponse(BaseModel):
    """Current weather response model"""
    success: bool = Field(True, description="Operation success status")
    city: str = Field(..., description="City name")
    country: str = Field(..., description="Country code")
    weather: WeatherDetail = Field(..., description="Weather details")
    timestamp: int = Field(..., description="Data timestamp (Unix, UTC)")
    timezone: int = Field(..., description="Timezone offset from UTC in seconds")


class ForecastItem(BaseModel):
    """Forecast item model"""
    date: str = Field(..., description="Forecast date (YYYY-MM-DD)")
    time: str = Field(..., description="Forecast time (HH:MM:SS)")
    timestamp: int = Field(..., description="Data timestamp (Unix, UTC)")
    temperature: float = Field(..., description="Temperature in Celsius")
    feels_like: float = Field(..., description="Feels like temperature in Celsius")
    humidity: int = Field(..., description="Humidity percentage")
    pressure: int = Field(..., description="Atmospheric pressure in hPa")
    description: str = Field(..., description="Weather description")
    icon: str = Field(..., description="Weather icon code")
    wind_speed: float = Field(..., description="Wind speed in m/s")
    clouds: int = Field(..., description="Cloudiness percentage")


class ForecastResponse(BaseModel):
    """Forecast response model"""
    success: bool = Field(True, description="Operation success status")
    city: str = Field(..., description="City name")
    country: str = Field(..., description="Country code")
    forecast: List[ForecastItem] = Field(..., description="Forecast items")
    timezone: int = Field(..., description="Timezone offset from UTC in seconds")


class ErrorResponse(BaseModel):
    """Error response model"""
    success: bool = Field(False, description="Operation success status")
    error: str = Field(..., description="Error message")
