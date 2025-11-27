# scripts/test_owner_names.py
"""Test different owner names to find correct one"""

import sys
from pathlib import Path

# Add nexdata package to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'packages' / 'nexdata'))

from nexdata.btrieve.btrieve_client import BtrieveClient


def test_owner_names():
    """Test different owner names"""

    print("=" * 70)
    print("Btrieve Owner Name Test")
    print("=" * 70)

    test_file = r"C:\NEX\YEARACT\STORES\GSCAT.BTR"

    # Test different owner names
    owner_names = [
        ("", "Empty (no owner)"),
        ("NEX", "NEX"),
        ("GENESIS", "GENESIS"),
        ("ADMIN", "ADMIN"),
        ("SYSDBA", "SYSDBA"),
        ("PSQL", "PSQL"),
        ("BTRIEVE", "BTRIEVE"),
        ("ROOT", "ROOT"),
    ]

    client = BtrieveClient("config/database.yaml")

    for owner, description in owner_names:
        print(f"\n{'=' * 70}")
        print(f"Testing owner: '{owner}' ({description})")
        print(f"{'=' * 70}")

        status, pos_block = client.open_file(test_file, owner_name=owner, mode=-2)

        if status == 0:
            print(f"✅ SUCCESS with owner '{owner}'!")

            # Try to read first record
            try:
                read_status, data = client.get_first(pos_block)

                if read_status == 0:
                    print(f"   ✅ Read first record: {len(data)} bytes")

                    # Parse first few bytes
                    if len(data) >= 100:
                        print(f"   First 100 bytes: {data[:100]}")
                else:
                    print(f"   ❌ Read failed: {read_status}")

                # Close file
                close_status = client.close_file(pos_block)
                print(f"   Close: {close_status}")

                # If we got here, we found the correct owner!
                print(f"\n{'=' * 70}")
                print(f"✅✅✅ FOUND CORRECT OWNER: '{owner}' ✅✅✅")
                print(f"{'=' * 70}")
                return owner

            except Exception as e:
                print(f"   ❌ Error during read: {e}")
        else:
            print(f"❌ FAILED with status {status}")

            if status == 30:
                print(f"   Still PERMISSION_ERROR - wrong owner")
            elif status == 58:
                print(f"   INVALID_OWNER - owner name incorrect")

    print(f"\n{'=' * 70}")
    print("❌ No valid owner name found")
    print(f"{'=' * 70}")
    print("\nTry checking NEX Genesis configuration files:")
    print("  • C:\\NEX\\*.ini")
    print("  • C:\\NEX\\*.cfg")
    print("  • NEX Genesis documentation")

    return None


if __name__ == "__main__":
    test_owner_names()