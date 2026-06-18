"""Application configuration loaded from environment variables."""
import os
from functools import lru_cache


class Settings:
    """Central configuration object.

    Values are read from environment variables so the same code base can run
    locally (SQLite) and in production (PostgreSQL) without changes.
    """

    def __init__(self) -> None:
        self.app_name: str = os.getenv("APP_NAME", "ZHKG Service API")
        self.database_url: str = os.getenv(
            "DATABASE_URL", "sqlite:///./zhkg.db"
        )
        self.jwt_secret: str = os.getenv("JWT_SECRET", "change-me-in-production")
        self.jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
        self.access_token_expire_minutes: int = int(
            os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
        )
        self.log_level: str = os.getenv("LOG_LEVEL", "INFO")


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance."""
    return Settings()
