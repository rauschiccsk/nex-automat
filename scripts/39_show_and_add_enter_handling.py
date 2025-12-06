#!/usr/bin/env python3
"""
Script 39: Show keyPressEvent and add ENTER handling
Zobrazí keyPressEvent a pridá spracovanie ENTER klávesy
"""

from pathlib import Path


def add_enter_handling():
    """Pridá ENTER handling do keyPressEvent"""

    main_window_path = Path("apps/supplier-invoice-editor/src/ui/main_window.py")

    if not main_window_path.exists():
        print(f"❌ File not found: {main_window_path}")
        return False

    content = main_window_path.read_text(encoding='utf-8')
    lines = content.split('\n')

    print("=" * 80)
    print("CURRENT keyPressEvent METHOD")
    print("=" * 80)

    # Zobraz keyPressEvent metódu
    in_method = False
    for i, line in enumerate(lines, 1):
        if 'def keyPressEvent(self, event):' in line:
            in_method = True
            indent_level = len(line) - len(line.lstrip())
            print(f"{i:4d}: {line}")

            for j in range(i, len(lines)):
                current_indent = len(lines[j]) - len(lines[j].lstrip())
                if lines[j].strip() and current_indent <= indent_level and j > i - 1:
                    break
                print(f"{j + 1:4d}: {lines[j]}")
            break

    # Pridaj ENTER handling pred super().keyPressEvent(event)
    old_code = """    def keyPressEvent(self, event):
        \"\"\"Handle key press events.\"\"\"
        # TODO: Add keyboard shortcuts
        super().keyPressEvent(event)"""

    new_code = """    def keyPressEvent(self, event):
        \"\"\"Handle key press events.\"\"\"
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

        super().keyPressEvent(event)"""

    if old_code in content:
        content = content.replace(old_code, new_code)

        main_window_path.write_text(content, encoding='utf-8')

        print("\n✅ Added ENTER key handling to keyPressEvent")
        print("\n📝 CHANGES:")
        print("  - Detects Qt.Key_Return and Qt.Key_Enter")
        print("  - Gets current selected invoice")
        print("  - Opens detail window via _on_invoice_activated()")

        return True
    else:
        print("\n❌ Pattern not found - keyPressEvent might have different structure")
        return False


if __name__ == "__main__":
    success = add_enter_handling()
    if success:
        print("\n" + "=" * 80)
        print("TEST ENTER KEY")
        print("=" * 80)
        print("cd apps/supplier-invoice-editor")
        print("python main.py")
        print("\n1. Vyber faktúru v zozname")
        print("2. Stlač ENTER")
        print("3. Mal by sa otvoriť detail faktúry! ✅")