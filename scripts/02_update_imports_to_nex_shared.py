#!/usr/bin/env python3
"""
Script 02: Update imports to use nex_shared package
Removes sys.path hacks and updates imports to use proper package
"""

from pathlib import Path
import re

# Target files
MAIN_WINDOW = Path("apps/supplier-invoice-editor/src/ui/main_window.py")
UI_INIT = Path("apps/supplier-invoice-editor/src/ui/__init__.py")
MAIN_PY = Path("apps/supplier-invoice-editor/main.py")


def remove_sys_path_hacks(content: str) -> str:
    """Remove all sys.path manipulation code"""
    lines = content.split('\n')
    cleaned_lines = []
    skip_next = False

    for i, line in enumerate(lines):
        # Skip sys.path related lines
        if 'sys.path.insert' in line or 'sys.path.append' in line:
            continue

        # Skip import sys if only used for path manipulation
        if line.strip() == 'import sys':
            # Check if sys is used elsewhere
            if not any('sys.' in l and 'sys.path' not in l for l in lines):
                continue

        # Skip from pathlib import Path if only used for sys.path
        if 'from pathlib import Path' in line:
            # Check if Path is used elsewhere
            if not any('Path(' in l and 'sys.path' not in l for l in lines):
                continue

        cleaned_lines.append(line)

    return '\n'.join(cleaned_lines)


def update_base_window_import(content: str) -> str:
    """Update BaseWindow import to use nex_shared"""
    # Replace: from ui.base_window import BaseWindow
    # With: from nex_shared.ui import BaseWindow
    content = re.sub(
        r'from ui\.base_window import BaseWindow',
        'from nex_shared.ui import BaseWindow',
        content
    )

    return content


def clean_empty_lines(content: str) -> str:
    """Remove excessive empty lines"""
    # Replace 3+ consecutive empty lines with 2
    content = re.sub(r'\n\n\n+', '\n\n', content)
    return content


def update_file(file_path: Path, description: str):
    """Update single file"""
    if not file_path.exists():
        print(f"⚠️  SKIP: {file_path} - file not found")
        return False

    print(f"\n📝 Processing: {file_path}")

    # Read original
    original = file_path.read_text(encoding='utf-8')

    # Apply transformations
    updated = original
    updated = remove_sys_path_hacks(updated)
    updated = update_base_window_import(updated)
    updated = clean_empty_lines(updated)

    # Check if changed
    if original == updated:
        print(f"   ℹ️  No changes needed")
        return True

    # Write updated
    file_path.write_text(updated, encoding='utf-8')
    print(f"   ✅ Updated: {description}")

    # Show what changed
    if 'from nex_shared.ui import BaseWindow' in updated and 'from nex_shared.ui import BaseWindow' not in original:
        print(f"   ✓ Import changed to: from nex_shared.ui import BaseWindow")

    if 'sys.path' in original and 'sys.path' not in updated:
        print(f"   ✓ Removed sys.path hacks")

    return True


def main():
    """Update all files"""
    print("=" * 60)
    print("Updating imports to use nex_shared package")
    print("=" * 60)

    success = True

    # Update main_window.py
    success &= update_file(
        MAIN_WINDOW,
        "Changed BaseWindow import, removed sys.path hacks"
    )

    # Update ui/__init__.py
    success &= update_file(
        UI_INIT,
        "Removed sys.path hacks from UI module init"
    )

    # Update main.py
    success &= update_file(
        MAIN_PY,
        "Removed sys.path hacks from main entry point"
    )

    print("\n" + "=" * 60)
    if success:
        print("ÚSPECH: Všetky imports updated")
        print("=" * 60)
        print("\nNext step: Test application")
        print("cd apps/supplier-invoice-editor")
        print("python main.py")
    else:
        print("⚠️  WARNINGS: Some files not found")
        print("=" * 60)

    return success


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)