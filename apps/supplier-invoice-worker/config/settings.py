"""Supplier Invoice Worker - Configuration Settings."""

from functools import lru_cache

from nex_config.limits import MAX_RETRIES
from nex_config.security import SMTP_HOST, SMTP_PORT
from nex_config.services import FASTAPI_URL, TEMPORAL_PORT
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Temporal Server
    temporal_host: str = "localhost"
    temporal_port: int = TEMPORAL_PORT
    temporal_namespace: str = "default"
    temporal_task_queue: str = "supplier-invoice-queue"

    # IMAP (Gmail)
    imap_host: str = "imap.gmail.com"
    imap_port: int = 993
    imap_user: str = ""
    imap_password: str = ""
    imap_folder: str = "INBOX"

    # FastAPI Invoice Service
    fastapi_url: str = FASTAPI_URL
    ls_api_key: str = ""

    # SMTP Notifications
    smtp_host: str = SMTP_HOST
    smtp_port: int = SMTP_PORT
    smtp_user: str = ""
    smtp_password: str = ""
    notify_email: str = ""

    # Logging
    log_level: str = "INFO"

    # Retry settings
    max_retries: int = MAX_RETRIES
    retry_delay_seconds: int = 5

    @property
    def temporal_address(self) -> str:
        """Return Temporal server address."""
        return f"{self.temporal_host}:{self.temporal_port}"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
