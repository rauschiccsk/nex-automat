#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Entry point for Daily Summary Report
Run via Windows Task Scheduler at 18:00 on workdays
"""

import sys
import os
import logging
from pathlib import Path
from datetime import date

# Add app to path
APP_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(APP_DIR))
sys.path.insert(0, str(APP_DIR.parent.parent))  # Project root for packages

# Load .env first
from pathlib import Path
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent.parent / "supplier-invoice-worker" / ".env"
    if env_path.exists():
        load_dotenv(env_path)
except ImportError:
    pass

from reports.daily_summary import DailySummaryReport
from reports.config import ReportConfig

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(APP_DIR / "logs" / "daily_report.log", encoding="utf-8")
    ]
)
logger = logging.getLogger(__name__)


def load_config() -> ReportConfig:
    """Load configuration from environment/config file"""
    config = ReportConfig(
        # Recipients
        admin_email="rausch@icc.sk",
        customer_emails=[],  # Add customer email here

        # SMTP - from environment or config
        smtp_host=os.environ.get("SMTP_HOST", "smtp.gmail.com"),
        smtp_port=int(os.environ.get("SMTP_PORT", "587")),
        smtp_user=os.environ.get("SMTP_USER", ""),
        smtp_password=os.environ.get("SMTP_PASSWORD", ""),
        from_email=os.environ.get("SMTP_FROM", ""),

        # Database
        db_name="supplier_invoice_staging",
        db_host=os.environ.get("DB_HOST", "localhost"),
        db_port=int(os.environ.get("DB_PORT", "5432")),
        db_user=os.environ.get("DB_USER", "postgres"),

        # Options
        workdays_only=True,
        send_empty_report=True
    )
    return config


def main():
    """Main entry point"""
    logger.info("=" * 50)
    logger.info("Starting Daily Summary Report")
    logger.info("=" * 50)

    try:
        config = load_config()
        report = DailySummaryReport(config)

        # Run for today (or specific date from args)
        report_date = date.today()
        if len(sys.argv) > 1:
            from datetime import datetime
            report_date = datetime.strptime(sys.argv[1], "%Y-%m-%d").date()

        success = report.run(report_date)

        if success:
            logger.info("Report completed successfully")
            sys.exit(0)
        else:
            logger.error("Report failed")
            sys.exit(1)

    except Exception as e:
        logger.exception(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
