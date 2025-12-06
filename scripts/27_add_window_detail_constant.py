#!/usr/bin/env python3
"""
Script 27: Add WINDOW_DETAIL constant to constants.py
Pridá konštantu pre detail window
"""

from pathlib import Path


def add_constant():
    """Pridá WINDOW_DETAIL konštantu"""

    constants_path = Path("apps/supplier-invoice-editor/src/utils/constants.py")

    if not constants_path.exists():
        print(f"❌ File not found: {constants_path}")
        return False

    content = constants_path.read_text(encoding='utf-8')
    lines = content.split('\n')

    print("=" * 80)
    print("CURRENT WINDOW CONSTANTS")
    print("=" * 80)

    # Zobraz existujúce window konštanty
    for i, line in enumerate(lines, 1):
        if 'WINDOW_' in line and '=' in line:
            print(f"{i:4d}: {line}")

    # Skontroluj či už existuje
    if 'WINDOW_DETAIL' in content:
        print("\n⚠️  WINDOW_DETAIL already exists!")
        return False

    # Nájdi WINDOW_MAIN a pridaj WINDOW_DETAIL hned za ním
    new_lines = []
    added = False

    for line in lines:
        new_lines.append(line)

        if 'WINDOW_MAIN = ' in line and not added:
            # Pridaj WINDOW_DETAIL hneď za WINDOW_MAIN
            new_lines.append('WINDOW_DETAIL = "sie_detail_window"')
            added = True
            print(f"\n✅ Adding WINDOW_DETAIL constant after WINDOW_MAIN")

    if not added:
        # Ak WINDOW_MAIN neexistuje, pridaj na koniec súboru
        new_lines.append('\n# Window identifiers')
        new_lines.append('WINDOW_DETAIL = "sie_detail_window"')
        print(f"\n✅ Adding WINDOW_DETAIL at end of file")

    # Ulož súbor
    content = '\n'.join(new_lines)
    constants_path.write_text(content, encoding='utf-8')

    print(f"\n📝 Added: WINDOW_DETAIL = \"sie_detail_window\"")

    return True


if __name__ == "__main__":
    success = add_constant()
    if success:
        print("\n" + "=" * 80)
        print("NEXT: Test detail window persistence")
        print("=" * 80)
        print("cd apps/supplier-invoice-editor")
        print("python main.py")
        print("\n1. Otvor faktúru")
        print("2. Zmeň veľkosť detail okna")
        print("3. Zavri detail okno")
        print("4. Otvor inú faktúru")
        print("5. Detail okno by malo mať ZAPAMÄTANÚ veľkosť! ✅")