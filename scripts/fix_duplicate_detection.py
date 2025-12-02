#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix: Add duplicate detection in POST /invoice endpoint
=======================================================

This script adds proper duplicate detection before database insert
to prevent UNIQUE constraint violations.
"""

from pathlib import Path

# Target file
TARGET_FILE = Path("C:/Development/nex-automat/apps/supplier-invoice-loader/main.py")

# Find and replace pattern
OLD_CODE = '''        # Calculate file hash for duplicate detection
        file_hash = hashlib.md5(pdf_data).hexdigest()

        # 2. Extract data from PDF
        invoice_data = extract_invoice_data(str(pdf_path))

        if not invoice_data:
            raise Exception("Failed to extract data from PDF")

        print(f"[OK] Data extracted: Invoice {invoice_data.invoice_number}")

        # 3. Save to SQLite database
        database.init_database()
        database.save_invoice('''

NEW_CODE = '''        # Calculate file hash for duplicate detection
        file_hash = hashlib.md5(pdf_data).hexdigest()

        # Check for duplicate BEFORE extraction (save processing time)
        database.init_database()
        is_duplicate = database.check_duplicate(file_hash)

        if is_duplicate:
            print(f"[WARN] Duplicate invoice detected: file_hash={file_hash}")
            return {
                "success": True,
                "message": "Duplicate invoice detected - already processed",
                "duplicate": True,
                "file_hash": file_hash,
                "received_date": request.received_date
            }

        # 2. Extract data from PDF
        invoice_data = extract_invoice_data(str(pdf_path))

        if not invoice_data:
            raise Exception("Failed to extract data from PDF")

        print(f"[OK] Data extracted: Invoice {invoice_data.invoice_number}")

        # 3. Save to SQLite database
        database.save_invoice('''


def main():
    """Apply the fix"""
    print("=" * 70)
    print("FIX: Add Duplicate Detection in POST /invoice")
    print("=" * 70)

    # Read current content
    if not TARGET_FILE.exists():
        print(f"[ERROR] File not found: {TARGET_FILE}")
        return False

    print(f"\n[1] Reading: {TARGET_FILE}")
    content = TARGET_FILE.read_text(encoding='utf-8')

    # Check if already fixed
    if "is_duplicate = database.check_duplicate(file_hash)" in content:
        print("[INFO] Duplicate detection already implemented!")
        return True

    # Apply fix
    if OLD_CODE not in content:
        print("[ERROR] Pattern not found in file!")
        print("[INFO] File might have been modified. Manual fix required.")
        return False

    print("[2] Applying fix...")
    new_content = content.replace(OLD_CODE, NEW_CODE)

    # Save backup
    backup_file = TARGET_FILE.with_suffix('.py.backup')
    print(f"[3] Creating backup: {backup_file}")
    backup_file.write_text(content, encoding='utf-8')

    # Save fixed file
    print(f"[4] Saving fixed file: {TARGET_FILE}")
    TARGET_FILE.write_text(new_content, encoding='utf-8')

    print("\n" + "=" * 70)
    print("[SUCCESS] Duplicate detection added!")
    print("=" * 70)
    print("\nChanges:")
    print("  1. Added: database.check_duplicate(file_hash) before extraction")
    print("  2. Returns: {duplicate: true} for duplicates")
    print("  3. Skips: PDF extraction if duplicate detected")
    print("\nNext steps:")
    print("  1. Review the changes in main.py")
    print("  2. Restart NEXAutomat service on Mágerstav server")
    print("  3. Test with duplicate invoice")
    print("=" * 70)

    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)