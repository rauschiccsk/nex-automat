# scripts/fix_btrieve_owner_name.py
"""
Fix BtrieveClient to support owner name in open_file()

CRITICAL FIX: Owner name must go into data_buffer during OPEN operation
"""

import sys
from pathlib import Path


def fix_btrieve_client():
    """Fix open_file() method to include owner name"""

    file_path = Path("packages/nexdata/nexdata/btrieve/btrieve_client.py")

    print(f"Fixing: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find and replace open_file method
    old_code = '''    def open_file(self, filename: str, owner_name: str = "", mode: int = -2) -> Tuple[int, bytes]:
        """
        Otvor Btrieve súbor - FIXED syntax podľa Delphi BtrOpen

        IMPORTANT: Based on Delphi BtrOpen (BtrHand.pas):
        - Filename goes in KEY_BUFFER (not data_buffer!)
        - Data_buffer is EMPTY (dataLen = 0!)
        - keyLen = 255 (max key length)

        Args:
            filename: Cesta k .dat/.BTR súboru
            owner_name: Owner name (optional, not used)
            mode: Open mode
                  0 = Normal
                 -1 = Accelerated
                 -2 = Read-only (DEFAULT - safest)
                 -3 = Exclusive

        Returns:
            Tuple[status_code, position_block]
        """
        # Position block (128 bytes)
        pos_block = ctypes.create_string_buffer(128)

        # Data buffer is EMPTY for OPEN! (according to Delphi BtrOpen)
        data_buffer = ctypes.create_string_buffer(256)
        data_len = ctypes.c_uint32(0)  # ZERO! (and longInt = 4 bytes)

        # FILENAME goes into KEY_BUFFER! (not data_buffer!)
        # Resolve table name to filepath using config
        filepath = self._resolve_table_path(filename)

        filename_bytes = filepath.encode('ascii') + b'\\x00'
        key_buffer = ctypes.create_string_buffer(filename_bytes)

        # keyLen = 255 (max key length, as in BTRV wrapper)
        key_len = 255

        # Call BTRCALL with CORRECT parameters
        status = self.btrcall(
            self.B_OPEN,
            pos_block,
            data_buffer,  # EMPTY!
            ctypes.byref(data_len),  # 0!
            key_buffer,  # FILENAME!
            key_len,  # 255!
            mode & 0xFF  # mode as unsigned BYTE
        )

        return status, pos_block.raw'''

    new_code = '''    def open_file(self, filename: str, owner_name: str = "", mode: int = -2) -> Tuple[int, bytes]:
        """
        Otvor Btrieve súbor - FIXED with owner name support

        CRITICAL: Owner name must be in data_buffer for files with owner security!

        Args:
            filename: Cesta k .dat/.BTR súboru
            owner_name: Owner name (required for secured files!)
            mode: Open mode
                  0 = Normal
                 -1 = Accelerated
                 -2 = Read-only (DEFAULT - safest)
                 -3 = Exclusive

        Returns:
            Tuple[status_code, position_block]
        """
        # Position block (128 bytes)
        pos_block = ctypes.create_string_buffer(128)

        # Data buffer with OWNER NAME (if provided)
        if owner_name:
            # Owner name goes into data_buffer (null-terminated, max 8 chars)
            owner_bytes = owner_name.encode('ascii')[:8].ljust(8, b'\\x00')
            data_buffer = ctypes.create_string_buffer(owner_bytes, 256)
            data_len = ctypes.c_uint32(len(owner_bytes))
        else:
            # No owner name - empty data buffer
            data_buffer = ctypes.create_string_buffer(256)
            data_len = ctypes.c_uint32(0)

        # FILENAME goes into KEY_BUFFER!
        # Resolve table name to filepath using config
        filepath = self._resolve_table_path(filename)

        filename_bytes = filepath.encode('ascii') + b'\\x00'
        key_buffer = ctypes.create_string_buffer(filename_bytes)

        # keyLen = 255 (max key length)
        key_len = 255

        # Call BTRCALL
        status = self.btrcall(
            self.B_OPEN,
            pos_block,
            data_buffer,
            ctypes.byref(data_len),
            key_buffer,
            key_len,
            mode & 0xFF
        )

        return status, pos_block.raw'''

    # Replace
    if old_code in content:
        content = content.replace(old_code, new_code)

        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print("✅ Fixed open_file() method")
        print("   Added owner_name support in data_buffer")
        return True
    else:
        print("❌ Could not find old code to replace")
        print("   File may have been modified already")
        return False


if __name__ == "__main__":
    if fix_btrieve_client():
        print("\n" + "=" * 70)
        print("NEXT STEP: Test with owner name")
        print("=" * 70)
        print("\nTry these owner names:")
        print("  • 'NEX'")
        print("  • 'GENESIS'")
        print("  • 'ADMIN'")
        print("  • '' (empty)")
        print("\nRun: python scripts/test_owner_names.py")
    else:
        print("\n❌ Fix failed - manual edit required")
        sys.exit(1)