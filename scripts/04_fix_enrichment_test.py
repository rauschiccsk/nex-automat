"""
Session Script 04: Fix Failing Test
Fixes test_marks_item_as_not_found assertion
"""
from pathlib import Path


def main():
    test_file = Path(r"C:\Development\nex-automat\tests\unit\test_postgres_staging_enrichment.py")

    print("=" * 60)
    print("Phase 1: Fixing Test")
    print("=" * 60)

    with open(test_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix the assertion
    old_assertion = "assert 'validation_status = %s' in call_args[0]"
    new_assertion = "assert \"validation_status = 'needs_review'\" in call_args[0]"

    if old_assertion in content:
        content = content.replace(old_assertion, new_assertion)

        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✅ Fixed test in {test_file.name}")
        print(f"\nChanged:")
        print(f"  FROM: {old_assertion}")
        print(f"  TO:   {new_assertion}")
    else:
        print("⚠️  Assertion already fixed or not found")

    print("\n" + "=" * 60)
    print("✅ Test fix complete!")
    print("=" * 60)
    print("\nRe-run tests:")
    print("  python -m pytest tests/unit/test_postgres_staging_enrichment.py -v")

    return 0


if __name__ == '__main__':
    import sys

    sys.exit(main())