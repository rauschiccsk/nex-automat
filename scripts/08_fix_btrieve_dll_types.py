#!/usr/bin/env python3
"""
Fix BtrieveClient DLL loading and argtypes to match nex-genesis-server
"""

from pathlib import Path

TARGET_FILE = Path("packages/nexdata/nexdata/btrieve/btrieve_client.py")


def fix_dll_types():
    """Fix DLL loading and function signature"""

    print("=" * 70)
    print("Fix BtrieveClient DLL Types")
    print("=" * 70)
    print()

    if not TARGET_FILE.exists():
        print(f"❌ File not found: {TARGET_FILE}")
        return False

    content = TARGET_FILE.read_text(encoding='utf-8')

    # 1. Change CDLL to WinDLL
    print("🔧 Step 1: Change CDLL to WinDLL...")
    content = content.replace(
        'self.dll = ctypes.CDLL(str(dll_path))',
        'self.dll = ctypes.WinDLL(str(dll_path))'
    )
    print("  ✓ Changed CDLL → WinDLL")

    # 2. Fix argtypes (change last parameter from c_int8 to c_uint8)
    print()
    print("🔧 Step 2: Fix argtypes...")

    old_argtypes = '''self.btrcall.argtypes = [
            ctypes.c_uint16,  # operation
            ctypes.POINTER(ctypes.c_char),  # posBlock
            ctypes.POINTER(ctypes.c_char),  # dataBuffer
            ctypes.POINTER(ctypes.c_uint32),  # dataLen
            ctypes.POINTER(ctypes.c_char),  # keyBuffer
            ctypes.c_uint8,  # keyLen
            ctypes.c_int8  # keyNum'''

    new_argtypes = '''self.btrcall.argtypes = [
            ctypes.c_uint16,  # operation (WORD)
            ctypes.POINTER(ctypes.c_char),  # posBlock (VAR)
            ctypes.POINTER(ctypes.c_char),  # dataBuffer (VAR)
            ctypes.POINTER(ctypes.c_uint32),  # dataLen (longInt = 4 bytes!)
            ctypes.POINTER(ctypes.c_char),  # keyBuffer (VAR)
            ctypes.c_uint8,  # keyLen (BYTE)
            ctypes.c_uint8  # keyNum (BYTE, unsigned!)'''

    if old_argtypes in content:
        content = content.replace(old_argtypes, new_argtypes)
        print("  ✓ Fixed keyNum: c_int8 → c_uint8")
    else:
        print("  ⚠️  Could not find exact argtypes pattern")

    # 3. Fix restype (change from c_uint16 to c_int16)
    print()
    print("🔧 Step 3: Fix restype...")
    content = content.replace(
        'self.btrcall.restype = ctypes.c_uint16',
        'self.btrcall.restype = ctypes.c_int16  # Status code (SMALLINT)'
    )
    print("  ✓ Fixed restype: c_uint16 → c_int16")

    # Write back
    TARGET_FILE.write_text(content, encoding='utf-8')

    print()
    print(f"✅ Fixed: {TARGET_FILE}")
    print()
    print("Changes:")
    print("  ✓ CDLL → WinDLL (Windows calling convention)")
    print("  ✓ keyNum: c_int8 → c_uint8 (unsigned)")
    print("  ✓ restype: c_uint16 → c_int16 (signed)")
    print()
    print("=" * 70)

    return True


if __name__ == "__main__":
    success = fix_dll_types()

    if success:
        print("✅ DLL types fixed!")
        print()
        print("Next: Test again")
        print("  python scripts/test_direct_open.py")
        print("  python scripts/04_test_config_lookup.py")
    else:
        print("❌ Fix failed!")

    print("=" * 70)