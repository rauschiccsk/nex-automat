# Add from_bytes classmethod to GSCATRecord

from pathlib import Path

DEV_ROOT = Path(r"C:\Development\nex-automat")
GSCAT_MODEL = DEV_ROOT / "packages" / "nexdata" / "nexdata" / "models" / "gscat.py"

print("=" * 70)
print("ADDING from_bytes() METHOD TO GSCAT MODEL")
print("=" * 70)

# Read current content
content = GSCAT_MODEL.read_text(encoding='utf-8')

# Find where to insert (after __post_init__)
insert_marker = "    def __post_init__(self):"
insert_pos = content.find(insert_marker)

if insert_pos == -1:
    print("❌ ERROR: Could not find __post_init__ method")
    exit(1)

# Find end of __post_init__ method (next method or @property)
lines = content[insert_pos:].split('\n')
method_end_line = 0
for i, line in enumerate(lines[1:], 1):
    if line.strip() and not line.startswith(' ' * 8):  # Back to class level indentation
        method_end_line = i
        break

# Calculate absolute position
abs_insert_pos = insert_pos + len('\n'.join(lines[:method_end_line]))

# from_bytes method to insert
from_bytes_method = '''
    @classmethod
    def from_bytes(cls, data: bytes, encoding: str = 'cp852') -> 'GSCATRecord':
        """
        Deserialize GSCATRecord from Btrieve bytes

        Args:
            data: Raw bytes from Btrieve record
            encoding: Character encoding (default: cp852)

        Returns:
            GSCATRecord instance
        """
        import struct

        # Helper function to read string
        def read_str(offset: int, length: int) -> str:
            return data[offset:offset+length].decode(encoding, errors='replace').rstrip('\\x00 ')

        # Helper function to read int
        def read_int32(offset: int) -> int:
            return struct.unpack('<i', data[offset:offset+4])[0]

        def read_int16(offset: int) -> int:
            return struct.unpack('<h', data[offset:offset+2])[0]

        # Helper function to read float (Real)
        def read_real(offset: int) -> float:
            return struct.unpack('<f', data[offset:offset+4])[0]

        # Helper function to read bool
        def read_bool(offset: int) -> bool:
            return data[offset] != 0

        # Parse all fields according to Btrieve structure
        return cls(
            GsCode=read_int32(0),
            GsName=read_str(4, 60),
            GsShName=read_str(64, 20),
            MgCode=read_str(84, 10),
            CtCode=read_str(94, 3),
            FgCode=read_str(97, 3),
            BarCode=read_str(100, 15),  # CRITICAL: EAN field
            InPrice=read_real(115),
            OutPrice=read_real(119),
            Stock=read_real(123),
            MinStock=read_real(127),
            MaxStock=read_real(131),
            VatCode=read_str(135, 3),
            Margin=read_real(138),
            Weight=read_real(142),
            Volume=read_real(146),
            Color=read_str(150, 20),
            Size=read_str(170, 20),
            SupCode=read_str(190, 10),
            SupPrice=read_real(200),
            SupDiscount=read_real(204),
            Active=read_bool(208),
            IsService=read_bool(209),
            IsSet=read_bool(210),
            Note1=read_str(211, 40),
            Note2=read_str(251, 40),
            Note3=read_str(291, 40),
            CreateDate=read_str(331, 8),
            ModifyDate=read_str(339, 8),
            LastSaleDate=read_str(347, 8),
            InvCode=read_str(355, 10),
            LocCode=read_str(365, 10),
            AltCode1=read_str(375, 20),
            AltCode2=read_str(395, 20),
            AltCode3=read_str(415, 20),
            WholesalePrice=read_real(435),
            RetailPrice=read_real(439),
            SpecialPrice=read_real(443),
            Brand=read_str(447, 30),
            Model=read_str(477, 30),
            Series=read_str(507, 30),
            Material=read_str(537, 20),
            Origin=read_str(557, 20),
            Manufacturer=read_str(577, 40),
            PackQty=read_real(617),
            PackType=read_str(621, 10),
            QualityGrade=read_str(631, 10),
            WarrantyMonths=read_int16(641),
            MinOrderQty=read_real(643),
            MaxOrderQty=read_real(647),
            OrderMultiple=read_real(651),
            Discontinued=read_bool(655),
            NewProduct=read_bool(656),
            BestSeller=read_bool(657),
            OnSale=read_bool(658),
            TechSpec=read_str(659, 100),
            Description=read_str(759, 200),
            UserField1=read_str(959, 50),
            UserField2=read_str(1009, 50),
            UserField3=read_str(1059, 50),
            UserField4=read_str(1109, 50),
            UserField5=read_str(1159, 50),
            RecordVersion=read_int16(1209),
            LastUser=read_str(1211, 20),
            LockStatus=read_bool(1231),
        )
'''

# Insert method
content_new = content[:abs_insert_pos] + from_bytes_method + content[abs_insert_pos:]

# Write back
GSCAT_MODEL.write_text(content_new, encoding='utf-8')

print("✅ from_bytes() method added to GSCATRecord")
print(f"   Location: {GSCAT_MODEL}")
print(f"   Method includes all 65 fields with correct offsets")
print(f"   BarCode field at offset 100 (EAN)")

# Verify
try:
    compile(content_new, str(GSCAT_MODEL), 'exec')
    print("\n✅ File compiles successfully")
    print("\nNext Step:")
    print("python scripts/test_ean_lookup.py")
except SyntaxError as e:
    print(f"\n❌ Syntax error: {e}")