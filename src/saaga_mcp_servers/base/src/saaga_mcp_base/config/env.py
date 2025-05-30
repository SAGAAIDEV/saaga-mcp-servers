from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import List, Optional
import os  # Added for os.getenv and os.environ.setdefault


class RedisSettings(BaseSettings):
    URL: str = "redis://localhost:6379/0"
    BACKUP_PATH: Optional[str] = None

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="allow",
        env_prefix="REDIS_",
    )


class CelerySettings(BaseSettings):
    APP_NAME: str = "saaga_mcp_scheduler"
    # Points to environment variables that will be set using REDIS settings
    BROKER_URL_ENV_VAR: str = "CELERY_BROKER_URL_ACTUAL"
    BACKEND_URL_ENV_VAR: str = "CELERY_BACKEND_URL_ACTUAL"
    RESULT_EXPIRES: int = 3600
    TASK_SERIALIZER: str = "json"
    ACCEPT_CONTENT: List[str] = ["json"]
    RESULT_SERIALIZER: str = "json"
    TIMEZONE: str = "UTC"
    ENABLE_UTC: bool = True
    BACKUP_PATH: Optional[str] = None

    def get_broker_url(self) -> str:
        # Fetches the actual broker URL from an env var that will be set dynamically
        return os.getenv(self.BROKER_URL_ENV_VAR, "redis://default_broker_not_set")

    def get_backend_url(self) -> str:
        # Fetches the actual backend URL from an env var that will be set dynamically
        return os.getenv(self.BACKEND_URL_ENV_VAR, "redis://default_backend_not_set")

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="allow",
        env_prefix="CELERY_",
    )


class FlowerSettings(BaseSettings):
    ADDRESS: str = "0.0.0.0"
    PORT: int = 5555
    URL_PREFIX: Optional[str] = None
    BASIC_AUTH: Optional[str] = None  # "user:pass"
    MAX_TASKS: int = 10000
    DB: str = "flower.db"
    # Points to an environment variable that will be set using REDIS settings
    BROKER_API_ENV_VAR: str = "FLOWER_BROKER_API_ACTUAL"
    BACKUP_PATH: Optional[str] = None

    @property
    def BROKER_API(self) -> str:
        # Fetches the actual broker API URL from an env var that will be set dynamically
        return os.getenv(
            self.BROKER_API_ENV_VAR, "redis://default_broker_api_not_set/0"
        )

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="allow",
        env_prefix="FLOWER_",
    )


class Settings(BaseSettings):
    sqldb_path: str = ".db/saaga-mcp-base.sqlite3"

    model_config = ConfigDict(
        env_file=".env",  # Expects .env in the directory where the main script is run
        env_file_encoding="utf-8",
        extra="allow",  # Allow extra inputs
    )


# Instantiate settings objects
settings = Settings()  # Main app settings
REDIS = RedisSettings()
CELERY = CelerySettings()
FLOWER = FlowerSettings()

# Dynamically set environment variables for Celery and Flower based on REDIS settings
# This ensures that Celery and Flower use the same Redis instance defined by REDIS.URL
os.environ[CELERY.BROKER_URL_ENV_VAR] = REDIS.URL
os.environ[CELERY.BACKEND_URL_ENV_VAR] = REDIS.URL
os.environ[FLOWER.BROKER_API_ENV_VAR] = (
    f"{REDIS.URL}/0"  # Flower typically uses DB 0 for API
)

# Expose for easy import by other modules
__all__ = ["settings", "REDIS", "CELERY", "FLOWER"]
