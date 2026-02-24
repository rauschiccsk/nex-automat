"""Report configuration"""

import os
from dataclasses import dataclass, field
from pathlib import Path

# Load .env from supplier-invoice-worker
try:
    from dotenv import load_dotenv

    env_path = Path(__file__).parent.parent.parent / "supplier-invoice-worker" / ".env"
    if env_path.exists():
        load_dotenv(env_path)
        print(f"Loaded .env from: {env_path}")
except ImportError:
    pass  # dotenv not installed


@dataclass
class ReportConfig:
    """Daily report configuration"""

    # Schedule
    send_time: str = "18:00"
    workdays_only: bool = True
    send_empty_report: bool = True

    # Recipients
    admin_email: str = field(
        default_factory=lambda: os.getenv("NOTIFY_EMAIL", "rausch@icc.sk")
    )
    customer_emails: list[str] = field(
        default_factory=lambda: [
            e.strip()
            for e in os.getenv("REPORT_CUSTOMER_EMAIL", "").split(",")
            if e.strip()
        ]
    )

    # SMTP (Gmail SSL on port 465)
    smtp_host: str = field(
        default_factory=lambda: os.getenv("SMTP_HOST", "smtp.gmail.com")
    )
    smtp_port: int = field(default_factory=lambda: int(os.getenv("SMTP_PORT", "465")))
    smtp_user: str = field(default_factory=lambda: os.getenv("SMTP_USER", ""))
    smtp_password: str = field(default_factory=lambda: os.getenv("SMTP_PASSWORD", ""))
    from_email: str = field(default_factory=lambda: os.getenv("SMTP_FROM", ""))

    # Database
    db_name: str = "supplier_invoice_staging"
    db_host: str = field(default_factory=lambda: os.getenv("DB_HOST", "localhost"))
    db_port: int = field(default_factory=lambda: int(os.getenv("DB_PORT", "5432")))
    db_user: str = field(default_factory=lambda: os.getenv("DB_USER", "postgres"))

    @property
    def all_recipients(self) -> list[str]:
        """All email recipients"""
        recipients = [self.admin_email] if self.admin_email else []
        recipients.extend(self.customer_emails)
        return [r for r in recipients if r]
