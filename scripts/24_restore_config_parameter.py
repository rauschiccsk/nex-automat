#!/usr/bin/env python3
"""
Script 24: Restore config parameter to MainWindow and InvoiceService
Config is actually needed for PostgresClient
"""

from pathlib import Path
import re

# Target files
MAIN_WINDOW = Path("apps/supplier-invoice-editor/src/ui/main_window.py")
INVOICE_SERVICE = Path("apps/supplier-invoice-editor/src/business/invoice_service.py")
MAIN_PY = Path("apps/supplier-invoice-editor/main.py")


def restore_main_window_config():
    """Restore config parameter to MainWindow"""
    if not MAIN_WINDOW.exists():
        return False

    content = MAIN_WINDOW.read_text(encoding='utf-8')

    # Change: def __init__(self, parent=None):
    # To: def __init__(self, config, parent=None):
    content = re.sub(
        r'def __init__\(self, parent=None\):',
        'def __init__(self, config, parent=None):',
        content
    )

    # Add: self.config = config (after super().__init__)
    # Find the line after super().__init__() closing parenthesis
    content = re.sub(
        r'(\)[\r\n]+\s+)(self\.logger)',
        r'\1self.config = config\n        \2',
        content
    )

    # Change: InvoiceService() to InvoiceService(config)
    content = re.sub(
        r'InvoiceService\(\)',
        'InvoiceService(config)',
        content
    )

    MAIN_WINDOW.write_text(content, encoding='utf-8')
    print("✅ MainWindow: restored config parameter")
    return True


def restore_invoice_service_config():
    """Restore config parameter to InvoiceService"""
    if not INVOICE_SERVICE.exists():
        return False

    content = INVOICE_SERVICE.read_text(encoding='utf-8')

    # Change: def __init__(self):
    # To: def __init__(self, config):
    content = re.sub(
        r'def __init__\(self\):',
        'def __init__(self, config):',
        content
    )

    # Add: self.config = config (before self.logger)
    content = re.sub(
        r'(def __init__\(self, config\):[\r\n]+\s+)(self\.logger)',
        r'\1self.config = config\n        \2',
        content
    )

    INVOICE_SERVICE.write_text(content, encoding='utf-8')
    print("✅ InvoiceService: restored config parameter")
    return True


def update_main_py_with_config():
    """Update main.py to create and pass Config"""
    if not MAIN_PY.exists():
        return False

    content = '''"""
Supplier Invoice Editor - Main Entry Point
"""

import sys
from PyQt5.QtWidgets import QApplication
from src.ui.main_window import MainWindow
from src.config import Config


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("Supplier Invoice Editor")
    app.setOrganizationName("ICC Komárno")

    # Initialize config
    config = Config()

    # Create and show main window
    window = MainWindow(config)
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
'''

    MAIN_PY.write_text(content, encoding='utf-8')
    print("✅ main.py: updated to create and pass Config")
    return True


def main():
    """Restore config parameter"""
    print("=" * 60)
    print("Restoring config parameter")
    print("=" * 60)
    print()

    success = True
    success &= restore_main_window_config()
    success &= restore_invoice_service_config()
    success &= update_main_py_with_config()

    print()
    print("=" * 60)
    if success:
        print("ÚSPECH: Config parameter restored")
        print("=" * 60)
        print("\nNext step: Test application")
        print("cd apps/supplier-invoice-editor")
        print("python main.py")
        print("\nExpected: Database should connect successfully")
    else:
        print("⚠️  Some files not updated")
        print("=" * 60)

    return success


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)