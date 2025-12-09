"""
Fix GSCATRepository to Use Correct BarCode Field
================================================

This script fixes GSCATRepository.find_by_barcode() to use the correct
BarCode field name for optimal performance.

Change: product.barcode → product.BarCode

Phase: NEX Automat v2.4 Phase 4 Deployment
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

# Paths
DEV_ROOT = Path(r"C:\Development\nex-automat")
GSCAT_REPO = DEV_ROOT / "packages" / "nexdata" / "nexdata" / "repositories" / "gscat_repository.py"
BACKUP_DIR = DEV_ROOT / "backups" / "gscat_repository"


def create_backup():
    """Create backup of current repository"""
    print("=" * 70)
    print("STEP 1: Creating Backup")
    print("=" * 70)

    if not GSCAT_REPO.exists():
        print(f"❌ ERROR: Repository not found at {GSCAT_REPO}")
        return False

    # Create backup directory
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    # Backup filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = BACKUP_DIR / f"gscat_repository_backup_{timestamp}.py"

    # Copy current file
    shutil.copy2(GSCAT_REPO, backup_file)
    print(f"✅ Backup created: {backup_file}")
    print(f"   Size: {backup_file.stat().st_size} bytes")

    return True


def fix_repository():
    """Fix find_by_barcode method to use BarCode field"""
    print("\n" + "=" * 70)
    print("STEP 2: Fixing find_by_barcode Method")
    print("=" * 70)

    # Read current content
    content = GSCAT_REPO.read_text(encoding='utf-8')

    # Find and replace
    old_line = "                if product.barcode and product.barcode.strip() == barcode:"
    new_line = "                if product.BarCode and product.BarCode.strip() == barcode:"

    if old_line not in content:
        print("⚠️  WARNING: Expected line not found")
        print(f"   Looking for: {old_line.strip()}")
        print("\n   Trying alternative search...")

        # Alternative: replace any occurrence
        content_new = content.replace("product.barcode", "product.BarCode")
        changes = content.count("product.barcode")

        if changes > 0:
            print(f"✅ Found and replaced {changes} occurrence(s)")
            GSCAT_REPO.write_text(content_new, encoding='utf-8')
            return True
        else:
            print("❌ ERROR: No occurrences found to replace")
            return False

    # Replace line
    content_new = content.replace(old_line, new_line)

    # Write back
    GSCAT_REPO.write_text(content_new, encoding='utf-8')

    print("✅ Method fixed")
    print(f"   Changed: product.barcode → product.BarCode")
    print(f"   Location: {GSCAT_REPO}")

    return True


def verify_fix():
    """Verify the fix"""
    print("\n" + "=" * 70)
    print("STEP 3: Verification")
    print("=" * 70)

    # Read fixed file
    content = GSCAT_REPO.read_text(encoding='utf-8')

    # Check for old pattern
    if 'product.barcode' in content:
        print("⚠️  WARNING: Still found 'product.barcode' in file")
        # Count occurrences
        count = content.count('product.barcode')
        print(f"   Occurrences: {count}")

        # Show context
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'product.barcode' in line:
                print(f"   Line {i + 1}: {line.strip()}")

        # This might be OK if in comments or other contexts
        if 'def barcode(self)' in content:
            print("\n✅ Note: 'product.barcode' in property definition is OK")

    # Check for new pattern in find_by_barcode method
    if 'def find_by_barcode' in content:
        # Extract method
        lines = content.split('\n')
        in_method = False
        indent_level = 0

        for line in lines:
            if 'def find_by_barcode' in line:
                in_method = True
                indent_level = len(line) - len(line.lstrip())
            elif in_method:
                current_indent = len(line) - len(line.lstrip())
                if line.strip() and current_indent <= indent_level:
                    break
                if 'product.BarCode' in line:
                    print("✅ Method uses correct field: product.BarCode")
                    return True

        print("❌ ERROR: Method does not use product.BarCode")
        return False

    print("✅ Verification complete")
    return True


def main():
    """Main fix function"""
    print("\n" + "=" * 70)
    print("FIX GSCAT REPOSITORY - BARCODE FIELD")
    print("=" * 70)
    print(f"Target: {GSCAT_REPO}")
    print("=" * 70)

    # Step 1: Backup
    if not create_backup():
        print("\n❌ FAILED: Could not create backup")
        return False

    # Step 2: Fix
    if not fix_repository():
        print("\n❌ FAILED: Could not fix repository")
        return False

    # Step 3: Verify
    if not verify_fix():
        print("\n❌ FAILED: Verification failed")
        return False

    # Success
    print("\n" + "=" * 70)
    print("✅ FIX SUCCESSFUL")
    print("=" * 70)
    print("\nNext Steps:")
    print("1. Run: python scripts/03_test_ean_lookup.py")
    print("   Expected: 3/20 EAN codes found (15%)")
    print("\n2. Run: python scripts/02_reprocess_nex_enrichment.py")
    print("   Expected: >70% match rate")

    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)