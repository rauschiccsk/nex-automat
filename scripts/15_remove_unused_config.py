#!/usr/bin/env python3
"""
Script 15: Remove unused config parameter
Config is not used anywhere, so remove it completely
"""

from pathlib import Path
import re

# Target files
MAIN_WINDOW = Path("apps/supplier-invoice-editor/src/ui/main_window.py")
INVOICE_SERVICE = Path("apps/supplier-invoice-editor/src/business/invoice_service.py")
MAIN_PY = Path("apps/supplier-invoice-editor/main.py")


def remove_config_from_main_window():
    """Remove config parameter from MainWindow"""
    if not MAIN_WINDOW.exists():
        print(f"⚠️  MainWindow not found: {MAIN_WINDOW}")
        return False

    content = MAIN_WINDOW.read_text(encoding='utf-8')

    # Change: def __init__(self, config, parent=None):
    # To: def __init__(self, parent=None):
    content = re.sub(
        r'def __init__\(self, config, parent=None\):',
        'def __init__(self, parent=None):',
        content
    )

    # Remove: self.config = config
    content = re.sub(
        r'\s*self\.config = config\n',
        '',
        content
    )

    # Change: self.invoice_service = InvoiceService(config)
    # To: self.invoice_service = InvoiceService()
    content = re.sub(
        r'InvoiceService\(config\)',
        'InvoiceService()',
        content
    )

    MAIN_WINDOW.write_text(content, encoding='utf-8')
    print("✅ MainWindow: removed config parameter")
    return True


def remove_config_from_invoice_service():
    """Remove config parameter from InvoiceService"""
    if not INVOICE_SERVICE.exists():
        print(f"⚠️  InvoiceService not found: {INVOICE_SERVICE}")
        return False

    content = INVOICE_SERVICE.read_text(encoding='utf-8')

    # Change: def __init__(self, config):
    # To: def __init__(self):
    content = re.sub(
        r'def __init__\(self, config\):',
        'def __init__(self):',
        content
    )

    # Remove: self.config = config
    content = re.sub(
        r'\s*self\.config = config\n',
        '',
        content
    )

    INVOICE_SERVICE.write_text(content, encoding='utf-8')
    print("✅ InvoiceService: removed config parameter")
    return True


def fix_main_py():
    """Update main.py to not use config"""
    if not MAIN_PY.exists():
        print(f"⚠️  main.py not found: {MAIN_PY}")
        return False

    # Simple main.py without config
    content = '''"""
Supplier Invoice Editor - Main Entry Point
"""

import sys
from PyQt5.QtWidgets import QApplication
from src.ui.main_window import MainWindow


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("Supplier Invoice Editor")
    app.setOrganizationName("ICC Komárno")

    # Create and show main window
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
'''

    MAIN_PY.write_text(content, encoding='utf-8')
    print("✅ main.py: removed config usage")
    return True


def main():
    """Remove unused config from all files"""
    print("=" * 60)
    print("Removing unused config parameter")
    print("=" * 60)
    print()

    success = True
    success &= remove_config_from_main_window()
    success &= remove_config_from_invoice_service()
    success &= fix_main_py()

    print()
    print("=" * 60)
    if success:
        print("ÚSPECH: Config removed from all files")
        print("=" * 60)
        print("\nNext step: Test application")
        print("cd apps/supplier-invoice-editor")
        print("python main.py")
    else:
        print("⚠️  Some files not updated")
        print("=" * 60)

    return success


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)