"""
FIX: DB_PATH definition - použije správnu cestu k databáze
"""
from pathlib import Path

WINDOW_SETTINGS_PATH = Path("apps/supplier-invoice-editor/src/utils/window_settings.py")


def main():
    print("=" * 80)
    print("FIX: DB_PATH definition")
    print("=" * 80)

    # Načítaj súbor
    with open(WINDOW_SETTINGS_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Nájdi ako ostatné funkcie používajú db_path
    print("\nHľadám db_path použitie v module...")

    db_path_usage = []
    for i, line in enumerate(lines[:100]):  # Prvých 100 riadkov
        if 'db_path' in line.lower() and '=' in line:
            db_path_usage.append((i, line.strip()))
            print(f"Riadok {i + 1}: {line.strip()}")

    # Najdi load_window_settings funkciu ako vzor
    load_func_start = None
    for i, line in enumerate(lines):
        if 'def load_window_settings(' in line:
            load_func_start = i
            break

    if load_func_start:
        print(f"\n✅ load_window_settings() nájdená na riadku {load_func_start + 1}")

        # Zobraz prvých 20 riadkov load_window_settings
        print("\nDB connection pattern v load_window_settings():")
        for i in range(load_func_start, min(load_func_start + 20, len(lines))):
            if 'sqlite3.connect' in lines[i] or 'db_path' in lines[i].lower():
                print(f"  {i + 1}: {lines[i].strip()}")

    # Nájdi save_window_settings funkciu
    save_func_start = None
    for i, line in enumerate(lines):
        if 'def save_window_settings(' in line:
            save_func_start = i
            break

    if save_func_start is None:
        print("❌ save_window_settings() nenájdená")
        return

    print(f"\n✅ save_window_settings() nájdená na riadku {save_func_start + 1}")

    # Nájdi riadok s sqlite3.connect(DB_PATH)
    connect_line = None
    for i in range(save_func_start, min(save_func_start + 30, len(lines))):
        if 'sqlite3.connect(DB_PATH)' in lines[i]:
            connect_line = i
            break

    if connect_line:
        print(f"✅ Problémový riadok nájdený na {connect_line + 1}")

        # Nahraď DB_PATH za plnú cestu alebo config hodnotu
        # Zoberieme pattern z load_window_settings
        indent = "        "

        # Použiť priamo hardcoded path ako v init_db()
        new_line = f'{indent}db_path = Path(r"C:\\NEX\\YEARACT\\SYSTEM\\SQLITE\\window_settings.db")\n'

        # Vložiť pred sqlite3.connect
        lines.insert(connect_line, new_line)

        # Zmeniť sqlite3.connect(DB_PATH) na sqlite3.connect(db_path)
        lines[connect_line + 1] = lines[connect_line + 1].replace('DB_PATH', 'db_path')

        print(f"✅ Pridaný riadok: db_path = Path(...)")
        print(f"✅ Zmenené: DB_PATH → db_path")

    # Ulož súbor
    with open(WINDOW_SETTINGS_PATH, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    print(f"\n✅ Súbor opravený: {WINDOW_SETTINGS_PATH}")

    print("\n" + "=" * 80)
    print("TEST:")
    print("=" * 80)
    print("cd apps\\supplier-invoice-editor")
    print("python main.py")
    print("  → zavri aplikáciu")
    print("  → NESMIE byť ERROR 'DB_PATH is not defined'")
    print("  → python ..\\..\\scripts\\06_verify_db_immediately.py")
    print("=" * 80)


if __name__ == '__main__':
    main()