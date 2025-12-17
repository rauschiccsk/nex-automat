"""
Add Enter key handler to MainWindow for opening invoice items.
Run from: C:\Development\nex-automat
"""

from pathlib import Path


def main():
    file_path = Path("apps/supplier-invoice-staging/ui/main_window.py")

    if not file_path.exists():
        print(f"ERROR: {file_path} not found")
        return False

    content = file_path.read_text(encoding="utf-8")

    # Check if already implemented
    if "keyPressEvent" in content:
        print("keyPressEvent already exists in MainWindow")
        return False

    # Add import for Qt.Key if not present
    if "from PySide6.QtCore import Qt, Slot" in content:
        # Qt is already imported, we have Qt.Key available
        pass

    # Find the closeEvent method and insert keyPressEvent before it
    old_code = '''    def closeEvent(self, event):
        for window in list(self._items_windows.values()):
            window.close()
        super().closeEvent(event)'''

    new_code = '''    def keyPressEvent(self, event):
        """Handle key press - Enter opens invoice items."""
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            current_row = self.grid.table_view.currentIndex().row()
            if current_row >= 0:
                self._on_row_activated(current_row)
                return
        super().keyPressEvent(event)

    def closeEvent(self, event):
        for window in list(self._items_windows.values()):
            window.close()
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