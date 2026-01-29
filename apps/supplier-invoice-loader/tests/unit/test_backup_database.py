"""
Unit tests for backup_database.py
Tests backup creation, compression, verification, and rotation.
"""

import gzip
import hashlib
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
import yaml
from src.backup.database_backup import DatabaseBackup, load_config


@pytest.fixture
def temp_backup_dir(tmp_path):
    """Create temporary backup directory."""
    backup_dir = tmp_path / "backups"
    backup_dir.mkdir()
    return backup_dir


@pytest.fixture
def db_config():
    """Sample database configuration."""
    return {
        "host": "localhost",
        "port": 5432,
        "user": "postgres",
        "password": "testpass",
        "database": "invoice_staging",
    }


@pytest.fixture
def backup_manager(temp_backup_dir, db_config):
    """Create DatabaseBackup instance for testing."""
    return DatabaseBackup(
        backup_dir=str(temp_backup_dir),
        db_config=db_config,
        retention_days=7,
        retention_weeks=4,
        compression_level=6,
    )


class TestDatabaseBackupInit:
    """Test DatabaseBackup initialization."""

    def test_init_creates_directories(self, temp_backup_dir, db_config):
        """Test that initialization creates required directories."""
        backup = DatabaseBackup(
            backup_dir=str(temp_backup_dir),
            db_config=db_config,
        )

        assert backup.daily_dir.exists()
        assert backup.weekly_dir.exists()
        assert backup.daily_dir == temp_backup_dir / "daily"
        assert backup.weekly_dir == temp_backup_dir / "weekly"

    def test_init_sets_config(self, temp_backup_dir, db_config):
        """Test that configuration is properly stored."""
        backup = DatabaseBackup(
            backup_dir=str(temp_backup_dir),
            db_config=db_config,
            retention_days=10,
            retention_weeks=6,
            compression_level=9,
        )

        assert backup.db_config == db_config
        assert backup.retention_days == 10
        assert backup.retention_weeks == 6
        assert backup.compression_level == 9

    def test_init_creates_log_file(self, temp_backup_dir, db_config):
        """Test that log file is created."""
        DatabaseBackup(
            backup_dir=str(temp_backup_dir),
            db_config=db_config,
        )

        log_file = temp_backup_dir / "backup.log"
        assert log_file.exists()


class TestBackupCreation:
    """Test backup creation functionality."""

    @patch("subprocess.run")
    def test_create_backup_success(self, mock_subprocess, backup_manager, temp_backup_dir):
        """Test successful backup creation."""

        def create_mock_backup(*args, **kwargs):
            cmd = args[0]
            output_file = Path(cmd[cmd.index("-f") + 1])
            with open(output_file, "w") as f:
                f.write("-- PostgreSQL database dump\n")
                f.write("CREATE TABLE test (id INT);\n" * 1000)
            return Mock(returncode=0, stderr="")

        mock_subprocess.side_effect = create_mock_backup
        result = backup_manager.create_backup(backup_type="daily")

        assert result is not None
        assert result.exists()
        assert result.suffix == ".gz"
        assert result.parent == backup_manager.daily_dir

        checksum_file = Path(f"{result}.sha256")
        assert checksum_file.exists()

    @patch("subprocess.run")
    def test_create_backup_pg_dump_failure(self, mock_subprocess, backup_manager):
        """Test backup creation when pg_dump fails."""
        mock_subprocess.return_value = Mock(returncode=1, stderr="pg_dump: error")
        result = backup_manager.create_backup()
        assert result is None

    @patch("subprocess.run")
    def test_create_backup_timeout(self, mock_subprocess, backup_manager):
        """Test backup creation with timeout."""
        mock_subprocess.side_effect = subprocess.TimeoutExpired(cmd="pg_dump", timeout=3600)
        result = backup_manager.create_backup()
        assert result is None

    @patch("subprocess.run")
    def test_create_weekly_backup(self, mock_subprocess, backup_manager):
        """Test weekly backup is stored in correct directory."""

        def create_mock_backup(*args, **kwargs):
            cmd = args[0]
            output_file = Path(cmd[cmd.index("-f") + 1])
            with open(output_file, "w") as f:
                f.write("-- PostgreSQL database dump\n")
            return Mock(returncode=0, stderr="")

        mock_subprocess.side_effect = create_mock_backup
        result = backup_manager.create_backup(backup_type="weekly")

        assert result is not None
        assert result.parent == backup_manager.weekly_dir


