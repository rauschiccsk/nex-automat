#!/usr/bin/env python3
"""
Script 11: Fix main.py to provide config to MainWindow
Add proper config initialization
"""

from pathlib import Path

# Target file
MAIN_PY = Path("apps/supplier-invoice-editor/main.py")

# Correct main.py content with config
MAIN_PY_CONTENT = '''"""
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


def main():
    """Fix main.py with config parameter"""
    print("=" * 60)
    print("Fixing main.py to provide config parameter")
    print("=" * 60)

    if not MAIN_PY.exists():
        print(f"❌ ERROR: File not found: {MAIN_PY}")
        return False

    # Write correct content
    MAIN_PY.write_text(MAIN_PY_CONTENT, encoding='utf-8')
    print(f"\n✅ Fixed: {MAIN_PY}")

    # Verify syntax
    try:
        compile(MAIN_PY_CONTENT, str(MAIN_PY), 'exec')
        print("✅ Python syntax valid")
    except SyntaxError as e:
        print(f"❌ Syntax error: {e}")
        return False

    print("\n📝 Changes:")
    print("   ✅ Added: from src.config import Config")
    print("   ✅ Added: config = Config()")
    print("   ✅ Updated: MainWindow(config)")

    print("\n" + "=" * 60)
    print("ÚSPECH: main.py fixed with config")
    print("=" * 60)
    print("\nNext step: Test application")
    print("cd apps/supplier-invoice-editor")
    print("python main.py")

    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)