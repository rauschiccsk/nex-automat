#!/usr/bin/env python3
"""
Script 36: Fix InvoiceDetailWindow layout for QMainWindow
Opraví layout aby používal central widget
"""

from pathlib import Path


def fix_layout():
    """Opraví layout v InvoiceDetailWindow"""

    window_path = Path("apps/supplier-invoice-editor/src/ui/invoice_detail_window.py")

    if not window_path.exists():
        print(f"❌ File not found: {window_path}")
        return False

    content = window_path.read_text(encoding='utf-8')
    lines = content.split('\n')

    # Nájdi _setup_ui metódu
    print("=" * 80)
    print("SEARCHING FOR _setup_ui METHOD")
    print("=" * 80)

    in_setup_ui = False
    setup_ui_start = None

    for i, line in enumerate(lines, 1):
        if 'def _setup_ui(self):' in line:
            setup_ui_start = i - 1
            in_setup_ui = True
            print(f"\nFound at line {i}")
            # Zobraz prvých 20 riadkov metódy
            for j in range(i - 1, min(len(lines), i + 19)):
                print(f"{j + 1:4d}: {lines[j]}")
            break

    if not in_setup_ui:
        print("❌ _setup_ui method not found")
        return False

    # Oprava: Pridaj central widget
    old_pattern = """    def _setup_ui(self):
        \"\"\"Setup UI components.\"\"\"
        # Create main layout
        layout = QVBoxLayout()"""

    new_pattern = """    def _setup_ui(self):
        \"\"\"Setup UI components.\"\"\"
        # Create central widget for QMainWindow
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create main layout on central widget
        layout = QVBoxLayout(central_widget)"""

    if old_pattern in content:
        content = content.replace(old_pattern, new_pattern)

        # Musíme pridať QWidget import
        if 'from PyQt5.QtWidgets import (' in content:
            content = content.replace(
                'from PyQt5.QtWidgets import (\n    QDialog,',
                'from PyQt5.QtWidgets import (\n    QDialog, QWidget,'
            )

        window_path.write_text(content, encoding='utf-8')

        print("\n✅ Fixed layout to use central widget")
        print("\n📝 CHANGES:")
        print("  - Added central_widget = QWidget()")
        print("  - Added self.setCentralWidget(central_widget)")
        print("  - Layout now attached to central_widget")
        print("  - Added QWidget to imports")

        return True
    else:
        print("❌ Pattern not found - manual fix needed")
        return False


if __name__ == "__main__":
    success = fix_layout()
    if success:
        print("\n" + "=" * 80)
        print("TEST AGAIN")
        print("=" * 80)
        print("cd apps/supplier-invoice-editor")
        print("python main.py")
        print("\nDetail window by teraz malo zobrazovať obsah! ✅")