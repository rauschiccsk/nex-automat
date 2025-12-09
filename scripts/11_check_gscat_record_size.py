# Check actual GSCAT record size from Btrieve

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from packages.nexdata.nexdata.btrieve.btrieve_client import BtrieveClient

print("=" * 70)
print("CHECKING GSCAT RECORD SIZE")
print("=" * 70)

# Initialize client
client = BtrieveClient()
print("✅ BtrieveClient initialized")

# Open GSCAT table
try:
    position_block = client.open_file('gscat')
    print(f"✅ GSCAT table opened")
except Exception as e:
    print(f"❌ ERROR: Could not open GSCAT: {e}")
    exit(1)

# Get first record to check size
try:
    result = client.get_first(position_block)

    if isinstance(result, tuple):
        status, record_bytes = result
    else:
        # get_first might return just bytes on success
        status = 0
        record_bytes = result

    if status == 0:
        print(f"\n✅ First record retrieved")
        print(f"   Record size: {len(record_bytes)} bytes")
        print(f"   Expected: ~1232 bytes (based on model)")

        # Show first 200 bytes in hex
        print(f"\n   First 200 bytes (hex):")
        for i in range(0, min(200, len(record_bytes)), 16):
            hex_str = ' '.join(f'{b:02x}' for b in record_bytes[i:i + 16])
            ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in record_bytes[i:i + 16])
            print(f"   {i:04d}: {hex_str:<48} {ascii_str}")

        # Try to decode key fields
        print(f"\n   Decoded fields (cp852):")
        try:
            import struct

            gs_code = struct.unpack('<i', record_bytes[0:4])[0]
            gs_name = record_bytes[4:64].decode('cp852', errors='replace').rstrip('\x00 ')
            mg_code = record_bytes[84:94].decode('cp852', errors='replace').rstrip('\x00 ')

            # Try BarCode at different offsets
            print(f"   GsCode: {gs_code}")
            print(f"   GsName: {gs_name}")
            print(f"   MgCode: {mg_code}")

            # Try BarCode at offset 100 (expected)
            if len(record_bytes) >= 115:
                barcode_100 = record_bytes[100:115].decode('cp852', errors='replace').rstrip('\x00 ')
                print(f"   BarCode @100: '{barcode_100}'")

            # Try alternative offsets
            if len(record_bytes) >= 110:
                barcode_95 = record_bytes[95:110].decode('cp852', errors='replace').rstrip('\x00 ')
                print(f"   BarCode @95:  '{barcode_95}'")

        except Exception as e:
            print(f"   ❌ Decode error: {e}")

        # Get a few more records to confirm size
        print(f"\n   Checking next 5 records:")
        for i in range(5):
            result = client.get_next(position_block)
            if isinstance(result, tuple):
                status, rec = result
            else:
                status = 0
                rec = result
            if status == 0:
                print(f"   Record {i + 2}: {len(rec)} bytes")

    else:
        print(f"❌ ERROR: Could not get first record, status: {status}")

except Exception as e:
    print(f"❌ ERROR: {e}")
finally:
    # Close file
    try:
        client.close_file(position_block)
        print(f"\n✅ GSCAT table closed")
    except:
        pass

print("\n" + "=" * 70)