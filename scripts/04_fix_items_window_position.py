"""
Fix InvoiceItemsWindow to use same window_name for all invoices.
This ensures consistent window position.
Run from: C:/Development/nex-automat
"""

from pathlib import Path


def main():
    file_path = Path("apps/supplier-invoice-staging/ui/invoice_items_window.py")

    if not file_path.exists():
        print(f"ERROR: {file_path} not found")
        return False

    content = file_path.read_text(encoding="utf-8")

    # Change dynamic window_name to static
    old_code = '''window_name=f"{self.WINDOW_ID}_{invoice['id']}",'''
    new_code = '''window_name=self.WINDOW_ID,'''

    if old_code not in content:
        print("ERROR: Could not find window_name assignment")
        return False

    content = content.replace(old_code, new_code)

    file_path.write_text(content, encoding="utf-8")
    print(f"OK: Fixed window_name in {file_path}")
    return True


if __name__ == "__main__":
    main()