#!/usr/bin/env python3
"""
Script 09: Fix base_window.py ui import
Change from ui.window_persistence to relative import
"""

from pathlib import Path

# Target file
BASE_WINDOW = Path("packages/nex-shared/ui/base_window.py")


def main():
    """Fix ui import in base_window.py"""
    print("=" * 60)
    print("Fixing base_window.py ui import")
    print("=" * 60)

    if not BASE_WINDOW.exists():
        print(f"❌ ERROR: File not found: {BASE_WINDOW}")
        return False

    # Read current content
    content = BASE_WINDOW.read_text(encoding='utf-8')
    print(f"\n📝 Current file size: {len(content)} chars")

    # Replace import
    old_import = "from ui.window_persistence import WindowPersistenceManager"
    new_import = "from .window_persistence import WindowPersistenceManager"

    if old_import not in content:
        print(f"⚠️  Import not found or already fixed")
        print(f"   Looking for: {old_import}")
        return True

    updated = content.replace(old_import, new_import)

    # Write updated content
    BASE_WINDOW.write_text(updated, encoding='utf-8')
    print(f"\n✅ Fixed: {BASE_WINDOW}")
    print(f"   {old_import}")
    print(f"   → {new_import}")

    # Verify
    new_content = BASE_WINDOW.read_text(encoding='utf-8')
    print(f"✅ New file size: {len(new_content)} chars")

    # Check syntax
    try:
        compile(new_content, str(BASE_WINDOW), 'exec')
        print("✅ Python syntax valid")
    except SyntaxError as e:
        print(f"❌ Syntax error: {e}")
        return False

    print("\n" + "=" * 60)
    print("ÚSPECH: base_window.py ui import fixed")
    print("=" * 60)
    print("\nNext step: Test application")
    print("cd apps/supplier-invoice-editor")
    print("python main.py")

    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)