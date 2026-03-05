"""ANDROS Invoice Worker - Configuration Settings."""

from functools import lru_cache

from nex_config.database import DB_NAME_INVOICES, DB_PORT
from nex_config.limits import MAX_RETRIES
from nex_config.paths import ARCHIVE_PATH
from nex_config.services import FASTAPI_URL, TEMPORAL_PORT
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Temporal Server
    temporal_host: str = "localhost"
    temporal_port: int = TEMPORAL_PORT
    temporal_namespace: str = "default"
    temporal_task_queue: str = "andros-invoice-queue"

    # PostgreSQL Database
    postgres_host: str = "localhost"
    postgres_port: int = DB_PORT
    postgres_db: str = DB_NAME_INVOICES
    postgres_user: str = "postgres"
    postgres_password: str = ""

    # ANDROS Customer Code
    customer_code: str = "ANDROS"

    # FastAPI Invoice Service
    fastapi_url: str = FASTAPI_URL
    ls_api_key: str = ""

    # Archive path
    archive_path: str = ARCHIVE_PATH

    # Logging
    log_level: str = "INFO"

    # Retry settings
    max_retries: int = MAX_RETRIES
    retry_delay_seconds: int = 5

    @property
    def temporal_address(self) -> str:
        """Return Temporal server address."""
        return f"{self.temporal_host}:{self.temporal_port}"

    @property
    def postgres_dsn(self) -> str:
        """Return PostgreSQL connection string."""
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
