"""
Window and Grid Settings Persistence
Grid settings functions (active column) - window persistence je v BaseWindow.
"""

import logging
import sqlite3
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

# Database path
DB_PATH = Path(r"C:\NEX\YEARACT\SYSTEM\SQLITE\window_settings.db")


def save_grid_settings(
    window_name: str, grid_name: str, active_column: int, user_id: str = "Server"
) -> bool:
    """
    Save grid settings (active column).

    Args:
        window_name: Window identifier
        grid_name: Grid identifier
        active_column: Active column index
        user_id: User ID

    Returns:
        bool: True if successful
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Create table if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS grid_settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                window_name TEXT NOT NULL,
                grid_name TEXT NOT NULL,
                active_column INTEGER,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, window_name, grid_name)
            )
        """)

        # DELETE + INSERT pattern
        cursor.execute(
            """
            DELETE FROM grid_settings
            WHERE user_id = ? AND window_name = ? AND grid_name = ?
        """,
            (user_id, window_name, grid_name),
        )

        cursor.execute(
            """
            INSERT INTO grid_settings
            (user_id, window_name, grid_name, active_column, updated_at)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
        """,
            (user_id, window_name, grid_name, active_column),
        )

        conn.commit()
        conn.close()

        logger.debug(f"Saved grid settings: {window_name}/{grid_name} column={active_column}")
        return True

    except Exception as e:
        logger.error(f"Error saving grid settings: {e}")
        return False


def load_grid_settings(window_name: str, grid_name: str, user_id: str = "Server") -> int | None:
    """
    Load grid settings (active column).

    Args:
        window_name: Window identifier
        grid_name: Grid identifier
        user_id: User ID

    Returns:
        int: Active column index or None
    """
    try:
        if not DB_PATH.exists():
            return None

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT active_column
            FROM grid_settings
            WHERE user_id = ? AND window_name = ? AND grid_name = ?
        """,
            (user_id, window_name, grid_name),
        )

        row = cursor.fetchone()
        conn.close()

        if row:
            logger.debug(f"Loaded grid settings: {window_name}/{grid_name} column={row[0]}")
            return row[0]

        return None

    except Exception as e:
        logger.error(f"Error loading grid settings: {e}")
        return None
