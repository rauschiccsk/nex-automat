#!/usr/bin/env python3
"""
Fix duplicate detection to ignore customer_name in single-tenant deployment.

Changes line 300 in main.py from:
    customer_name=config.CUSTOMER_NAME
to:
    customer_name=None

Usage:
    python fix_duplicate_detection.py
"""

from pathlib import Path


def fix_duplicate_detection():
    """Fix the duplicate detection call in main.py"""

    # Path to main.py in Development
    main_py_path = Path(r"C:\Development\nex-automat\apps\supplier-invoice-loader\main.py")

    if not main_py_path.exists():
        print(f"ERROR: File not found: {main_py_path}")
        return False

    # Read the file
    print(f"Reading {main_py_path}...")
    content = main_py_path.read_text(encoding='utf-8')
    lines = content.splitlines(keepends=True)

    # Find and fix line 300 (index 299)
    target_line = 299  # Line 300 (0-indexed)

    if target_line >= len(lines):
        print(f"ERROR: File has only {len(lines)} lines, cannot access line {target_line + 1}")
        return False

    original_line = lines[target_line]

    # Check if this is the line we want to fix
    if "customer_name=config.CUSTOMER_NAME" not in original_line:
        print(f"ERROR: Line {target_line + 1} does not contain expected content")
        print(f"Found: {original_line.strip()}")
        print(f"Expected: customer_name=config.CUSTOMER_NAME")
        return False

    # Replace the line
    fixed_line = original_line.replace(
        "customer_name=config.CUSTOMER_NAME",
        "customer_name=None  # Fixed: Single-tenant architecture"
    )

    lines[target_line] = fixed_line
    new_content = ''.join(lines)

    # Backup original file
    backup_path = main_py_path.with_suffix('.py.backup')
    print(f"Creating backup: {backup_path}")
    backup_path.write_text(content, encoding='utf-8')

    # Write fixed content
    print(f"Writing fixed content to {main_py_path}")
    main_py_path.write_text(new_content, encoding='utf-8')

    print("\n✓ SUCCESS: Duplicate detection fixed")
    print(f"\nLine {target_line + 1} changed:")
    print(f"  FROM: {original_line.strip()}")
    print(f"  TO:   {fixed_line.strip()}")

    print(f"\nBackup saved to: {backup_path}")
    print("\nNext steps:")
    print("  1. Verify the fix with:")
    print("     Select-String -Path main.py -Pattern 'customer_name=None' -Context 2,2")
    print("  2. Git commit and push")
    print("  3. Deploy to Production")

    return True


if __name__ == "__main__":
    print("=" * 70)
    print("Fix Duplicate Detection - Single Tenant Architecture")
    print("=" * 70)
    print()

    success = fix_duplicate_detection()

    if not success:
        print("\n✗ FAILED: Fix could not be applied")
        exit(1)

    print("\n" + "=" * 70)