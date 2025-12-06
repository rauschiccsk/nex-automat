#!/usr/bin/env python3
"""
Script 22: Analyze InvoiceItemsGrid
Nájde kde sa ukladajú grid settings a kde je chyba
"""

from pathlib import Path


def analyze_items_grid():
    """Analyzuje InvoiceItemsGrid"""

    grid_path = Path("apps/supplier-invoice-editor/src/ui/widgets/invoice_items_grid.py")

    if not grid_path.exists():
        print(f"❌ File not found: {grid_path}")
        return

    content = grid_path.read_text(encoding='utf-8')
    lines = content.split('\n')

    print("=" * 80)
    print("InvoiceItemsGrid CLASS")
    print("=" * 80)

    # Zobraz imports a class definíciu
    for i, line in enumerate(lines[:30], 1):
        print(f"{i:4d}: {line}")

    # Hľadaj "Chyba pri ukladaní grid settings"
    print("\n" + "=" * 80)
    print("SEARCHING FOR ERROR MESSAGE")
    print("=" * 80)

    for i, line in enumerate(lines, 1):
        if 'Chyba pri ukladaní grid settings' in line:
            print(f"\n✓ Found at line {i}:")
            # Zobraz okolie
            for j in range(max(0, i - 10), min(len(lines), i + 5)):
                marker = ">>>" if j == i - 1 else "   "
                print(f"{marker} {j + 1:4d}: {lines[j]}")

    # Hľadaj save metódy
    print("\n" + "=" * 80)
    print("SAVE METHODS")
    print("=" * 80)

    for i, line in enumerate(lines, 1):
        if 'def ' in line and ('save' in line.lower() or 'settings' in line.lower()):
            print(f"\n{i:4d}: {line.strip()}")


if __name__ == "__main__":
    analyze_items_grid()