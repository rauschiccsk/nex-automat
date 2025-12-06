#!/usr/bin/env python3
"""
Script 19: Remove closeEvent from MainWindow
BaseWindow already handles window state persistence
"""

from pathlib import Path
import re

# Target file
MAIN_WINDOW = Path("apps/supplier-invoice-editor/src/ui/main_window.py")


def remove_close_event():
    """Remove closeEvent method from MainWindow"""
    if not MAIN_WINDOW.exists():
        print(f"❌ ERROR: File not found: {MAIN_WINDOW}")
        return False

    content = MAIN_WINDOW.read_text(encoding='utf-8')

    # Find and remove closeEvent method
    # Pattern: def closeEvent... up to next method or end of class
    pattern = r'\n    def closeEvent\(self[^)]*\):.*?(?=\n    def |\n\nclass |\Z)'

    # Check if closeEvent exists
    if 'def closeEvent' not in content:
        print("⚠️  closeEvent not found, already removed?")
        return True

    # Remove closeEvent
    updated = re.sub(pattern, '', content, flags=re.DOTALL)

    # Write updated content
    MAIN_WINDOW.write_text(updated, encoding='utf-8')

    return True


def main():
    """Remove closeEvent from MainWindow"""
    print("=" * 60)
    print("Removing closeEvent from MainWindow")
    print("=" * 60)

    if not remove_close_event():
        return False

    print("\n✅ Removed: closeEvent method")
    print("   BaseWindow handles window persistence automatically")

    # Verify syntax
    content = MAIN_WINDOW.read_text(encoding='utf-8')
    try:
        compile(content, str(MAIN_WINDOW), 'exec')
        print("✅ Python syntax valid")
    except SyntaxError as e:
        print(f"❌ Syntax error at line {e.lineno}: {e.msg}")
        if e.text:
            print(f"   {e.text.strip()}")
        return False

    print("\n" + "=" * 60)
    print("ÚSPECH: closeEvent removed")
    print("=" * 60)
    print("\nNext step: Test application")
    print("cd apps/supplier-invoice-editor")
    print("python main.py")
    print("\nTest scenario:")
    print("1. Spusti aplikáciu")
    print("2. Maximalizuj okno")
    print("3. Zavri aplikáciu")
    print("4. Spusti znova → malo by sa otvoriť MAXIMALIZOVANÉ")

    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)