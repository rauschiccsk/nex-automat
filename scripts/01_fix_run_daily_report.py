#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Fix run_daily_report.py - use .env values instead of hardcoded"""

from pathlib import Path

target = Path("apps/supplier-invoice-loader/scripts/run_daily_report.py")

new_content = '''#!/usr/bin/env python
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
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent.parent / "supplier-invoice-worker" / ".env"
    if env_path.exists():
        load_dotenv(env_path)
        print(f"Loaded .env from: {env_path}")
except ImportError:
    pass

from reports.daily_summary import DailySummaryReport
from reports.config import ReportConfig

# Setup logging
log_dir = APP_DIR / "logs"
log_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(log_dir / "daily_report.log", encoding="utf-8")
    ]
)
logger = logging.getLogger(__name__)


def main():
    """Main entry point"""
    logger.info("=" * 50)
    logger.info("Starting Daily Summary Report")
    logger.info("=" * 50)

    try:
        # Use default ReportConfig - reads from .env automatically
        config = ReportConfig()

        logger.info(f"Recipients: {config.all_recipients}")

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
'''

target.write_text(new_content, encoding="utf-8")
print(f"✅ Fixed: {target}")