"""
Skontroluje load_window_settings() SELECT statement
"""
from pathlib import Path

WINDOW_SETTINGS_PATH = Path("apps/supplier-invoice-editor/src/utils/window_settings.py")


def main():
    print("=" * 80)
    print("CHECK: load_window_settings() SELECT statement")
    print("=" * 80)

    with open(WINDOW_SETTINGS_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Nájdi load_window_settings funkciu
    load_start = None
    for i, line in enumerate(lines):
        if 'def load_window_settings(' in line:
            load_start = i
            break

    if load_start is None:
        print("❌ load_window_settings() nenájdená")
        return

    print(f"✅ load_window_settings() nájdená na riadku {load_start + 1}")

    # Nájdi SELECT statement
    select_start = None
    for i in range(load_start, min(load_start + 50, len(lines))):
        if 'SELECT' in lines[i]:
            select_start = i
            break

    if select_start is None:
        print("❌ SELECT statement nenájdený")
        return

    print(f"✅ SELECT statement nájdený na riadku {select_start + 1}")

    # Zobraz SELECT statement
    print("\n" + "=" * 80)
    print("SELECT STATEMENT:")
    print("=" * 80)
    for i in range(select_start, min(select_start + 10, len(lines))):
        print(f"{i + 1:4d}: {lines[i]}", end='')
        if 'FROM window_settings' in lines[i]:
            break

    # Kontrola či window_state je v SELECT
    select_text = ''.join(lines[select_start:select_start + 10])

    print("\n" + "=" * 80)
    print("KONTROLA:")
    print("=" * 80)

    has_window_state = 'window_state' in select_text
    status = "✅" if has_window_state else "❌"
    print(f"{status} window_state v SELECT statement")

    if not has_window_state:
        print("\n🔴 PROBLÉM: SELECT nečíta window_state stĺpec!")
        print("   → Musí byť: SELECT x, y, width, height, window_state FROM...")

    # Nájdi return statement
    return_start = None
    for i in range(load_start, min(load_start + 50, len(lines))):
        if 'return {' in lines[i] or "return {'x'" in lines[i]:
            return_start = i
            break

    if return_start:
        print(f"\n✅ return statement nájdený na riadku {return_start + 1}")
        print("\nRETURN STATEMENT:")
        for i in range(return_start, min(return_start + 10, len(lines))):
            print(f"{i + 1:4d}: {lines[i]}", end='')
            if '}' in lines[i]:
                break

        return_text = ''.join(lines[return_start:return_start + 10])
        has_state_return = 'window_state' in return_text
        status = "✅" if has_state_return else "❌"
        print(f"\n{status} window_state v return dictionary")

    print("\n" + "=" * 80)


if __name__ == '__main__':
    main()