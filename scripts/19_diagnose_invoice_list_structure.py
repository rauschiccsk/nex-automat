r"""
Script 19: Diagnostika invoice_list_widget.py - štruktúra pre grid settings.

Zistí:
- Kde sa vytvára table_view a header
- Aké sú názvy stĺpcov
- Kde pripojiť signály pre resize/move
"""

from pathlib import Path

# Cesta k projektu
PROJECT_ROOT = Path("C:/Development/nex-automat")
TARGET_FILE = PROJECT_ROOT / "apps/supplier-invoice-editor/src/ui/widgets/invoice_list_widget.py"


def main():
    """Analyzuje invoice_list_widget.py."""
    print(f"Analyzujem: {TARGET_FILE}")
    print("=" * 70)

    if not TARGET_FILE.exists():
        print(f"❌ Súbor neexistuje: {TARGET_FILE}")
        return

    content = TARGET_FILE.read_text(encoding='utf-8')
    lines = content.splitlines()

    # 1. Nájdi definíciu COLUMNS
    print("\n1. DEFINÍCIA STĹPCOV:")
    print("-" * 70)
    in_columns = False
    for i, line in enumerate(lines, 1):
        if 'COLUMNS = [' in line or 'self.columns = [' in line:
            in_columns = True
            print(f"Začiatok na riadku {i}")

        if in_columns:
            print(f"  {i:4d}: {line}")
            if ']' in line and in_columns:
                break

    # 2. Nájdi vytvorenie table_view a header
    print("\n2. TABLE VIEW A HEADER:")
    print("-" * 70)
    for i, line in enumerate(lines, 1):
        if 'self.table_view' in line and '=' in line:
            print(f"  {i:4d}: {line.strip()}")
        if 'header' in line.lower() and 'table_view' in line:
            print(f"  {i:4d}: {line.strip()}")

    # 3. Nájdi quick search setup
    print("\n3. QUICK SEARCH SETUP:")
    print("-" * 70)
    for i, line in enumerate(lines, 1):
        if 'QuickSearchController' in line or 'quick_search' in line.lower():
            print(f"  {i:4d}: {line.strip()}")

    # 4. Nájdi signály
    print("\n4. EXISTUJÚCE SIGNÁLY:")
    print("-" * 70)
    for i, line in enumerate(lines, 1):
        if '.connect(' in line:
            print(f"  {i:4d}: {line.strip()}")

    # 5. Nájdi __init__ metódu
    print("\n5. __INIT__ METÓDA:")
    print("-" * 70)
    for i, line in enumerate(lines, 1):
        if 'def __init__(self' in line:
            print(f"Začína na riadku {i}")
            # Zobraz niekoľko riadkov
            for j in range(i - 1, min(i + 15, len(lines))):
                print(f"  {j + 1:4d}: {lines[j]}")
            break

    print("\n" + "=" * 70)
    print("ZÁVER:")
    print("Pre grid settings potrebujem:")
    print("  1. Názvy stĺpcov (COLUMNS alebo self.columns)")
    print("  2. Header objekt (self.table_view.horizontalHeader())")
    print("  3. Pripojiť signály: sectionResized, sectionMoved")
    print("  4. Načítať/uložiť settings v __init__ / pri zmene")


if __name__ == "__main__":
    main()