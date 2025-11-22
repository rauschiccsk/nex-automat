"""
Fix Pillow Import Name
======================
Opraví import name z "pillow" na "PIL" v test a preflight scriptoch.

Usage:
    cd C:\\Development\\nex-automat
    python scripts\\fix_pillow_import_name.py
"""

from pathlib import Path


def fix_script(script_path: Path) -> bool:
    """Fix pillow import in script."""

    if not script_path.exists():
        print(f"❌ Not found: {script_path}")
        return False

    try:
        content = script_path.read_text(encoding='utf-8')

        # Fix the import check
        old_pattern = '__import__(package)'

        # Check if script has the pillow problem
        if '"pillow"' in content or "'pillow'" in content:
            # Replace in dependency lists
            content = content.replace('"pillow"', '"PIL"')
            content = content.replace("'pillow'", "'PIL'")

            # Also need to handle the special case for PIL
            # Add special handling before __import__
            if '__import__(package)' in content and 'if package ==' not in content:
                # Find the __import__ line and add PIL handling
                lines = content.split('\n')
                new_lines = []

                for i, line in enumerate(lines):
                    new_lines.append(line)

                    # If this line has __import__(package), add PIL check before it
                    if '__import__(package)' in line and 'try:' in lines[max(0, i - 1)]:
                        indent = len(line) - len(line.lstrip())
                        new_lines.insert(-1, ' ' * indent + 'if package == "PIL":')
                        new_lines.insert(-1, ' ' * (indent + 4) + '__import__("PIL")')
                        new_lines.insert(-1, ' ' * indent + 'else:')
                        new_lines[-1] = ' ' * (indent + 4) + new_lines[-1].lstrip()

                content = '\n'.join(new_lines)

            script_path.write_text(content, encoding='utf-8')
            print(f"✅ Fixed: {script_path.name}")
            return True
        else:
            print(f"⚠️  No pillow import found in: {script_path.name}")
            return True

    except Exception as e:
        print(f"❌ Error fixing {script_path.name}: {e}")
        return False


def fix_simple(script_path: Path) -> bool:
    """Simple fix - just replace 'pillow' with 'PIL' in lists."""

    if not script_path.exists():
        print(f"⚠️  Not found: {script_path}")
        return True  # Not critical

    try:
        content = script_path.read_text(encoding='utf-8')

        modified = False

        # Replace in string lists
        if '"pillow"' in content:
            content = content.replace('"pillow"', '"PIL"')
            modified = True

        if "'pillow'" in content:
            content = content.replace("'pillow'", "'PIL'")
            modified = True

        if modified:
            script_path.write_text(content, encoding='utf-8')
            print(f"✅ Fixed: {script_path.name}")
            return True
        else:
            print(f"✓ OK (no changes needed): {script_path.name}")
            return True

    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """Fix all scripts."""
    print("=" * 70)
    print("  FIX PILLOW IMPORT NAME")
    print("=" * 70)

    scripts_to_fix = [
        Path("scripts/test_preflight_in_development.py"),
        Path("scripts/day5_preflight_check.py")
    ]

    print("\nFixing scripts...")
    results = []

    for script in scripts_to_fix:
        result = fix_simple(script)
        results.append(result)

    print("\n" + "=" * 70)
    print("  SUMMARY")
    print("=" * 70)

    if all(results):
        print("\n✅ All scripts fixed")
        print("✅ 'pillow' → 'PIL' (correct import name)")
        print("\nRun test again:")
        print("  python scripts\\test_preflight_in_development.py")
        return True
    else:
        print("\n⚠️  Some scripts could not be fixed")
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)