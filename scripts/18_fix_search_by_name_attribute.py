"""
Session Script 18: Fix search_by_name Attribute
Change C_002 to gs_name in search_by_name method
"""
from pathlib import Path


def main():
    gscat_repo = Path(r"C:\Development\nex-automat\packages\nexdata\nexdata\repositories\gscat_repository.py")

    print("=" * 60)
    print("Fixing search_by_name() Attribute")
    print("=" * 60)

    with open(gscat_repo, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix old attribute references
    replacements = [
        ('record.C_002.lower()', 'record.gs_name.lower()'),
        ('if search_lower in record.C_002.lower():', 'if search_lower in record.gs_name.lower():'),
    ]

    modified = False
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
            modified = True
            print(f"✅ Replaced: {old}")
            print(f"   With:     {new}")

    if modified:
        with open(gscat_repo, 'w', encoding='utf-8') as f:
            f.write(content)

        print("\n✅ File updated")
    else:
        print("⚠️  No changes needed or already fixed")

    print("\n" + "=" * 60)
    print("✅ Fix complete!")
    print("=" * 60)

    return 0


if __name__ == '__main__':
    import sys

    sys.exit(main())