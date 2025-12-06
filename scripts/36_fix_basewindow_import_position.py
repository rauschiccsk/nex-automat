"""
Opraví pozíciu BaseWindow importu - presunie po PyQt5 imports
"""
from pathlib import Path

MAIN_WINDOW_PATH = Path("apps/supplier-invoice-editor/src/ui/main_window.py")


def main():
    print("=" * 80)
    print("FIX: BaseWindow import position")
    print("=" * 80)

    # Načítaj súbor
    with open(MAIN_WINDOW_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 1. Odstráň zlý import (riadok 8)
    new_lines = []
    for i, line in enumerate(lines):
        if i == 7 and 'from ui.base_window import BaseWindow' in line:
            print(f"✅ Odstránený zlý import z riadku {i + 1}")
            continue
        new_lines.append(line)

    lines = new_lines

    # 2. Nájdi koniec PyQt5 imports
    pyqt_end = None
    for i, line in enumerate(lines):
        if 'from PyQt5.QtCore import' in line:
            pyqt_end = i + 1
            break

    if pyqt_end:
        print(f"✅ PyQt5 imports končia na riadku {pyqt_end}")

        # Pridaj BaseWindow import za PyQt5 imports
        lines.insert(pyqt_end, 'from ui.base_window import BaseWindow\n')

        print(f"✅ Pridaný import BaseWindow na riadok {pyqt_end + 1}")

    # Ulož súbor
    with open(MAIN_WINDOW_PATH, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    print(f"\n✅ Súbor opravený: {MAIN_WINDOW_PATH}")

    print("\n" + "=" * 80)
    print("VERIFY:")
    print("=" * 80)
    print("Zobraz riadky 5-15:")
    for i in range(4, min(15, len(lines))):
        print(f"{i + 1:3d}: {lines[i]}", end='')

    print("\n" + "=" * 80)
    print("TEST:")
    print("=" * 80)
    print("cd apps\\supplier-invoice-editor")
    print("python main.py")
    print("=" * 80)


if __name__ == '__main__':
    main()