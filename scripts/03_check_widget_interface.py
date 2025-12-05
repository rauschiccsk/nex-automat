"""
NEX Automat v2.1 - Kontrola rozhrania InvoiceListWidget
Zistí, aké metódy má widget a ako ich volá main_window.
"""

import re
from pathlib import Path

# Paths
BASE_DIR = Path(r"C:\Development\nex-automat")
WIDGET_FILE = BASE_DIR / "apps" / "supplier-invoice-editor" / "src" / "ui" / "widgets" / "invoice_list_widget.py"
MAIN_WINDOW_FILE = BASE_DIR / "apps" / "supplier-invoice-editor" / "src" / "ui" / "main_window.py"


def extract_methods(filepath):
    """Extrahuje všetky metódy z triedy."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Nájdi všetky metódy def method_name(self, ...)
    pattern = r'^\s*def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\('
    methods = []
    for match in re.finditer(pattern, content, re.MULTILINE):
        method_name = match.group(1)
        if not method_name.startswith('__'):  # Skip __init__, __str__, atď.
            methods.append(method_name)

    return sorted(set(methods))


def find_widget_calls(filepath):
    """Nájde všetky volania invoice_list.method()."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Nájdi self.invoice_list.method(...)
    pattern = r'self\.invoice_list\.([a-zA-Z_][a-zA-Z0-9_]*)\s*\('
    calls = []
    for match in re.finditer(pattern, content):
        method_name = match.group(1)
        calls.append(method_name)

    return sorted(set(calls))


def main():
    print("╔" + "═" * 78 + "╗")
    print("║" + " NEX AUTOMAT v2.1 - KONTROLA ROZHRANIA WIDGETU ".center(78) + "║")
    print("╚" + "═" * 78 + "╝")

    # 1. Metódy v InvoiceListWidget
    print(f"\n{'=' * 80}")
    print("1. METÓDY V invoice_list_widget.py")
    print(f"{'=' * 80}")

    widget_methods = extract_methods(WIDGET_FILE)
    print(f"\nNájdených {len(widget_methods)} metód:")
    for m in widget_methods:
        print(f"  - {m}")

    # 2. Volania z main_window.py
    print(f"\n{'=' * 80}")
    print("2. VOLANIA Z main_window.py")
    print(f"{'=' * 80}")

    main_calls = find_widget_calls(MAIN_WINDOW_FILE)
    print(f"\nNájdených {len(main_calls)} volaní:")
    for c in main_calls:
        print(f"  - {c}")

    # 3. Kompatibilita
    print(f"\n{'=' * 80}")
    print("3. KOMPATIBILITA")
    print(f"{'=' * 80}")

    print("\nKontrola volaní:")
    missing = []
    for call in main_calls:
        if call in widget_methods:
            print(f"  ✅ {call} - existuje")
        else:
            print(f"  ❌ {call} - CHÝBA v widgete!")
            missing.append(call)

    # 4. Podobné metódy
    if missing:
        print(f"\n{'=' * 80}")
        print("4. PODOBNÉ/ALTERNATÍVNE METÓDY")
        print(f"{'=' * 80}")

        for miss in missing:
            print(f"\nHľadám alternatívu pre: {miss}")
            # Hľadaj podobné názvy
            for method in widget_methods:
                if any(word in method for word in miss.split('_')):
                    print(f"  📝 Možno: {method}")

    # Zhrnutie
    print(f"\n{'=' * 80}")
    print("ZHRNUTIE")
    print(f"{'=' * 80}")

    if missing:
        print(f"\n❌ NEKOMPATIBILNÉ: {len(missing)} volaní chýba:")
        for m in missing:
            print(f"   - {m}")
        print("\n✅ RIEŠENIE: Pridať alias alebo opraviť volania")
    else:
        print("\n✅ Rozhranie je kompatibilné")


if __name__ == "__main__":
    main()