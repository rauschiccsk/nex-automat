"""
Fix GSCAT Model Unicode Escape Error
====================================

Fixes unicode escape error in GSCAT model docstring.
Changes C:\NEX\... paths to use raw strings or double backslashes.
"""

from pathlib import Path

# Paths
DEV_ROOT = Path(r"C:\Development\nex-automat")
GSCAT_MODEL = DEV_ROOT / "packages" / "nexdata" / "nexdata" / "models" / "gscat.py"


def fix_model():
    """Fix unicode escape in docstring"""
    print("=" * 70)
    print("FIXING GSCAT MODEL UNICODE ERROR")
    print("=" * 70)

    # Read current content
    content = GSCAT_MODEL.read_text(encoding='utf-8')

    # Fix: Replace single backslashes with double backslashes in path
    content_fixed = content.replace(
        r'Location: C:\NEX\YEARACT\STORES\GSCAT.BTR',
        r'Location: C:\\NEX\\YEARACT\\STORES\\GSCAT.BTR'
    )

    # Write back
    GSCAT_MODEL.write_text(content_fixed, encoding='utf-8')

    print("✅ Fixed unicode escape in docstring")
    print(f"   Changed: C:\\NEX\\... → C:\\\\NEX\\\\...")
    print(f"   Location: {GSCAT_MODEL}")

    return True


def verify_fix():
    """Verify the fix by trying to import"""
    print("\n" + "=" * 70)
    print("VERIFICATION - Testing Import")
    print("=" * 70)

    try:
        # Try to compile the file
        content = GSCAT_MODEL.read_text(encoding='utf-8')
        compile(content, str(GSCAT_MODEL), 'exec')
        print("✅ File compiles successfully")
        return True
    except SyntaxError as e:
        print(f"❌ Syntax error still present: {e}")
        return False
    except Exception as e:
        print(f"❌ Other error: {e}")
        return False


def main():
    """Main fix function"""
    print("\n")

    if not fix_model():
        print("\n❌ FAILED: Could not fix model")
        return False

    if not verify_fix():
        print("\n❌ FAILED: Verification failed")
        return False

    print("\n" + "=" * 70)
    print("✅ FIX SUCCESSFUL")
    print("=" * 70)
    print("\nNext Step:")
    print("Run: python scripts/test_ean_lookup.py")

    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)