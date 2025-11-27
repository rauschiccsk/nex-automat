# scripts/test_file_version.py
"""
Diagnostika Btrieve file version a štruktúry
Status 30 = B_NOT_A_BTRIEVE_FILE
"""

import struct
from pathlib import Path


def read_btrieve_header(filepath):
    """Read Btrieve file header"""

    print("=" * 70)
    print(f"Btrieve File Header Analysis: {filepath}")
    print("=" * 70)

    try:
        with open(filepath, 'rb') as f:
            # Read first 1024 bytes
            header = f.read(1024)

            print(f"\nFile size: {Path(filepath).stat().st_size:,} bytes")
            print(f"Header (first 64 bytes):")
            print(header[:64].hex())

            # Try to find version info
            # Btrieve files usually have version info in first few bytes

            # Check for common patterns
            if header[0:2] == b'\x46\x43':  # 'FC' - common Btrieve marker
                print("\n✅ Found Btrieve file marker (0x46 0x43)")
            else:
                print(f"\n❌ Unknown file marker: {header[0:2].hex()}")

            # Read page size (bytes 2-3, little endian)
            if len(header) >= 4:
                page_size = struct.unpack('<H', header[2:4])[0]
                print(f"Page size: {page_size} bytes")

                if page_size in [512, 1024, 2048, 3072, 4096]:
                    print(f"✅ Valid page size")
                else:
                    print(f"⚠️ Unusual page size")

            # Try to read version (offset varies by file format)
            # Common offsets: 4, 6, 8
            for offset in [4, 6, 8, 10]:
                if len(header) > offset + 2:
                    version = struct.unpack('<H', header[offset:offset + 2])[0]
                    print(f"Potential version at offset {offset}: {version} (0x{version:04x})")

                    # Decode version
                    major = (version >> 8) & 0xFF
                    minor = version & 0xFF
                    print(f"  Decoded: v{major}.{minor}")

            # Read record count (typically at offset 8-11, 4 bytes)
            if len(header) >= 12:
                try:
                    rec_count = struct.unpack('<I', header[8:12])[0]
                    print(f"\nRecord count at offset 8: {rec_count:,}")
                except:
                    pass

            # Read file flags (typically at offset 16-17)
            if len(header) >= 18:
                try:
                    flags = struct.unpack('<H', header[16:18])[0]
                    print(f"File flags at offset 16: 0x{flags:04x}")
                    print(f"  Variable records: {bool(flags & 0x0001)}")
                    print(f"  Blank truncation: {bool(flags & 0x0002)}")
                    print(f"  Pre-allocation: {bool(flags & 0x0004)}")
                    print(f"  Data compression: {bool(flags & 0x0008)}")
                    print(f"  Key-only: {bool(flags & 0x0010)}")
                except:
                    pass

    except Exception as e:
        print(f"❌ Error reading file: {e}")

    print("=" * 70)


def compare_files():
    """Compare multiple Btrieve files"""

    files = [
        r"C:\NEX\YEARACT\STORES\GSCAT.BTR",
        r"C:\NEX\YEARACT\STORES\BARCODE.BTR",
        r"C:\NEX\YEARACT\STORES\MGLST.BTR",
    ]

    for filepath in files:
        if Path(filepath).exists():
            read_btrieve_header(filepath)
            print("\n")
        else:
            print(f"❌ File not found: {filepath}\n")


if __name__ == "__main__":
    compare_files()

    print("\n" + "=" * 70)
    print("NEXT STEPS:")
    print("=" * 70)
    print("\n1. Check file versions above")
    print("2. If version > 9.x, files created by Pervasive v11")
    print("3. Need to convert files to Pervasive v9 format")
    print("4. Use BUTIL or Pervasive tools to rebuild/convert")
    print("\nRECOMMENDED:")
    print("  Contact NEX Genesis support")
    print("  Ask about Pervasive version compatibility")