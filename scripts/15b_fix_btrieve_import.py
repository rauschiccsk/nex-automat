"""
Session Script 15b: Fix BtrieveClient Import
Corrects import path to btrieve_client
"""
from pathlib import Path


def main():
    matcher_file = Path(r"C:\Development\nex-automat\apps\supplier-invoice-loader\src\business\product_matcher.py")

    print("=" * 60)
    print("Fixing BtrieveClient Import")
    print("=" * 60)

    with open(matcher_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix import
    old_import = 'from nexdata.btrieve.client import BtrieveClient'
    new_import = 'from nexdata.btrieve.btrieve_client import BtrieveClient'

    if old_import in content:
        content = content.replace(old_import, new_import)

        with open(matcher_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print("✅ Fixed import")
        print(f"\n  FROM: {old_import}")
        print(f"  TO:   {new_import}")
    else:
        print("⚠️  Import already fixed or not found")

    print("\n" + "=" * 60)
    print("✅ Fix complete!")
    print("=" * 60)

    return 0


if __name__ == '__main__':
    import sys

    sys.exit(main())