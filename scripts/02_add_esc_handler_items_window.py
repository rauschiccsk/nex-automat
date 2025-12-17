"""
Add ESC key handler to InvoiceItemsWindow for closing.
Run from: C:/Development/nex-automat
"""

from pathlib import Path


def main():
    file_path = Path("apps/supplier-invoice-staging/ui/invoice_items_window.py")

    if not file_path.exists():
        print(f"ERROR: {file_path} not found")
        return False

    content = file_path.read_text(encoding="utf-8")

    # Check if already implemented
    if "keyPressEvent" in content:
        print("keyPressEvent already exists in InvoiceItemsWindow")
        return False

    # Find closeEvent and insert keyPressEvent before it
    old_code = '''    def closeEvent(self, event):
        self.closed.emit()
        super().closeEvent(event)'''

    new_code = '''    def keyPressEvent(self, event):
        """Handle key press - ESC closes window."""
        if event.key() == Qt.Key.Key_Escape:
            self.close()
            return
        super().keyPressEvent(event)

    def closeEvent(self, event):
        self.closed.emit()
        super().closeEvent(event)'''

    if old_code not in content:
        print("ERROR: Could not find closeEvent method")
        return False

    content = content.replace(old_code, new_code)

    file_path.write_text(content, encoding="utf-8")
    print(f"OK: Added keyPressEvent to {file_path}")
    return True


if __name__ == "__main__":
    main()