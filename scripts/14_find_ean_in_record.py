# Find exact position of EAN barcode in GSCAT record

import sys
import struct
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from packages.nexdata.nexdata.btrieve.btrieve_client import BtrieveClient

# Known EAN codes to search for
KNOWN_EANS = [
    "3245066650142",  # Record 1
    "8715743018251",  # Verified EAN 1
    "5203473211316",  # Verified EAN 2
    "3838847028515",  # Verified EAN 3
]

print("=" * 70)
print("FINDING EAN BARCODE POSITION IN GSCAT")
print("=" * 70)

client = BtrieveClient()
status, position_block = client.open_file('gscat')

# Get first 20 records
records = []
result = client.get_first(position_block)
if isinstance(result, tuple):
    status, rec = result
    if status == 0:
        records.append(rec)

for i in range(19):
    result = client.get_next(position_block)
    if isinstance(result, tuple):
        status, rec = result
        if status == 0:
            records.append(rec)

client.close_file(position_block)

print(f"Loaded {len(records)} records\n")

# Search for known EANs in records
for ean in KNOWN_EANS:
    print(f"Searching for EAN: {ean}")
    found = False

    for i, rec in enumerate(records, 1):
        # Search in decoded string
        try:
            decoded = rec.decode('cp852', errors='replace')
            if ean in decoded:
                # Find exact byte position
                ean_bytes = ean.encode('cp852')
                pos = rec.find(ean_bytes)

                print(f"  ✅ FOUND in record {i} at offset {pos}")
                print(f"     GsCode: {struct.unpack('<i', rec[0:4])[0]}")
                print(
                    f"     Context: ...{rec[max(0, pos - 10):pos + len(ean) + 10].decode('cp852', errors='replace')}...")
                found = True
                break
        except:
            pass

    if not found:
        print(f"  ❌ NOT FOUND in first 20 records")
    print()

# Analyze first record in detail
print("=" * 70)
print("FIRST RECORD BYTE-BY-BYTE (offsets 0-150):")
print("=" * 70)

rec = records[0]
for i in range(150):
    byte_val = rec[i]
    hex_val = f"{byte_val:02x}"

    if 32 <= byte_val < 127:
        char = chr(byte_val)
    else:
        char = '.'

    # Decode as cp852
    try:
        cp852_char = rec[i:i + 1].decode('cp852')
        if not cp852_char.isprintable():
            cp852_char = '.'
    except:
        cp852_char = '.'

    marker = ""
    if i == 0:
        marker = " ← GsCode start"
    elif i == 4:
        marker = " ← GsName start"
    elif i == 64:
        marker = " ← Expected BarCode?"

    print(f"{i:3d}: {hex_val} {char} {cp852_char}{marker}")

    # Show 15-char strings starting at key positions
    if i in [50, 54, 56, 58, 60, 64]:
        test_str = rec[i:i + 15].decode('cp852', errors='replace')
        print(f"     15-char @{i}: '{test_str}'")