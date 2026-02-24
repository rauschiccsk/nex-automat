"""
GSCAT.BTR Model - Correct Structure (705 bytes)
===============================================

Correct model based on actual Btrieve record analysis.

CRITICAL: BarCode field starts at offset 60, not 64!

File: GSCAT.BTR
Location: C:\\NEX\\YEARACT\\STORES\\GSCAT.BTR
Record Size: 705 bytes
Encoding: Kamenický (KEYBCS2)
"""

from dataclasses import dataclass

from ..utils.encoding import decode_keybcs2


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
                cleaned = field_value.replace("\x00", "").strip()
                setattr(self, field_name, cleaned)

    @classmethod
    def from_bytes(cls, data: bytes) -> "GSCATRecord":
        """
        Deserialize GSCATRecord from Btrieve bytes

        Args:
            data: Raw bytes from Btrieve record (705 bytes)

        Returns:
            GSCATRecord instance
        """
        import struct

        # Helper function to read string (Kamenický encoding)
        def read_str(offset: int, length: int) -> str:
            return decode_keybcs2(data[offset : offset + length]).rstrip("\x00 ")

        # Helper function to read int32
        def read_int32(offset: int) -> int:
            if offset + 4 > len(data):
                return 0
            return struct.unpack("<i", data[offset : offset + 4])[0]

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
            RawData=data,
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
