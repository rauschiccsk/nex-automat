"""
NEX Automat v2.1 - Diagnostika grid_settings API
Zistí, aký formát dát očakáva save_column_settings().
"""

from pathlib import Path

# Paths
BASE_DIR = Path(r"C:\Development\nex-automat")
GRID_SETTINGS_FILE = BASE_DIR / "apps" / "supplier-invoice-editor" / "src" / "utils" / "grid_settings.py"
WIDGET_FILE = BASE_DIR / "apps" / "supplier-invoice-editor" / "src" / "ui" / "widgets" / "invoice_list_widget.py"


def analyze_save_column_settings():
    """Analyzuj save_column_settings funkciu."""
    print(f"\n{'=' * 80}")
    print("1. ANALÝZA save_column_settings() v grid_settings.py")
    print(f"{'=' * 80}")

    with open(GRID_SETTINGS_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Nájdi funkciu
    for i, line in enumerate(lines):
        if 'def save_column_settings(' in line:
            print(f"✅ Funkcia nájdená na riadku {i + 1}")
            print(f"\nSignatúra:")

            # Zobraz signatúru (môže byť na viacerých riadkoch)
            j = i
            while j < len(lines) and ':' not in lines[j]:
                print(f"  {j + 1:4d}: {lines[j].rstrip()}")
                j += 1
            if j < len(lines):
                print(f"  {j + 1:4d}: {lines[j].rstrip()}")

            # Zobraz prvých 30 riadkov funkcie
            print(f"\nTelo funkcie (prvých 30 riadkov):")
            for j in range(i, min(i + 30, len(lines))):
                print(f"  {j + 1:4d}: {lines[j].rstrip()}")

            break


def analyze_load_column_settings():
    """Analyzuj load_column_settings funkciu - aby sme videli očakávaný formát."""
    print(f"\n{'=' * 80}")
    print("2. ANALÝZA load_column_settings() - NÁVRATOVÝ FORMÁT")
    print(f"{'=' * 80}")

    with open(GRID_SETTINGS_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Nájdi funkciu
    for i, line in enumerate(lines):
        if 'def load_column_settings(' in line:
            print(f"✅ Funkcia nájdená na riadku {i + 1}")

            # Zobraz return statements
            print(f"\nReturn statements:")
            for j in range(i, min(i + 50, len(lines))):
                if 'return' in lines[j]:
                    # Zobraz kontext okolo return
                    for k in range(max(i, j - 3), min(len(lines), j + 2)):
                        marker = ">>>" if k == j else "   "
                        print(f"{marker} {k + 1:4d}: {lines[k].rstrip()}")
                    print()

            break


def show_current_widget_code():
    """Zobraz, ako widget používa save_column_settings."""
    print(f"\n{'=' * 80}")
    print("3. AKO WIDGET VOLÁ save_column_settings()")
    print(f"{'=' * 80}")

    with open(WIDGET_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Nájdi _save_grid_settings
    for i, line in enumerate(lines):
        if 'def _save_grid_settings(self):' in line:
            print(f"✅ Metóda nájdená na riadku {i + 1}")

            # Zobraz celú metódu
            print(f"\nCelá metóda:")
            indent = len(lines[i]) - len(lines[i].lstrip())
            for j in range(i, min(i + 30, len(lines))):
                line = lines[j]
                # Koniec metódy = ďalšia metóda na rovnakej úrovni
                if j > i and line.strip() and line.strip().startswith('def '):
                    current_indent = len(line) - len(line.lstrip())
                    if current_indent <= indent:
                        break
                print(f"  {j + 1:4d}: {line.rstrip()}")

            break


def suggest_fix():
    """Navrhni opravu."""
    print(f"\n{'=' * 80}")
    print("4. NÁVRH RIEŠENIA")
    print(f"{'=' * 80}")

    print("\nPravdepodobne potrebujeme zmeniť formát dát:")
    print("\nAktuálne posielame (dictionary):")
    print("  {")
    print("    'ID': {'width': 60, 'visual_index': 0, 'visible': True},")
    print("    'Invoice Number': {'width': 150, ...}")
    print("  }")
    print("\nFunkcia očakáva (list of dictionaries):")
    print("  [")
    print("    {'column_name': 'ID', 'width': 60, 'visual_index': 0, 'visible': True},")
    print("    {'column_name': 'Invoice Number', 'width': 150, ...}")
    print("  ]")
    print("\nAlebo:")
    print("  Funkcia má zlú implementáciu a potrebuje opravu.")


def main():
    """Hlavná funkcia."""
    print("╔" + "═" * 78 + "╗")
    print("║" + " NEX AUTOMAT v2.1 - DIAGNOSTIKA GRID SETTINGS API ".center(78) + "║")
    print("╚" + "═" * 78 + "╝")

    # 1. Analyzuj save_column_settings
    analyze_save_column_settings()

    # 2. Analyzuj load_column_settings
    analyze_load_column_settings()

    # 3. Zobraz widget kód
    show_current_widget_code()

    # 4. Návrh riešenia
    suggest_fix()

    # Zhrnutie
    print(f"\n{'=' * 80}")
    print("ZHRNUTIE")
    print(f"{'=' * 80}")
    print("Po analýze vytvorím opravu buď:")
    print("1. Zmeníme formát dát v _save_grid_settings()")
    print("2. Alebo opravíme save_column_settings() funkciu")


if __name__ == "__main__":
    main()