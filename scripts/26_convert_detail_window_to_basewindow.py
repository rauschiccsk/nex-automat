#!/usr/bin/env python3
"""
Script 26: Convert InvoiceDetailWindow to use BaseWindow
Zmení InvoiceDetailWindow aby dedil z BaseWindow namiesto QDialog
"""

from pathlib import Path


def convert_to_basewindow():
    """Zmení InvoiceDetailWindow na BaseWindow"""

    window_path = Path("apps/supplier-invoice-editor/src/ui/invoice_detail_window.py")

    if not window_path.exists():
        print(f"❌ File not found: {window_path}")
        return False

    content = window_path.read_text(encoding='utf-8')

    print("=" * 80)
    print("CONVERTING InvoiceDetailWindow TO BaseWindow")
    print("=" * 80)

    # 1. Pridaj import BaseWindow
    old_imports = """from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel,
    QPushButton, QMessageBox, QFormLayout
)"""

    new_imports = """from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel,
    QPushButton, QMessageBox, QFormLayout
)

from nex_shared.ui import BaseWindow
from ...utils.constants import WINDOW_DETAIL"""

    if old_imports in content:
        content = content.replace(old_imports, new_imports)
        print("✅ Added BaseWindow import")

    # 2. Zmení class definíciu
    old_class = "class InvoiceDetailWindow(QDialog):"
    new_class = "class InvoiceDetailWindow(BaseWindow):"

    if old_class in content:
        content = content.replace(old_class, new_class)
        print("✅ Changed inheritance from QDialog to BaseWindow")

    # 3. Uprav __init__ aby volal BaseWindow.__init__
    old_init = """    def __init__(self, invoice_service, invoice_id, parent=None):
        super().__init__(parent)

        self.invoice_service = invoice_service
        self.invoice_id = invoice_id
        self.logger = logging.getLogger(__name__)"""

    new_init = """    def __init__(self, invoice_service, invoice_id, parent=None):
        # Initialize BaseWindow first
        super().__init__(
            window_name=WINDOW_DETAIL,
            default_size=(900, 700),
            default_pos=(200, 100),
            parent=parent
        )

        self.invoice_service = invoice_service
        self.invoice_id = invoice_id
        self.logger = logging.getLogger(__name__)"""

    if old_init in content:
        content = content.replace(old_init, new_init)
        print("✅ Updated __init__ to call BaseWindow.__init__()")

    # Ulož súbor
    window_path.write_text(content, encoding='utf-8')

    print("\n📝 CHANGES SUMMARY:")
    print("  - Added: from nex_shared.ui import BaseWindow")
    print("  - Added: from ...utils.constants import WINDOW_DETAIL")
    print("  - Changed: class InvoiceDetailWindow(QDialog) → BaseWindow")
    print("  - Updated: __init__ to call super().__init__() with window_name")
    print("\n⚠️  Need to add WINDOW_DETAIL constant to constants.py!")

    return True


if __name__ == "__main__":
    success = convert_to_basewindow()
    if success:
        print("\n" + "=" * 80)
        print("NEXT STEP: Add WINDOW_DETAIL constant")
        print("=" * 80)