"""Application configuration loaded from environment variables via Pydantic Settings."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central configuration for the RetailBot AI application.

    Values are loaded from a ``.env`` file (or actual environment variables).
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- Gemini / LLM ---------------------------------------------------------
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.0-flash"

    # --- Application -----------------------------------------------------------
    app_env: str = "development"
    log_level: str = "INFO"

    # --- Business rules --------------------------------------------------------
    business_hours_start: int = 8
    business_hours_end: int = 20
    reservation_ttl_hours: int = 24
    handoff_confidence_threshold: float = 0.72
    stock_check_timeout_ms: int = 400


@lru_cache
def get_settings() -> Settings:
    """Return a cached ``Settings`` instance (created once per process)."""
    return Settings()
