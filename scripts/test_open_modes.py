# scripts/test_open_modes.py
"""Test different Btrieve open modes to diagnose status 30"""

import sys
from pathlib import Path

# Add nexdata package to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'packages' / 'nexdata'))

from nexdata.btrieve.btrieve_client import BtrieveClient

# Btrieve status codes (extended)
STATUS_CODES = {
    0: "SUCCESS",
    1: "INVALID_OPERATION",
    2: "IO_ERROR",
    3: "FILE_NOT_OPEN",
    4: "KEY_NOT_FOUND",
    5: "DUPLICATE_KEY",
    6: "INVALID_KEY_NUMBER",
    7: "DIFFERENT_KEY_NUMBER",
    8: "INVALID_POSITIONING",
    9: "END_OF_FILE",
    10: "MODIFIABLE_KEYVALUE_ERROR",
    11: "INVALID_FILENAME",
    12: "FILE_NOT_FOUND",
    13: "EXTENDED_FILE_ERROR",
    14: "PREIMAGE_OPEN_ERROR",
    15: "PREIMAGE_IO_ERROR",
    18: "DISK_FULL",
    20: "RECORD_MANAGER_INACTIVE",
    21: "KEY_BUFFER_TOO_SHORT",
    22: "DATA_BUFFER_LENGTH_ERROR",
    26: "PAGE_SIZE_ERROR",
    27: "CREATE_IO_ERROR",
    28: "NUMBER_OF_KEYS_ERROR",
    30: "PERMISSION_ERROR",  # ← This is our error!
    32: "TRANSACTION_ERROR",
    34: "LOST_POSITION_ERROR",
    35: "READ_OUTSIDE_TRANSACTION",
    36: "RECORD_IN_USE",
    37: "FILE_IN_USE",
    38: "FILE_TABLE_FULL",
    39: "HANDLE_TABLE_FULL",
    40: "INCOMPATIBLE_MODE_ERROR",
    41: "DEVICE_TABLE_FULL",
    42: "VAR_PAGE_ERROR",
    43: "AUTOINCREMENT_ERROR",
    44: "INCOMPLETE_ACCEL_ACCESS",
    45: "INCOMPLETE_INDEX",
    46: "EXPANED_MEM_ERROR",
    47: "COMPRESS_BUFFER_TOO_SHORT",
    48: "FILE_ALREADY_EXISTS",
    49: "REJECT_COUNT_REACHED",
    50: "PHYSICAL_IO_ERROR",
    51: "CLOSE_ERROR",
    52: "DISK_IO_ERROR",
    53: "WRITE_PROTECT_ERROR",
    54: "PAGE_SIZE_TOO_LARGE",
    55: "INVALID_ALT_SEQUENCE",
    56: "KEY_TYPE_ERROR",
    57: "OWNER_ALREADY_SET",
    58: "INVALID_OWNER",
    59: "ERROR_WRITING_CACHE",
    60: "INVALID_INTERFACE",
    61: "VARIABLE_PAGE_ERROR",
    62: "AUTOINCREMENT_DEFINED",
    63: "INCOMPLETE_REMOVE",
    64: "INCOMPLETE_RENAME",
    80: "CONFLICT",
    81: "LOCK_ERROR",
    82: "LOST_POSITION",
    83: "READ_OUTSIDE_TRANSACTION",
    84: "RECORD_IN_USE",
    85: "FILE_IN_USE_EXCLUSIVE",
    86: "FILE_IN_USE_SHARED",
    161: "FILE_NOT_FOUND",
}


def get_status_name(code):
    """Get status code name"""
    return STATUS_CODES.get(code, f"UNKNOWN_{code}")


def test_open_modes():
    """Test different open modes"""

    print("=" * 70)
    print("Btrieve Open Mode Test")
    print("=" * 70)

    test_file = r"C:\NEX\YEARACT\STORES\GSCAT.BTR"

    # Test different modes
    modes = {
        -2: "Read-only (Shared)",
        -1: "Accelerated (Shared)",
        0: "Normal (Shared)",
        -3: "Exclusive",
    }

    client = BtrieveClient("config/database.yaml")

    for mode, mode_name in modes.items():
        print(f"\n{'=' * 70}")
        print(f"Testing mode {mode}: {mode_name}")
        print(f"{'=' * 70}")

        status, pos_block = client.open_file(test_file, mode=mode)
        status_name = get_status_name(status)

        if status == 0:
            print(f"✅ SUCCESS!")
            print(f"   Status: {status} ({status_name})")

            # Try to read first record
            try:
                read_status, data = client.get_first(pos_block)
                read_name = get_status_name(read_status)

                if read_status == 0:
                    print(f"   ✅ Read first record: {len(data)} bytes")
                else:
                    print(f"   ❌ Read failed: {read_status} ({read_name})")

                # Close file
                close_status = client.close_file(pos_block)
                close_name = get_status_name(close_status)
                print(f"   Close: {close_status} ({close_name})")

            except Exception as e:
                print(f"   ❌ Error during read: {e}")
        else:
            print(f"❌ FAILED!")
            print(f"   Status: {status} ({status_name})")

            # Specific diagnostics for status 30
            if status == 30:
                print("\n   Status 30 = PERMISSION_ERROR")
                print("   Possible causes:")
                print("   • File permissions issue")
                print("   • Owner name required")
                print("   • Incompatible open mode")
                print("   • File locked by another process")

    print(f"\n{'=' * 70}")
    print("Test Complete")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    test_open_modes()