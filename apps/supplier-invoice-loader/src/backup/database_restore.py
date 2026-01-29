"""
Database Restore Module for NEX Automat
Restores PostgreSQL databases from backup files

Author: Zoltán Rausch, ICC Komárno
Date: 2025-11-21
"""

import gzip
import hashlib
import logging
import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

import yaml

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def load_config(config_path: str) -> dict:
    """Load configuration from YAML file with defaults."""
    try:
        with open(config_path, encoding="utf-8") as f:
            config = yaml.safe_load(f)
    except Exception as e:
        logger.error(f"Failed to load config from {config_path}: {e}")
        raise

    # Ensure database config exists with defaults
    if "database" not in config:
        config["database"] = {}

    if "postgres" not in config["database"]:
        config["database"]["postgres"] = {
            "host": "localhost",
            "port": 5432,
            "user": "postgres",
            "password": "",
            "database": "invoice_staging",
        }

    return config


class DatabaseRestore:
    """Manages PostgreSQL database restoration from backups"""

    def __init__(self, config_path: str = "config/config.yaml"):
        """
        Initialize DatabaseRestore

        Args:
            config_path: Path to configuration file
        """
        self.config_path = Path(config_path)
        self.config = load_config(str(self.config_path))
        self.backup_dir = Path(self.config.get("backup", {}).get("backup_dir", "backups"))

        # PostgreSQL connection parameters from config.database.postgres
        db_config = self.config.get("database", {}).get("postgres", {})
        self.host = db_config.get("host", "localhost")
        self.port = db_config.get("port", 5432)
        self.database = db_config.get("database", "invoice_staging")
        self.user = db_config.get("user", "postgres")
        self.password = db_config.get("password", "")

        if not all([self.database, self.user]):
            raise ValueError("Missing required database configuration")

    def list_backups(self, backup_type: str = "all") -> list[dict[str, any]]:
        """
        List available backup files

        Args:
            backup_type: Type of backups to list ('daily', 'weekly', 'all')

        Returns:
            List of backup info dictionaries
        """
        backups = []

        # Determine which directories to scan
        if backup_type == "all":
            dirs = [self.backup_dir / "daily", self.backup_dir / "weekly"]
        else:
            dirs = [self.backup_dir / backup_type]

        for backup_dir in dirs:
            if not backup_dir.exists():
                continue

            for backup_file in backup_dir.glob("backup_*.sql.gz"):
                checksum_file = backup_file.with_suffix(".sql.gz.sha256")

                info = {
                    "path": str(backup_file),
                    "name": backup_file.name,
                    "type": backup_dir.name,
                    "size": backup_file.stat().st_size,
                    "modified": datetime.fromtimestamp(backup_file.stat().st_mtime),
                    "has_checksum": checksum_file.exists(),
                }

                backups.append(info)

        # Sort by modification time (newest first)
        backups.sort(key=lambda x: x["modified"], reverse=True)
        return backups

    def verify_backup(self, backup_path: str) -> tuple[bool, str]:
        """
        Verify backup file integrity

        Args:
            backup_path: Path to backup file

        Returns:
            Tuple of (success, message)
        """
        backup_file = Path(backup_path)

        if not backup_file.exists():
            return False, f"Backup file not found: {backup_path}"

        # Check if it's a gzip file
        try:
            with gzip.open(backup_file, "rb") as f:
                f.read(1)
        except Exception as e:
            return False, f"Invalid gzip file: {e}"

        # Verify checksum if available
        checksum_file = backup_file.with_suffix(".sql.gz.sha256")
        if checksum_file.exists():
            try:
                with open(checksum_file) as f:
                    expected_checksum = f.read().strip().split()[0]

                # Calculate actual checksum
                sha256 = hashlib.sha256()
                with open(backup_file, "rb") as f:
                    for chunk in iter(lambda: f.read(8192), b""):
                        sha256.update(chunk)
                actual_checksum = sha256.hexdigest()

                if actual_checksum != expected_checksum:
                    return (
                        False,
                        f"Checksum mismatch: expected {expected_checksum}, got {actual_checksum}",
                    )

                return True, "Backup verified successfully (checksum OK)"
            except Exception as e:
                return False, f"Checksum verification failed: {e}"
        else:
            return True, "Backup verified (gzip OK, no checksum available)"

    def restore_database(
        self, backup_path: str, drop_existing: bool = False, verify_first: bool = True
    ) -> tuple[bool, str]:
        """
        Restore database from backup

        Args:
            backup_path: Path to backup file
            drop_existing: Whether to drop existing database first
            verify_first: Whether to verify backup before restore

        Returns:
            Tuple of (success, message)
        """
        backup_file = Path(backup_path)

        # Verify backup first
        if verify_first:
            logger.info(f"Verifying backup: {backup_path}")
            success, message = self.verify_backup(backup_path)
            if not success:
                return False, f"Backup verification failed: {message}"
            logger.info(message)

        # Drop existing database if requested
        if drop_existing:
            logger.warning(f"Dropping existing database: {self.database}")
            success, message = self._drop_database()
            if not success:
                return False, f"Failed to drop database: {message}"
            logger.info(message)

            # Create new database
            logger.info(f"Creating database: {self.database}")
            success, message = self._create_database()
            if not success:
                return False, f"Failed to create database: {message}"
            logger.info(message)

        # Restore from backup
        logger.info(f"Restoring database from: {backup_path}")
        try:
            # Set environment variable for password
            env = os.environ.copy()
            if self.password:
                env["PGPASSWORD"] = self.password

            # Build psql command
            cmd = [
                "psql",
                "-h",
                self.host,
                "-p",
                str(self.port),
                "-U",
                self.user,
                "-d",
                self.database,
                "-v",
                "ON_ERROR_STOP=1",
            ]

            # Decompress and pipe to psql
            with gzip.open(backup_file, "rb") as f:
                result = subprocess.run(
                    cmd,
                    stdin=f,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    env=env,
                    text=False,
                )

            if result.returncode != 0:
                error_msg = result.stderr.decode("utf-8", errors="ignore")
                return False, f"Restore failed: {error_msg}"

            logger.info("Database restored successfully")
            return True, f"Database restored successfully from {backup_file.name}"

        except Exception as e:
            logger.error(f"Restore failed: {e}")
            return False, f"Restore failed: {e}"

    def _drop_database(self) -> tuple[bool, str]:
        """Drop existing database"""
        try:
            env = os.environ.copy()
            if self.password:
                env["PGPASSWORD"] = self.password

            # Connect to postgres database to drop target database
            cmd = [
                "psql",
                "-h",
                self.host,
                "-p",
                str(self.port),
                "-U",
                self.user,
                "-d",
                "postgres",
                "-c",
                f'DROP DATABASE IF EXISTS "{self.database}";',
            ]

            result = subprocess.run(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, text=True
            )

            if result.returncode != 0:
                return False, result.stderr

            return True, f"Database {self.database} dropped"

        except Exception as e:
            return False, str(e)

    def _create_database(self) -> tuple[bool, str]:
        """Create new database"""
        try:
            env = os.environ.copy()
            if self.password:
                env["PGPASSWORD"] = self.password

            # Connect to postgres database to create target database
            cmd = [
                "psql",
                "-h",
                self.host,
                "-p",
                str(self.port),
                "-U",
                self.user,
                "-d",
                "postgres",
                "-c",
                f'CREATE DATABASE "{self.database}";',
            ]

            result = subprocess.run(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, text=True
            )

            if result.returncode != 0:
                return False, result.stderr

            return True, f"Database {self.database} created"

        except Exception as e:
            return False, str(e)

    def get_restore_point_info(self, backup_path: str) -> dict[str, any]:
        """
        Get information about a restore point

        Args:
            backup_path: Path to backup file

        Returns:
            Dictionary with restore point information
        """
        backup_file = Path(backup_path)

        if not backup_file.exists():
            return {"error": "Backup file not found"}

        # Parse timestamp from filename
        # Format: backup_YYYYMMDD_HHMMSS_dbname.sql.gz
        try:
            parts = backup_file.stem.split("_")
            if len(parts) >= 3:
                date_str = parts[1]
                time_str = parts[2]
                timestamp = datetime.strptime(f"{date_str}_{time_str}", "%Y%m%d_%H%M%S")
            else:
                timestamp = datetime.fromtimestamp(backup_file.stat().st_mtime)
        except:
            timestamp = datetime.fromtimestamp(backup_file.stat().st_mtime)

        # Get file info
        size_bytes = backup_file.stat().st_size
        size_mb = size_bytes / (1024 * 1024)

        # Check verification status
        is_verified, verify_msg = self.verify_backup(backup_path)

        return {
            "path": str(backup_file),
            "name": backup_file.name,
            "timestamp": timestamp,
            "size_bytes": size_bytes,
            "size_mb": round(size_mb, 2),
            "verified": is_verified,
            "verification_message": verify_msg,
        }
