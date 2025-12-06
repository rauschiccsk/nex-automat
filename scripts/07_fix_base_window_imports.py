#!/usr/bin/env python3
"""
Script 07: Fix base_window.py imports
Change absolute imports to relative imports for proper package structure
"""

from pathlib import Path

# Target files
BASE_WINDOW = Path("packages/nex-shared/ui/base_window.py")
WINDOW_PERSISTENCE = Path("packages/nex-shared/ui/window_persistence.py")


def fix_imports_in_file(file_path: Path, old_import: str, new_import: str) -> bool:
    """Fix imports in a single file"""
    if not file_path.exists():
        print(f"❌ ERROR: File not found: {file_path}")
        return False

    # Read current content
    content = file_path.read_text(encoding='utf-8')

    # Check if import exists
    if old_import not in content:
        print(f"   ℹ️  Import already correct or not found in {file_path.name}")
        return True

    # Replace import
    updated = content.replace(old_import, new_import)

    # Write updated content
    file_path.write_text(updated, encoding='utf-8')
    print(f"   ✅ Updated: {file_path.name}")
    print(f"      {old_import}")
    print(f"      → {new_import}")

    # Verify syntax
    try:
        compile(updated, str(file_path), 'exec')
        print(f"   ✅ Python syntax valid")
    except SyntaxError as e:
        print(f"   ❌ Syntax error: {e}")
        return False

    return True


def main():
    """Fix imports in nex-shared UI files"""
    print("=" * 60)
    print("Fixing imports in nex-shared UI files")
    print("=" * 60)

    success = True

    # Fix base_window.py
    print("\n📝 Processing: base_window.py")
    success &= fix_imports_in_file(
        BASE_WINDOW,
        "from database.window_settings_db import WindowSettingsDB",
        "from ..database.window_settings_db import WindowSettingsDB"
    )

    # Fix window_persistence.py (if it has similar imports)
    print("\n📝 Processing: window_persistence.py")
    success &= fix_imports_in_file(
        WINDOW_PERSISTENCE,
        "from database.window_settings_db import WindowSettingsDB",
        "from ..database.window_settings_db import WindowSettingsDB"
    )

    print("\n" + "=" * 60)
    if success:
        print("ÚSPECH: All imports fixed")
        print("=" * 60)
        print("\nNext step: Test application")
        print("cd apps/supplier-invoice-editor")
        print("python main.py")
    else:
        print("⚠️  ERRORS: Some fixes failed")
        print("=" * 60)

    return success


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)