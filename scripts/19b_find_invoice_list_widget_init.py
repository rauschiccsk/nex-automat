r"""
Script 19b: Nájdi InvoiceListWidget.__init__() kde sa vytvára table_view.
"""

from pathlib import Path

# Cesta k projektu
PROJECT_ROOT = Path("C:/Development/nex-automat")
TARGET_FILE = PROJECT_ROOT / "apps/supplier-invoice-editor/src/ui/widgets/invoice_list_widget.py"


def main():
    """Nájdi InvoiceListWidget.__init__()."""
    print(f"Analyzujem: {TARGET_FILE}")
    print("=" * 70)

    if not TARGET_FILE.exists():
        print(f"❌ Súbor neexistuje: {TARGET_FILE}")
        return

    content = TARGET_FILE.read_text(encoding='utf-8')
    lines = content.splitlines()

    # Nájdi InvoiceListWidget class
    print("\n1. HĽADÁM TRIEDU InvoiceListWidget:")
    print("-" * 70)

    widget_class_line = 0
    for i, line in enumerate(lines, 1):
        if 'class InvoiceListWidget' in line:
            widget_class_line = i
            print(f"✅ Nájdená na riadku {i}: {line.strip()}")
            break

    if widget_class_line == 0:
        print("❌ InvoiceListWidget trieda nenájdená!")
        return

    # Nájdi __init__ metódu tejto triedy
    print("\n2. __INIT__ METÓDA InvoiceListWidget:")
    print("-" * 70)

    init_line = 0
    in_class = False
    for i, line in enumerate(lines, 1):
        if i >= widget_class_line:
            in_class = True

        # Koniec triedy - ďalšia trieda alebo koniec súboru
        if in_class and i > widget_class_line and line.strip().startswith('class '):
            break

        if in_class and 'def __init__(self' in line:
            init_line = i
            print(f"✅ Nájdená na riadku {i}")
            # Zobraz 30 riadkov od __init__
            for j in range(i - 1, min(i + 30, len(lines))):
                print(f"  {j + 1:4d}: {lines[j]}")
            break

    if init_line == 0:
        print("❌ __init__ metóda nenájdená!")
        return

    # Nájdi koniec __init__
    print("\n3. KONIEC __init__ METÓDY:")
    print("-" * 70)

    for i in range(init_line, len(lines)):
        line = lines[i]
        # Ďalšia metóda = koniec __init__
        if i > init_line and line.strip().startswith('def '):
            print(f"✅ Koniec pred riadkom {i + 1}: {line.strip()}")
            break

    print("\n" + "=" * 70)
    print("ZÁVER:")
    print("Pre integráciu grid settings potrebujem:")
    print("  1. Pridať volanie _load_grid_settings() na koniec __init__")
    print("  2. Vytvoriť metódu _load_grid_settings()")
    print("  3. Pripojiť header.sectionResized.connect(_save_grid_settings)")
    print("  4. Pripojiť header.sectionMoved.connect(_save_grid_settings)")
    print("  5. Vytvoriť metódu _save_grid_settings()")


if __name__ == "__main__":
    main()