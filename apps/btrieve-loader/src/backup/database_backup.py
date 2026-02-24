"""
Database Backup Module
Handles PostgreSQL database backups with rotation, compression, and verification.
"""

import gzip
import hashlib
import logging
import os
import shutil
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

import yaml


class DatabaseBackup:
    """Handles PostgreSQL database backups with rotation and verification."""

    def __init__(
        self,
        backup_dir: str,
        db_config: dict[str, str],
        retention_days: int = 7,
        retention_weeks: int = 4,
        compression_level: int = 6,
    ):
        """
        Initialize backup manager.

        Args:
            backup_dir: Directory for storing backups
            db_config: Database connection configuration
            retention_days: Number of daily backups to keep
            retention_weeks: Number of weekly backups to keep
            compression_level: Gzip compression level (1-9)
        """
        self.backup_dir = Path(backup_dir)
        self.daily_dir = self.backup_dir / "daily"
        self.weekly_dir = self.backup_dir / "weekly"
        self.db_config = db_config
        self.retention_days = retention_days
        self.retention_weeks = retention_weeks
        self.compression_level = compression_level

        # Setup logging
        self.logger = logging.getLogger(__name__)
        self._setup_logging()

        # Create backup directories
        self._create_directories()

    def _setup_logging(self) -> None:
        """Configure logging for backup operations."""
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler(
                    self.backup_dir / "backup.log",
                    encoding="utf-8",
                ),
            ],
        )

    def _create_directories(self) -> None:
        """Create backup directory structure."""
        self.daily_dir.mkdir(parents=True, exist_ok=True)
        self.weekly_dir.mkdir(parents=True, exist_ok=True)
        self.logger.info(f"Backup directories ready: {self.backup_dir}")

    def create_backup(self, backup_type: str = "daily") -> Path | None:
        """
        Create database backup.

        Args:
            backup_type: Type of backup ('daily' or 'weekly')

        Returns:
            Path to created backup file, or None on failure
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            db_name = self.db_config.get("database", "invoice_staging")

            # Determine backup directory
            target_dir = self.weekly_dir if backup_type == "weekly" else self.daily_dir

            # Backup filename
            backup_file = target_dir / f"backup_{timestamp}_{db_name}.sql"
            compressed_file = Path(f"{backup_file}.gz")

            self.logger.info(f"Starting {backup_type} backup: {compressed_file.name}")

            # Build pg_dump command
            pg_dump_cmd = self._build_pg_dump_command(backup_file)

            # Execute backup
            self.logger.info(f"Executing: {' '.join(pg_dump_cmd)}")
            result = subprocess.run(
                pg_dump_cmd,
                capture_output=True,
                text=True,
                timeout=3600,
            )

            if result.returncode != 0:
                self.logger.error(f"pg_dump failed: {result.stderr}")
                return None

            # Check if backup file was created
            if not backup_file.exists():
                self.logger.error(f"Backup file not created: {backup_file}")
                return None

            backup_size = backup_file.stat().st_size
            self.logger.info(f"Backup created: {backup_size:,} bytes")

            # Compress backup
            compressed_file = self._compress_backup(backup_file)
            if not compressed_file:
                return None

            # Generate checksum
            checksum = self._generate_checksum(compressed_file)
            self._save_checksum(compressed_file, checksum)

            # Verify backup
            if not self._verify_backup(compressed_file):
                self.logger.error("Backup verification failed")
                return None

            self.logger.info(f"Backup completed successfully: {compressed_file.name}")
            return compressed_file

        except subprocess.TimeoutExpired:
            self.logger.error("Backup timeout - operation took too long")
            return None
        except Exception as e:
            self.logger.error(f"Backup failed: {str(e)}", exc_info=True)
            return None

    def _build_pg_dump_command(self, output_file: Path) -> list[str]:
        """Build pg_dump command with connection parameters."""
        cmd = [
            "pg_dump",
            "-h",
            self.db_config.get("host", "localhost"),
            "-p",
            str(self.db_config.get("port", 5432)),
            "-U",
            self.db_config.get("user", "postgres"),
            "-d",
            self.db_config.get("database", "invoice_staging"),
            "-F",
            "p",
            "-f",
            str(output_file),
            "--verbose",
        ]

        os.environ["PGPASSWORD"] = self.db_config.get("password", "")
        return cmd

    def _compress_backup(self, backup_file: Path) -> Path | None:
        """Compress backup file with gzip."""
        try:
            compressed_file = Path(f"{backup_file}.gz")

            self.logger.info(f"Compressing backup (level {self.compression_level})...")

            with open(backup_file, "rb") as f_in:
                with gzip.open(
                    compressed_file, "wb", compresslevel=self.compression_level
                ) as f_out:
                    shutil.copyfileobj(f_in, f_out)

            backup_file.unlink()

            compressed_size = compressed_file.stat().st_size
            self.logger.info(f"Compression complete: {compressed_size:,} bytes")

            return compressed_file

        except Exception as e:
            self.logger.error(f"Compression failed: {str(e)}")
            return None

    def _generate_checksum(self, file_path: Path) -> str:
        """Generate SHA256 checksum for file."""
        sha256 = hashlib.sha256()

        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                sha256.update(chunk)

        return sha256.hexdigest()

    def _save_checksum(self, backup_file: Path, checksum: str) -> None:
        """Save checksum to file."""
        checksum_file = Path(f"{backup_file}.sha256")

        with open(checksum_file, "w", encoding="utf-8") as f:
            f.write(f"{checksum}  {backup_file.name}\n")

        self.logger.info(f"Checksum saved: {checksum_file.name}")

    def _verify_backup(self, backup_file: Path) -> bool:
        """Verify backup file integrity."""
        try:
            checksum_file = Path(f"{backup_file}.sha256")

            if not checksum_file.exists():
                self.logger.warning("Checksum file not found")
                return False

            with open(checksum_file, encoding="utf-8") as f:
                stored_checksum = f.read().split()[0]

            current_checksum = self._generate_checksum(backup_file)

            if stored_checksum != current_checksum:
                self.logger.error("Checksum mismatch!")
                return False

            with gzip.open(backup_file, "rb") as f:
                f.read(1024)

            self.logger.info("Backup verification successful")
            return True

        except Exception as e:
            self.logger.error(f"Verification failed: {str(e)}")
            return False

    def rotate_backups(self) -> tuple[int, int]:
        """Remove old backups based on retention policy."""
        daily_removed = self._rotate_directory(self.daily_dir, self.retention_days)
        weekly_removed = self._rotate_directory(
            self.weekly_dir, self.retention_weeks * 7
        )

        self.logger.info(
            f"Rotation complete: {daily_removed} daily, {weekly_removed} weekly removed"
        )
        return daily_removed, weekly_removed

    def _rotate_directory(self, directory: Path, max_age_days: int) -> int:
        """Remove old backup files from directory."""
        removed = 0
        cutoff_date = datetime.now() - timedelta(days=max_age_days)

        for backup_file in directory.glob("backup_*.sql.gz"):
            try:
                timestamp_str = (
                    backup_file.stem.split("_")[1] + backup_file.stem.split("_")[2]
                )
                file_date = datetime.strptime(timestamp_str, "%Y%m%d%H%M%S")

                if file_date < cutoff_date:
                    backup_file.unlink()
                    checksum_file = Path(f"{backup_file}.sha256")
                    if checksum_file.exists():
                        checksum_file.unlink()

                    removed += 1
                    self.logger.info(f"Removed old backup: {backup_file.name}")

            except Exception as e:
                self.logger.warning(f"Failed to process {backup_file.name}: {str(e)}")

        return removed

    def list_backups(self) -> dict[str, list[dict[str, str]]]:
        """List all available backups."""
        return {
            "daily": self._list_directory_backups(self.daily_dir),
            "weekly": self._list_directory_backups(self.weekly_dir),
        }

    def _list_directory_backups(self, directory: Path) -> list[dict[str, str]]:
        """List backups in directory."""
        backups = []

        for backup_file in sorted(directory.glob("backup_*.sql.gz"), reverse=True):
            checksum_file = Path(f"{backup_file}.sha256")

            backup_info = {
                "filename": backup_file.name,
                "path": str(backup_file),
                "size": backup_file.stat().st_size,
                "created": datetime.fromtimestamp(
                    backup_file.stat().st_mtime
                ).isoformat(),
                "verified": checksum_file.exists(),
            }

            backups.append(backup_info)

        return backups


def load_config(config_path: str) -> dict:
    """Load configuration from YAML file."""
    with open(config_path, encoding="utf-8") as f:
        return yaml.safe_load(f)
