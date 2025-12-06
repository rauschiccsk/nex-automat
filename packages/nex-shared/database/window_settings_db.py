"""
Window Settings Database Layer
Univerzálne DB operácie pre window persistence.
"""
import sqlite3
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class WindowSettingsDB:
    """
    Database layer for window settings persistence.

    Singleton pattern - jedna inštancia pre celú aplikáciu.
    """

    _instance = None
    _db_path = None

    def __new__(cls, db_path: Optional[str] = None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._db_path = db_path or r"C:\NEX\YEARACT\SYSTEM\SQLITE\window_settings.db"
            cls._instance._init_db()
        return cls._instance

    def _init_db(self):
        """Initialize database and create table if not exists."""
        db_path = Path(self._db_path)

        # Create directory if not exists
        db_path.parent.mkdir(parents=True, exist_ok=True)

        # Create table
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS window_settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                window_name TEXT NOT NULL,
                x INTEGER,
                y INTEGER,
                width INTEGER,
                height INTEGER,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                window_state INTEGER DEFAULT 0,
                UNIQUE(user_id, window_name)
            )
        """)

        conn.commit()
        conn.close()

        logger.info(f"Window settings database initialized: {db_path}")

    def save(self, 
             window_name: str,
             x: int,
             y: int,
             width: int,
             height: int,
             window_state: int = 0,
             user_id: str = "Server") -> bool:
        """
        Save window settings using DELETE + INSERT pattern.

        Args:
            window_name: Unique window identifier
            x, y: Window position
            width, height: Window size
            window_state: 0=normal, 2=maximized
            user_id: User identifier

        Returns:
            bool: True if successful
        """
        try:
            db_path = Path(self._db_path)
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # DELETE existing record
            cursor.execute("""
                DELETE FROM window_settings
                WHERE user_id = ? AND window_name = ?
            """, (user_id, window_name))

            # INSERT new record
            cursor.execute("""
                INSERT INTO window_settings
                (user_id, window_name, x, y, width, height, window_state, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (user_id, window_name, x, y, width, height, window_state, datetime.now()))

            conn.commit()
            conn.close()

            logger.debug(f"Saved window settings: {window_name} at ({x}, {y}) [{width}x{height}] state={window_state}")
            return True

        except Exception as e:
            logger.error(f"Error saving window settings for {window_name}: {e}")
            return False

    def load(self, window_name: str, user_id: str = "Server") -> Optional[Dict[str, Any]]:
        """
        Load window settings from database.

        Args:
            window_name: Unique window identifier
            user_id: User identifier

        Returns:
            dict: {'x', 'y', 'width', 'height', 'window_state'} or None
        """
        try:
            db_path = Path(self._db_path)

            if not db_path.exists():
                logger.warning(f"Database not found: {db_path}")
                return None

            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT x, y, width, height, window_state
                FROM window_settings
                WHERE user_id = ? AND window_name = ?
            """, (user_id, window_name))

            row = cursor.fetchone()
            conn.close()

            if row:
                settings = {
                    'x': row[0],
                    'y': row[1],
                    'width': row[2],
                    'height': row[3],
                    'window_state': row[4] if len(row) > 4 else 0
                }
                logger.debug(f"Loaded window settings: {window_name} = {settings}")
                return settings
            else:
                logger.debug(f"No settings found for window: {window_name}")
                return None

        except Exception as e:
            logger.error(f"Error loading window settings for {window_name}: {e}")
            return None

    def delete(self, window_name: str, user_id: str = "Server") -> bool:
        """
        Delete window settings from database.

        Args:
            window_name: Unique window identifier
            user_id: User identifier

        Returns:
            bool: True if successful
        """
        try:
            db_path = Path(self._db_path)
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM window_settings
                WHERE user_id = ? AND window_name = ?
            """, (user_id, window_name))

            conn.commit()
            conn.close()

            logger.debug(f"Deleted window settings: {window_name}")
            return True

        except Exception as e:
            logger.error(f"Error deleting window settings for {window_name}: {e}")
            return False
