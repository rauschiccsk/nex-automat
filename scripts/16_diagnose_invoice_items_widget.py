"""
NEX Automat v2.1 - Diagnostika Invoice Items Widget
Zistí, ktorý widget zobrazuje položky faktúr.
"""

import os
from pathlib import Path

# Paths
BASE_DIR = Path(r"C:\Development\nex-automat")
WIDGETS_DIR = BASE_DIR / "apps" / "supplier-invoice-editor" / "src" / "ui" / "widgets"


def find_items_widget():
    """Nájdi widget pre položky faktúr."""
    print(f"\n{'=' * 80}")
    print("1. HĽADANIE INVOICE ITEMS WIDGETU")
    print(f"{'=' * 80}")

    # Zoznam možných názvov
    possible_names = [
        'invoice_items_widget.py',
        'invoice_detail_widget.py',
        'items_list_widget.py',
        'invoice_editor_widget.py',
        'detail_widget.py'
    ]

    found_files = []

    for file in WIDGETS_DIR.glob('*.py'):
        if file.name in possible_names:
            found_files.append(file)
            print(f"✅ Našiel som: {file.name}")

    # Ak nenájdeme, zobraz všetky widgety
    if not found_files:
        print("\n⚠️  Žiadny z očakávaných názvov nenájdený")
        print("\nVšetky widgety v adresári:")
        for file in sorted(WIDGETS_DIR.glob('*.py')):
            print(f"  - {file.name}")

    return found_files


def search_for_items_grid():
    """Hľadaj v kóde odkaz na items grid."""
    print(f"\n{'=' * 80}")
    print("2. HĽADANIE REFERENCIÍ NA ITEMS/POLOŽKY")
    print(f"{'=' * 80}")

    keywords = ['items', 'item', 'detail', 'položk']

    results = {}

    for file in WIDGETS_DIR.glob('*.py'):
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read().lower()

            for keyword in keywords:
                if keyword in content:
                    if file.name not in results:
                        results[file.name] = []
                    results[file.name].append(keyword)

    if results:
        print("\nSúbory obsahujúce items/detail referencie:")
        for filename, keywords_found in sorted(results.items()):
            print(f"  ✅ {filename}: {', '.join(set(keywords_found))}")

    return results


def analyze_main_window():
    """Analyzuj main_window.py - tam je reference na items widget."""
    print(f"\n{'=' * 80}")
    print("3. ANALÝZA main_window.py")
    print(f"{'=' * 80}")

    main_window = BASE_DIR / "apps" / "supplier-invoice-editor" / "src" / "ui" / "main_window.py"

    with open(main_window, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    print("\nImporty widgetov:")
    for i, line in enumerate(lines[:50]):
        if 'import' in line.lower() and 'widget' in line.lower():
            print(f"  {i + 1:4d}: {line.rstrip()}")

    print("\nInicializácia widgetov v _setup_ui():")
    in_setup = False
    for i, line in enumerate(lines):
        if 'def _setup_ui(' in line:
            in_setup = True

        if in_setup:
            if 'widget' in line.lower() and ('self.' in line or '=' in line):
                print(f"  {i + 1:4d}: {line.rstrip()}")

            if 'def ' in line and i > 0 and 'def _setup_ui' not in line:
                break


def check_constants():
    """Skontroluj constants.py pre GRID_INVOICE_ITEMS."""
    print(f"\n{'=' * 80}")
    print("4. KONTROLA KONŠTÁNT")
    print(f"{'=' * 80}")

    constants = BASE_DIR / "apps" / "supplier-invoice-editor" / "src" / "utils" / "constants.py"

    if constants.exists():
        with open(constants, 'r', encoding='utf-8') as f:
            content = f.read()

        print("\nGRID konštanty:")
        for line in content.split('\n'):
            if 'GRID_' in line:
                print(f"  {line.strip()}")

        if 'GRID_INVOICE_ITEMS' in content:
            print("\n✅ GRID_INVOICE_ITEMS už existuje")
        else:
            print("\n⚠️  GRID_INVOICE_ITEMS chýba - treba pridať")
    else:
        print("❌ constants.py neexistuje")


def main():
    """Hlavná funkcia."""
    print("╔" + "═" * 78 + "╗")
    print("║" + " NEX AUTOMAT v2.1 - DIAGNOSTIKA ITEMS WIDGETU ".center(78) + "║")
    print("╚" + "═" * 78 + "╝")

    # 1. Nájdi items widget
    found_files = find_items_widget()

    # 2. Hľadaj referencie
    results = search_for_items_grid()

    # 3. Analyzuj main_window
    analyze_main_window()

    # 4. Skontroluj konštanty
    check_constants()

    # Zhrnutie
    print(f"\n{'=' * 80}")
    print("ZHRNUTIE")
    print(f"{'=' * 80}")

    if found_files:
        print(f"✅ Našiel som {len(found_files)} relevantný widget(y)")
        for f in found_files:
            print(f"   - {f.name}")
    else:
        print("⚠️  Potrebujem bližší pohľad na main_window.py")

    print("\n⏭️  ĎALŠÍ KROK:")
    print("   Po identifikácii widgetu aplikujeme grid settings")


if __name__ == "__main__":
    main()