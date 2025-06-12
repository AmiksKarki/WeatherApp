from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """Create a test client for the app"""
    with TestClient(app) as client:
        yield client


def test_health_check(client):
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


@patch("app.services.weather_service.WeatherService.get_current_weather", new_callable=AsyncMock)
def test_get_weather(mock_get_weather, client):
    """Test the weather endpoint"""
    # Mock the weather service
    mock_weather_data = {
        "success": True,
        "city": "London",
        "country": "GB",
        "weather": {
            "description": "few clouds",
            "icon": "02d",
            "temperature": 18.5,
            "feels_like": 17.9,
            "humidity": 65,
            "pressure": 1013,
            "wind_speed": 3.6,
            "clouds": 20,
        },
        "timestamp": 1619712000,
        "timezone": 3600,
    }
    mock_get_weather.return_value = mock_weather_data

    # Call the API
    response = client.get("/api/weather?city=London")

    # Check response
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["city"] == "London"
    assert data["country"] == "GB"
    assert "weather" in data
    assert data["weather"]["temperature"] == 18.5


@patch("app.services.weather_service.WeatherService.get_forecast", new_callable=AsyncMock)
def test_get_forecast(mock_get_forecast, client):
    """Test the forecast endpoint"""
    # Mock the forecast service
    mock_forecast_data = {
        "success": True,
        "city": "London",
        "country": "GB",
        "forecast": [
            {
                "date": "2023-05-16",
                "time": "12:00:00",
                "timestamp": 1621159200,
                "temperature": 19.2,
                "feels_like": 18.5,
                "humidity": 60,
                "pressure": 1015,
                "description": "scattered clouds",
                "icon": "03d",
                "wind_speed": 4.5,
                "clouds": 40,
            },
            {
                "date": "2023-05-16",
                "time": "15:00:00",
                "timestamp": 1621170000,
                "temperature": 20.5,
                "feels_like": 19.8,
                "humidity": 55,
                "pressure": 1014,
                "description": "broken clouds",
                "icon": "04d",
                "wind_speed": 5.1,
                "clouds": 75,
            },
        ],
        "timezone": 3600,
    }
    mock_get_forecast.return_value = mock_forecast_data

    # Call the API
    response = client.get("/api/forecast?city=London")

    # Check response
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["city"] == "London"
    assert data["country"] == "GB"
    assert "forecast" in data
    assert len(data["forecast"]) == 2
    assert data["forecast"][0]["temperature"] == 19.2
