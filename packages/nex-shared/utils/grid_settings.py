r"""
Modul pre ukladanie a načítavanie grid a column nastavení.

Používa SQLite databázu v C:\NEX\YEARACT\SYSTEM\SQLITE\grid_settings.db
Databáza je zdieľaná medzi všetkými NEX aplikáciami.
"""

import os
import sqlite3
from pathlib import Path
from typing import Optional, List, Dict
from datetime import datetime


def get_grid_settings_db_path() -> str:
    """
    Vráti cestu k grid_settings.db v NEX systémovom priečinku.

    Returns:
        str: Absolútna cesta k databáze
    """
    base_path = Path("C:/NEX/YEARACT/SYSTEM/SQLITE")
    base_path.mkdir(parents=True, exist_ok=True)
    return str(base_path / "grid_settings.db")


def init_grid_settings_db() -> None:
    """
    Inicializuje databázu grid_settings.db ak ešte neexistuje.
    Vytvorí tabuľky grid_column_settings a grid_settings.
    """
    db_path = get_grid_settings_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Tabuľka pre nastavenia jednotlivých stĺpcov
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS grid_column_settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            window_name TEXT NOT NULL,
            grid_name TEXT NOT NULL,
            column_name TEXT NOT NULL,
            width INTEGER,
            visual_index INTEGER,
            visible INTEGER DEFAULT 1,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, window_name, grid_name, column_name)
        )
    """)

    # Tabuľka pre grid-level nastavenia (aktívny stĺpec pre quick search)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS grid_settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            window_name TEXT NOT NULL,
            grid_name TEXT NOT NULL,
            active_column_index INTEGER,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, window_name, grid_name)
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


def load_column_settings(window_name: str, grid_name: str, 
                        user_id: Optional[str] = None) -> List[Dict]:
    """
    Načíta uložené nastavenia stĺpcov pre daný grid.

    Args:
        window_name: Identifikátor okna (napr. 'sie_main_window')
        grid_name: Identifikátor gridu (napr. 'invoice_list')
        user_id: ID používateľa (ak None, použije sa aktuálny Windows username)

    Returns:
        List[Dict]: Zoznam slovníkov s nastaveniami stĺpcov
                   [{'column_name': 'id', 'width': 100, 'visual_index': 0, 'visible': True}, ...]
                   Prázdny list ak neexistuje
    """
    if user_id is None:
        user_id = get_current_user_id()

    db_path = get_grid_settings_db_path()

    if not Path(db_path).exists():
        return []

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT column_name, width, visual_index, visible
            FROM grid_column_settings
            WHERE user_id = ? AND window_name = ? AND grid_name = ?
            ORDER BY visual_index
        """, (user_id, window_name, grid_name))

        rows = cursor.fetchall()
        conn.close()

        return [
            {
                'column_name': row[0],
                'width': row[1],
                'visual_index': row[2],
                'visible': bool(row[3])
            }
            for row in rows
        ]

    except sqlite3.Error as e:
        print(f"Chyba pri načítaní column settings: {e}")
        return []


def save_column_settings(window_name: str, grid_name: str, columns: List[Dict],
                        user_id: Optional[str] = None) -> bool:
    """
    Uloží nastavenia stĺpcov pre daný grid.

    Args:
        window_name: Identifikátor okna
        grid_name: Identifikátor gridu
        columns: Zoznam slovníkov s nastaveniami stĺpcov
                [{'column_name': 'id', 'width': 100, 'visual_index': 0, 'visible': True}, ...]
        user_id: ID používateľa (ak None, použije sa aktuálny Windows username)

    Returns:
        bool: True ak úspešné, False pri chybe
    """
    if user_id is None:
        user_id = get_current_user_id()

    try:
        init_grid_settings_db()

        db_path = get_grid_settings_db_path()
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Ulož každý stĺpec
        for col in columns:
            cursor.execute("""
                INSERT OR REPLACE INTO grid_column_settings 
                (user_id, window_name, grid_name, column_name, width, visual_index, visible, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                user_id,
                window_name,
                grid_name,
                col['column_name'],
                col.get('width'),
                col.get('visual_index'),
                1 if col.get('visible', True) else 0,
                datetime.now()
            ))

        conn.commit()
        conn.close()
        return True

    except sqlite3.Error as e:
        print(f"Chyba pri ukladaní column settings: {e}")
        return False


def load_grid_settings(window_name: str, grid_name: str,
                      user_id: Optional[str] = None) -> Optional[Dict]:
    """
    Načíta grid-level nastavenia (aktívny stĺpec).

    Args:
        window_name: Identifikátor okna
        grid_name: Identifikátor gridu
        user_id: ID používateľa (ak None, použije sa aktuálny Windows username)

    Returns:
        Dict s kľúčom 'active_column_index' alebo None ak neexistuje
    """
    if user_id is None:
        user_id = get_current_user_id()

    db_path = get_grid_settings_db_path()

    if not Path(db_path).exists():
        return None

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT active_column_index
            FROM grid_settings
            WHERE user_id = ? AND window_name = ? AND grid_name = ?
        """, (user_id, window_name, grid_name))

        row = cursor.fetchone()
        conn.close()

        if row:
            return {'active_column_index': row[0]}
        return None

    except sqlite3.Error as e:
        print(f"Chyba pri načítaní grid settings: {e}")
        return None


def save_grid_settings(window_name: str, grid_name: str, active_column_index: int,
                      user_id: Optional[str] = None) -> bool:
    """
    Uloží grid-level nastavenia (aktívny stĺpec).

    Args:
        window_name: Identifikátor okna
        grid_name: Identifikátor gridu
        active_column_index: Index aktívneho stĺpca
        user_id: ID používateľa (ak None, použije sa aktuálny Windows username)

    Returns:
        bool: True ak úspešné, False pri chybe
    """
    if user_id is None:
        user_id = get_current_user_id()

    try:
        init_grid_settings_db()

        db_path = get_grid_settings_db_path()
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT OR REPLACE INTO grid_settings 
            (user_id, window_name, grid_name, active_column_index, updated_at)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, window_name, grid_name, active_column_index, datetime.now()))

        conn.commit()
        conn.close()
        return True

    except sqlite3.Error as e:
        print(f"Chyba pri ukladaní grid settings: {e}")
        return False