"""
Fix settings save on window close for both MainWindow and InvoiceItemsWindow.
Run from: C:/Development/nex-automat
"""

from pathlib import Path


def fix_main_window():
    file_path = Path("apps/supplier-invoice-staging/ui/main_window.py")

    if not file_path.exists():
        print(f"ERROR: {file_path} not found")
        return False

    content = file_path.read_text(encoding="utf-8")

    # Check if already fixed
    if "self.grid.save_grid_settings_now()" in content:
        print(f"SKIP: {file_path} already fixed")
        return True

    old_code = '''    def closeEvent(self, event):
        for window in list(self._items_windows.values()):
            window.close()
        super().closeEvent(event)'''

    new_code = '''    def closeEvent(self, event):
        for window in list(self._items_windows.values()):
            window.close()
        self.grid.save_grid_settings_now()
        super().closeEvent(event)'''

    if old_code not in content:
        print(f"ERROR: Could not find closeEvent in {file_path}")
        return False

    content = content.replace(old_code, new_code)
    file_path.write_text(content, encoding="utf-8")
    print(f"OK: Fixed {file_path}")
    return True


def fix_items_window():
    file_path = Path("apps/supplier-invoice-staging/ui/invoice_items_window.py")

    if not file_path.exists():
        print(f"ERROR: {file_path} not found")
        return False

    content = file_path.read_text(encoding="utf-8")

    # Check if already fixed
    if "self.grid.save_grid_settings_now()" in content:
        print(f"SKIP: {file_path} already fixed")
        return True

    old_code = '''    def closeEvent(self, event):
        self.closed.emit()
        super().closeEvent(event)'''

    new_code = '''    def closeEvent(self, event):
        self.grid.save_grid_settings_now()
        self.closed.emit()
        super().closeEvent(event)'''

    if old_code not in content:
        print(f"ERROR: Could not find closeEvent in {file_path}")
        return False

    content = content.replace(old_code, new_code)
    file_path.write_text(content, encoding="utf-8")
    print(f"OK: Fixed {file_path}")
    return True


def main():
    fix_main_window()
    fix_items_window()
    print("Done!")


if __name__ == "__main__":
    main()