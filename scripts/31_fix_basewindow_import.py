"""
Opraví BaseWindow import v main_window.py
"""
from pathlib import Path

MAIN_WINDOW_PATH = Path("apps/supplier-invoice-editor/src/ui/main_window.py")


def main():
    print("=" * 80)
    print("FIX: BaseWindow import")
    print("=" * 80)

    # Načítaj súbor
    with open(MAIN_WINDOW_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Nájdi import BaseWindow
    for i, line in enumerate(lines):
        if 'from nex_shared.ui import BaseWindow' in line:
            print(f"✅ Našiel import na riadku {i + 1}: {line.strip()}")

            # Zmeniť na správny import (podľa sys.path)
            # sys.path obsahuje packages/nex-shared, takže import je from ui.base_window
            lines[i] = 'from ui.base_window import BaseWindow\n'

            print(f"   → Zmenené na: from ui.base_window import BaseWindow")
            break

    # Ulož súbor
    with open(MAIN_WINDOW_PATH, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    print(f"\n✅ Súbor opravený: {MAIN_WINDOW_PATH}")

    print("\n" + "=" * 80)
    print("TEST:")
    print("=" * 80)
    print("python main.py")
    print("  → Aplikácia by sa MUSÍ spustiť")
    print("=" * 80)


if __name__ == '__main__':
    main()