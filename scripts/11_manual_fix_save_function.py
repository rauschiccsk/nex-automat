#!/usr/bin/env python3
"""
Manual Fix Save Function
=========================
Session: 2025-12-05
Location: scripts/11_manual_fix_save_function.py

Manuálne opraví save_window_settings() aby prijímala window_state parameter.
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
TARGET = PROJECT_ROOT / "apps/supplier-invoice-editor/src/utils/window_settings.py"


def fix_save_function():
    """Opraví save_window_settings kompletne"""

    print("=" * 80)
    print("MANUAL FIX SAVE FUNCTION")
    print("=" * 80)

    with open(TARGET, 'r', encoding='utf-8') as f:
        content = f.read()

    # Celá stará save_window_settings funkcia
    old_function = """def save_window_settings(window_name: str, x: int, y: int, width: int, height: int,
                        window_state: int = 0,
                        user_id: Optional[str] = None) -> bool:
    \"\"\"
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
    \"\"\"
    if user_id is None:
        user_id = get_current_user_id()

    try:
        # Inicializuj databázu ak neexistuje
        init_settings_db()

        db_path = get_settings_db_path()
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # INSERT alebo UPDATE pomocou REPLACE
        cursor.execute(\"\"\"
            INSERT OR REPLACE INTO window_settings
            (user_id, window_name, x, y, width, height, window_state, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        \"\"\", (user_id, window_name, x, y, width, height, window_state, datetime.now()))

        conn.commit()
        conn.close()
        return True

    except sqlite3.Error as e:
        print(f"Chyba pri ukladaní window settings: {e}")
        return False"""

    # Nová verzia (pre istotu celá)
    new_function = """def save_window_settings(window_name: str, x: int, y: int, width: int, height: int,
                        window_state: int = 0, user_id: Optional[str] = None) -> bool:
    \"\"\"
    Uloží pozíciu a veľkosť okna pre daného používateľa.

    Args:
        window_name: Identifikátor okna (napr. 'sie_main_window')
        x: Pozícia X na obrazovke
        y: Pozícia Y na obrazovke
        width: Šírka okna v pixeloch
        height: Výška okna v pixeloch
        window_state: Stav okna (0=normal, 2=maximized)
        user_id: ID používateľa (ak None, použije sa aktuálny Windows username)

    Returns:
        bool: True ak úspešné, False pri chybe
    \"\"\"
    if user_id is None:
        user_id = get_current_user_id()

    try:
        # Inicializuj databázu ak neexistuje
        init_settings_db()

        db_path = get_settings_db_path()
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # INSERT alebo UPDATE pomocou REPLACE
        cursor.execute(\"\"\"
            INSERT OR REPLACE INTO window_settings
            (user_id, window_name, x, y, width, height, window_state, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        \"\"\", (user_id, window_name, x, y, width, height, window_state, datetime.now()))

        conn.commit()
        conn.close()
        return True

    except sqlite3.Error as e:
        print(f"Chyba pri ukladaní window settings: {e}")
        return False"""

    print("\n1. Nahrádzam save_window_settings()...")

    # Skús náhradu
    if "def save_window_settings(window_name: str" in content:
        # Nájdi začiatok funkcie
        start = content.find("def save_window_settings(")
        if start == -1:
            print("   ❌ Funkcia nenájdená")
            return False

        # Nájdi koniec funkcie (ďalšia def alebo koniec súboru)
        end = content.find("\ndef ", start + 10)
        if end == -1:
            end = len(content)

        # Nahraď
        before = content[:start]
        after = content[end:]
        new_content = before + new_function + "\n" + after

        print("   ✅ Funkcia nahradená")

        # Ulož
        print("\n2. Ukladám...")
        with open(TARGET, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print("   ✅ Uložené")

        print("\n" + "=" * 80)
        print("✅ HOTOVO - Save Function Fixed")
        print("=" * 80)
        return True
    else:
        print("   ❌ Funkcia nenájdená v súbore")
        return False


if __name__ == "__main__":
    success = fix_save_function()
    exit(0 if success else 1)