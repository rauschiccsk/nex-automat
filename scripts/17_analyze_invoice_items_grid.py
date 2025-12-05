"""
NEX Automat v2.1 - Analýza invoice_items_grid.py
Zistí štruktúru a či už má grid settings.
"""

from pathlib import Path
import re

# Paths
BASE_DIR = Path(r"C:\Development\nex-automat")
ITEMS_GRID = BASE_DIR / "apps" / "supplier-invoice-editor" / "src" / "ui" / "widgets" / "invoice_items_grid.py"


def analyze_file_structure():
    """Analyzuj štruktúru súboru."""
    print(f"\n{'=' * 80}")
    print("1. ŠTRUKTÚRA SÚBORU")
    print(f"{'=' * 80}")

    with open(ITEMS_GRID, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    print(f"Súbor: {ITEMS_GRID.name}")
    print(f"Riadkov: {len(lines)}")

    # Nájdi triedy
    print("\nTriedy:")
    for i, line in enumerate(lines):
        if line.strip().startswith('class '):
            class_name = line.strip().split('(')[0].replace('class ', '')
            print(f"  {i + 1:4d}: {class_name}")

    # Nájdi metódy
    print("\nMetódy (prvých 20):")
    method_count = 0
    for i, line in enumerate(lines):
        if line.strip().startswith('def '):
            method = line.strip().split('(')[0].replace('def ', '')
            print(f"  {i + 1:4d}: {method}()")
            method_count += 1
            if method_count >= 20:
                print(f"  ... a ďalšie")
                break

    return lines


def check_grid_settings():
    """Skontroluj, či už má grid settings."""
    print(f"\n{'=' * 80}")
    print("2. KONTROLA GRID SETTINGS")
    print(f"{'=' * 80}")

    with open(ITEMS_GRID, 'r', encoding='utf-8') as f:
        content = f.read()

    checks = {
        'Import grid_settings': 'from utils.grid_settings import' in content,
        'Import GRID_INVOICE_ITEMS': 'GRID_INVOICE_ITEMS' in content,
        '_load_grid_settings()': 'def _load_grid_settings(' in content,
        '_save_grid_settings()': 'def _save_grid_settings(' in content,
        '_on_column_resized()': 'def _on_column_resized(' in content,
        '_on_column_moved()': 'def _on_column_moved(' in content,
    }

    has_grid_settings = False
    for check_name, result in checks.items():
        status = "✅" if result else "❌"
        print(f"{status} {check_name}")
        if result:
            has_grid_settings = True

    return has_grid_settings


def check_table_attribute():
    """Zistí, aký atribút používa pre table."""
    print(f"\n{'=' * 80}")
    print("3. TABLE ATRIBÚT")
    print(f"{'=' * 80}")

    with open(ITEMS_GRID, 'r', encoding='utf-8') as f:
        content = f.read()

    # Hľadaj self.table alebo self.table_view
    if 'self.table_view' in content:
        print("✅ Používa: self.table_view")
        return 'table_view'
    elif 'self.table' in content:
        print("✅ Používa: self.table")
        return 'table'
    else:
        print("⚠️  Nepodarilo sa identifikovať")
        return None


def check_model_structure():
    """Zistí, ako je definovaný model."""
    print(f"\n{'=' * 80}")
    print("4. MODEL ŠTRUKTÚRA")
    print(f"{'=' * 80}")

    with open(ITEMS_GRID, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Hľadaj COLUMNS alebo HEADERS
    for i, line in enumerate(lines):
        if 'COLUMNS = [' in line or 'HEADERS = [' in line:
            print(f"✅ Našiel som definíciu na riadku {i + 1}")
            # Zobraz niekoľko riadkov
            for j in range(i, min(i + 10, len(lines))):
                print(f"  {j + 1:4d}: {lines[j].rstrip()}")
            return

    print("⚠️  COLUMNS/HEADERS nenájdené - model je možno vonku")


def show_setup_ui():
    """Zobraz _setup_ui metódu."""
    print(f"\n{'=' * 80}")
    print("5. _setup_ui() METÓDA")
    print(f"{'=' * 80}")

    with open(ITEMS_GRID, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if 'def _setup_ui(' in line:
            print(f"✅ Metóda nájdená na riadku {i + 1}")

            # Zobraz metódu (max 40 riadkov)
            indent = len(lines[i]) - len(lines[i].lstrip())
            for j in range(i, min(i + 40, len(lines))):
                line = lines[j]
                # Koniec metódy
                if j > i and line.strip() and line.strip().startswith('def '):
                    current_indent = len(line) - len(line.lstrip())
                    if current_indent <= indent:
                        break
                print(f"  {j + 1:4d}: {line.rstrip()}")

            return

    print("⚠️  _setup_ui nenájdená")


def compare_with_invoice_list():
    """Porovnaj s invoice_list_widget.py."""
    print(f"\n{'=' * 80}")
    print("6. POROVNANIE S invoice_list_widget.py")
    print(f"{'=' * 80}")

    invoice_list = BASE_DIR / "apps" / "supplier-invoice-editor" / "src" / "ui" / "widgets" / "invoice_list_widget.py"

    with open(invoice_list, 'r', encoding='utf-8') as f:
        list_lines = len(f.readlines())

    with open(ITEMS_GRID, 'r', encoding='utf-8') as f:
        grid_lines = len(f.readlines())

    print(f"invoice_list_widget.py: {list_lines} riadkov (✅ má grid settings)")
    print(f"invoice_items_grid.py:  {grid_lines} riadkov (❌ nemá grid settings)")
    print(f"\nRozdiel: {list_lines - grid_lines} riadkov")


def main():
    """Hlavná funkcia."""
    print("╔" + "═" * 78 + "╗")
    print("║" + " NEX AUTOMAT v2.1 - ANALÝZA invoice_items_grid.py ".center(78) + "║")
    print("╚" + "═" * 78 + "╝")

    # 1. Štruktúra
    lines = analyze_file_structure()

    # 2. Grid settings check
    has_grid = check_grid_settings()

    # 3. Table atribút
    table_attr = check_table_attribute()

    # 4. Model
    check_model_structure()

    # 5. Setup UI
    show_setup_ui()

    # 6. Porovnanie
    compare_with_invoice_list()

    # Zhrnutie
    print(f"\n{'=' * 80}")
    print("ZHRNUTIE")
    print(f"{'=' * 80}")

    if has_grid:
        print("✅ Items grid už má grid settings")
    else:
        print("❌ Items grid NEMÁ grid settings")
        print("\n⏭️  ĎALŠÍ KROK:")
        print("   Aplikovať grid settings ako pre invoice_list_widget")
        print("   Použiť konštantu: GRID_INVOICE_ITEMS")
        if table_attr:
            print(f"   Table atribút: self.{table_attr}")


if __name__ == "__main__":
    main()