#!/usr/bin/env python3
"""
Script 06: Fix nex-shared ui/__init__.py imports
Change to relative imports for proper package structure
"""

from pathlib import Path

# Target file
UI_INIT = Path("packages/nex-shared/ui/__init__.py")

# Correct content with relative imports
UI_INIT_CONTENT = '''"""
UI components for nex-shared package
"""

from .base_window import BaseWindow
from .window_persistence import WindowPersistenceManager

__all__ = ['BaseWindow', 'WindowPersistenceManager']
'''


def main():
    """Fix ui/__init__.py in nex-shared package"""
    print("=" * 60)
    print("Fixing nex-shared/ui/__init__.py imports")
    print("=" * 60)

    if not UI_INIT.exists():
        print(f"❌ ERROR: File not found: {UI_INIT}")
        return False

    # Read current content
    current = UI_INIT.read_text(encoding='utf-8')
    print(f"\n📝 Current content:")
    print(current)
    print(f"\n📝 Current file size: {len(current)} chars")

    # Write correct content with relative imports
    UI_INIT.write_text(UI_INIT_CONTENT, encoding='utf-8')
    print(f"\n✅ Fixed: {UI_INIT}")

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

    # Verify relative imports
    if 'from .base_window import' in new_content:
        print("✅ Using relative imports (.base_window)")

    print("\n" + "=" * 60)
    print("ÚSPECH: nex-shared ui/__init__.py fixed")
    print("=" * 60)
    print("\nNext step: Test application")
    print("cd apps/supplier-invoice-editor")
    print("python main.py")

    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)