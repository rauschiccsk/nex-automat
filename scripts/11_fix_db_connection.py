"""
FIX: _get_db_connection() error - použije existujúci DB connection pattern
"""
from pathlib import Path

WINDOW_SETTINGS_PATH = Path("apps/supplier-invoice-editor/src/utils/window_settings.py")


def main():
    print("=" * 80)
    print("FIX: _get_db_connection() error")
    print("=" * 80)

    # Načítaj súbor
    with open(WINDOW_SETTINGS_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Nájdi ako load_window_settings() alebo iná funkcia robí DB connection
    print("\nHľadám existujúci DB connection pattern...")

    # Hľadaj sqlite3.connect pattern
    db_path_line = None
    for i, line in enumerate(lines):
        if 'DB_PATH' in line and '=' in line:
            db_path_line = i
            print(f"✅ DB_PATH definícia nájdená na riadku {i + 1}: {line.strip()}")
            break

    # Hľadaj sqlite3.connect volanie
    connect_pattern = None
    for i, line in enumerate(lines):
        if 'sqlite3.connect' in line:
            connect_pattern = line.strip()
            print(f"✅ sqlite3.connect pattern nájdený na riadku {i + 1}: {connect_pattern}")
            break

    if not connect_pattern:
        print("❌ sqlite3.connect pattern nenájdený")
        return

    # Nájdi save_window_settings funkciu
    func_start = None
    for i, line in enumerate(lines):
        if 'def save_window_settings(' in line:
            func_start = i
            break

    if func_start is None:
        print("❌ save_window_settings() nenájdená")
        return

    print(f"✅ save_window_settings() nájdená na riadku {func_start + 1}")

    # Nájdi riadok s _get_db_connection()
    error_line = None
    for i in range(func_start, min(func_start + 30, len(lines))):
        if '_get_db_connection()' in lines[i]:
            error_line = i
            break

    if error_line:
        print(f"✅ Chybný riadok nájdený na {error_line + 1}")

        # Nahraď _get_db_connection() za priamy sqlite3.connect
        indent = "        "
        lines[error_line] = f"{indent}conn = sqlite3.connect(DB_PATH)\n"

        print(f"✅ Nahradené: _get_db_connection() → sqlite3.connect(DB_PATH)")

    # Ulož súbor
    with open(WINDOW_SETTINGS_PATH, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    print(f"\n✅ Súbor opravený: {WINDOW_SETTINGS_PATH}")

    print("\n" + "=" * 80)
    print("TEST:")
    print("=" * 80)
    print("cd apps\\supplier-invoice-editor")
    print("python main.py")
    print("  → zavri aplikáciu (nesmie byť ERROR)")
    print("  → python ..\\..\\scripts\\06_verify_db_immediately.py")
    print("     MUSÍ byť záznam v DB")
    print("=" * 80)


if __name__ == '__main__':
    main()