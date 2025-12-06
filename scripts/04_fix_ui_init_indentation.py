#!/usr/bin/env python3
"""
Script 04: Fix ui/__init__.py indentation error
Properly reconstructs ui/__init__.py without sys.path hacks
"""

from pathlib import Path

# Target file
UI_INIT = Path("apps/supplier-invoice-editor/src/ui/__init__.py")

# Correct ui/__init__.py content
UI_INIT_CONTENT = '''"""
UI Module for Supplier Invoice Editor
"""

from .main_window import MainWindow

__all__ = ['MainWindow']
'''


def main():
    """Fix ui/__init__.py file"""
    print("=" * 60)
    print("Fixing ui/__init__.py indentation")
    print("=" * 60)

    if not UI_INIT.exists():
        print(f"❌ ERROR: File not found: {UI_INIT}")
        return False

    # Read current content
    current = UI_INIT.read_text(encoding='utf-8')
    print(f"\n📝 Current file size: {len(current)} chars")

    # Write correct content
    UI_INIT.write_text(UI_INIT_CONTENT, encoding='utf-8')
    print(f"✅ Fixed: {UI_INIT}")

    # Verify
    new_content = UI_INIT.read_text(encoding='utf-8')
    print(f"✅ New file size: {len(new_content)} chars")

    # Check syntax
    try:
        compile(new_content, str(UI_INIT), 'exec')
        print("✅ Python syntax valid")
    except SyntaxError as e:
        print(f"❌ Syntax error: {e}")
        return False

    print("\n" + "=" * 60)
    print("ÚSPECH: ui/__init__.py fixed")
    print("=" * 60)
    print("\nNext step: Test application")
    print("cd apps/supplier-invoice-editor")
    print("python main.py")

    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)