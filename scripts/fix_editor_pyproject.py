"""
Fix supplier-invoice-editor pyproject.toml
Add missing [tool.hatch.build.targets.wheel] section
"""

from pathlib import Path

EDITOR_PYPROJECT = Path("apps/supplier-invoice-editor/pyproject.toml")


def fix_pyproject():
    print("=" * 60)
    print("FIX: supplier-invoice-editor pyproject.toml")
    print("=" * 60)

    if not EDITOR_PYPROJECT.exists():
        print(f"❌ File not found: {EDITOR_PYPROJECT}")
        return False

    print(f"\n📄 Reading: {EDITOR_PYPROJECT}")

    # Read file
    with open(EDITOR_PYPROJECT, "r", encoding="utf-8") as f:
        content = f.read()

    # Check if already has the section
    if "[tool.hatch.build.targets.wheel]" in content:
        print("✅ Section already exists - no changes needed")
        return True

    # Find insertion point (after [build-system])
    lines = content.split('\n')
    new_lines = []
    inserted = False

    for i, line in enumerate(lines):
        new_lines.append(line)

        # Insert after build-backend line
        if line.startswith('build-backend = "hatchling.build"') and not inserted:
            new_lines.append('')
            new_lines.append('[tool.hatch.build.targets.wheel]')
            new_lines.append('packages = ["src"]')
            inserted = True
            print("➕ Added [tool.hatch.build.targets.wheel] section")

    if not inserted:
        print("❌ Could not find insertion point")
        return False

    # Write back
    new_content = '\n'.join(new_lines)
    with open(EDITOR_PYPROJECT, "w", encoding="utf-8") as f:
        f.write(new_content)

    print("✅ File updated")

    # Show the added section
    print("\n📋 Added section:")
    print("   [tool.hatch.build.targets.wheel]")
    print('   packages = ["src"]')

    return True


def main():
    success = fix_pyproject()

    print("\n" + "=" * 60)
    if success:
        print("✅ SUCCESS")
        print("\n📝 Next step:")
        print("   pip install -e apps/supplier-invoice-editor")
    else:
        print("❌ FAILED")
    print("=" * 60)

    return success


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)