"""
Btrieve File Version Analyzer
Analyzes Btrieve file headers to determine version and compatibility.
"""
import struct
import os
from pathlib import Path


class BtrieveFileAnalyzer:
    """Analyzer for Btrieve file format."""

    # Known Btrieve file signatures
    SIGNATURES = {
        0x4643: "Btrieve File (FC)",
        0x4946: "Btrieve Index File (IF)",
    }

    # Known page sizes
    PAGE_SIZES = [512, 1024, 1536, 2048, 2560, 3072, 3584, 4096]

    # Version information
    VERSIONS = {
        (6, 0): "Btrieve 6.x",
        (6, 15): "Btrieve 6.15",
        (7, 0): "Btrieve 7.x / Pervasive SQL 2000",
        (8, 0): "Pervasive SQL V8.x",
        (9, 0): "Pervasive SQL V9.x",
        (9, 5): "Pervasive SQL V9.5",
        (10, 0): "Pervasive SQL V10.x",
        (11, 0): "Pervasive SQL V11.x",
        (12, 0): "Actian Zen V12.x",
        (13, 0): "Actian Zen V13.x",
    }

    def __init__(self, filepath: str):
        self.filepath = Path(filepath)
        self.header_data = None

    def read_header(self) -> bool:
        """Read first 512 bytes of file header."""
        try:
            with open(self.filepath, 'rb') as f:
                self.header_data = f.read(512)
            return len(self.header_data) >= 512
        except Exception as e:
            print(f"❌ Error reading file: {e}")
            return False

    def analyze(self) -> dict:
        """Analyze file header and return information."""
        if not self.read_header():
            return {"error": "Cannot read file header"}

        result = {
            "filepath": str(self.filepath),
            "filesize": self.filepath.stat().st_size,
            "filesize_mb": round(self.filepath.stat().st_size / (1024 * 1024), 2),
        }

        # Parse header fields
        try:
            # Offset 0-1: File signature
            signature = struct.unpack('<H', self.header_data[0:2])[0]
            result["signature_hex"] = f"0x{signature:04X}"
            result["signature_desc"] = self.SIGNATURES.get(signature, "Unknown")

            # Offset 2-3: Physical page size
            page_size = struct.unpack('<H', self.header_data[2:4])[0]
            result["page_size"] = page_size
            result["page_size_valid"] = page_size in self.PAGE_SIZES

            # Offset 4-5: File version
            version_word = struct.unpack('<H', self.header_data[4:6])[0]
            major = (version_word >> 8) & 0xFF
            minor = version_word & 0xFF
            result["version_word"] = f"0x{version_word:04X}"
            result["version_major"] = major
            result["version_minor"] = minor
            result["version_desc"] = self.VERSIONS.get((major, minor), f"Unknown {major}.{minor}")

            # Offset 8-11: Number of records (estimated)
            record_count = struct.unpack('<I', self.header_data[8:12])[0]
            result["record_count"] = record_count

            # Offset 16-17: File flags
            file_flags = struct.unpack('<H', self.header_data[16:18])[0]
            result["file_flags"] = f"0x{file_flags:04X}"

            # Offset 24-25: Number of keys
            num_keys = struct.unpack('<H', self.header_data[24:26])[0]
            result["num_keys"] = num_keys

            # Offset 26-27: Record length
            record_length = struct.unpack('<H', self.header_data[26:28])[0]
            result["record_length"] = record_length

            # Offset 30-31: Page usage
            page_usage = struct.unpack('<H', self.header_data[30:32])[0]
            result["page_usage"] = page_usage

            # Compatibility check
            result["compatible_v9"] = major <= 9
            result["compatible_v11"] = major <= 11
            result["is_v11_format"] = major == 11
            result["is_v9_format"] = major == 9

        except Exception as e:
            result["parse_error"] = str(e)

        return result

    def print_analysis(self):
        """Print detailed analysis."""
        result = self.analyze()

        print("\n" + "=" * 70)
        print(f"BTRIEVE FILE ANALYSIS: {self.filepath.name}")
        print("=" * 70)

        if "error" in result:
            print(f"\n❌ {result['error']}")
            return

        if "parse_error" in result:
            print(f"\n❌ Parse error: {result['parse_error']}")
            return

        # Basic info
        print(f"\n📁 FILE INFORMATION:")
        print(f"   Path: {result['filepath']}")
        print(f"   Size: {result['filesize']:,} bytes ({result['filesize_mb']} MB)")

        # Header info
        print(f"\n🔍 FILE HEADER:")
        print(f"   Signature: {result['signature_hex']} - {result['signature_desc']}")
        print(f"   Page Size: {result['page_size']} bytes", end="")
        if result['page_size_valid']:
            print(" ✅")
        else:
            print(" ❌ INVALID")

        # Version info
        print(f"\n📊 VERSION INFORMATION:")
        print(f"   Version Word: {result['version_word']}")
        print(f"   Version: {result['version_major']}.{result['version_minor']}")
        print(f"   Description: {result['version_desc']}")

        # Data info
        print(f"\n📈 DATA INFORMATION:")
        print(f"   Record Count: {result['record_count']:,}")
        print(f"   Record Length: {result['record_length']} bytes")
        print(f"   Number of Keys: {result['num_keys']}")
        print(f"   Page Usage: {result['page_usage']}%")
        print(f"   File Flags: {result['file_flags']}")

        # Compatibility
        print(f"\n🔧 COMPATIBILITY:")
        print(f"   Pervasive V9 Format: {'✅ YES' if result['is_v9_format'] else '❌ NO'}")
        print(f"   Pervasive V11 Format: {'✅ YES' if result['is_v11_format'] else '❌ NO'}")
        print(f"   Compatible with V9 API: {'✅ YES' if result['compatible_v9'] else '❌ NO'}")
        print(f"   Compatible with V11 API: {'✅ YES' if result['compatible_v11'] else '❌ NO'}")

        # Diagnosis
        print(f"\n💡 DIAGNOSIS:")
        if result['is_v11_format']:
            print("   ⚠️  This file is in Pervasive V11 format!")
            print("   ⚠️  Pervasive V9 API cannot open V11 format files.")
            print("   ⚠️  This explains Status 30 (NOT_A_BTRIEVE_FILE) error.")
            print("\n   RECOMMENDED ACTION:")
            print("   → Convert file to V9 format using BUTIL")
            print("   → OR upgrade to Pervasive V11 Licensed version")
        elif result['is_v9_format']:
            print("   ✅ This file is in Pervasive V9 format.")
            print("   ✅ Should be compatible with V9 API.")
            print("\n   IF Status 30 persists:")
            print("   → Check file corruption")
            print("   → Verify Pervasive service configuration")
            print("   → Check file permissions")
        elif result['version_major'] < 9:
            print(f"   ℹ️  This file is in older format (v{result['version_major']}.{result['version_minor']}).")
            print("   ✅ Should be compatible with V9 API.")
        else:
            print(f"   ⚠️  Unknown version: {result['version_major']}.{result['version_minor']}")
            print("   → May require specific Pervasive version")

        print("\n" + "=" * 70 + "\n")


