"""Application configuration loaded from environment variables."""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings — loaded from .env file or environment."""

    # --- App ---
    APP_NAME: str = "Sales Insight Automator"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # --- CORS ---
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173"

    # --- AI Engine ---
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.0-flash"

    # --- Email (Resend) ---
    RESEND_API_KEY: str = ""
    EMAIL_FROM: str = "Sales Automator <onboarding@resend.dev>"

    # --- Security ---
    API_KEY: str = ""  # Optional: set to enforce X-API-Key header
    RATE_LIMIT: str = "5/minute"
    MAX_FILE_SIZE_MB: int = 10

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Cached settings singleton."""
    return Settings()
