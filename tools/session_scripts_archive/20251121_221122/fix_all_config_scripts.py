#!/usr/bin/env python3
"""
Fix all scripts to use correct config path
"""

from pathlib import Path

BASE_PATH = Path(r"C:\Development\nex-automat")

SCRIPTS = [
    "scripts/validate_config.py",
    "scripts/test_database_connection.py",
    "scripts/create_production_config.py"
]

OLD_PATTERNS = [
    ('Path(__file__).parent.parent / "config" / "config.yaml"',
     'Path(__file__).parent.parent / "apps" / "supplier-invoice-loader" / "config" / "config.yaml"'),

    ('Path(__file__).parent.parent / "config" / "config.template.yaml"',
     'Path(__file__).parent.parent / "apps" / "supplier-invoice-loader" / "config" / "config.template.yaml"'),
]


def fix_script(script_path: Path):
    """Fix single script"""
    if not script_path.exists():
        print(f"⚠️  Not found: {script_path.name}")
        return False

    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()

    modified = False
    for old_pattern, new_pattern in OLD_PATTERNS:
        if old_pattern in content:
            content = content.replace(old_pattern, new_pattern)
            modified = True

    if modified:
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Fixed: {script_path.name}")
        return True
    else:
        print(f"✅ OK: {script_path.name}")
        return False


def main():
    print("=" * 70)
    print("FIX CONFIG PATHS IN ALL SCRIPTS")
    print("=" * 70)
    print()

    fixed_count = 0
    for script_rel in SCRIPTS:
        script_path = BASE_PATH / script_rel
        if fix_script(script_path):
            fixed_count += 1

    print()
    print("=" * 70)
    print(f"✅ Fixed {fixed_count} scripts")
    print("=" * 70)
    print()
    print("Now run:")
    print("  python scripts/validate_config.py")
    print()


if __name__ == "__main__":
    main()