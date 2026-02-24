"""
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
            instance._connection = None
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

        conn = sqlite3.connect(self._db_path)
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
        conn.close()

    def _get_connection(self) -> sqlite3.Connection:
        """Get database connection."""
        return sqlite3.connect(self._db_path)

    def close(self) -> None:
        """Close repository and remove from instances."""
        key = str(self._db_path)
        if key in self._instances:
            del self._instances[key]
        self._initialized = False

    # === Window Settings ===

    def save_window_settings(
        self,
        window_name: str,
        user_id: str,
        x: int,
        y: int,
        width: int,
        height: int,
        is_maximized: bool = False,
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
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
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
            """,
                (window_name, user_id, x, y, width, height, int(is_maximized)),
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error saving window settings: {e}")
            return False

    def load_window_settings(
        self, window_name: str, user_id: str
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
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT x, y, width, height, is_maximized
                FROM window_settings
                WHERE window_name = ? AND user_id = ?
            """,
                (window_name, user_id),
            )
            row = cursor.fetchone()
            conn.close()

            if row:
                return {
                    "x": row[0],
                    "y": row[1],
                    "width": row[2],
                    "height": row[3],
                    "is_maximized": bool(row[4]),
                }
            return None
        except Exception as e:
            print(f"Error loading window settings: {e}")
            return None

    def delete_window_settings(self, window_name: str, user_id: str) -> bool:
        """Delete window settings."""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                DELETE FROM window_settings
                WHERE window_name = ? AND user_id = ?
            """,
                (window_name, user_id),
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting window settings: {e}")
            return False

    # === Grid Settings ===

    def save_grid_settings(
        self, window_name: str, grid_name: str, user_id: str, settings: dict[str, Any]
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
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO grid_settings 
                    (window_name, grid_name, user_id, settings, updated_at)
                VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(window_name, grid_name, user_id) DO UPDATE SET
                    settings = excluded.settings,
                    updated_at = CURRENT_TIMESTAMP
            """,
                (window_name, grid_name, user_id, settings_json),
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error saving grid settings: {e}")
            return False

    def load_grid_settings(
        self, window_name: str, grid_name: str, user_id: str
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
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT settings
                FROM grid_settings
                WHERE window_name = ? AND grid_name = ? AND user_id = ?
            """,
                (window_name, grid_name, user_id),
            )
            row = cursor.fetchone()
            conn.close()

            if row:
                return json.loads(row[0])
            return None
        except Exception as e:
            print(f"Error loading grid settings: {e}")
            return None

    def delete_grid_settings(
        self, window_name: str, grid_name: str, user_id: str
    ) -> bool:
        """Delete grid settings."""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                DELETE FROM grid_settings
                WHERE window_name = ? AND grid_name = ? AND user_id = ?
            """,
                (window_name, grid_name, user_id),
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting grid settings: {e}")
            return False
