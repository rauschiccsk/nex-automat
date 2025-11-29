"""
Hex dump viewer for Btrieve file headers.
Shows first 512 bytes in hex + ASCII format for manual analysis.
"""
import struct
from pathlib import Path


def hex_dump(data: bytes, offset: int = 0, length: int = None) -> str:
    """Create hex dump with ASCII representation."""
    if length:
        data = data[:length]

    lines = []
    for i in range(0, len(data), 16):
        # Offset
        line = f"{offset + i:08X}  "

        # Hex bytes
        hex_part = ""
        ascii_part = ""
        for j in range(16):
            if i + j < len(data):
                byte = data[i + j]
                hex_part += f"{byte:02X} "
                ascii_part += chr(byte) if 32 <= byte < 127 else '.'
            else:
                hex_part += "   "
                ascii_part += " "

            # Add separator after 8 bytes
            if j == 7:
                hex_part += " "

        line += hex_part + " |" + ascii_part + "|"
        lines.append(line)

    return "\n".join(lines)


def analyze_btrieve_header(filepath: str):
    """Analyze and display Btrieve file header."""
    path = Path(filepath)

    if not path.exists():
        print(f"❌ File not found: {filepath}")
        return

    print("\n" + "=" * 80)
    print(f"BTRIEVE FILE HEX DUMP: {path.name}")
    print("=" * 80)
    print(f"Path: {filepath}")
    print(f"Size: {path.stat().st_size:,} bytes ({path.stat().st_size / (1024 * 1024):.2f} MB)")
    print("=" * 80)

    # Read first 512 bytes
    with open(filepath, 'rb') as f:
        header = f.read(512)

    print("\nFIRST 512 BYTES (Hex Dump):")
    print("-" * 80)
    print(hex_dump(header))
    print("-" * 80)

    # Try to parse some known fields
    print("\nKNOWN FIELD ATTEMPTS:")
    print("-" * 80)

    # Signature at offset 0 (2 bytes)
    sig_le = struct.unpack('<H', header[0:2])[0]
    sig_be = struct.unpack('>H', header[0:2])[0]
    print(f"Offset 0x00 (Signature):")
    print(f"  Little-endian: 0x{sig_le:04X} = '{chr(sig_le & 0xFF)}{chr(sig_le >> 8)}'")
    print(f"  Big-endian:    0x{sig_be:04X} = '{chr(sig_be >> 8)}{chr(sig_be & 0xFF)}'")

    # Page size at offset 2 (2 bytes)
    ps_le = struct.unpack('<H', header[2:4])[0]
    ps_be = struct.unpack('>H', header[2:4])[0]
    print(f"\nOffset 0x02 (Page Size?):")
    print(f"  Little-endian: {ps_le} (0x{ps_le:04X})")
    print(f"  Big-endian:    {ps_be} (0x{ps_be:04X})")

    # Version at offset 4 (2 bytes)
    ver_le = struct.unpack('<H', header[4:6])[0]
    ver_be = struct.unpack('>H', header[4:6])[0]
    print(f"\nOffset 0x04 (Version?):")
    print(f"  Little-endian: 0x{ver_le:04X} = {ver_le >> 8}.{ver_le & 0xFF}")
    print(f"  Big-endian:    0x{ver_be:04X} = {ver_be >> 8}.{ver_be & 0xFF}")

    # Try different offsets for page size
    print(f"\nSEARCHING FOR PAGE SIZE (512, 1024, 2048, 4096):")
    valid_sizes = [512, 1024, 2048, 4096]
    for offset in range(0, 32, 2):
        val_le = struct.unpack('<H', header[offset:offset + 2])[0]
        val_be = struct.unpack('>H', header[offset:offset + 2])[0]

        if val_le in valid_sizes or val_be in valid_sizes:
            print(f"  Offset 0x{offset:02X}: LE={val_le}, BE={val_be}")

    # ASCII strings
    print(f"\nASCII STRINGS (first 128 bytes):")
    ascii_view = ""
    for i in range(128):
        b = header[i]
        if 32 <= b < 127:
            ascii_view += chr(b)
        else:
            ascii_view += '.'
    print(f"  {ascii_view}")

    print("\n" + "=" * 80 + "\n")


def main():
    """Analyze target files."""
    files = [
        r"C:\NEX\YEARACT\STORES\GSCAT.BTR",
        r"C:\NEX\YEARACT\STORES\BARCODE.BTR",
    ]

    for filepath in files:
        analyze_btrieve_header(filepath)


if __name__ == "__main__":
    main()