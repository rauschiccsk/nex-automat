#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix v2: Correct duplicate detection method name
================================================

Fixes the incorrect method call from v1 fix.
"""

from pathlib import Path

# Target file
TARGET_FILE = Path("C:/Development/nex-automat/apps/supplier-invoice-loader/main.py")

# Find and replace pattern
OLD_CODE = '''        # Check for duplicate BEFORE extraction (save processing time)
        database.init_database()
        is_duplicate = database.check_duplicate(file_hash)

        if is_duplicate:'''

NEW_CODE = '''        # Check for duplicate BEFORE extraction (save processing time)
        database.init_database()
        is_duplicate_found = database.is_duplicate(
            file_hash=file_hash,
            customer_name=config.CUSTOMER_NAME
        )

        if is_duplicate_found:'''


def main():
    """Apply the fix"""
    print("=" * 70)
    print("FIX v2: Correct Duplicate Detection Method Name")
    print("=" * 70)

    # Read current content
    if not TARGET_FILE.exists():
        print(f"[ERROR] File not found: {TARGET_FILE}")
        return False

    print(f"\n[1] Reading: {TARGET_FILE}")
    content = TARGET_FILE.read_text(encoding='utf-8')

    # Check if already fixed
    if "database.is_duplicate(" in content and "customer_name=config.CUSTOMER_NAME" in content:
        print("[INFO] Already using correct method name!")
        return True

    # Apply fix
    if OLD_CODE not in content:
        print("[ERROR] Pattern not found in file!")
        print("[INFO] Searching for alternative pattern...")

        # Check if old incorrect method exists
        if "database.check_duplicate(file_hash)" in content:
            print("[FOUND] Incorrect method call found, fixing...")
        else:
            print("[ERROR] File might have been modified. Manual fix required.")
            return False

    print("[2] Applying fix...")
    new_content = content.replace(OLD_CODE, NEW_CODE)

    # Save backup
    backup_file = TARGET_FILE.with_suffix('.py.backup2')
    print(f"[3] Creating backup: {backup_file}")
    backup_file.write_text(content, encoding='utf-8')

    # Save fixed file
    print(f"[4] Saving fixed file: {TARGET_FILE}")
    TARGET_FILE.write_text(new_content, encoding='utf-8')

    print("\n" + "=" * 70)
    print("[SUCCESS] Method name corrected!")
    print("=" * 70)
    print("\nChanges:")
    print("  1. Changed: database.check_duplicate(file_hash)")
    print("  2. To: database.is_duplicate(file_hash, customer_name)")
    print("  3. Added: customer_name parameter for multi-customer support")
    print("\nNext steps:")
    print("  1. Copy fixed file to Mágerstav deployment")
    print("  2. Start NEXAutomat service")
    print("  3. Test duplicate detection")
    print("=" * 70)

    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)