#!/usr/bin/env python3
"""
Script 10: Fix absolute imports in supplier-invoice-editor
Change utils/models/services imports to relative imports
"""

from pathlib import Path
import re

# Target directory
APP_DIR = Path("apps/supplier-invoice-editor/src")


def fix_absolute_imports(content: str, file_path: Path) -> str:
    """Fix absolute imports to relative imports"""

    # Determine current module depth
    rel_path = file_path.relative_to(APP_DIR)
    parts = rel_path.parts
    depth = len(parts) - 1  # -1 for the file itself

    # Common absolute import patterns in the app
    replacements = []

    # from utils.xxx -> from ...utils.xxx or ..utils.xxx based on depth
    if depth == 2:  # src/ui/widgets/file.py
        replacements.append(
            (r'from utils\.', 'from ...utils.')
        )
        replacements.append(
            (r'from models\.', 'from ...models.')
        )
        replacements.append(
            (r'from services\.', 'from ...services.')
        )
        replacements.append(
            (r'from business\.', 'from ...business.')
        )
    elif depth == 1:  # src/ui/file.py or src/business/file.py
        replacements.append(
            (r'from utils\.', 'from ..utils.')
        )
        replacements.append(
            (r'from models\.', 'from ..models.')
        )
        replacements.append(
            (r'from services\.', 'from ..services.')
        )
        replacements.append(
            (r'from business\.', 'from ..business.')
        )

    # Apply replacements
    updated = content
    for old_pattern, new_prefix in replacements:
        updated = re.sub(old_pattern, new_prefix, updated)

    return updated


def process_file(file_path: Path) -> bool:
    """Process single Python file"""
    try:
        # Read content
        content = file_path.read_text(encoding='utf-8')

        # Check if file has absolute imports
        if not any(
                pattern in content for pattern in ['from utils.', 'from models.', 'from services.', 'from business.']):
            return True

        # Fix imports
        updated = fix_absolute_imports(content, file_path)

        # Check if changed
        if updated == content:
            return True

        # Write updated content
        file_path.write_text(updated, encoding='utf-8')

        # Show what changed
        rel_path = file_path.relative_to(APP_DIR.parent)
        print(f"   ✅ {rel_path}")

        # Verify syntax
        try:
            compile(updated, str(file_path), 'exec')
        except SyntaxError as e:
            print(f"      ❌ Syntax error: {e}")
            return False

        return True

    except Exception as e:
        print(f"   ❌ Error processing {file_path}: {e}")
        return False


def main():
    """Fix all absolute imports in the app"""
    print("=" * 60)
    print("Fixing absolute imports in supplier-invoice-editor")
    print("=" * 60)

    if not APP_DIR.exists():
        print(f"❌ ERROR: Directory not found: {APP_DIR}")
        return False

    # Find all Python files
    py_files = list(APP_DIR.rglob("*.py"))
    print(f"\n📝 Found {len(py_files)} Python files")

    # Process files
    print("\n🔧 Processing files...")
    success = True
    changed = 0

    for py_file in py_files:
        if '__pycache__' in str(py_file):
            continue

        original = py_file.read_text(encoding='utf-8')
        if process_file(py_file):
            new_content = py_file.read_text(encoding='utf-8')
            if new_content != original:
                changed += 1
        else:
            success = False

    print(f"\n📊 Changed {changed} files")

    print("\n" + "=" * 60)
    if success:
        print("ÚSPECH: All absolute imports fixed")
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