#!/usr/bin/env python3
"""
Test Btrieve config lookup and read operations
"""

import sys
from pathlib import Path

# Add packages to path
sys.path.insert(0, str(Path(__file__).parent.parent / "packages" / "nexdata"))

from nexdata.btrieve.btrieve_client import BtrieveClient
from nexdata.repositories.gscat_repository import GSCATRepository
from nexdata.repositories.tsh_repository import TSHRepository


def test_config_loading():
    """Test 1: Config loading"""
    print("\n" + "=" * 70)
    print("TEST 1: Config Loading")
    print("=" * 70)

    try:
        client = BtrieveClient(config_or_path="config/database.yaml")
        print("✅ BtrieveClient created with config")

        # Check config loaded
        if client.config and 'nex_genesis' in client.config:
            tables = client.config['nex_genesis']['tables']
            print(f"✅ Config loaded: {len(tables)} tables")

            # Show table mappings
            print("\nTable mappings:")
            for table_name, path in tables.items():
                print(f"  • {table_name:10s} → {path}")

            return True, client
        else:
            print("❌ Config not loaded properly")
            return False, None

    except Exception as e:
        print(f"❌ Error: {e}")
        return False, None


def test_path_resolution(client: BtrieveClient):
    """Test 2: Path resolution"""
    print("\n" + "=" * 70)
    print("TEST 2: Path Resolution")
    print("=" * 70)

    test_cases = [
        ("gscat", "C:\\NEX\\YEARACT\\STORES\\GSCAT.BTR"),
        ("tsh-001", "C:\\NEX\\YEARACT\\STORES\\TSHA-001.BTR"),
        ("C:/DIRECT/PATH.BTR", "C:/DIRECT/PATH.BTR"),  # Direct path unchanged
    ]

    all_passed = True

    for table_name, expected_path in test_cases:
        resolved = client._resolve_table_path(table_name)

        # Normalize paths for comparison (handle forward/backward slashes)
        resolved_norm = resolved.replace('/', '\\')
        expected_norm = expected_path.replace('/', '\\')

        if resolved_norm == expected_norm:
            print(f"✅ '{table_name}' → {resolved}")
        else:
            print(f"❌ '{table_name}'")
            print(f"   Expected: {expected_path}")
            print(f"   Got:      {resolved}")
            all_passed = False

    return all_passed


def test_gscat_read(client: BtrieveClient):
    """Test 3: GSCAT read operation"""
    print("\n" + "=" * 70)
    print("TEST 3: GSCAT Read Operation")
    print("=" * 70)

    try:
        # Create repository with table name (not path!)
        repo = GSCATRepository(client)

        print(f"✓ Repository created")
        print(f"✓ Table name: {repo.table_name}")

        # Debug: show what path will be resolved
        resolved_path = client._resolve_table_path(repo.table_name)
        print(f"✓ Resolved path: {resolved_path}")

        # Check if file exists
        from pathlib import Path
        file_path = Path(resolved_path)
        if file_path.exists():
            print(f"✓ File exists on disk")
        else:
            print(f"⚠️  File does NOT exist: {resolved_path}")

        # Open file
        print(f"\nOpening file: '{repo.table_name}'...")
        success = repo.open()

        if success:
            print(f"✅ File opened successfully")

            # Try to read first record
            print("\nReading first record...")
            try:
                record = repo.get_first()
                if record:
                    print(f"✅ First record read:")
                    print(f"   Code:        {record.code}")
                    print(f"   Description: {record.description}")
                    print(f"   EAN:         {record.ean}")

                    # Count total records
                    print("\nCounting total records...")
                    count = sum(1 for _ in repo.get_all())
                    print(f"✅ Total records: {count}")

                    return True
                else:
                    print("⚠️  No records found (empty table)")
                    return True  # Still success - file opened

            except Exception as e:
                print(f"❌ Error reading record: {e}")
                return False
            finally:
                repo.close()
                print("✓ File closed")
        else:
            print(f"❌ File open failed")
            return False

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_tsh_read(client: BtrieveClient):
    """Test 4: TSH read operation (dynamic table)"""
    print("\n" + "=" * 70)
    print("TEST 4: TSH Read Operation (Dynamic Table)")
    print("=" * 70)

    try:
        # Create repository with book_id
        book_id = "001"
        repo = TSHRepository(client, book_id=book_id)

        print(f"✓ Repository created with book_id='{book_id}'")
        print(f"✓ Table name: {repo.table_name}")

        # Debug: show what path will be resolved
        resolved_path = client._resolve_table_path(repo.table_name)
        print(f"✓ Resolved path: {resolved_path}")

        # Check if file exists
        from pathlib import Path
        file_path = Path(resolved_path)
        if file_path.exists():
            print(f"✓ File exists on disk")
        else:
            print(f"⚠️  File does NOT exist: {resolved_path}")

        # Open file
        print(f"\nOpening file: '{repo.table_name}'...")
        success = repo.open()

        if success:
            print(f"✅ File opened successfully")

            # Try to read first record
            print("\nReading first record...")
            try:
                record = repo.get_first()
                if record:
                    print(f"✅ First record read:")
                    print(f"   Doc Number:  {record.C_001}")
                    print(f"   Date:        {record.C_002}")
                    print(f"   Customer ID: {record.C_003}")

                    return True
                else:
                    print("⚠️  No records found (empty table)")
                    return True  # Still success - file opened

            except Exception as e:
                print(f"❌ Error reading record: {e}")
                return False
            finally:
                repo.close()
                print("✓ File closed")
        else:
            print(f"❌ File open failed")
            return False

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    print("=" * 70)
    print("Btrieve Config Lookup - Integration Test")
    print("=" * 70)

    results = []

    # Test 1: Config loading
    success, client = test_config_loading()
    results.append(("Config Loading", success))

    if not success or not client:
        print("\n❌ Cannot continue without client")
        return

    # Test 2: Path resolution
    success = test_path_resolution(client)
    results.append(("Path Resolution", success))

    # Test 3: GSCAT read
    success = test_gscat_read(client)
    results.append(("GSCAT Read", success))

    # Test 4: TSH read
    success = test_tsh_read(client)
    results.append(("TSH Read", success))

    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)

    passed = sum(1 for _, success in results if success)
    total = len(results)

    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}")

    print()
    print(f"Results: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("\n✅ Btrieve config lookup implementation complete!")
        print("\nYou can now:")
        print("  • Use table names instead of full paths")
        print("  • Configure paths in database.yaml")
        print("  • Support multiple environments (dev/prod)")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")

    print("=" * 70)


if __name__ == "__main__":
    main()