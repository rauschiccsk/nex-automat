"""Tests for BaseWindow."""

import os
import tempfile
from pathlib import Path

import pytest
from shared_pyside6.database import SettingsRepository


@pytest.fixture
def temp_db():
    """Create temporary database path."""
    # Use tempfile to get unique path, but don't use context manager
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)  # Close file descriptor
    os.unlink(path)  # Delete file, we just need the path
    yield Path(path)
    # Cleanup - try to delete, ignore if fails
    try:
        if Path(path).exists():
            os.unlink(path)
    except:
        pass


@pytest.fixture
def repository(temp_db):
    """Create repository with temp database."""
    # Clear singleton for testing
    SettingsRepository._instances.clear()
    repo = SettingsRepository(temp_db)
    yield repo
    # Cleanup
    repo.close()


class TestSettingsRepository:
    """Tests for SettingsRepository."""

    def test_save_and_load_window_settings(self, repository):
        """Test saving and loading window settings."""
        repository.save_window_settings(
            window_name="test_window", user_id="user1", x=100, y=200, width=800, height=600, is_maximized=False
        )

        settings = repository.load_window_settings("test_window", "user1")

        assert settings is not None
        assert settings["x"] == 100
        assert settings["y"] == 200
        assert settings["width"] == 800
        assert settings["height"] == 600
        assert settings["is_maximized"] is False

    def test_load_nonexistent_settings(self, repository):
        """Test loading non-existent settings."""
        settings = repository.load_window_settings("nonexistent", "user1")
        assert settings is None

    def test_update_window_settings(self, repository):
        """Test updating existing settings."""
        repository.save_window_settings("test_window", "user1", 100, 200, 800, 600, False)
        repository.save_window_settings("test_window", "user1", 150, 250, 1024, 768, True)

        settings = repository.load_window_settings("test_window", "user1")

        assert settings["x"] == 150
        assert settings["y"] == 250
        assert settings["width"] == 1024
        assert settings["height"] == 768
        assert settings["is_maximized"] is True

    def test_multi_user_isolation(self, repository):
        """Test that different users have separate settings."""
        repository.save_window_settings("test_window", "user1", 100, 100, 800, 600, False)
        repository.save_window_settings("test_window", "user2", 200, 200, 1024, 768, True)

        settings1 = repository.load_window_settings("test_window", "user1")
        settings2 = repository.load_window_settings("test_window", "user2")

        assert settings1["x"] == 100
        assert settings2["x"] == 200

    def test_delete_window_settings(self, repository):
        """Test deleting window settings."""
        repository.save_window_settings("test_window", "user1", 100, 200, 800, 600, False)
        repository.delete_window_settings("test_window", "user1")

        settings = repository.load_window_settings("test_window", "user1")
        assert settings is None

    def test_save_and_load_grid_settings(self, repository):
        """Test saving and loading grid settings."""
        # Use string keys for JSON compatibility
        grid_settings = {"column_widths": {"0": 100, "1": 200}, "column_order": [0, 1, 2], "active_column": 1}

        repository.save_grid_settings(
            window_name="test_window", grid_name="test_grid", user_id="user1", settings=grid_settings
        )

        loaded = repository.load_grid_settings("test_window", "test_grid", "user1")

        assert loaded is not None
        assert loaded["column_widths"] == {"0": 100, "1": 200}
        assert loaded["column_order"] == [0, 1, 2]
        assert loaded["active_column"] == 1
