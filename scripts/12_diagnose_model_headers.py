"""
NEX Automat v2.1 - Diagnostika InvoiceListModel
Zistí, ako získať názvy stĺpcov z modelu.
"""

from pathlib import Path
import re

# Paths
BASE_DIR = Path(r"C:\Development\nex-automat")
WIDGET_FILE = BASE_DIR / "apps" / "supplier-invoice-editor" / "src" / "ui" / "widgets" / "invoice_list_widget.py"


def analyze_model_class():
    """Analyzuj InvoiceListModel triedu."""
    print(f"\n{'=' * 80}")
    print("1. ANALÝZA InvoiceListModel")
    print(f"{'=' * 80}")

    with open(WIDGET_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Nájdi InvoiceListModel
    model_start = None
    model_end = None

    for i, line in enumerate(lines):
        if 'class InvoiceListModel' in line:
            model_start = i
            print(f"✅ InvoiceListModel začína na riadku {i + 1}")
            break

    if model_start is None:
        print("❌ InvoiceListModel nenájdený!")
        return None

    # Nájdi koniec triedy (ďalšia trieda alebo koniec sekcie)
    for i in range(model_start + 1, len(lines)):
        if lines[i].strip().startswith('class '):
            model_end = i
            break

    if model_end is None:
        model_end = min(model_start + 150, len(lines))

    print(f"✅ InvoiceListModel končí na riadku {model_end}")

    # Zobraz atribúty a metódy
    print("\nAtribúty triedy:")
    for i in range(model_start, model_end):
        line = lines[i]
        # Hľadaj atribúty (veľké písmená alebo self.)
        if re.match(r'\s+(HEADERS|COLUMNS|headers|columns)\s*=', line):
            print(f"  {i + 1:4d}: {line.rstrip()}")

    print("\nMetódy triedy:")
    for i in range(model_start, model_end):
        line = lines[i]
        if line.strip().startswith('def '):
            method = line.strip().split('(')[0].replace('def ', '')
            print(f"  {i + 1:4d}: {method}()")

    return lines, model_start, model_end


def find_header_data():
    """Nájdi, kde sú definované názvy hlavičiek."""
    print(f"\n{'=' * 80}")
    print("2. HĽADANIE HLAVIČIEK")
    print(f"{'=' * 80}")

    with open(WIDGET_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')

    # Hľadaj hardcoded názvy stĺpcov
    headers_found = []

    keywords = ['ID', 'Invoice Number', 'Date', 'Supplier', 'Amount', 'Status']

    for i, line in enumerate(lines):
        for keyword in keywords:
            if f'"{keyword}"' in line or f"'{keyword}'" in line:
                if line not in [h[1] for h in headers_found]:
                    headers_found.append((i + 1, line.strip()))
                break

    if headers_found:
        print(f"\nNájdených {len(headers_found)} riadkov s názvami stĺpcov:")
        for line_num, line in headers_found[:10]:
            print(f"  {line_num:4d}: {line}")

    # Hľadaj headerData metódu
    print("\nMetóda headerData():")
    in_header_data = False
    for i, line in enumerate(lines):
        if 'def headerData(' in line:
            in_header_data = True
            start = i

        if in_header_data:
            print(f"  {i + 1:4d}: {line}")
            if i > start + 20:
                break


def suggest_fix():
    """Navrhni opravu."""
    print(f"\n{'=' * 80}")
    print("3. NÁVRH RIEŠENIA")
    print(f"{'=' * 80}")

    with open(WIDGET_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Skontroluj headerData
    has_headers_list = False
    for line in lines:
        if 'headers = [' in line.lower():
            has_headers_list = True
            break

    if has_headers_list:
        print("\n✅ Model má zoznam hlavičiek v headerData()")
        print("\nRiešenie:")
        print("1. Extrahovať hlavičky z headerData() do atribútu")
        print("2. Alebo použiť headerData() metódu na získanie názvov")
    else:
        print("\n⚠️  Model nemá explicitný zoznam hlavičiek")
        print("\nRiešenie:")
        print("1. Pridať HEADERS atribút do InvoiceListModel")
        print("2. Alebo získať názvy z columnCount() + headerData()")


def show_current_usage():
    """Zobraz aktuálne použitie self.model.HEADERS."""
    print(f"\n{'=' * 80}")
    print("4. POUŽITIE self.model.HEADERS")
    print(f"{'=' * 80}")

    with open(WIDGET_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    uses = []
    for i, line in enumerate(lines):
        if 'self.model.HEADERS' in line:
            uses.append((i + 1, line.rstrip()))

    if uses:
        print(f"\nNájdených {len(uses)} použití:")
        for line_num, line in uses:
            print(f"  {line_num:4d}: {line}")
    else:
        print("\n✅ Žiadne použitie self.model.HEADERS")


def main():
    """Hlavná funkcia."""
    print("╔" + "═" * 78 + "╗")
    print("║" + " NEX AUTOMAT v2.1 - DIAGNOSTIKA MODEL HEADERS ".center(78) + "║")
    print("╚" + "═" * 78 + "╝")

    # 1. Analyzuj model
    result = analyze_model_class()

    if result is None:
        return

    # 2. Nájdi hlavičky
    find_header_data()

    # 3. Návrh riešenia
    suggest_fix()

    # 4. Aktuálne použitie
    show_current_usage()

    # Zhrnutie
    print(f"\n{'=' * 80}")
    print("ZHRNUTIE")
    print(f"{'=' * 80}")
    print("Potrebujem zistiť správny spôsob získania názvov stĺpcov.")
    print("Potom vytvorím opravu pre grid settings metódy.")


if __name__ == "__main__":
    main()