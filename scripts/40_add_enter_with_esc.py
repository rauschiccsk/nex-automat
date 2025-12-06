#!/usr/bin/env python3
"""
Script 40: Add ENTER handling alongside ESC
Pridá ENTER handling vedľa existujúceho ESC handlingu
"""

from pathlib import Path


def add_enter():
    """Pridá ENTER handling"""

    main_window_path = Path("apps/supplier-invoice-editor/src/ui/main_window.py")

    if not main_window_path.exists():
        print(f"❌ File not found: {main_window_path}")
        return False

    content = main_window_path.read_text(encoding='utf-8')

    print("=" * 80)
    print("ADDING ENTER KEY HANDLING")
    print("=" * 80)

    # Pridaj ENTER pred ESC handling
    old_code = """    def keyPressEvent(self, event):
        \"\"\"Handle key press events - ESC closes application.\"\"\"
        from PyQt5.QtCore import Qt

        if event.key() == Qt.Key_Escape:"""

    new_code = """    def keyPressEvent(self, event):
        \"\"\"Handle key press events - ESC closes application, ENTER opens detail.\"\"\"
        from PyQt5.QtCore import Qt

        # Open invoice detail on Enter/Return
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            # Get current selection
            if hasattr(self, 'invoice_list') and self.invoice_list:
                current_index = self.invoice_list.get_current_index()
                if current_index is not None:
                    invoice_id = self.invoice_list.get_invoice_id_at_index(current_index)
                    if invoice_id:
                        self._on_invoice_activated(invoice_id)
                        event.accept()
                        return

        if event.key() == Qt.Key_Escape:"""

    if old_code in content:
        content = content.replace(old_code, new_code)

        main_window_path.write_text(content, encoding='utf-8')

        print("✅ Added ENTER key handling")
        print("\n📝 Key bindings:")
        print("  - ENTER/RETURN → Open invoice detail")
        print("  - ESC → Close application")

        return True
    else:
        print("❌ Pattern not found")
        return False


if __name__ == "__main__":
    success = add_enter()
    if success:
        print("\n" + "=" * 80)
        print("TEST ENTER KEY")
        print("=" * 80)
        print("cd apps/supplier-invoice-editor")
        print("python main.py")
        print("\n1. Vyber faktúru (šípky hore/dole)")
        print("2. Stlač ENTER")
        print("3. Detail faktúry by sa mal otvoriť! ✅")