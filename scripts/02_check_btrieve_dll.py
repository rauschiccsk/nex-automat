"""
Script 02: Check Btrieve DLL Location
======================================

Purpose: Find where w3btrv7.dll is actually located

Usage:
    python scripts/02_check_btrieve_dll.py
"""

import os
from pathlib import Path


def check_path(path_str):
    """Check if path exists and contains w3btrv7.dll"""
    path = Path(path_str)
    dll_path = path / "w3btrv7.dll"

    print(f"\n📁 {path_str}")
    print(f"   Directory exists: {'✅' if path.exists() else '❌'}")

    if path.exists():
        print(f"   w3btrv7.dll exists: {'✅' if dll_path.exists() else '❌'}")
        if dll_path.exists():
            size = dll_path.stat().st_size
            print(f"   DLL size: {size:,} bytes")
            return True

    return False


def main():
    print("=" * 70)
    print("BTRIEVE DLL LOCATION CHECK")
    print("=" * 70)

    # Paths that BtrieveClient searches
    search_paths = [
        r"C:\Program Files (x86)\Pervasive Software\PSQL\bin",
        r"C:\PVSW\bin",
        r"C:\Windows\SysWOW64"
    ]

    print("\n🔍 Checking standard search paths:")
    found = False
    for path in search_paths:
        if check_path(path):
            found = True

    if not found:
        print("\n❌ w3btrv7.dll NOT FOUND in any standard location")
        print("\n🔍 Searching entire C:\\ drive for w3btrv7.dll...")
        print("   (This may take a minute...)")

        # Search common locations first
        common_locations = [
            r"C:\PVSW",
            r"C:\Pervasive",
            r"C:\Program Files (x86)\Pervasive",
            r"C:\Program Files\Pervasive",
            r"C:\Windows\System32",
            r"C:\NEX"
        ]

        print("\n📁 Checking common locations:")
        for location in common_locations:
            if Path(location).exists():
                for root, dirs, files in os.walk(location):
                    if "w3btrv7.dll" in files:
                        dll_path = Path(root) / "w3btrv7.dll"
                        size = dll_path.stat().st_size
                        print(f"\n✅ FOUND: {dll_path}")
                        print(f"   Size: {size:,} bytes")
                        found = True

        if not found:
            print("\n❌ w3btrv7.dll not found anywhere on C:\\ drive")
            print("\n💡 POSSIBLE SOLUTIONS:")
            print("   1. Btrieve/Pervasive is not installed")
            print("   2. DLL is in a custom location")
            print("   3. Need to install Pervasive PSQL")
    else:
        print("\n✅ w3btrv7.dll found in standard location")


if __name__ == "__main__":
    main()