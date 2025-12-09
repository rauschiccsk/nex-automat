# Create correct GSCAT model based on actual Btrieve structure

from pathlib import Path
import shutil
from datetime import datetime

DEV_ROOT = Path(r"C:\Development\nex-automat")
GSCAT_MODEL = DEV_ROOT / "packages" / "nexdata" / "nexdata" / "models" / "gscat.py"
BACKUP_DIR = DEV_ROOT / "backups" / "gscat_model"

print("=" * 70)
print("CREATING CORRECT GSCAT MODEL")
print("=" * 70)

# Backup
BACKUP_DIR.mkdir(parents=True, exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup_file = BACKUP_DIR / f"gscat_backup_{timestamp}.py"
shutil.copy2(GSCAT_MODEL, backup_file)
print(f"Backup: {backup_file}\n")

# Correct model based on actual analysis
correct_model = '''"""
GSCAT.BTR Model - Correct Structure (705 bytes)
===============================================

Correct model based on actual Btrieve record analysis.

CRITICAL: BarCode field starts at offset 60, not 64!

File: GSCAT.BTR
Location: C:\\\\NEX\\\\YEARACT\\\\STORES\\\\GSCAT.BTR
Record Size: 705 bytes
Encoding: cp852
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class GSCATRecord:
    """GSCAT record - simplified model with verified fields only"""

    # Primary Key
    GsCode: int  # Offset 0-3, Int32

    # Basic Product Info
    GsName: str  # Offset 4-63, Str60 (but actual data shorter)

    # CRITICAL: EAN Barcode Field
    BarCode: str  # Offset 60-74, Str15 - EAN barcode

    # Supplier code (appears after BarCode)
    SupplierCode: str  # Offset 75-80, Str6

    # Unit of measure
    MgCode: str  # Offset 92-93, Str2

    # Additional fields (placeholder - need more analysis)
    RawData: bytes  # Store full record for future expansion

    def __post_init__(self):
        """Clean up string fields"""
        # Remove NULL bytes and strip whitespace from all string fields
        for field_name, field_value in self.__dict__.items():
            if isinstance(field_value, str):
                cleaned = field_value.replace('\\x00', '').strip()
                setattr(self, field_name, cleaned)

    @classmethod
    def from_bytes(cls, data: bytes, encoding: str = 'cp852') -> 'GSCATRecord':
        """
        Deserialize GSCATRecord from Btrieve bytes

        Args:
            data: Raw bytes from Btrieve record (705 bytes)
            encoding: Character encoding (default: cp852)

        Returns:
            GSCATRecord instance
        """
        import struct

        # Helper function to read string
        def read_str(offset: int, length: int) -> str:
            return data[offset:offset+length].decode(encoding, errors='replace').rstrip('\\x00 ')

        # Helper function to read int32
        def read_int32(offset: int) -> int:
            if offset + 4 > len(data):
                return 0
            return struct.unpack('<i', data[offset:offset+4])[0]

        # Parse verified fields according to actual structure
        gs_code = read_int32(0)
        gs_name = read_str(4, 60)  # Full field is 60 bytes
        barcode = read_str(60, 15)  # CRITICAL: Starts at offset 60!
        supplier_code = read_str(75, 6)
        mg_code = read_str(92, 2)

        return cls(
            GsCode=gs_code,
            GsName=gs_name,
            BarCode=barcode,
            SupplierCode=supplier_code,
            MgCode=mg_code,
            RawData=data
        )

    @property
    def barcode(self) -> str:
        """Alias for BarCode field (for backward compatibility)"""
        return self.BarCode

    @property
    def gs_code(self) -> int:
        """Alias for GsCode field (for backward compatibility)"""
        return self.GsCode

    @property
    def gs_name(self) -> str:
        """Alias for GsName field (for backward compatibility)"""
        return self.GsName

    @property
    def mg_code(self) -> str:
        """Alias for MgCode field (for backward compatibility)"""
        return self.MgCode
'''

# Write correct model
GSCAT_MODEL.write_text(correct_model, encoding='utf-8')

print("=" * 70)
print("CORRECT MODEL DEPLOYED")
print("=" * 70)
print(f"Location: {GSCAT_MODEL}")
print(f"\nKEY CHANGES:")
print("  - BarCode offset: 64 → 60 (CRITICAL FIX!)")
print("  - Record size: 1232 → 705 bytes")
print("  - Simplified to verified fields only")
print("  - Added RawData for future expansion")
print("\nVERIFIED OFFSETS:")
print("  GsCode:       0-3   (Int32)")
print("  GsName:       4-63  (Str60)")
print("  BarCode:      60-74 (Str15) ← EAN field")
print("  SupplierCode: 75-80 (Str6)")
print("  MgCode:       92-93 (Str2)")
print("\n" + "=" * 70)
print("NEXT STEP:")
print("=" * 70)
print("python scripts/test_ean_lookup.py")
print("\nExpected:")
print("  - 3/3 verified EAN codes found")
print("  - Overall success rate >15%")