r"""
MGLST Table Model
Tovarové skupiny (hierarchická kategorizácia produktov)

Table: MGLST.BTR
Location: C:\NEX\YEARACT\STORES\MGLST.BTR
Definition: mglst.bdf
Record Size: ~200 bytes
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import struct


@dataclass
class MGLSTRecord:
    """
    MGLST record structure - Tovarové skupiny

    Hierarchická štruktúra kategórií produktov.
    Podporuje multi-level kategorizáciu (napr. Elektronika > Počítače > Notebooky).
    """

    # Primary key
    mglst_code: int  # Kód tovarovej skupiny - primary key

    # Basic info
    mglst_name: str = ""  # Názov tovarovej skupiny
    short_name: str = ""  # Krátky názov

    # Hierarchy
    parent_code: int = 0  # Kód nadradenej skupiny (0 = root level)
    level: int = 1  # Úroveň v hierarchii (1 = top level)

    # Display
    sort_order: int = 0  # Poradie zobrazovania
    color_code: str = ""  # Farebné označenie (hex color)

    # Business rules
    default_vat_rate: float = 20.0  # Predvolená DPH sadzba pre produkty v skupine
    default_unit: str = "ks"  # Predvolená merná jednotka

    # Status
    active: bool = True  # Aktívna skupina
    show_in_catalog: bool = True  # Zobrazovať v katalógu

    # Notes
    note: str = ""  # Poznámka
    description: str = ""  # Popis skupiny

    # Audit fields
    mod_user: str = ""  # Užívateľ poslednej zmeny
    mod_date: Optional[datetime] = None  # Dátum poslednej zmeny
    mod_time: Optional[datetime] = None  # Čas poslednej zmeny

    # Indexes (constants)
    INDEX_MGLSTCODE = 'MglstCode'  # Primary index
    INDEX_NAME = 'MglstName'  # Index podľa názvu
    INDEX_PARENT = 'ParentCode'  # Index podľa nadriadenej skupiny
    INDEX_SORT = 'SortOrder'  # Index pre zoradenie

    @classmethod
    def from_bytes(cls, data: bytes, encoding: str = 'cp852') -> 'MGLSTRecord':
        """
        Deserialize MGLST record from bytes

        Field Layout (approximate, ~200 bytes):
        - MglstCode: 4 bytes (0-3) - longint
        - MglstName: 80 bytes (4-83) - string
        - ShortName: 30 bytes (84-113) - string
        - ParentCode: 4 bytes (114-117) - longint
        - Level: 4 bytes (118-121) - longint
        - SortOrder: 4 bytes (122-125) - longint
        - ColorCode: 10 bytes (126-135) - string
        - DefaultVatRate: 8 bytes (136-143) - double
        - DefaultUnit: 10 bytes (144-153) - string
        - Active: 1 byte (154) - boolean
        - ShowInCatalog: 1 byte (155) - boolean
        - Note: 100 bytes (156-255) - string
        - Description: 200 bytes (256-455) - string (may be shorter)
        - ModUser: 8 bytes - string
        - ModDate: 4 bytes - longint
        - ModTime: 4 bytes - longint

        Args:
            data: Raw bytes from Btrieve
            encoding: String encoding (cp852 for Czech/Slovak)

        Returns:
            MGLSTRecord instance
        """
        if len(data) < 200:
            raise ValueError(f"Invalid record size: {len(data)} bytes (expected >= 200)")

        # Primary key
        mglst_code = struct.unpack('<i', data[0:4])[0]

        # Basic info
        mglst_name = data[4:84].decode(encoding, errors='ignore').rstrip('\x00 ')
        short_name = data[84:114].decode(encoding, errors='ignore').rstrip('\x00 ')

        # Hierarchy
        parent_code = struct.unpack('<i', data[114:118])[0]
        level = struct.unpack('<i', data[118:122])[0]

        # Display
        sort_order = struct.unpack('<i', data[122:126])[0]
        color_code = data[126:136].decode(encoding, errors='ignore').rstrip('\x00 ')

        # Business rules
        default_vat_rate = struct.unpack('<d', data[136:144])[0]
        default_unit = data[144:154].decode(encoding, errors='ignore').rstrip('\x00 ')

        # Status
        active = bool(data[154])
        show_in_catalog = bool(data[155])

        # Notes (flexible based on actual record size)
        note = ""
        description = ""
        mod_user = ""
        mod_date = None
        mod_time = None

        if len(data) >= 256:
            note = data[156:256].decode(encoding, errors='ignore').rstrip('\x00 ')

        if len(data) >= 456:
            description = data[256:456].decode(encoding, errors='ignore').rstrip('\x00 ')

        # Try to extract audit fields if present
        if len(data) >= 472:
            mod_user = data[456:464].decode(encoding, errors='ignore').rstrip('\x00 ')
            mod_date_int = struct.unpack('<i', data[464:468])[0]
            mod_date = cls._decode_delphi_date(mod_date_int) if mod_date_int > 0 else None
            mod_time_int = struct.unpack('<i', data[468:472])[0]
            mod_time = cls._decode_delphi_time(mod_time_int) if mod_time_int >= 0 else None

        return cls(
            mglst_code=mglst_code,
            mglst_name=mglst_name,
            short_name=short_name,
            parent_code=parent_code,
            level=level,
            sort_order=sort_order,
            color_code=color_code,
            default_vat_rate=default_vat_rate,
            default_unit=default_unit,
            active=active,
            show_in_catalog=show_in_catalog,
            note=note,
            description=description,
            mod_user=mod_user,
            mod_date=mod_date,
            mod_time=mod_time
        )

    @staticmethod
    def _decode_delphi_date(days: int) -> datetime:
        """Convert Delphi date to Python datetime"""
        from datetime import timedelta
        base_date = datetime(1899, 12, 30)
        return base_date + timedelta(days=days)

    @staticmethod
    def _decode_delphi_time(milliseconds: int) -> datetime:
        """Convert Delphi time to Python datetime"""
        from datetime import timedelta
        base = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        return base + timedelta(milliseconds=milliseconds)

    def validate(self) -> list[str]:
        """Validate record"""
        errors = []

        if self.mglst_code <= 0:
            errors.append("MglstCode must be positive")
        if not self.mglst_name.strip():
            errors.append("MglstName cannot be empty")
        if self.level < 1:
            errors.append("Level must be >= 1")
        if self.parent_code < 0:
            errors.append("ParentCode cannot be negative")
        if self.default_vat_rate < 0 or self.default_vat_rate > 100:
            errors.append(f"Invalid VAT rate: {self.default_vat_rate}%")

        return errors

    def is_root(self) -> bool:
        """Check if this is a root-level category"""
        return self.parent_code == 0

    def is_child_of(self, parent_code: int) -> bool:
        """Check if this category is a child of specified parent"""
        return self.parent_code == parent_code

    def get_path(self, all_categories: list['MGLSTRecord']) -> list['MGLSTRecord']:
        """
        Get full path from root to this category

        Args:
            all_categories: List of all categories

        Returns:
            List of categories from root to this one
        """
        path = [self]
        current = self

        while not current.is_root():
            parent = next((c for c in all_categories if c.mglst_code == current.parent_code), None)
            if parent:
                path.insert(0, parent)
                current = parent
            else:
                break  # Parent not found, stop

        return path

    def get_full_path_name(self, all_categories: list['MGLSTRecord'], separator: str = " > ") -> str:
        """
        Get full category path as string (e.g., "Elektronika > Počítače > Notebooky")

        Args:
            all_categories: List of all categories
            separator: Path separator

        Returns:
            Full path string
        """
        path = self.get_path(all_categories)
        return separator.join([c.mglst_name for c in path])

    def __str__(self) -> str:
        return f"MGLST({self.mglst_code}: {self.mglst_name})"