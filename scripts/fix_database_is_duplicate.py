#!/usr/bin/env python3
"""
Fix database.is_duplicate() for single-tenant architecture.

When customer_name=None is passed, the function should check only file_hash
without forcing customer_name from config.

Usage:
    python fix_database_is_duplicate.py
"""

from pathlib import Path


def fix_is_duplicate():
    """Fix the is_duplicate function in database.py"""

    # Path to database.py in Development
    db_py_path = Path(r"C:\Development\nex-automat\apps\supplier-invoice-loader\src\database\database.py")

    if not db_py_path.exists():
        print(f"ERROR: File not found: {db_py_path}")
        return False

    # Read the file
    print(f"Reading {db_py_path}...")
    content = db_py_path.read_text(encoding='utf-8')

    # Old code block to replace (lines 119-139)
    old_code = """    # Use customer from config if not provided
    if customer_name is None:
        customer_name = CUSTOMER_NAME

    # Check by file hash (primary) within customer
    cursor.execute(
        "SELECT id FROM invoices WHERE file_hash = ? AND customer_name = ?",
        (file_hash, customer_name)
    )
    result = cursor.fetchone()

    # Check by message_id (secondary) within customer
    if not result and message_id:
        cursor.execute(
            "SELECT id FROM invoices WHERE message_id = ? AND customer_name = ?",
            (message_id, customer_name)
        )
        result = cursor.fetchone()"""

    # New code for single-tenant architecture
    new_code = """    # Single-tenant architecture: if customer_name is None, check only file_hash
    if customer_name is None:
        # Check by file hash only (no customer filter)
        cursor.execute(
            "SELECT id FROM invoices WHERE file_hash = ?",
            (file_hash,)
        )
        result = cursor.fetchone()

        # Check by message_id (secondary) if provided
        if not result and message_id:
            cursor.execute(
                "SELECT id FROM invoices WHERE message_id = ?",
                (message_id,)
            )
            result = cursor.fetchone()
    else:
        # Multi-tenant: check within customer scope
        cursor.execute(
            "SELECT id FROM invoices WHERE file_hash = ? AND customer_name = ?",
            (file_hash, customer_name)
        )
        result = cursor.fetchone()

        # Check by message_id (secondary) within customer
        if not result and message_id:
            cursor.execute(
                "SELECT id FROM invoices WHERE message_id = ? AND customer_name = ?",
                (message_id, customer_name)
            )
            result = cursor.fetchone()"""

    # Check if old code exists
    if old_code not in content:
        print("ERROR: Could not find the expected code block in database.py")
        print("The file might have been modified differently.")
        return False

    # Replace old code with new code
    new_content = content.replace(old_code, new_code)

    # Verify change was made
    if new_content == content:
        print("WARNING: No changes were made.")
        return False

    # Backup original file
    backup_path = db_py_path.with_suffix('.py.backup')
    print(f"Creating backup: {backup_path}")
    backup_path.write_text(content, encoding='utf-8')

    # Write fixed content
    print(f"Writing fixed content to {db_py_path}")
    db_py_path.write_text(new_content, encoding='utf-8')

    print("\n✓ SUCCESS: is_duplicate() fixed for single-tenant architecture")
    print("\nChanges:")
    print("  - When customer_name=None: Check only file_hash (no customer filter)")
    print("  - When customer_name provided: Check file_hash AND customer_name (multi-tenant)")

    print(f"\nBackup saved to: {backup_path}")
    print("\nNext steps:")
    print("  1. Git commit and push")
    print("  2. Deploy to Production (Magerstav server)")
    print("  3. Restart NEXAutomat service")
    print("  4. Test duplicate detection")

    return True


if __name__ == "__main__":
    print("=" * 70)
    print("Fix database.is_duplicate() - Single Tenant Architecture")
    print("=" * 70)
    print()

    success = fix_is_duplicate()

    if not success:
        print("\n✗ FAILED: Fix could not be applied")
        exit(1)

    print("\n" + "=" * 70)