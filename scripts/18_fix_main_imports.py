"""
Script 18: Fix main.py imports - remove unused clean_string import
"""

from pathlib import Path


def main():
    """Fix imports in main.py"""

    dev_root = Path(r"C:\Development\nex-automat")
    main_py = dev_root / "apps" / "supplier-invoice-loader" / "main.py"

    if not main_py.exists():
        print(f"❌ File not found: {main_py}")
        return False

    print(f"📝 Reading: {main_py}")
    content = main_py.read_text(encoding='utf-8')

    # Remove clean_string import line
    lines = content.split('\n')
    new_lines = []

    for line in lines:
        # Skip the clean_string import line
        if 'from nex_shared.utils import clean_string' in line:
            print(f"Removing line: {line.strip()}")
            continue
        new_lines.append(line)

    content = '\n'.join(new_lines)

    # Write fixed content
    print(f"💾 Writing fixed file...")
    main_py.write_text(content, encoding='utf-8')

    print("✅ SUCCESS: main.py fixed - removed unused clean_string import")

    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)