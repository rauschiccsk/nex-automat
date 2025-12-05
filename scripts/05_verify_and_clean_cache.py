"""
NEX Automat v2.1 - Overenie súboru a vyčistenie cache
"""

import os
import shutil
from pathlib import Path

# Paths
BASE_DIR = Path(r"C:\Development\nex-automat")
WIDGET_FILE = BASE_DIR / "apps" / "supplier-invoice-editor" / "src" / "ui" / "widgets" / "invoice_list_widget.py"
SRC_DIR = BASE_DIR / "apps" / "supplier-invoice-editor" / "src"


def verify_update_invoices():
    """Overí prítomnosť update_invoices v súbore."""
    print(f"\n{'=' * 80}")
    print("1. VERIFIKÁCIA SÚBORU")
    print(f"{'=' * 80}")

    with open(WIDGET_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')

    print(f"Súbor: {WIDGET_FILE}")
    print(f"Riadkov: {len(lines)}")

    # Hľadaj update_invoices
    found = False
    for i, line in enumerate(lines):
        if 'def update_invoices(' in line:
            found = True
            print(f"\n✅ Metóda update_invoices nájdená na riadku {i + 1}")
            # Zobraz 5 riadkov kontextu
            print("\nKontext:")
            for j in range(max(0, i - 2), min(len(lines), i + 6)):
                marker = ">>>" if j == i else "   "
                print(f"{marker} {j + 1:4d}: {lines[j]}")
            break

    if not found:
        print("\n❌ Metóda update_invoices NENÁJDENÁ!")

    return found


def clean_pycache():
    """Vymaže všetky __pycache__ a .pyc súbory."""
    print(f"\n{'=' * 80}")
    print("2. ČISTENIE PYTHON CACHE")
    print(f"{'=' * 80}")

    deleted_dirs = 0
    deleted_files = 0

    # Prejdi všetky adresáre
    for root, dirs, files in os.walk(SRC_DIR):
        # Vymaž __pycache__ adresáre
        if '__pycache__' in dirs:
            cache_dir = Path(root) / '__pycache__'
            try:
                shutil.rmtree(cache_dir)
                print(f"✅ Vymazaný: {cache_dir.relative_to(SRC_DIR)}")
                deleted_dirs += 1
            except Exception as e:
                print(f"❌ Chyba pri mazaní {cache_dir}: {e}")

        # Vymaž .pyc súbory
        for file in files:
            if file.endswith('.pyc'):
                pyc_file = Path(root) / file
                try:
                    pyc_file.unlink()
                    print(f"✅ Vymazaný: {pyc_file.relative_to(SRC_DIR)}")
                    deleted_files += 1
                except Exception as e:
                    print(f"❌ Chyba pri mazaní {pyc_file}: {e}")

    print(f"\n✅ Vymazaných {deleted_dirs} __pycache__ adresárov")
    print(f"✅ Vymazaných {deleted_files} .pyc súborov")

    return True


def show_widget_methods():
    """Zobrazí všetky metódy v InvoiceListWidget."""
    print(f"\n{'=' * 80}")
    print("3. ZOZNAM METÓD V WIDGETE")
    print(f"{'=' * 80}")

    with open(WIDGET_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    methods = []
    for i, line in enumerate(lines):
        if line.strip().startswith('def ') and '(self' in line:
            method_name = line.strip().split('(')[0].replace('def ', '')
            methods.append((i + 1, method_name))

    print(f"\nNájdených {len(methods)} metód:")
    for line_num, method in methods:
        marker = "✅" if method == "update_invoices" else "  "
        print(f"{marker} {line_num:4d}: {method}")


def main():
    """Hlavná funkcia."""
    print("╔" + "═" * 78 + "╗")
    print("║" + " NEX AUTOMAT v2.1 - VERIFIKÁCIA A ČISTENIE ".center(78) + "║")
    print("╚" + "═" * 78 + "╝")

    # 1. Verifikuj súbor
    has_method = verify_update_invoices()

    # 2. Zobraz metódy
    show_widget_methods()

    # 3. Vyčisti cache
    clean_pycache()

    # Zhrnutie
    print(f"\n{'=' * 80}")
    print("ZHRNUTIE")
    print(f"{'=' * 80}")

    if has_method:
        print("✅ Metóda update_invoices JE v súbore")
        print("✅ Python cache vyčistená")
        print("\n⏭️  ĎALŠÍ KROK: Opäť spustiť aplikáciu:")
        print("   python main.py")
    else:
        print("❌ Metóda update_invoices CHÝBA v súbore")
        print("⚠️  Script 04 možno zlyhal pri zápise")
        print("\n⏭️  RIEŠENIE: Manuálne pridať metódu alebo opäť spustiť script 04")


if __name__ == "__main__":
    main()