"""
Script 03: Check BtrieveClient DLL Loading
===========================================

Purpose: Debug why BtrieveClient cannot load w3btrv7.dll

Usage:
    python scripts/03_check_btrieve_client.py
"""

import os
import sys
from pathlib import Path
import ctypes
from ctypes import windll


def test_dll_load(dll_path):
    """Try to load DLL directly with ctypes"""
    print(f"\n🔍 Testing: {dll_path}")
    print(f"   Exists: {'✅' if Path(dll_path).exists() else '❌'}")

    if not Path(dll_path).exists():
        return False

    try:
        # Try windll (stdcall)
        dll = windll.LoadLibrary(str(dll_path))
        print(f"   ✅ Loaded with windll.LoadLibrary")
        return True
    except Exception as e:
        print(f"   ❌ windll.LoadLibrary failed: {e}")

    try:
        # Try cdll (cdecl)
        dll = ctypes.cdll.LoadLibrary(str(dll_path))
        print(f"   ✅ Loaded with cdll.LoadLibrary")
        return True
    except Exception as e:
        print(f"   ❌ cdll.LoadLibrary failed: {e}")

    try:
        # Try CDLL
        dll = ctypes.CDLL(str(dll_path))
        print(f"   ✅ Loaded with CDLL")
        return True
    except Exception as e:
        print(f"   ❌ CDLL failed: {e}")

    return False


def check_path_in_env():
    """Check if C:\PVSW\bin is in PATH"""
    path_env = os.environ.get('PATH', '')
    paths = path_env.split(os.pathsep)

    print("\n🔍 Checking PATH environment variable:")
    print(f"   Total paths: {len(paths)}")

    pvsw_in_path = any('PVSW' in p.upper() for p in paths)
    print(f"   C:\\PVSW\\bin in PATH: {'✅' if pvsw_in_path else '❌'}")

    if pvsw_in_path:
        for p in paths:
            if 'PVSW' in p.upper():
                print(f"      Found: {p}")


def check_python_arch():
    """Check Python architecture"""
    import struct
    bits = struct.calcsize("P") * 8
    print(f"\n🔍 Python architecture: {bits}-bit")
    return bits


def main():
    print("=" * 70)
    print("BTRIEVE CLIENT DLL LOADING DEBUG")
    print("=" * 70)

    # Check Python architecture
    bits = check_python_arch()

    # Check PATH
    check_path_in_env()

    # Test DLL loading
    print("\n" + "=" * 70)
    print("TESTING DLL LOADING")
    print("=" * 70)

    dll_locations = [
        r"C:\PVSW\bin\w3btrv7.dll",
        r"C:\Windows\SysWOW64\w3btrv7.dll",
        r"C:\Program Files (x86)\Pervasive Software\PSQL\bin\w3btrv7.dll"
    ]

    loaded = False
    for dll_path in dll_locations:
        if test_dll_load(dll_path):
            loaded = True
            break

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    if loaded:
        print("\n✅ DLL can be loaded with ctypes")
        print("\n🔍 NEXT STEPS:")
        print("   1. Check BtrieveClient._load_dll() method")
        print("   2. Verify it's using correct loading method")
        print("   3. Check if PATH is set before import")
    else:
        print("\n❌ DLL cannot be loaded with ctypes")
        print("\n💡 POSSIBLE CAUSES:")
        print("   1. 32-bit Python trying to load 64-bit DLL (or vice versa)")
        print("   2. Missing dependencies (other DLLs)")
        print("   3. Corrupted DLL file")
        print("\n💡 SOLUTIONS:")
        print("   1. Check DLL architecture (32-bit vs 64-bit)")
        print("   2. Try adding C:\\PVSW\\bin to PATH before starting app")
        print("   3. Install Pervasive PSQL runtime")


if __name__ == "__main__":
    main()