"""
Add ESC key handler to MainWindow for closing.
Run from: C:/Development/nex-automat
"""

from pathlib import Path


def main():
    file_path = Path("apps/supplier-invoice-staging/ui/main_window.py")

    if not file_path.exists():
        print(f"ERROR: {file_path} not found")
        return False

    content = file_path.read_text(encoding="utf-8")

    # Update keyPressEvent to handle both ESC and Enter
    old_code = '''    def keyPressEvent(self, event):
        """Handle key press - Enter opens invoice items."""
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            current_row = self.grid.table_view.currentIndex().row()
            if current_row >= 0:
                self._on_row_activated(current_row)
                return
        super().keyPressEvent(event)'''

    new_code = '''    def keyPressEvent(self, event):
        """Handle key press - Enter opens invoice items, ESC closes window."""
        if event.key() == Qt.Key.Key_Escape:
            self.close()
            return
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            current_row = self.grid.table_view.currentIndex().row()
            if current_row >= 0:
                self._on_row_activated(current_row)
                return
        super().keyPressEvent(event)'''

    if old_code not in content:
        print("ERROR: Could not find keyPressEvent method")
        return False

    content = content.replace(old_code, new_code)

    file_path.write_text(content, encoding="utf-8")
    print(f"OK: Added ESC handler to {file_path}")
    return True


if __name__ == "__main__":
    main()