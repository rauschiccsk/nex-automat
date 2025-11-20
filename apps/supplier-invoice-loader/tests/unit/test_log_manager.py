"""Tests for log manager system"""

import pytest
import logging
from pathlib import Path
from datetime import datetime, timedelta
import tempfile
import shutil
from src.monitoring import LogManager, LogConfig, setup_logging


@pytest.fixture
def temp_log_dir():
    """Create temporary log directory"""
    temp_dir = Path(tempfile.mkdtemp())
    yield temp_dir
    # Cleanup
    if temp_dir.exists():
        shutil.rmtree(temp_dir)


@pytest.fixture
def log_config(temp_log_dir):
    """Create test log configuration"""
    return LogConfig(
        log_dir=temp_log_dir,
        log_filename="test.log",
        log_level="DEBUG",
        retention_days=7
    )


@pytest.fixture
def log_manager(log_config):
    """Create log manager instance"""
    return LogManager(log_config)


def test_log_manager_initialization(log_manager, temp_log_dir):
    """Test log manager initializes correctly"""
    assert log_manager.config is not None
    assert temp_log_dir.exists()
    assert log_manager.logger is not None


def test_log_directory_creation(temp_log_dir, log_config):
    """Test log directory is created"""
    LogManager(log_config)
    assert temp_log_dir.exists()


def test_logging_to_file(log_manager, temp_log_dir):
    """Test logs are written to file"""
    logger = log_manager.get_logger()
    test_message = "Test log message"

    logger.info(test_message)

    log_file = temp_log_dir / "test.log"
    assert log_file.exists()

    content = log_file.read_text()
    assert test_message in content


def test_log_levels(log_manager):
    """Test different log levels"""
    logger = log_manager.get_logger()

    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    logger.critical("Critical message")

    log_file = log_manager.config.log_dir / log_manager.config.log_filename
    content = log_file.read_text()

    assert "Debug message" in content
    assert "Info message" in content
    assert "Warning message" in content
    assert "Error message" in content
    assert "Critical message" in content


def test_get_log_files(log_manager, temp_log_dir):
    """Test getting list of log files"""
    # Create some log files
    logger = log_manager.get_logger()
    logger.info("Test message")

    log_files = log_manager.get_log_files()
    assert len(log_files) > 0
    assert any("test.log" in str(f) for f in log_files)


def test_log_stats(log_manager):
    """Test log statistics"""
    logger = log_manager.get_logger()
    logger.info("Test message for stats")

    stats = log_manager.get_log_stats()

    assert 'log_directory' in stats
    assert 'total_files' in stats
    assert 'total_size_mb' in stats
    assert stats['total_files'] >= 1


def test_cleanup_old_logs(log_manager, temp_log_dir):
    """Test cleanup of old log files"""
    # Create an old log file
    old_log = temp_log_dir / "old.log"
    old_log.write_text("old content")

    # Set modification time to 40 days ago
    old_time = (datetime.now() - timedelta(days=40)).timestamp()
    old_log.touch()
    import os
    os.utime(old_log, (old_time, old_time))

    # Run cleanup
    deleted = log_manager.cleanup_old_logs(days=30)

    assert deleted >= 1
    assert not old_log.exists()


def test_set_log_level(log_manager):
    """Test changing log level dynamically"""
    log_manager.set_level('WARNING')
    assert log_manager.config.log_level == 'WARNING'

    log_manager.set_level('DEBUG')
    assert log_manager.config.log_level == 'DEBUG'


def test_error_summary(log_manager):
    """Test error summary generation"""
    logger = log_manager.get_logger()

    logger.error("Test error 1")
    logger.error("Test error 2")
    logger.critical("Test critical")

    summary = log_manager.get_error_summary(hours=1)

    assert 'error_count' in summary
    assert 'critical_count' in summary
    assert summary['total_issues'] >= 0


def test_setup_logging_helper(temp_log_dir):
    """Test quick setup helper function"""
    manager = setup_logging(
        log_dir=str(temp_log_dir),
        log_level="INFO",
        console=False
    )

    assert manager is not None
    assert manager.config.log_dir == temp_log_dir


def test_json_logging(temp_log_dir):
    """Test JSON formatted logging"""
    config = LogConfig(
        log_dir=temp_log_dir,
        log_filename="json_test.log",
        use_json=True
    )

    manager = LogManager(config)
    logger = manager.get_logger()

    logger.info("JSON test message")

    log_file = temp_log_dir / "json_test.log"
    content = log_file.read_text()

    # Should contain JSON structure
    assert '"message"' in content or 'JSON test message' in content


def test_named_logger(log_manager):
    """Test getting named logger"""
    logger = log_manager.get_logger("test_module")
    assert logger.name == "test_module"

    logger.info("Named logger test")

    log_file = log_manager.config.log_dir / log_manager.config.log_filename
    content = log_file.read_text()
    assert "Named logger test" in content
