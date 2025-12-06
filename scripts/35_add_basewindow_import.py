"""
Pridá BaseWindow import do main_window.py
"""
from pathlib import Path

MAIN_WINDOW_PATH = Path("apps/supplier-invoice-editor/src/ui/main_window.py")


def main():
    print("=" * 80)
    print("PRIDANIE: BaseWindow import")
    print("=" * 80)

    # Načítaj súbor
    with open(MAIN_WINDOW_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Skontroluj či už import existuje
    has_import = any('from ui.base_window import BaseWindow' in line for line in lines)

    if has_import:
        print("⏭️  Import už existuje")
        return

    # Nájdi import PyQt5.QtWidgets
    insert_pos = None
    for i, line in enumerate(lines):
        if 'from PyQt5.QtWidgets import' in line:
            insert_pos = i + 1
            break

    if insert_pos is None:
        print("❌ Nenašiel PyQt5 import")
        return

    print(f"✅ Pridám import za riadok {insert_pos}")

    # Pridaj import
    lines.insert(insert_pos, 'from ui.base_window import BaseWindow\n')

    # Ulož súbor
    with open(MAIN_WINDOW_PATH, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    print(f"✅ Súbor opravený: {MAIN_WINDOW_PATH}")
    print(f"   Pridaný riadok {insert_pos + 1}: from ui.base_window import BaseWindow")

    print("\n" + "=" * 80)
    print("TEST:")
    print("=" * 80)
    print("python main.py")
    print("  → Aplikácia by sa MUSÍ spustiť ✅")
    print("=" * 80)


if __name__ == '__main__':
    main()