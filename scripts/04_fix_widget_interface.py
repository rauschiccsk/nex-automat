"""
NEX Automat v2.1 - Oprava rozhrania InvoiceListWidget
Pridá alias update_invoices() -> set_invoices()
"""

from pathlib import Path

# Paths
BASE_DIR = Path(r"C:\Development\nex-automat")
WIDGET_FILE = BASE_DIR / "apps" / "supplier-invoice-editor" / "src" / "ui" / "widgets" / "invoice_list_widget.py"


def add_update_invoices_alias():
    """Pridá alias metódu update_invoices."""
    print(f"\n{'=' * 80}")
    print("1. ČÍTAM SÚBOR")
    print(f"{'=' * 80}")

    with open(WIDGET_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')

    print(f"✅ Načítaných {len(lines)} riadkov")

    # Nájdi koniec metódy set_invoices
    print(f"\n{'=' * 80}")
    print("2. HĽADÁM MIESTO PRE ALIAS")
    print(f"{'=' * 80}")

    insert_line = None
    in_set_invoices = False
    indent_level = 0

    for i, line in enumerate(lines):
        # Nájdi začiatok set_invoices
        if 'def set_invoices(' in line:
            in_set_invoices = True
            indent_level = len(line) - len(line.lstrip())
            print(f"✅ Nájdená metóda set_invoices na riadku {i + 1}")
            continue

        # Ak sme v set_invoices, hľadáme jej koniec
        if in_set_invoices:
            # Koniec metódy = ďalšia metóda na rovnakej úrovni alebo koniec súboru
            stripped = line.lstrip()
            if stripped and not stripped.startswith('#'):
                current_indent = len(line) - len(stripped)
                if current_indent <= indent_level and (stripped.startswith('def ') or stripped.startswith('class ')):
                    insert_line = i
                    print(f"✅ Koniec metódy set_invoices na riadku {i}")
                    break

    if insert_line is None:
        # Ak sme na konci súboru
        insert_line = len(lines)
        print(f"✅ Pridám na koniec súboru (riadok {insert_line})")

    # Vytvor alias metódu
    print(f"\n{'=' * 80}")
    print("3. VYTVÁRAM ALIAS METÓDU")
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
    print("4. VKLADÁM ALIAS DO SÚBORU")
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


def verify_fix():
    """Overí, že alias bol pridaný."""
    print(f"\n{'=' * 80}")
    print("6. VERIFIKÁCIA")
    print(f"{'=' * 80}")

    with open(WIDGET_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'def update_invoices(' in content and 'self.set_invoices(invoices)' in content:
        print("✅ Alias update_invoices() EXISTUJE")
        print("✅ Volá set_invoices()")
        return True
    else:
        print("❌ Alias nebol správne pridaný")
        return False


def main():
    """Hlavná funkcia."""
    print("╔" + "═" * 78 + "╗")
    print("║" + " NEX AUTOMAT v2.1 - OPRAVA ROZHRANIA WIDGETU ".center(78) + "║")
    print("╚" + "═" * 78 + "╝")

    # Pridaj alias
    if not add_update_invoices_alias():
        print("\n❌ STOP: Pridanie aliasu zlyhalo")
        return

    # Overenie
    if not verify_fix():
        print("\n❌ STOP: Verifikácia zlyhala")
        return

    # Zhrnutie
    print(f"\n{'=' * 80}")
    print("ZHRNUTIE")
    print(f"{'=' * 80}")
    print("✅ Alias update_invoices() pridaný")
    print("✅ Kompatibilita s main_window.py obnovená")
    print("\n⏭️  ĎALŠÍ KROK: Otestovať aplikáciu:")
    print("   python main.py")


if __name__ == "__main__":
    main()