class TestCompression:
    """Test backup compression functionality."""

    def test_compress_backup(self, backup_manager, temp_backup_dir):
        """Test backup file compression."""
        test_file = temp_backup_dir / "daily" / "test_backup.sql"
        test_content = "CREATE TABLE test (id INT);\n" * 1000

        with open(test_file, "w") as f:
            f.write(test_content)

        original_size = test_file.stat().st_size
        compressed = backup_manager._compress_backup(test_file)

        assert compressed is not None
        assert compressed.exists()
        assert compressed.suffix == ".gz"
        assert not test_file.exists()
        assert compressed.stat().st_size < original_size

        with gzip.open(compressed, "rt") as f:
            decompressed_content = f.read()
        assert decompressed_content == test_content

    def test_compress_backup_failure(self, backup_manager, temp_backup_dir):
        """Test compression handles non-existent file."""
        non_existent = temp_backup_dir / "daily" / "nonexistent.sql"
        result = backup_manager._compress_backup(non_existent)
        assert result is None


class TestChecksumVerification:
    """Test checksum generation and verification."""

    def test_generate_checksum(self, backup_manager, temp_backup_dir):
        """Test SHA256 checksum generation."""
        test_file = temp_backup_dir / "test.txt"
        test_content = b"Test content for checksum"

        with open(test_file, "wb") as f:
            f.write(test_content)

        checksum = backup_manager._generate_checksum(test_file)
        assert len(checksum) == 64

        expected = hashlib.sha256(test_content).hexdigest()
        assert checksum == expected

    def test_save_and_verify_checksum(self, backup_manager, temp_backup_dir):
        """Test checksum saving and verification."""
        backup_file = temp_backup_dir / "daily" / "test_backup.sql.gz"
        test_content = b"Compressed backup data"

        # Create actual gzip file
        import gzip

        with gzip.open(backup_file, "wb") as f:
            f.write(test_content)

        checksum = backup_manager._generate_checksum(backup_file)
        backup_manager._save_checksum(backup_file, checksum)

        checksum_file = Path(f"{backup_file}.sha256")
        assert checksum_file.exists()
        assert backup_manager._verify_backup(backup_file) is True

    def test_verify_backup_checksum_mismatch(self, backup_manager, temp_backup_dir):
        """Test verification fails when checksum doesn't match."""
        backup_file = temp_backup_dir / "daily" / "test_backup.sql.gz"

        with open(backup_file, "wb") as f:
            f.write(b"Original content")

        checksum = backup_manager._generate_checksum(backup_file)
        backup_manager._save_checksum(backup_file, checksum)

        with open(backup_file, "wb") as f:
            f.write(b"Modified content")

        assert backup_manager._verify_backup(backup_file) is False

    def test_verify_backup_missing_checksum(self, backup_manager, temp_backup_dir):
        """Test verification fails when checksum file missing."""
        backup_file = temp_backup_dir / "daily" / "test_backup.sql.gz"

        with open(backup_file, "wb") as f:
            f.write(b"Test content")

        assert backup_manager._verify_backup(backup_file) is False


