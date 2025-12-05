r"""
Script 02: Vytvorenie window_settings.py pre ukladanie pozícií a veľkostí okien.

Vytvorí súbor src/utils/window_settings.py s funkciami pre prácu s SQLite databázou.
Databáza: C:\NEX\YEARACT\SYSTEM\SQLITE\window_settings.db
"""

from pathlib import Path

# Cesta k projektu
PROJECT_ROOT = Path("C:/Development/nex-automat")
TARGET_FILE = PROJECT_ROOT / "apps/supplier-invoice-editor/src/utils/window_settings.py"

# Obsah súboru
CONTENT = r'''"""
Modul pre ukladanie a načítavanie pozícií a veľkostí okien.

Používa SQLite databázu v C:\NEX\YEARACT\SYSTEM\SQLITE\window_settings.db
Databáza je zdieľaná medzi všetkými NEX aplikáciami.
"""

import os
import sqlite3
from pathlib import Path
from typing import Optional, Dict
from datetime import datetime


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
            SELECT x, y, width, height
            FROM window_settings
            WHERE user_id = ? AND window_name = ?
        """, (user_id, window_name))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'x': row[0],
                'y': row[1],
                'width': row[2],
                'height': row[3]
            }
        return None
        
    except sqlite3.Error as e:
        print(f"Chyba pri načítaní window settings: {e}")
        return None


def save_window_settings(window_name: str, x: int, y: int, width: int, height: int, 
                        user_id: Optional[str] = None) -> bool:
    """
    Uloží pozíciu a veľkosť okna pre daného používateľa.
    
    Args:
        window_name: Identifikátor okna (napr. 'sie_main_window')
        x: Pozícia X na obrazovke
        y: Pozícia Y na obrazovke
        width: Šírka okna v pixeloch
        height: Výška okna v pixeloch
        user_id: ID používateľa (ak None, použije sa aktuálny Windows username)
        
    Returns:
        bool: True ak úspešné, False pri chybe
    """
    if user_id is None:
        user_id = get_current_user_id()
    
    try:
        # Inicializuj databázu ak neexistuje
        init_settings_db()
        
        db_path = get_settings_db_path()
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # INSERT alebo UPDATE pomocou REPLACE
        cursor.execute("""
            INSERT OR REPLACE INTO window_settings 
            (user_id, window_name, x, y, width, height, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (user_id, window_name, x, y, width, height, datetime.now()))
        
        conn.commit()
        conn.close()
        return True
        
    except sqlite3.Error as e:
        print(f"Chyba pri ukladaní window settings: {e}")
        return False
'''

def main():
    """Vytvorí window_settings.py súbor."""
    print(f"Vytváram: {TARGET_FILE}")

    # Vytvor priečinok ak neexistuje
    TARGET_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Zapíš obsah
    TARGET_FILE.write_text(CONTENT.strip(), encoding='utf-8')

    print(f"✅ Súbor vytvorený: {TARGET_FILE}")
    print(f"   Veľkosť: {TARGET_FILE.stat().st_size} bytes")
    print(f"   Riadkov: {len(CONTENT.strip().splitlines())}")
    print("\nDefinované funkcie:")
    print("  - get_settings_db_path() → str")
    print("  - init_settings_db() → None")
    print("  - get_current_user_id() → str")
    print("  - load_window_settings(window_name, user_id?) → Dict|None")
    print("  - save_window_settings(window_name, x, y, width, height, user_id?) → bool")
    print("\nDatabáza:")
    print("  📂 C:\\NEX\\YEARACT\\SYSTEM\\SQLITE\\window_settings.db")

if __name__ == "__main__":
    main()