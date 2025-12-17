#!/usr/bin/env python
"""
Create BaseWindow and SettingsRepository for shared-pyside6 package.
Phase 2 of PySide6 migration.
"""
import os
from pathlib import Path

BASE_DIR = Path(r"C:\Development\nex-automat")
PACKAGE_DIR = BASE_DIR / "packages" / "shared-pyside6" / "shared_pyside6"


def create_file(path: Path, content: str) -> None:
    """Create file with content."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"✅ Created: {path.relative_to(BASE_DIR)}")


def main():
    print("=" * 60)
    print("Phase 2: Creating BaseWindow for PySide6")
    print("=" * 60)

    # === SettingsRepository ===
    create_file(PACKAGE_DIR / "database" / "settings_repository.py", '''"""
SettingsRepository - Repository for user settings persistence.
Handles window and grid settings storage in SQLite.
"""
import json
import sqlite3
from pathlib import Path
from typing import Any


class SettingsRepository:
    """
    Repository for persisting user settings.

    Uses SQLite for storage with JSON serialization.
    Singleton pattern - one instance per database path.

    Usage:
        repo = SettingsRepository()
        repo.save_window_settings("main_window", "user1", {...})
        settings = repo.load_window_settings("main_window", "user1")
    """

    _instances: dict[str, "SettingsRepository"] = {}

    def __new__(cls, db_path: str | Path | None = None):
        if db_path is None:
            db_path = Path.home() / ".nex-automat" / "settings.db"
        db_path = Path(db_path)

        key = str(db_path)
        if key not in cls._instances:
            instance = super().__new__(cls)
            instance._db_path = db_path
            instance._initialized = False
            cls._instances[key] = instance
        return cls._instances[key]

    def __init__(self, db_path: str | Path | None = None):
        if self._initialized:
            return
        self._init_db()
        self._initialized = True

    def _init_db(self) -> None:
        """Initialize database and create tables if not exists."""
        self._db_path.parent.mkdir(parents=True, exist_ok=True)

        with sqlite3.connect(self._db_path) as conn:
            cursor = conn.cursor()

            # Window settings table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS window_settings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    window_name TEXT NOT NULL,
                    user_id TEXT NOT NULL,
                    x INTEGER,
                    y INTEGER,
                    width INTEGER,
                    height INTEGER,
                    is_maximized INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(window_name, user_id)
                )
            """)

            # Grid settings table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS grid_settings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    window_name TEXT NOT NULL,
                    grid_name TEXT NOT NULL,
                    user_id TEXT NOT NULL,
                    settings TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(window_name, grid_name, user_id)
                )
            """)

            conn.commit()

    # === Window Settings ===

    def save_window_settings(
        self,
        window_name: str,
        user_id: str,
        x: int,
        y: int,
        width: int,
        height: int,
        is_maximized: bool = False
    ) -> bool:
        """
        Save window settings.

        Args:
            window_name: Unique window identifier
            user_id: User identifier
            x, y: Window position
            width, height: Window size
            is_maximized: Whether window is maximized

        Returns:
            True if successful
        """
        try:
            with sqlite3.connect(self._db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO window_settings 
                        (window_name, user_id, x, y, width, height, is_maximized, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                    ON CONFLICT(window_name, user_id) DO UPDATE SET
                        x = excluded.x,
                        y = excluded.y,
                        width = excluded.width,
                        height = excluded.height,
                        is_maximized = excluded.is_maximized,
                        updated_at = CURRENT_TIMESTAMP
                """, (window_name, user_id, x, y, width, height, int(is_maximized)))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error saving window settings: {e}")
            return False

    def load_window_settings(
        self,
        window_name: str,
        user_id: str
    ) -> dict[str, Any] | None:
        """
        Load window settings.

        Args:
            window_name: Unique window identifier
            user_id: User identifier

        Returns:
            Dict with x, y, width, height, is_maximized or None
        """
        try:
            with sqlite3.connect(self._db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT x, y, width, height, is_maximized
                    FROM window_settings
                    WHERE window_name = ? AND user_id = ?
                """, (window_name, user_id))
                row = cursor.fetchone()

                if row:
                    return {
                        "x": row[0],
                        "y": row[1],
                        "width": row[2],
                        "height": row[3],
                        "is_maximized": bool(row[4])
                    }
                return None
        except Exception as e:
            print(f"Error loading window settings: {e}")
            return None

    def delete_window_settings(self, window_name: str, user_id: str) -> bool:
        """Delete window settings."""
        try:
            with sqlite3.connect(self._db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    DELETE FROM window_settings
                    WHERE window_name = ? AND user_id = ?
                """, (window_name, user_id))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error deleting window settings: {e}")
            return False

    # === Grid Settings ===

    def save_grid_settings(
        self,
        window_name: str,
        grid_name: str,
        user_id: str,
        settings: dict[str, Any]
    ) -> bool:
        """
        Save grid settings as JSON.

        Args:
            window_name: Window identifier
            grid_name: Grid identifier
            user_id: User identifier
            settings: Dict with grid settings

        Returns:
            True if successful
        """
        try:
            settings_json = json.dumps(settings, ensure_ascii=False)
            with sqlite3.connect(self._db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO grid_settings 
                        (window_name, grid_name, user_id, settings, updated_at)
                    VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
                    ON CONFLICT(window_name, grid_name, user_id) DO UPDATE SET
                        settings = excluded.settings,
                        updated_at = CURRENT_TIMESTAMP
                """, (window_name, grid_name, user_id, settings_json))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error saving grid settings: {e}")
            return False

    def load_grid_settings(
        self,
        window_name: str,
        grid_name: str,
        user_id: str
    ) -> dict[str, Any] | None:
        """
        Load grid settings.

        Args:
            window_name: Window identifier
            grid_name: Grid identifier
            user_id: User identifier

        Returns:
            Dict with grid settings or None
        """
        try:
            with sqlite3.connect(self._db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT settings
                    FROM grid_settings
                    WHERE window_name = ? AND grid_name = ? AND user_id = ?
                """, (window_name, grid_name, user_id))
                row = cursor.fetchone()

                if row:
                    return json.loads(row[0])
                return None
        except Exception as e:
            print(f"Error loading grid settings: {e}")
            return None

    def delete_grid_settings(
        self,
        window_name: str,
        grid_name: str,
        user_id: str
    ) -> bool:
        """Delete grid settings."""
        try:
            with sqlite3.connect(self._db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    DELETE FROM grid_settings
                    WHERE window_name = ? AND grid_name = ? AND user_id = ?
                """, (window_name, grid_name, user_id))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error deleting grid settings: {e}")
            return False
''')

    # === BaseWindow ===
    create_file(PACKAGE_DIR / "ui" / "base_window.py", '''"""
BaseWindow - Base class for all windows with persistence.
PySide6 version for NEX Automat.
"""
from PySide6.QtWidgets import QMainWindow, QWidget, QApplication
from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QScreen

from shared_pyside6.database import SettingsRepository


class BaseWindow(QMainWindow):
    """
    Base class for all windows in NEX Automat system.

    Features:
    - Automatic window settings load on open
    - Automatic window settings save on close
    - Position validation (multi-monitor support)
    - Maximize state persistence
    - Multi-user support (user_id)

    Usage:
        class MyWindow(BaseWindow):
            def __init__(self):
                super().__init__(
                    window_name="my_unique_window",
                    default_size=(800, 600),
                    default_pos=(100, 100)
                )
                self._setup_ui()
    """

    def __init__(
        self,
        window_name: str,
        default_size: tuple[int, int] = (800, 600),
        default_pos: tuple[int, int] = (100, 100),
        user_id: str = "default",
        auto_load: bool = True,
        parent: QWidget | None = None
    ):
        """
        Initialize BaseWindow.

        Args:
            window_name: Unique window identifier (e.g., "invoice_editor_main")
            default_size: Default size (width, height) if no settings
            default_pos: Default position (x, y) if no settings
            user_id: User ID for multi-user support
            auto_load: If True, automatically load settings
            parent: Parent widget
        """
        super().__init__(parent)

        self._window_name = window_name
        self._default_size = default_size
        self._default_pos = default_pos
        self._user_id = user_id
        self._repository = SettingsRepository()

        # Set default geometry
        self.resize(*default_size)
        self.move(*default_pos)

        if auto_load:
            self._load_and_apply_settings()

    @property
    def window_name(self) -> str:
        """Return window name."""
        return self._window_name

    def _load_and_apply_settings(self) -> None:
        """Load and apply window settings from DB."""
        settings = self._repository.load_window_settings(
            self._window_name, 
            self._user_id
        )

        if settings:
            # Validate position is on visible screen
            x, y = settings["x"], settings["y"]
            width, height = settings["width"], settings["height"]

            if self._is_position_valid(x, y, width, height):
                self.setGeometry(x, y, width, height)
            else:
                # Position not valid, use default
                self.resize(*self._default_size)
                self.move(*self._default_pos)

            # Restore maximized state
            if settings.get("is_maximized", False):
                self.showMaximized()

    def _is_position_valid(self, x: int, y: int, width: int, height: int) -> bool:
        """
        Check if position is valid (visible on any screen).

        Args:
            x, y: Position
            width, height: Size

        Returns:
            True if at least 50x50 pixels are visible on some screen
        """
        window_rect = QRect(x, y, width, height)

        for screen in QApplication.screens():
            screen_rect = screen.availableGeometry()
            intersection = window_rect.intersected(screen_rect)

            # At least 50x50 pixels must be visible
            if intersection.width() >= 50 and intersection.height() >= 50:
                return True

        return False

    def _save_settings(self) -> None:
        """Save window settings to DB."""
        # Don't save if minimized
        if self.isMinimized():
            return

        is_maximized = self.isMaximized()

        # If maximized, save normal geometry
        if is_maximized:
            geometry = self.normalGeometry()
        else:
            geometry = self.geometry()

        self._repository.save_window_settings(
            window_name=self._window_name,
            user_id=self._user_id,
            x=geometry.x(),
            y=geometry.y(),
            width=geometry.width(),
            height=geometry.height(),
            is_maximized=is_maximized
        )

    def closeEvent(self, event) -> None:
        """Override closeEvent to save settings."""
        self._save_settings()
        super().closeEvent(event)

    def save_window_settings(self) -> None:
        """Manual save window settings (e.g., for Apply button)."""
        self._save_settings()

    def reload_window_settings(self) -> None:
        """Manual reload window settings."""
        self._load_and_apply_settings()

    def get_window_settings(self) -> dict | None:
        """
        Get current window settings from DB.

        Returns:
            dict: Settings or None
        """
        return self._repository.load_window_settings(
            self._window_name,
            self._user_id
        )

    def delete_window_settings(self) -> None:
        """Delete window settings from DB."""
        self._repository.delete_window_settings(
            self._window_name,
            self._user_id
        )
''')

    # === Update database __init__.py ===
    create_file(PACKAGE_DIR / "database" / "__init__.py", '''"""
Database utilities for NEX Automat.

Classes:
    SettingsRepository: Repository for user settings persistence
"""
from shared_pyside6.database.settings_repository import SettingsRepository

__all__ = ["SettingsRepository"]
''')

    # === Test for BaseWindow ===
    create_file(BASE_DIR / "packages" / "shared-pyside6" / "tests" / "test_base_window.py", '''"""Tests for BaseWindow."""
import pytest
import tempfile
from pathlib import Path

from shared_pyside6.database import SettingsRepository
from shared_pyside6.ui import BaseWindow


@pytest.fixture
def temp_db():
    """Create temporary database."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test_settings.db"
        yield db_path


@pytest.fixture
def repository(temp_db):
    """Create repository with temp database."""
    # Clear singleton for testing
    SettingsRepository._instances.clear()
    return SettingsRepository(temp_db)


class TestSettingsRepository:
    """Tests for SettingsRepository."""

    def test_save_and_load_window_settings(self, repository):
        """Test saving and loading window settings."""
        repository.save_window_settings(
            window_name="test_window",
            user_id="user1",
            x=100, y=200,
            width=800, height=600,
            is_maximized=False
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
        repository.save_window_settings(
            "test_window", "user1", 100, 200, 800, 600, False
        )
        repository.save_window_settings(
            "test_window", "user1", 150, 250, 1024, 768, True
        )

        settings = repository.load_window_settings("test_window", "user1")

        assert settings["x"] == 150
        assert settings["y"] == 250
        assert settings["width"] == 1024
        assert settings["height"] == 768
        assert settings["is_maximized"] is True

    def test_multi_user_isolation(self, repository):
        """Test that different users have separate settings."""
        repository.save_window_settings(
            "test_window", "user1", 100, 100, 800, 600, False
        )
        repository.save_window_settings(
            "test_window", "user2", 200, 200, 1024, 768, True
        )

        settings1 = repository.load_window_settings("test_window", "user1")
        settings2 = repository.load_window_settings("test_window", "user2")

        assert settings1["x"] == 100
        assert settings2["x"] == 200

    def test_delete_window_settings(self, repository):
        """Test deleting window settings."""
        repository.save_window_settings(
            "test_window", "user1", 100, 200, 800, 600, False
        )
        repository.delete_window_settings("test_window", "user1")

        settings = repository.load_window_settings("test_window", "user1")
        assert settings is None

    def test_save_and_load_grid_settings(self, repository):
        """Test saving and loading grid settings."""
        grid_settings = {
            "column_widths": {0: 100, 1: 200},
            "column_order": [0, 1, 2],
            "active_column": 1
        }

        repository.save_grid_settings(
            window_name="test_window",
            grid_name="test_grid",
            user_id="user1",
            settings=grid_settings
        )

        loaded = repository.load_grid_settings("test_window", "test_grid", "user1")

        assert loaded is not None
        assert loaded["column_widths"] == {0: 100, 1: 200}
        assert loaded["column_order"] == [0, 1, 2]
        assert loaded["active_column"] == 1
''')

    print()
    print("=" * 60)
    print("✅ Phase 2 complete!")
    print("=" * 60)
    print()
    print("Created files:")
    print("  - shared_pyside6/database/settings_repository.py")
    print("  - shared_pyside6/ui/base_window.py")
    print("  - tests/test_base_window.py")
    print()
    print("Run tests:")
    print("  cd packages/shared-pyside6")
    print("  python -m pytest tests/test_base_window.py -v")
    print()


if __name__ == "__main__":
    main()