class TestBackupRotation:
    """Test backup rotation functionality."""

    def test_rotate_backups_removes_old(self, backup_manager, temp_backup_dir):
        """Test rotation removes old backups."""
        daily_dir = temp_backup_dir / "daily"
        now = datetime.now()

        recent = daily_dir / f"backup_{now.strftime('%Y%m%d_%H%M%S')}_invoice_staging.sql.gz"
        recent.touch()

        old_date = now - timedelta(days=10)
        old = daily_dir / f"backup_{old_date.strftime('%Y%m%d_%H%M%S')}_invoice_staging.sql.gz"
        old.touch()

        Path(f"{recent}.sha256").touch()
        Path(f"{old}.sha256").touch()

        daily_removed, _ = backup_manager.rotate_backups()

        assert not old.exists()
        assert not Path(f"{old}.sha256").exists()
        assert recent.exists()
        assert Path(f"{recent}.sha256").exists()
        assert daily_removed == 1

    def test_rotate_backups_keeps_recent(self, backup_manager, temp_backup_dir):
        """Test rotation keeps recent backups."""
        daily_dir = temp_backup_dir / "daily"
        now = datetime.now()

        for i in range(5):
            backup_date = now - timedelta(days=i)
            backup_file = daily_dir / f"backup_{backup_date.strftime('%Y%m%d_%H%M%S')}_invoice_staging.sql.gz"
            backup_file.touch()

        daily_removed, _ = backup_manager.rotate_backups()
        assert daily_removed == 0
        assert len(list(daily_dir.glob("backup_*.sql.gz"))) == 5


class TestBackupListing:
    """Test backup listing functionality."""

    def test_list_backups_empty(self, backup_manager):
        """Test listing when no backups exist."""
        backups = backup_manager.list_backups()
        assert backups["daily"] == []
        assert backups["weekly"] == []

    def test_list_backups_with_files(self, backup_manager, temp_backup_dir):
        """Test listing backups."""
        daily_dir = temp_backup_dir / "daily"
        weekly_dir = temp_backup_dir / "weekly"

        daily_backup = daily_dir / "backup_20251121_120000_invoice_staging.sql.gz"
        weekly_backup = weekly_dir / "backup_20251114_120000_invoice_staging.sql.gz"

        daily_backup.write_bytes(b"daily backup data")
        weekly_backup.write_bytes(b"weekly backup data")

        Path(f"{daily_backup}.sha256").touch()
        Path(f"{weekly_backup}.sha256").touch()

        backups = backup_manager.list_backups()

        assert len(backups["daily"]) == 1
        assert len(backups["weekly"]) == 1

        daily_info = backups["daily"][0]
        assert daily_info["filename"] == daily_backup.name
        assert daily_info["size"] == len(b"daily backup data")
        assert daily_info["verified"] is True


class TestConfigLoading:
    """Test configuration loading."""

    def test_load_config_success(self, tmp_path):
        """Test loading valid configuration."""
        config_file = tmp_path / "config.yaml"
        config_data = {
            "database": {
                "postgres": {
                    "host": "localhost",
                    "port": 5432,
                    "database": "test_db",
                    "user": "test_user",
                    "password": "test_pass",
                }
            }
        }

        with open(config_file, "w") as f:
            yaml.dump(config_data, f)

        config = load_config(str(config_file))
        assert config == config_data
        assert config["database"]["postgres"]["host"] == "localhost"


class TestCommandInterface:
    """Test command line interface."""

    @patch("subprocess.run")
    def test_pg_dump_command_building(self, mock_subprocess, backup_manager):
        """Test pg_dump command is built correctly."""
        test_file = Path("/tmp/test_backup.sql")
        cmd = backup_manager._build_pg_dump_command(test_file)

        assert "pg_dump" in cmd
        assert "-h" in cmd
        assert "localhost" in cmd
        assert "-p" in cmd
        assert "5432" in cmd
        assert "-U" in cmd
        assert "postgres" in cmd
        assert "-d" in cmd
        assert "invoice_staging" in cmd
        assert "-f" in cmd
        assert str(test_file) in cmd


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
