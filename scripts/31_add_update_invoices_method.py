r"""
Script 31: Pridanie update_invoices() metódy do InvoiceListWidget.
"""

from pathlib import Path

# Cesta k projektu
PROJECT_ROOT = Path("C:/Development/nex-automat")
TARGET_FILE = PROJECT_ROOT / "apps/supplier-invoice-editor/src/ui/widgets/invoice_list_widget.py"


def main():
    """Pridá update_invoices() metódu."""
    print(f"Upravujem: {TARGET_FILE}")

    if not TARGET_FILE.exists():
        print(f"❌ Súbor neexistuje: {TARGET_FILE}")
        return

    content = TARGET_FILE.read_text(encoding='utf-8')
    lines = content.splitlines()

    # Skontroluj či už metóda existuje
    if 'def update_invoices' in content:
        print("✅ Metóda update_invoices už existuje!")
        return

    # Nájdi _setup_ui metódu (po __init__)
    setup_ui_line = 0
    for i, line in enumerate(lines):
        if 'def _setup_ui(self):' in line and i > 130:
            setup_ui_line = i
            break

    if setup_ui_line == 0:
        print("❌ Nepodarilo sa nájsť _setup_ui metódu!")
        return

    # Pridaj update_invoices pred _setup_ui
    print(f"✅ Vkladám update_invoices pred riadok {setup_ui_line + 1}")

    method = [
        '',
        '    def update_invoices(self, invoices):',
        '        """Update invoice list with new data."""',
        '        self.model.set_invoices(invoices)',
        '        self.logger.info(f"Invoice list updated with {len(invoices)} invoices")',
        '',
    ]

    # Vlož metódu
    for line in reversed(method):
        lines.insert(setup_ui_line, line)

    # Zapíš späť
    content = '\n'.join(lines)
    TARGET_FILE.write_text(content, encoding='utf-8')

    print(f"\n✅ Súbor upravený: {TARGET_FILE}")
    print(f"   Nové riadky: {len(lines)}")
    print("\nPridaná metóda:")
    print("  ✅ update_invoices(invoices) - volá model.set_invoices()")
    print("\nTeraz spusti aplikáciu znova!")


if __name__ == "__main__":
    main()