# Analyze GSCAT record structure with multiple records

import sys
import struct
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from packages.nexdata.nexdata.btrieve.btrieve_client import BtrieveClient

print("=" * 70)
print("ANALYZING GSCAT RECORD STRUCTURE")
print("=" * 70)

client = BtrieveClient()
status, position_block = client.open_file('gscat')

# Get 10 records to analyze
records = []
result = client.get_first(position_block)
if isinstance(result, tuple):
    status, rec = result
    if status == 0:
        records.append(rec)

for i in range(9):
    result = client.get_next(position_block)
    if isinstance(result, tuple):
        status, rec = result
        if status == 0:
            records.append(rec)

client.close_file(position_block)

print(f"Analyzed {len(records)} records")
print(f"Record size: {len(records[0])} bytes")

# Decode known fields from multiple records
print("\n" + "=" * 70)
print("DECODED FIELDS FROM 10 RECORDS:")
print("=" * 70)

for i, rec in enumerate(records, 1):
    try:
        gs_code = struct.unpack('<i', rec[0:4])[0]
        gs_name = rec[4:64].decode('cp852', errors='replace').rstrip('\x00 ')
        barcode = rec[64:79].decode('cp852', errors='replace').rstrip('\x00 ')

        # Try to find more fields
        # After barcode (offset 79), look for other data

        print(f"\nRecord {i}:")
        print(f"  GsCode: {gs_code}")
        print(f"  GsName: {gs_name[:40]}...")
        print(f"  BarCode @64-78: '{barcode}'")

        # Look for MgCode (unit) - should be after name, typically 2-3 chars
        # Try different positions after barcode
        for offset in [79, 82, 85, 90, 95, 100]:
            if offset + 10 <= len(rec):
                candidate = rec[offset:offset + 10].decode('cp852', errors='replace').rstrip('\x00 ')
                if candidate and len(candidate) <= 3 and candidate.isalpha():
                    print(f"  MgCode candidate @{offset}: '{candidate}'")
                    break

    except Exception as e:
        print(f"Record {i}: Error - {e}")

# Detailed analysis of first record
print("\n" + "=" * 70)
print("DETAILED FIRST RECORD ANALYSIS:")
print("=" * 70)

rec = records[0]
print(f"Total length: {len(rec)} bytes\n")

# Show structure in chunks
chunk_size = 50
for i in range(0, min(300, len(rec)), chunk_size):
    hex_str = ' '.join(f'{b:02x}' for b in rec[i:i + chunk_size])
    ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in rec[i:i + chunk_size])
    decoded = rec[i:i + chunk_size].decode('cp852', errors='replace')
    print(f"{i:03d}-{i + chunk_size - 1:03d}: {ascii_str}")
    print(f"         Decoded: {decoded}")
    print()

# Summary of findings
print("=" * 70)
print("FIELD OFFSET SUMMARY:")
print("=" * 70)
print("GsCode:   0-3    (Int32)")
print("GsName:   4-63   (Str60)")
print("BarCode:  64-78  (Str15) ← CRITICAL: EAN field")
print("MgCode:   79-?   (Str2-3) ← Need to confirm")
print("\nTotal record size: 705 bytes")