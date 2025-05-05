"""Configuration module for the Inequality App API."""
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings.

    These settings can be configured via environment variables.
    """

    # Database
    DATABASE_URL: str

    # API configurations
    API_PREFIX: str = "/api"
    DEBUG: bool = False
    PROJECT_NAME: str = "Inequality App API"
    VERSION: str = "0.1.0"

    # External APIs
    FORBES_API_KEY: Optional[str] = None
    COMPANIES_HOUSE_API_KEY: Optional[str] = None

    # S3-compatible storage
    S3_ENDPOINT: str
    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str
    S3_BUCKET: str = "inequality-data"

    # CORS
    CORS_ORIGINS: str = "*"

    # Cache settings
    REDIS_URL: Optional[str] = None
    CACHE_TTL: int = 3600  # 1 hour

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    ) 