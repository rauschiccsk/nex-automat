"""
Fix invoice_items_window.py to use new field names.
"""

from pathlib import Path

TARGET_FILE = Path("apps/supplier-invoice-staging/ui/invoice_items_window.py")

REPLACEMENTS = [
    # Window title
    (
        '''self.setWindowTitle(f"Polozky faktury: {invoice['invoice_number']} - {invoice['supplier_name']}")''',
        '''self.setWindowTitle(f"Polozky faktury: {invoice['xml_invoice_number']} - {invoice['xml_supplier_name']}")'''
    ),
    # Header info
    (
        '''info_text = (f"Dodavatel: {self.invoice['supplier_name']} | "
                     f"Faktura: {self.invoice['invoice_number']} | "
                     f"Datum: {self.invoice['invoice_date']} | "
                     f"Suma: {self.invoice['total_amount']} {self.invoice['currency']}")''',
        '''info_text = (f"Dodavatel: {self.invoice['xml_supplier_name']} | "
                     f"Faktura: {self.invoice['xml_invoice_number']} | "
                     f"Datum: {self.invoice['xml_issue_date']} | "
                     f"Suma: {self.invoice['xml_total_with_vat']} {self.invoice['xml_currency']}")'''
    ),
]


def main():
    if not TARGET_FILE.exists():
        print(f"ERROR: {TARGET_FILE} not found!")
        return

    content = TARGET_FILE.read_text(encoding="utf-8")
    changed = False

    for old, new in REPLACEMENTS:
        if old in content:
            content = content.replace(old, new)
            print(f"Fixed: {old[:60]}...")
            changed = True

    if changed:
        TARGET_FILE.write_text(content, encoding="utf-8")
        print(f"Saved: {TARGET_FILE}")
    else:
        print("No changes needed or patterns not found")


if __name__ == "__main__":
    main()