r"""
Modul pre ukladanie a načítavanie pozícií a veľkostí okien.

Používa SQLite databázu v C:\NEX\YEARACT\SYSTEM\SQLITE\window_settings.db
Databáza je zdieľaná medzi všetkými NEX aplikáciami.
"""

import os
import sqlite3
from pathlib import Path
from typing import Optional, Dict
from datetime import datetime
import logging


def get_settings_db_path() -> str:
    """
    Vráti cestu k window_settings.db v NEX systémovom priečinku.
    
    Returns:
        str: Absolútna cesta k databáze
    """
    base_path = Path("C:/NEX/YEARACT/SYSTEM/SQLITE")
    base_path.mkdir(parents=True, exist_ok=True)
    return str(base_path / "window_settings.db")


def init_settings_db() -> None:
    """
    Inicializuje databázu window_settings.db ak ešte neexistuje.
    Vytvorí tabuľku window_settings s potrebnými stĺpcami.
    """
    db_path = get_settings_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Vytvor tabuľku ak neexistuje
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS window_settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            window_name TEXT NOT NULL,
            x INTEGER NOT NULL,
            y INTEGER NOT NULL,
            width INTEGER NOT NULL,
            height INTEGER NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, window_name)
        )
    """)
    
    conn.commit()
    conn.close()


def get_current_user_id() -> str:
    """
    Vráti identifikátor aktuálneho používateľa.
    
    Momentálne používa Windows username (os.getenv('USERNAME')).
    V budúcnosti môže byť nahradené aplikačným prihlásením.
    
    Returns:
        str: Identifikátor používateľa
    """
    return os.getenv('USERNAME', 'default_user')


def load_window_settings(window_name: str, user_id: Optional[str] = None) -> Optional[Dict[str, int]]:
    """
    Načíta uložené nastavenia okna pre daného používateľa.
    
    Args:
        window_name: Identifikátor okna (napr. 'sie_main_window')
        user_id: ID používateľa (ak None, použije sa aktuálny Windows username)
        
    Returns:
        Dict s kľúčmi 'x', 'y', 'width', 'height' alebo None ak neexistuje
    """
    if user_id is None:
        user_id = get_current_user_id()
    
    db_path = get_settings_db_path()
    
    # Ak databáza neexistuje, vráť None
    if not Path(db_path).exists():
        return None
    
    try:
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
            x, y, width, height = row[0], row[1], row[2], row[3]
            window_state = row[4] if len(row) > 4 else 0

            # Validácia pozície okna - musí byť viditeľné na obrazovke
            MIN_X = -3840  # Dual 4K monitor support  # Povoliť čiastočne mimo obrazovky (pre multi-monitor)
            MIN_Y = 0    # Y musí byť >= 0 (hlavička musí byť viditeľná)
            MIN_WIDTH = 400
            MIN_HEIGHT = 300
            MAX_WIDTH = 3840  # 4K rozlíšenie
            MAX_HEIGHT = 2160

            # Kontrola hraníc
            if x < MIN_X or y < MIN_Y:
                print(f"⚠️  Invalid position: x={x}, y={y} (outside screen bounds)")
                return None

            if width < MIN_WIDTH or width > MAX_WIDTH:
                print(f"⚠️  Invalid width: {width} (must be {MIN_WIDTH}-{MAX_WIDTH})")
                return None

            if height < MIN_HEIGHT or height > MAX_HEIGHT:
                print(f"⚠️  Invalid height: {height} (must be {MIN_HEIGHT}-{MAX_HEIGHT})")
                return None

            return {
                'x': x,
                'y': y,
                'width': width,
                'height': height,
                'window_state': window_state
            }
        return None
        
    except sqlite3.Error as e:
        print(f"Chyba pri načítaní window settings: {e}")
        return None


def save_window_settings(window_name: str, x: int, y: int, width: int, height: int,
                        window_state: int = 0, user_id: Optional[str] = None) -> bool:
    """
    Save window settings to database using DELETE + INSERT pattern.

    Args:
        window_name: Unique window identifier
        x, y: Window position
        width, height: Window size
        window_state: 0=normal, 2=maximized
        user_id: User identifier (default from config)

    Returns:
        bool: True if successful
    """
    try:
        if user_id is None:
            user_id = 'Server'  # Default user ID

        db_path = Path(r"C:\NEX\YEARACT\SYSTEM\SQLITE\window_settings.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

                    f"x={x}, y={y}, width={width}, height={height}, "
                    f"window_state={window_state}, user_id={user_id}")

        # First DELETE existing record to avoid INSERT OR REPLACE issues
        cursor.execute("""
            DELETE FROM window_settings
            WHERE user_id = ? AND window_name = ?
        """, (user_id, window_name))

        # Then INSERT new record with all current values
        cursor.execute("""
            INSERT INTO window_settings
            (user_id, window_name, x, y, width, height, window_state, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (user_id, window_name, x, y, width, height, window_state, datetime.now()))

        conn.commit()
        conn.close()

        return True

    except Exception as e:
        logger.error(f"Error saving window settings: {e}")
        return False



    except sqlite3.Error as e:
        print(f"Chyba pri ukladaní window settings: {e}")
        return False
