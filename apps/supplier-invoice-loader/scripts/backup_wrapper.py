#!/usr/bin/env python3
"""
Backup Wrapper Script
Wraps backup_database.py with logging and error notifications

Author: Zoltán Rausch, ICC Komárno
Date: 2025-11-21
"""

import argparse
import logging
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Setup paths
PROJECT_ROOT = Path(__file__).parent.parent
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)


# Setup logging
def setup_logging(backup_type: str) -> logging.Logger:
    """Setup file and console logging"""
    timestamp = datetime.now().strftime("%Y%m%d")
    log_file = LOG_DIR / f"backup_{backup_type}_{timestamp}.log"

    logger = logging.getLogger("backup_wrapper")
    logger.setLevel(logging.INFO)

    # File handler
    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setLevel(logging.INFO)

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # Formatter
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger


def send_email_notification(subject: str, message: str):
    """Send email notification on backup failure"""
    try:
        # TODO: Implement email sending
        # For now, just log the notification
        logger = logging.getLogger("backup_wrapper")
        logger.warning(f"EMAIL NOTIFICATION: {subject}")
        logger.warning(f"MESSAGE: {message}")

        # Future implementation:
        # import smtplib
        # from email.mime.text import MIMEText
        # ... send email via SMTP

    except Exception as e:
        logger = logging.getLogger("backup_wrapper")
        logger.error(f"Failed to send email notification: {e}")


def main():
    """Main wrapper entry point"""
    parser = argparse.ArgumentParser(description="Backup wrapper with logging")
    parser.add_argument("--type", choices=["daily", "weekly"], default="daily", help="Backup type")
    args = parser.parse_args()

    logger = setup_logging(args.type)

    logger.info("=" * 70)
    logger.info(f"Starting {args.type.upper()} backup")
    logger.info("=" * 70)

    # Build backup command
    backup_script = PROJECT_ROOT / "scripts" / "backup_database.py"
    config_file = PROJECT_ROOT / "config" / "config.yaml"

    cmd = [sys.executable, str(backup_script), "--config", str(config_file), "--type", args.type]

    logger.info(f"Command: {' '.join(cmd)}")

    try:
        # Execute backup
        result = subprocess.run(
            cmd,
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
            timeout=7200,  # 2 hour timeout
        )

        # Log stdout
        if result.stdout:
            for line in result.stdout.splitlines():
                logger.info(f"BACKUP: {line}")

        # Log stderr
        if result.stderr:
            for line in result.stderr.splitlines():
                logger.error(f"BACKUP ERROR: {line}")

        # Check result
        if result.returncode == 0:
            logger.info("=" * 70)
            logger.info("✓ Backup completed successfully")
            logger.info("=" * 70)
            return 0
        else:
            logger.error("=" * 70)
            logger.error(f"✗ Backup failed with return code: {result.returncode}")
            logger.error("=" * 70)

            # Send email notification
            send_email_notification(
                subject=f"NEX Automat - {args.type.capitalize()} Backup Failed",
                message=f"Backup failed with return code {result.returncode}\n\nError output:\n{result.stderr}",
            )

            return result.returncode

    except subprocess.TimeoutExpired:
        logger.error("=" * 70)
        logger.error("✗ Backup timeout (2 hours)")
        logger.error("=" * 70)

        send_email_notification(
            subject=f"NEX Automat - {args.type.capitalize()} Backup Timeout",
            message="Backup exceeded 2 hour timeout limit",
        )

        return 1

    except Exception as e:
        logger.error("=" * 70)
        logger.error(f"✗ Backup failed with exception: {e}")
        logger.error("=" * 70)

        send_email_notification(
            subject=f"NEX Automat - {args.type.capitalize()} Backup Error",
            message=f"Backup failed with exception:\n{e}",
        )

        return 1


if __name__ == "__main__":
    sys.exit(main())
