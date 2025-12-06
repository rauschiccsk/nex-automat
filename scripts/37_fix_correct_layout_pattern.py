#!/usr/bin/env python3
"""
Script 37: Fix layout with correct pattern
Opraví QVBoxLayout(self) na central widget pattern
"""

from pathlib import Path


def fix_layout_pattern():
    """Opraví layout pattern"""

    window_path = Path("apps/supplier-invoice-editor/src/ui/invoice_detail_window.py")

    if not window_path.exists():
        print(f"❌ File not found: {window_path}")
        return False

    content = window_path.read_text(encoding='utf-8')

    print("=" * 80)
    print("FIXING LAYOUT PATTERN")
    print("=" * 80)

    # Nájdi a nahraď problematický riadok
    old_line = "        layout = QVBoxLayout(self)"
    new_lines = """        # Create central widget for QMainWindow
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create layout on central widget
        layout = QVBoxLayout(central_widget)"""

    if old_line in content:
        content = content.replace(old_line, new_lines)

        # Pridaj QWidget do importov ak chýba
        if 'QWidget' not in content.split('from PyQt5.QtWidgets import')[1].split(')')[0]:
            content = content.replace(
                'from PyQt5.QtWidgets import (',
                'from PyQt5.QtWidgets import (\n    QWidget,'
            )

        window_path.write_text(content, encoding='utf-8')

        print("✅ Fixed layout pattern:")
        print(f"   OLD: {old_line}")
        print(f"   NEW: Created central_widget and attached layout to it")

        return True
    else:
        print("❌ Pattern 'layout = QVBoxLayout(self)' not found")
        return False


if __name__ == "__main__":
    success = fix_layout_pattern()
    if success:
        print("\n" + "=" * 80)
        print("TEST AGAIN")
        print("=" * 80)
        print("cd apps/supplier-invoice-editor")
        print("python main.py")
        print("\n1. Otvor faktúru")
        print("2. Detail okno by malo zobrazovať OBSAH (nie prázdne) ✅")