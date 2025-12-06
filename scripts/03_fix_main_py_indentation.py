#!/usr/bin/env python3
"""
Script 03: Fix main.py indentation error
Properly reconstructs main.py without sys.path hacks
"""

from pathlib import Path

# Target file
MAIN_PY = Path("apps/supplier-invoice-editor/main.py")

# Correct main.py content
MAIN_PY_CONTENT = '''"""
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

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
'''


def main():
    """Fix main.py file"""
    print("=" * 60)
    print("Fixing main.py indentation")
    print("=" * 60)

    if not MAIN_PY.exists():
        print(f"❌ ERROR: File not found: {MAIN_PY}")
        return False

    # Read current content to see what's wrong
    current = MAIN_PY.read_text(encoding='utf-8')
    print(f"\n📝 Current file size: {len(current)} chars")

    # Write correct content
    MAIN_PY.write_text(MAIN_PY_CONTENT, encoding='utf-8')
    print(f"✅ Fixed: {MAIN_PY}")

    # Verify
    new_content = MAIN_PY.read_text(encoding='utf-8')
    print(f"✅ New file size: {len(new_content)} chars")

    # Check syntax
    try:
        compile(new_content, str(MAIN_PY), 'exec')
        print("✅ Python syntax valid")
    except SyntaxError as e:
        print(f"❌ Syntax error: {e}")
        return False

    print("\n" + "=" * 60)
    print("ÚSPECH: main.py fixed")
    print("=" * 60)
    print("\nNext step: Test application")
    print("cd apps/supplier-invoice-editor")
    print("python main.py")

    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)