"""
NEX Automat v2.1 - Oprava: Pridanie update_invoices do SPRÁVNEJ triedy
Pridá alias do InvoiceListWidget (nie do InvoiceListModel)
"""

from pathlib import Path

# Paths
BASE_DIR = Path(r"C:\Development\nex-automat")
WIDGET_FILE = BASE_DIR / "apps" / "supplier-invoice-editor" / "src" / "ui" / "widgets" / "invoice_list_widget.py"


def add_update_invoices_to_widget_class():
    """Pridá update_invoices do InvoiceListWidget (druhá trieda)."""
    print(f"\n{'=' * 80}")
    print("1. ČÍTAM SÚBOR")
    print(f"{'=' * 80}")

    with open(WIDGET_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')

    print(f"✅ Načítaných {len(lines)} riadkov")

    # Nájdi druhý set_invoices (v InvoiceListWidget)
    print(f"\n{'=' * 80}")
    print("2. HĽADÁM DRUHÝ set_invoices (v InvoiceListWidget)")
    print(f"{'=' * 80}")

    set_invoices_count = 0
    insert_line = None
    in_second_set_invoices = False
    indent_level = 0

    for i, line in enumerate(lines):
        # Počítaj set_invoices
        if 'def set_invoices(' in line:
            set_invoices_count += 1
            if set_invoices_count == 2:
                # Toto je druhý set_invoices v InvoiceListWidget
                in_second_set_invoices = True
                indent_level = len(line) - len(line.lstrip())
                print(f"✅ Druhý set_invoices nájdený na riadku {i + 1}")
                continue

        # Hľadaj koniec druhého set_invoices
        if in_second_set_invoices:
            stripped = line.lstrip()
            if stripped and not stripped.startswith('#'):
                current_indent = len(line) - len(stripped)
                if current_indent <= indent_level and (stripped.startswith('def ') or stripped.startswith('class ')):
                    insert_line = i
                    print(f"✅ Koniec druhého set_invoices na riadku {i}")
                    break

    if insert_line is None:
        print("❌ Nepodarilo sa nájsť vhodné miesto!")
        return False

    # Vytvor alias
    print(f"\n{'=' * 80}")
    print("3. VYTVÁRAM ALIAS PRE InvoiceListWidget")
    print(f"{'=' * 80}")

    alias_code = [
        '',
        '    def update_invoices(self, invoices):',
        '        """Alias for set_invoices() - for compatibility with main_window.py"""',
        '        self.set_invoices(invoices)',
        ''
    ]

    print("Alias metóda:")
    for line in alias_code:
        print(f"  {line}")

    # Vlož alias
    print(f"\n{'=' * 80}")
    print("4. VKLADÁM ALIAS")
    print(f"{'=' * 80}")

    for idx, line in enumerate(alias_code):
        lines.insert(insert_line + idx, line)

    print(f"✅ Alias vložený na riadok {insert_line}")

    # Zapíš späť
    print(f"\n{'=' * 80}")
    print("5. UKLADÁM SÚBOR")
    print(f"{'=' * 80}")

    new_content = '\n'.join(lines)

    with open(WIDGET_FILE, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"✅ Súbor uložený")
    print(f"✅ Nový počet riadkov: {len(lines)}")

    return True


def verify_both_classes():
    """Overí, že obe triedy majú update_invoices."""
    print(f"\n{'=' * 80}")
    print("6. VERIFIKÁCIA OBOCH TRIED")
    print(f"{'=' * 80}")

    with open(WIDGET_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    update_invoices_count = 0
    for i, line in enumerate(lines):
        if 'def update_invoices(' in line:
            update_invoices_count += 1
            print(f"✅ update_invoices #{update_invoices_count} na riadku {i + 1}")

    if update_invoices_count == 2:
        print(f"\n✅ Obe triedy majú update_invoices()")
        return True
    else:
        print(f"\n❌ Nájdených len {update_invoices_count} update_invoices")
        return False


def show_class_structure():
    """Zobrazí štruktúru tried."""
    print(f"\n{'=' * 80}")
    print("7. ŠTRUKTÚRA TRIED")
    print(f"{'=' * 80}")

    with open(WIDGET_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    in_class = None
    for i, line in enumerate(lines):
        if line.strip().startswith('class '):
            in_class = line.strip().split('(')[0].replace('class ', '')
            print(f"\n{i + 1:4d}: {in_class}")
        elif in_class and line.strip().startswith('def '):
            method = line.strip().split('(')[0].replace('def ', '')
            marker = "✅" if method == "update_invoices" else "   "
            print(f"{marker} {i + 1:4d}:   └─ {method}()")


def main():
    """Hlavná funkcia."""
    print("╔" + "═" * 78 + "╗")
    print("║" + " NEX AUTOMAT v2.1 - FIX SPRÁVNEJ TRIEDY ".center(78) + "║")
    print("╚" + "═" * 78 + "╝")

    # Ukáž aktuálnu štruktúru
    show_class_structure()

    # Pridaj alias
    if not add_update_invoices_to_widget_class():
        print("\n❌ STOP: Pridanie zlyhalo")
        return

    # Overenie
    if not verify_both_classes():
        print("\n❌ STOP: Verifikácia zlyhala")
        return

    # Znovu ukáž štruktúru
    show_class_structure()

    # Zhrnutie
    print(f"\n{'=' * 80}")
    print("ZHRNUTIE")
    print(f"{'=' * 80}")
    print("✅ update_invoices() pridaný do InvoiceListWidget")
    print("✅ Obe triedy majú teraz update_invoices()")
    print("\n⏭️  ĎALŠÍ KROK: Otestovať aplikáciu:")
    print("   python main.py")


if __name__ == "__main__":
    main()