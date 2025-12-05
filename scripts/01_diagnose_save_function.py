"""
Diagnostika save_window_settings() funkcie
Overí INSERT statement a parametre
"""
import sys
from pathlib import Path

# Cesta k window_settings.py
WINDOW_SETTINGS_PATH = Path("apps/supplier-invoice-editor/src/utils/window_settings.py")


def main():
    print("=" * 80)
    print("DIAGNOSTIKA: save_window_settings() funkcia")
    print("=" * 80)

    if not WINDOW_SETTINGS_PATH.exists():
        print(f"❌ Súbor neexistuje: {WINDOW_SETTINGS_PATH}")
        sys.exit(1)

    # Načítaj súbor
    with open(WINDOW_SETTINGS_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Nájdi save_window_settings funkciu
    func_start = None
    for i, line in enumerate(lines):
        if 'def save_window_settings(' in line:
            func_start = i
            break

    if func_start is None:
        print("❌ Funkcia save_window_settings() nenájdená")
        sys.exit(1)

    print(f"\n✅ Funkcia nájdená na riadku {func_start + 1}")

    # Nájdi INSERT statement
    insert_start = None
    for i in range(func_start, min(func_start + 50, len(lines))):
        if 'INSERT OR REPLACE' in lines[i]:
            insert_start = i
            break

    if insert_start is None:
        print("❌ INSERT OR REPLACE statement nenájdený")
        sys.exit(1)

    print(f"✅ INSERT statement nájdený na riadku {insert_start + 1}")

    # Zobraz INSERT statement (5 riadkov)
    print("\n" + "=" * 80)
    print("INSERT STATEMENT:")
    print("=" * 80)
    for i in range(insert_start, min(insert_start + 5, len(lines))):
        print(f"{i + 1:4d}: {lines[i]}", end='')

    # Nájdi VALUES časť
    values_line = None
    for i in range(insert_start, min(insert_start + 10, len(lines))):
        if 'VALUES' in lines[i]:
            values_line = i
            break

    if values_line:
        print(f"\n✅ VALUES klauzula na riadku {values_line + 1}")
        print(f"{values_line + 1:4d}: {lines[values_line]}", end='')

    # Zobraz funkciu signature
    print("\n" + "=" * 80)
    print("FUNCTION SIGNATURE:")
    print("=" * 80)
    print(f"{func_start + 1:4d}: {lines[func_start]}", end='')
    if func_start + 1 < len(lines):
        print(f"{func_start + 2:4d}: {lines[func_start + 1]}", end='')

    # Kontrola parametrov
    print("\n" + "=" * 80)
    print("KONTROLA:")
    print("=" * 80)

    func_text = ''.join(lines[func_start:min(func_start + 50, len(lines))])

    checks = {
        'window_state parameter v signature': 'window_state' in lines[func_start] or 'window_state' in lines[
            func_start + 1],
        'window_state v INSERT columns': 'window_state' in func_text and '(user_id, window_name' in func_text,
        'window_state v VALUES': 'window_state' in func_text and 'VALUES' in func_text,
        'datetime.now()': 'datetime.now()' in func_text,
        'cursor.execute': 'cursor.execute' in func_text,
        'conn.commit': 'conn.commit' in func_text or 'commit' in func_text
    }

    for check, result in checks.items():
        status = "✅" if result else "❌"
        print(f"{status} {check}")

    print("\n" + "=" * 80)
    print("ODPORÚČANIE:")
    print("=" * 80)

    if all(checks.values()):
        print("✅ INSERT statement vyzerá kompletne")
        print("→ Problém môže byť v:")
        print("  1. Poradí parametrov vo VALUES")
        print("  2. UNIQUE constraint a INSERT OR REPLACE logike")
        print("  3. Commit nevolá sa správne")
        print("\n→ Ďalší krok: Pridať debug output pred cursor.execute()")
    else:
        print("❌ Našli sa problémy v INSERT statemente")
        print("→ Potrebné opraviť chýbajúce časti")

    print("\n" + "=" * 80)


if __name__ == '__main__':
    main()