"""
Test NEX Shared Import
"""

import sys
from pathlib import Path


def test_import():
    """Test import nex_shared"""

    print("=" * 60)
    print("TESTING NEX-SHARED IMPORT")
    print("=" * 60)
    print()

    # Show Python version and paths
    print(f"Python: {sys.version}")
    print()
    print("Python paths:")
    for p in sys.path:
        print(f"  {p}")
    print()

    # Try import
    try:
        print("Importing nex_shared...")
        import nex_shared
        print(f"✅ SUCCESS: nex_shared imported")
        print(f"   Location: {nex_shared.__file__}")
        print()

        print("Importing BtrieveClient...")
        from nex_shared import BtrieveClient
        print(f"✅ SUCCESS: BtrieveClient imported")
        print(f"   Class: {BtrieveClient}")
        print()

        print("Importing TSHRecord...")
        from nex_shared import TSHRecord
        print(f"✅ SUCCESS: TSHRecord imported")
        print(f"   Class: {TSHRecord}")
        print()

        print("Importing TSIRecord...")
        from nex_shared import TSIRecord
        print(f"✅ SUCCESS: TSIRecord imported")
        print(f"   Class: {TSIRecord}")
        print()

        print("=" * 60)
        print("✅ ALL IMPORTS SUCCESSFUL")
        print("=" * 60)
        return True

    except ImportError as e:
        print(f"❌ IMPORT FAILED: {e}")
        print()
        import traceback
        traceback.print_exc()
        print()
        print("=" * 60)
        print("❌ IMPORT FAILED")
        print("=" * 60)
        return False


def test_basic_functionality():
    """Test základná funkcionalita"""

    print()
    print("=" * 60)
    print("TESTING BASIC FUNCTIONALITY")
    print("=" * 60)
    print()

    try:
        from nex_shared import BtrieveClient, TSHRecord, TSIRecord

        # Test BtrieveClient constants
        print("BtrieveClient constants:")
        print(f"  B_OPEN = {BtrieveClient.B_OPEN}")
        print(f"  B_CLOSE = {BtrieveClient.B_CLOSE}")
        print(f"  B_GET_FIRST = {BtrieveClient.B_GET_FIRST}")
        print(f"  STATUS_SUCCESS = {BtrieveClient.STATUS_SUCCESS}")
        print()

        # Test TSHRecord creation
        print("Creating test TSHRecord...")
        tsh = TSHRecord(doc_number="TEST001")
        print(f"✅ TSHRecord created: {tsh}")
        print()

        # Test TSIRecord creation
        print("Creating test TSIRecord...")
        tsi = TSIRecord(doc_number="TEST001", line_number=1)
        print(f"✅ TSIRecord created: {tsi}")
        print()

        print("=" * 60)
        print("✅ BASIC FUNCTIONALITY OK")
        print("=" * 60)
        return True

    except Exception as e:
        print(f"❌ FUNCTIONALITY TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main execution"""

    success_import = test_import()

    if success_import:
        success_func = test_basic_functionality()

        if success_func:
            print()
            print("🎉 NEX-SHARED PACKAGE FULLY FUNCTIONAL!")
            sys.exit(0)
        else:
            print()
            print("⚠️  Import OK, but functionality test failed")
            sys.exit(1)
    else:
        print()
        print("❌ Import failed. Run reinstall:")
        print("   pip uninstall -y nex-shared")
        print("   pip install -e packages/nex-shared")
        sys.exit(1)


if __name__ == "__main__":
    main()