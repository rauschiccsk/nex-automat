"""
Fix InvoiceItemsWindow call in main_window.py - add repository parameter.
"""

from pathlib import Path

TARGET_FILE = Path("apps/supplier-invoice-staging/ui/main_window.py")

OLD_CALL = '''        window = InvoiceItemsWindow(
            invoice=invoice,
            settings=self.settings,
            parent=self
        )'''

NEW_CALL = '''        window = InvoiceItemsWindow(
            invoice=invoice,
            settings=self.settings,
            repository=self.repository,
            parent=self
        )'''


def main():
    if not TARGET_FILE.exists():
        print(f"ERROR: {TARGET_FILE} not found!")
        return

    content = TARGET_FILE.read_text(encoding="utf-8")

    if OLD_CALL in content:
        content = content.replace(OLD_CALL, NEW_CALL)
        TARGET_FILE.write_text(content, encoding="utf-8")
        print(f"Updated: {TARGET_FILE}")
        print("Added repository parameter to InvoiceItemsWindow call")
    else:
        print("Pattern not found or already updated")


if __name__ == "__main__":
    main()