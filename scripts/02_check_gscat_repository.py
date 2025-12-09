"""
Check GSCATRepository for Correct BarCode Field Usage
=====================================================

This script checks if GSCATRepository.find_by_barcode() uses the correct
field name (BarCode vs barcode) after deploying the complete GSCAT model.

Phase: NEX Automat v2.4 Phase 4 Deployment
"""

from pathlib import Path

# Paths
DEV_ROOT = Path(r"C:\Development\nex-automat")
GSCAT_REPO = DEV_ROOT / "packages" / "nexdata" / "nexdata" / "repositories" / "gscat_repository.py"


def check_repository():
    """Check GSCATRepository for field usage"""
    print("=" * 70)
    print("CHECKING GSCAT REPOSITORY")
    print("=" * 70)
    print(f"File: {GSCAT_REPO}")
    print("=" * 70)

    if not GSCAT_REPO.exists():
        print(f"❌ ERROR: Repository file not found at {GSCAT_REPO}")
        return False

    # Read file
    content = GSCAT_REPO.read_text(encoding='utf-8')

    # Check for find_by_barcode method
    if 'def find_by_barcode' not in content:
        print("⚠️  WARNING: find_by_barcode method not found")
        print("   This might be OK if EAN matching is handled elsewhere")
        return True

    print("\n✅ find_by_barcode method found")

    # Extract method
    lines = content.split('\n')
    method_lines = []
    in_method = False
    indent_level = 0

    for i, line in enumerate(lines):
        if 'def find_by_barcode' in line:
            in_method = True
            indent_level = len(line) - len(line.lstrip())
            method_lines.append(f"{i + 1:4d}: {line}")
        elif in_method:
            current_indent = len(line) - len(line.lstrip())
            # End of method when we return to same or lower indent (and line is not empty)
            if line.strip() and current_indent <= indent_level:
                break
            method_lines.append(f"{i + 1:4d}: {line}")

    print("\n" + "-" * 70)
    print("METHOD CODE:")
    print("-" * 70)
    for line in method_lines:
        print(line)
    print("-" * 70)

    # Check field usage
    method_content = '\n'.join(method_lines)

    issues = []
    fixes_needed = []

    # Check for lowercase 'barcode' usage
    if 'product.barcode' in method_content.lower() and 'product.BarCode' not in method_content:
        issues.append("❌ ISSUE: Uses 'product.barcode' (lowercase)")
        fixes_needed.append("Change: product.barcode → product.BarCode")

    # Check for correct BarCode usage
    if 'product.BarCode' in method_content or '.barcode' in method_content:
        print("\n✅ Field access found in method")

    # Report results
    print("\n" + "=" * 70)
    if issues:
        print("⚠️  ISSUES FOUND:")
        print("=" * 70)
        for issue in issues:
            print(issue)
        print("\n" + "=" * 70)
        print("FIXES NEEDED:")
        print("=" * 70)
        for fix in fixes_needed:
            print(f"  • {fix}")
        return False
    else:
        print("✅ NO ISSUES FOUND")
        print("=" * 70)
        print("Repository appears to use correct field names.")
        return True


def main():
    """Main check function"""
    print("\n")
    success = check_repository()

    if success:
        print("\n" + "=" * 70)
        print("NEXT STEP: Test EAN Lookup")
        print("=" * 70)
        print("Run: python scripts/03_test_ean_lookup.py")
        print("Expected: 3/20 EAN codes found (15%)")
    else:
        print("\n" + "=" * 70)
        print("NEXT STEP: Fix Repository")
        print("=" * 70)
        print("A fix script will be generated to update field names.")

    return success


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)