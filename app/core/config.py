from typing import List, Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings that are loaded from environment variables"""

    # Application
    PROJECT_NAME: str = "WeatherPy"
    PROJECT_DESCRIPTION: str = "12-Factor FastAPI Weather Service"
    PROJECT_VERSION: str = "0.1.0"

    # API Keys & External Services
    OPENWEATHER_API_KEY: str = Field(
        default_factory=lambda: "dummy_key", description="OpenWeatherMap API key"
    )
    OPENWEATHER_API_URL: str = "https://api.openweathermap.org/data/2.5"

    # Redis Configuration
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: Optional[str] = None  # <-- Make it optional
    REDIS_DB: int = 0
    REDIS_CACHE_TTL: int = 600  # 10 minutes cache time

    # CORS
    ALLOWED_ORIGINS: List[str] = ["*"]

    # Logging
    LOG_LEVEL: str = "INFO"

    # Deployment Mode
    DEBUG: bool = False

    # Model config
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


# Create settings instance
settings = Settings()
