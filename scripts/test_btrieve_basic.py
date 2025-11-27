#!/usr/bin/env python3
"""
Test basic Btrieve operations matching nex-genesis-server approach
"""

import ctypes
from pathlib import Path

# Load Btrieve DLL
dll_path = r"C:\Program Files (x86)\Pervasive Software\PSQL\bin\w3btrv7.dll"
dll = ctypes.CDLL(dll_path)

# Get BTRCALL function
btrcall = dll.BTRCALL
btrcall.argtypes = [
    ctypes.c_uint16,  # operation
    ctypes.POINTER(ctypes.c_char),  # posBlock
    ctypes.POINTER(ctypes.c_char),  # dataBuffer
    ctypes.POINTER(ctypes.c_uint32),  # dataLen
    ctypes.POINTER(ctypes.c_char),  # keyBuffer
    ctypes.c_uint16,  # keyLen (changed from c_uint8)
    ctypes.c_int8  # ckeynum
]
btrcall.restype = ctypes.c_uint16

print("=" * 70)
print("Basic Btrieve Test (matching nex-genesis-server)")
print("=" * 70)
print()
print(f"✓ Loaded DLL: {dll_path}")
print(f"✓ Found BTRCALL function")
print()

# Test file
test_file = r"C:\NEX\YEARACT\STORES\GSCAT.BTR"
print(f"Test file: {test_file}")
print(f"File exists: {Path(test_file).exists()}")
print()

# Prepare buffers (matching Delphi BtrOpen from nex-genesis-server)
pos_block = ctypes.create_string_buffer(128)
data_buffer = ctypes.create_string_buffer(256)
data_len = ctypes.c_uint32(0)  # EMPTY for OPEN

# Filename in key_buffer
filename_bytes = test_file.encode('ascii') + b'\x00'
key_buffer = ctypes.create_string_buffer(filename_bytes)
key_len = 255

# Mode
B_OPEN = 0
modes_to_test = [
    (0, "Normal"),
    (-1, "Accelerated"),
    (-2, "Read-only"),
]

for mode_val, mode_desc in modes_to_test:
    print(f"\n--- Testing mode: {mode_val} ({mode_desc}) ---")

    # Call BTRCALL
    status = btrcall(
        B_OPEN,
        pos_block,
        data_buffer,
        ctypes.byref(data_len),
        key_buffer,
        key_len,
        mode_val & 0xFF
    )

    print(f"  Status: {status}")

    if status == 0:
        print(f"  ✅ SUCCESS with mode {mode_val}!")

        # Try to close
        B_CLOSE = 1
        close_status = btrcall(
            B_CLOSE,
            pos_block,
            data_buffer,
            ctypes.byref(data_len),
            key_buffer,
            key_len,
            0
        )
        print(f"  Close status: {close_status}")
        break
    else:
        print(f"  ❌ Failed with mode {mode_val}")

print()
print("=" * 70)