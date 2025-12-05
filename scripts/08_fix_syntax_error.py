"""
FIX: Syntax error v window_settings.py
Kompletne prepíše save_window_settings() funkciu
"""
from pathlib import Path

WINDOW_SETTINGS_PATH = Path("apps/supplier-invoice-editor/src/utils/window_settings.py")


def main():
    print("=" * 80)
    print("FIX: Syntax error v save_window_settings()")
    print("=" * 80)

    # Načítaj súbor
    with open(WINDOW_SETTINGS_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Nájdi začiatok funkcie save_window_settings
    func_start = None
    for i, line in enumerate(lines):
        if 'def save_window_settings(' in line:
            func_start = i
            break

    if func_start is None:
        print("❌ Funkcia save_window_settings() nenájdená")
        return

    # Nájdi koniec funkcie (ďalšia def alebo koniec súboru)
    func_end = None
    for i in range(func_start + 1, len(lines)):
        if lines[i].startswith('def ') and not lines[i].startswith('    '):
            func_end = i
            break

    if func_end is None:
        # Ak nie je ďalšia funkcia, nájdi posledný return
        for i in range(func_start + 1, len(lines)):
            if 'return True' in lines[i] or 'return False' in lines[i]:
                func_end = i + 1
                break

    print(f"✅ Funkcia save_window_settings() nájdená: riadky {func_start + 1} - {func_end}")

    # Nová správna implementácia
    new_function = '''def save_window_settings(window_name: str, x: int, y: int, width: int, height: int,
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
            user_id = get_user_id()

        conn = _get_db_connection()
        cursor = conn.cursor()

        # DEBUG: Log parameters before save
        logger = logging.getLogger(__name__)
        logger.info(f"DEBUG save_window_settings: window_name={window_name}, "
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
        logger.info(f"DEBUG: Database committed successfully")
        conn.close()

        return True

    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.error(f"Error saving window settings: {e}")
        return False

'''

    # Nahraď starú funkciu novou
    new_lines = lines[:func_start] + [new_function + '\n'] + lines[func_end:]

    # Ulož súbor
    with open(WINDOW_SETTINGS_PATH, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

    print(f"\n✅ Funkcia save_window_settings() úspešne prepísaná")
    print("\nImplementácia:")
    print("  ✅ DELETE WHERE user_id AND window_name")
    print("  ✅ INSERT INTO s window_state")
    print("  ✅ DEBUG log pred a po commit")
    print("  ✅ Správna syntax")

    print("\n" + "=" * 80)
    print("TEST:")
    print("=" * 80)
    print("cd apps\\supplier-invoice-editor")
    print("python main.py")
    print("  → maximalizuj okno")
    print("  → zavri aplikáciu")
    print("  → python ..\\..\\scripts\\06_verify_db_immediately.py")
    print("=" * 80)


if __name__ == '__main__':
    main()