def main():
    """Main function."""
    import sys

    # Test files
    test_files = [
        r"C:\NEX\YEARACT\STORES\GSCAT.BTR",
        r"C:\NEX\YEARACT\STORES\TSH.BTR",
        r"C:\NEX\YEARACT\STORES\TSI.BTR",
        r"C:\NEX\YEARACT\STORES\BARCODE.BTR",
        r"C:\NEX\YEARACT\STORES\PAB.BTR",
        r"C:\NEX\YEARACT\STORES\MGLST.BTR",
    ]

    print("\n" + "=" * 70)
    print("BTRIEVE FILE VERSION ANALYZER")
    print("=" * 70)
    print(f"\nAnalyzing {len(test_files)} Btrieve files...")

    results = []
    for filepath in test_files:
        if not os.path.exists(filepath):
            print(f"\n⚠️  File not found: {filepath}")
            continue

        analyzer = BtrieveFileAnalyzer(filepath)
        analyzer.print_analysis()
        results.append(analyzer.analyze())

    # Summary
    if results:
        print("\n" + "=" * 70)
        print("SUMMARY")
        print("=" * 70)

        v9_count = sum(1 for r in results if r.get('is_v9_format'))
        v11_count = sum(1 for r in results if r.get('is_v11_format'))

        print(f"\nTotal files analyzed: {len(results)}")
        print(f"Pervasive V9 format: {v9_count}")
        print(f"Pervasive V11 format: {v11_count}")

        if v11_count > 0:
            print("\n⚠️  CRITICAL ISSUE CONFIRMED:")
            print(f"   {v11_count} file(s) are in Pervasive V11 format")
            print("   Pervasive V9 API cannot open V11 files (Status 30)")
            print("\n   NEXT STEPS:")
            print("   1. Contact NEX Genesis support for migration guidance")
            print("   2. Consider file conversion to V9 format using BUTIL")
            print("   3. OR obtain Pervasive V11 Licensed version")
        elif v9_count == len(results):
            print("\n✅ All files are in Pervasive V9 format")
            print("   Status 30 error has different cause - investigate further")

        print("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    main()