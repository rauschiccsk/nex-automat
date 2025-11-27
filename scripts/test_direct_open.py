#!/usr/bin/env python3
"""
Test direct open_file call with different path formats
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "packages" / "nexdata"))

from nexdata.btrieve.btrieve_client import BtrieveClient


def test_path_formats():
    """Test different path formats"""

    print("=" * 70)
    print("Direct open_file() Test")
    print("=" * 70)
    print()

    # Create client WITHOUT config (direct path test)
    client = BtrieveClient(config_or_path=None)

    # Test paths
    paths = [
        r"C:\NEX\YEARACT\STORES\GSCAT.BTR",  # Backslash raw string
        "C:\\NEX\\YEARACT\\STORES\\GSCAT.BTR",  # Escaped backslash
        "C:/NEX/YEARACT/STORES/GSCAT.BTR",  # Forward slash
    ]

    for i, path in enumerate(paths, 1):
        print(f"Test {i}: {path}")

        # Check if file exists
        if Path(path).exists():
            print(f"  ✓ File exists")
        else:
            print(f"  ✗ File does NOT exist")
            continue

        # Try to open
        try:
            status, pos_block = client.open_file(path)

            if status == 0:
                print(f"  ✅ SUCCESS! (status={status})")
                # Close it
                client.close_file(pos_block)
            else:
                print(f"  ❌ FAILED (status={status})")
                print(f"     Error: {client.get_status_message(status)}")
        except Exception as e:
            print(f"  ❌ Exception: {e}")

        print()

    print("=" * 70)


if __name__ == "__main__":
    test_path_formats()