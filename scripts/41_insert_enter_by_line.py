#!/usr/bin/env python3
"""
Script 41: Insert ENTER handling by line number
Vloží ENTER handling na správne miesto podľa čísla riadku
"""

from pathlib import Path


def insert_enter_by_line():
    """Vloží ENTER handling na riadok 241 (pred ESC check)"""

    main_window_path = Path("apps/supplier-invoice-editor/src/ui/main_window.py")

    if not main_window_path.exists():
        print(f"❌ File not found: {main_window_path}")
        return False

    content = main_window_path.read_text(encoding='utf-8')
    lines = content.split('\n')

    print("=" * 80)
    print("CURRENT LINES 237-249")
    print("=" * 80)

    for i in range(236, min(249, len(lines))):
        print(f"{i + 1:4d}: {lines[i]}")

    # Nájdi riadok s "if event.key() == Qt.Key_Escape:"
    insert_position = None
    for i, line in enumerate(lines):
        if 'if event.key() == Qt.Key_Escape:' in line:
            insert_position = i
            break

    if insert_position is None:
        print("\n❌ Could not find 'if event.key() == Qt.Key_Escape:'")
        return False

    print(f"\n✓ Found ESC check at line {insert_position + 1}")
    print(f"  Will insert ENTER handling before it")

    # ENTER handling kód na vloženie
    enter_code = [
        "",
        "        # Open invoice detail on Enter/Return",
        "        if event.key() in (Qt.Key_Return, Qt.Key_Enter):",
        "            # Get current selection",
        "            if hasattr(self, 'invoice_list') and self.invoice_list:",
        "                current_index = self.invoice_list.get_current_index()",
        "                if current_index is not None:",
        "                    invoice_id = self.invoice_list.get_invoice_id_at_index(current_index)",
        "                    if invoice_id:",
        "                        self._on_invoice_activated(invoice_id)",
        "                        event.accept()",
        "                        return",
        ""
    ]

    # Vlož ENTER kód pred ESC check
    new_lines = lines[:insert_position] + enter_code + lines[insert_position:]

    # Ulož súbor
    content = '\n'.join(new_lines)
    main_window_path.write_text(content, encoding='utf-8')

    print(f"\n✅ Inserted ENTER handling at line {insert_position + 1}")

    print("\n" + "=" * 80)
    print("NEW LINES 237-262")
    print("=" * 80)

    new_lines_check = content.split('\n')
    for i in range(236, min(262, len(new_lines_check))):
        print(f"{i + 1:4d}: {new_lines_check[i]}")

    return True


if __name__ == "__main__":
    success = insert_enter_by_line()
    if success:
        print("\n" + "=" * 80)
        print("TEST ENTER KEY")
        print("=" * 80)
        print("cd apps/supplier-invoice-editor")
        print("python main.py")
        print("\n1. Vyber faktúru")
        print("2. Stlač ENTER")
        print("3. Detail by sa mal otvoriť! ✅")