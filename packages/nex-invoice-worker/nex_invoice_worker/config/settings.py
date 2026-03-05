"""Tenant-aware settings for the shared invoice worker.

Loads appropriate settings based on WORKER_TENANT environment variable.
Supplier mode includes IMAP/SMTP settings; Andros mode includes PostgreSQL settings.
"""

from functools import lru_cache

from nex_config.database import DB_NAME_INVOICES, DB_PORT
from nex_config.limits import MAX_RETRIES
from nex_config.paths import ARCHIVE_PATH
from nex_config.services import FASTAPI_URL, TEMPORAL_PORT
from pydantic import ConfigDict
from pydantic_settings import BaseSettings

from nex_invoice_worker.config.tenant import WorkerTenant, get_tenant


# --- Tenant-specific task queue names ---
_TASK_QUEUES = {
    WorkerTenant.SUPPLIER: "supplier-invoice-queue",
    WorkerTenant.ANDROS: "andros-invoice-queue",
}

# --- Tenant-specific customer codes ---
_CUSTOMER_CODES = {
    WorkerTenant.SUPPLIER: "ICC",
    WorkerTenant.ANDROS: "ANDROS",
}


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    Contains both shared and tenant-specific fields. Tenant-specific defaults
    are resolved at instantiation time based on WORKER_TENANT.
    """

    # --- Shared settings ---

    # Temporal Server
    temporal_host: str = "localhost"
    temporal_port: int = TEMPORAL_PORT
    temporal_namespace: str = "default"
    temporal_task_queue: str = ""  # resolved in model_post_init

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

    # Customer code
    customer_code: str = ""  # resolved in model_post_init

    # --- Supplier-mode settings (IMAP/SMTP) ---
    imap_host: str = "imap.gmail.com"
    imap_port: int = 993
    imap_user: str = ""
    imap_password: str = ""
    imap_folder: str = "INBOX"

    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    notify_email: str = ""

    # --- Andros-mode settings (PostgreSQL) ---
    postgres_host: str = "localhost"
    postgres_port: int = DB_PORT
    postgres_db: str = DB_NAME_INVOICES
    postgres_user: str = "postgres"
    postgres_password: str = ""

    def model_post_init(self, __context: object) -> None:
        """Set tenant-specific defaults after initialization."""
        tenant = get_tenant()
        if not self.temporal_task_queue:
            self.temporal_task_queue = _TASK_QUEUES[tenant]
        if not self.customer_code:
            self.customer_code = _CUSTOMER_CODES[tenant]

    @property
    def temporal_address(self) -> str:
        """Return Temporal server address."""
        return f"{self.temporal_host}:{self.temporal_port}"

    @property
    def postgres_dsn(self) -> str:
        """Return PostgreSQL connection string (used in andros mode)."""
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
