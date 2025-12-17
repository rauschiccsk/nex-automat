"""
Make InvoiceItemsWindow modal - only one invoice can be open at a time.
Run from: C:/Development/nex-automat
"""

from pathlib import Path


def main():
    file_path = Path("apps/supplier-invoice-staging/ui/main_window.py")

    if not file_path.exists():
        print(f"ERROR: {file_path} not found")
        return False

    content = file_path.read_text(encoding="utf-8")

    # Replace _open_items_window to use modal window with self as parent
    old_code = '''    def _open_items_window(self, invoice: dict):
        invoice_id = invoice["id"]

        if invoice_id in self._items_windows:
            window = self._items_windows[invoice_id]
            if window.isVisible():
                window.activateWindow()
                window.raise_()
                return

        window = InvoiceItemsWindow(
            invoice=invoice,
            settings=self.settings,
            parent=None
        )
        window.closed.connect(lambda: self._on_items_window_closed(invoice_id))
        self._items_windows[invoice_id] = window
        window.show()'''

    new_code = '''    def _open_items_window(self, invoice: dict):
        invoice_id = invoice["id"]

        if invoice_id in self._items_windows:
            window = self._items_windows[invoice_id]
            if window.isVisible():
                window.activateWindow()
                window.raise_()
                return

        window = InvoiceItemsWindow(
            invoice=invoice,
            settings=self.settings,
            parent=self
        )
        window.closed.connect(lambda: self._on_items_window_closed(invoice_id))
        self._items_windows[invoice_id] = window
        window.setWindowModality(Qt.WindowModality.ApplicationModal)
        window.show()'''

    if old_code not in content:
        print("ERROR: Could not find _open_items_window method")
        return False

    content = content.replace(old_code, new_code)

    file_path.write_text(content, encoding="utf-8")
    print(f"OK: Made InvoiceItemsWindow modal in {file_path}")
    return True


if __name__ == "__main__":
    main()