r"""
GSCAT Table Model
Produktový katalóg (master produktová tabuľka)

Table: GSCAT.BTR
Location: C:\NEX\YEARACT\STORES\GSCAT.BTR
Definition: gscat.bdf
Record Size: 705 bytes
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from decimal import Decimal
import struct


@dataclass
class GSCATRecord:
    """
    GSCAT record structure - Produktový katalóg

    Master tabuľka pre všetky produkty v systéme.
    """

    # Primary key
    gs_code: int  # Tovarové číslo (PLU) - primary key

    # Basic product info
    gs_name: str = ""  # Názov produktu (hlavný)
    gs_name2: str = ""  # Názov produktu (alternatívny/cudzojazyčný)
    gs_short_name: str = ""  # Krátky názov

    # Classification
    mglst_code: int = 0  # Kód tovarovej skupiny (foreign key to MGLST)

    # Measurement units
    unit: str = ""  # Merná jednotka (ks, kg, m, l, etc.)
    unit_coef: Decimal = Decimal("1.0")  # Koeficient prepočtu jednotiek

    # Pricing
    price_buy: Decimal = Decimal("0.00")  # Nákupná cena
    price_sell: Decimal = Decimal("0.00")  # Predajná cena
    vat_rate: Decimal = Decimal("20.0")  # DPH sadzba (%)

    # Stock management
    stock_min: Decimal = Decimal("0.0")  # Minimálny stav
    stock_max: Decimal = Decimal("0.0")  # Maximálny stav
    stock_current: Decimal = Decimal("0.0")  # Aktuálny stav

    # Status flags
    active: bool = True  # Aktívny produkt
    discontinued: bool = False  # Produkt je vyradený

    # Supplier info
    supplier_code: int = 0  # Kód hlavného dodávateľa (PAB)
    supplier_item_code: str = ""  # Kód produktu u dodávateľa

    # Additional info
    note: str = ""  # Poznámka
    note2: str = ""  # Poznámka 2

    # Audit fields
    mod_user: str = ""  # Užívateľ poslednej zmeny
    mod_date: Optional[datetime] = None  # Dátum poslednej zmeny
    mod_time: Optional[datetime] = None  # Čas poslednej zmeny
    created_date: Optional[datetime] = None  # Dátum vytvorenia
    created_user: str = ""  # Užívateľ, ktorý vytvoril

    # Indexes (constants)
    INDEX_GSCODE = 'GsCode'  # Primary index
    INDEX_NAME = 'GsName'  # Index podľa názvu
    INDEX_MGLST = 'MglstCode'  # Index podľa tovarovej skupiny
    INDEX_SUPPLIER = 'SupplierCode'  # Index podľa dodávateľa

    @classmethod
    def from_bytes(cls, data: bytes, encoding: str = 'cp852') -> 'GSCATRecord':
        """
        Deserialize GSCAT record from bytes

        Field Layout (approximate, based on 705 bytes record):
        - GsCode: 4 bytes (0-3) - longint
        - GsName: 80 bytes (4-83) - string
        - GsName2: 80 bytes (84-163) - string
        - GsShortName: 30 bytes (164-193) - string
        - MglstCode: 4 bytes (194-197) - longint
        - Unit: 10 bytes (198-207) - string
        - UnitCoef: 8 bytes (208-215) - double
        - PriceBuy: 8 bytes (216-223) - double
        - PriceSell: 8 bytes (224-231) - double
        - VatRate: 8 bytes (232-239) - double
        - StockMin: 8 bytes (240-247) - double
        - StockMax: 8 bytes (248-255) - double
        - StockCurrent: 8 bytes (256-263) - double
        - Active: 1 byte (264) - boolean
        - Discontinued: 1 byte (265) - boolean
        - SupplierCode: 4 bytes (266-269) - longint
        - SupplierItemCode: 30 bytes (270-299) - string
        - Note: 200 bytes (300-499) - string
        - Note2: 100 bytes (500-599) - string
        - ModUser: 8 bytes (600-607) - string
        - ModDate: 4 bytes (608-611) - longint
        - ModTime: 4 bytes (612-615) - longint
        - CreatedDate: 4 bytes (616-619) - longint
        - CreatedUser: 8 bytes (620-627) - string
        - Reserved: ~78 bytes (628-705) - padding/reserved

        Args:
            data: Raw bytes from Btrieve
            encoding: String encoding (cp852 for Czech/Slovak)

        Returns:
            GSCATRecord instance
        """
        if len(data) < 705:
            raise ValueError(f"Invalid record size: {len(data)} bytes (expected 705)")

        # Primary key
        gs_code = struct.unpack('<i', data[0:4])[0]

        # Product names
        gs_name = data[4:84].decode(encoding, errors='ignore').rstrip('\x00 ')
        gs_name2 = data[84:164].decode(encoding, errors='ignore').rstrip('\x00 ')
        gs_short_name = data[164:194].decode(encoding, errors='ignore').rstrip('\x00 ')

        # Classification
        mglst_code = struct.unpack('<i', data[194:198])[0]

        # Unit
        unit = data[198:208].decode(encoding, errors='ignore').rstrip('\x00 ')
        unit_coef = Decimal(str(struct.unpack('<d', data[208:216])[0]))

        # Pricing
        price_buy = Decimal(str(round(struct.unpack('<d', data[216:224])[0], 2)))
        price_sell = Decimal(str(round(struct.unpack('<d', data[224:232])[0], 2)))
        vat_rate = Decimal(str(round(struct.unpack('<d', data[232:240])[0], 1)))

        # Stock
        stock_min = Decimal(str(round(struct.unpack('<d', data[240:248])[0], 2)))
        stock_max = Decimal(str(round(struct.unpack('<d', data[248:256])[0], 2)))
        stock_current = Decimal(str(round(struct.unpack('<d', data[256:264])[0], 2)))

        # Status
        active = bool(data[264])
        discontinued = bool(data[265])

        # Supplier
        supplier_code = struct.unpack('<i', data[266:270])[0]
        supplier_item_code = data[270:300].decode(encoding, errors='ignore').rstrip('\x00 ')

        # Notes
        note = data[300:500].decode(encoding, errors='ignore').rstrip('\x00 ')
        note2 = data[500:600].decode(encoding, errors='ignore').rstrip('\x00 ')

        # Audit
        mod_user = data[600:608].decode(encoding, errors='ignore').rstrip('\x00 ')
        mod_date_int = struct.unpack('<i', data[608:612])[0]
        mod_date = cls._decode_delphi_date(mod_date_int) if mod_date_int > 0 else None
        mod_time_int = struct.unpack('<i', data[612:616])[0]
        mod_time = cls._decode_delphi_time(mod_time_int) if mod_time_int >= 0 else None
        created_date_int = struct.unpack('<i', data[616:620])[0]
        created_date = cls._decode_delphi_date(created_date_int) if created_date_int > 0 else None
        created_user = data[620:628].decode(encoding, errors='ignore').rstrip('\x00 ')

        return cls(
            gs_code=gs_code,
            gs_name=gs_name,
            gs_name2=gs_name2,
            gs_short_name=gs_short_name,
            mglst_code=mglst_code,
            unit=unit,
            unit_coef=unit_coef,
            price_buy=price_buy,
            price_sell=price_sell,
            vat_rate=vat_rate,
            stock_min=stock_min,
            stock_max=stock_max,
            stock_current=stock_current,
            active=active,
            discontinued=discontinued,
            supplier_code=supplier_code,
            supplier_item_code=supplier_item_code,
            note=note,
            note2=note2,
            mod_user=mod_user,
            mod_date=mod_date,
            mod_time=mod_time,
            created_date=created_date,
            created_user=created_user
        )

    def to_bytes(self, encoding: str = 'cp852') -> bytes:
        """
        Serialize record to bytes for Btrieve

        Args:
            encoding: String encoding

        Returns:
            Raw bytes (705 bytes)
        """
        result = bytearray(705)

        # Primary key
        struct.pack_into('<i', result, 0, self.gs_code)

        # Names
        result[4:4 + len(self.gs_name.encode(encoding)[:80])] = self.gs_name.encode(encoding)[:80]
        result[84:84 + len(self.gs_name2.encode(encoding)[:80])] = self.gs_name2.encode(encoding)[:80]
        result[164:164 + len(self.gs_short_name.encode(encoding)[:30])] = self.gs_short_name.encode(encoding)[:30]

        # Classification
        struct.pack_into('<i', result, 194, self.mglst_code)

        # Unit
        result[198:198 + len(self.unit.encode(encoding)[:10])] = self.unit.encode(encoding)[:10]
        struct.pack_into('<d', result, 208, float(self.unit_coef))

        # Pricing
        struct.pack_into('<d', result, 216, float(self.price_buy))
        struct.pack_into('<d', result, 224, float(self.price_sell))
        struct.pack_into('<d', result, 232, float(self.vat_rate))

        # Stock
        struct.pack_into('<d', result, 240, float(self.stock_min))
        struct.pack_into('<d', result, 248, float(self.stock_max))
        struct.pack_into('<d', result, 256, float(self.stock_current))

        # Status
        result[264] = 1 if self.active else 0
        result[265] = 1 if self.discontinued else 0

        # Supplier
        struct.pack_into('<i', result, 266, self.supplier_code)
        result[270:270 + len(self.supplier_item_code.encode(encoding)[:30])] = self.supplier_item_code.encode(encoding)[
            :30]

        # Notes
        result[300:300 + len(self.note.encode(encoding)[:200])] = self.note.encode(encoding)[:200]
        result[500:500 + len(self.note2.encode(encoding)[:100])] = self.note2.encode(encoding)[:100]

        # Audit
        result[600:600 + len(self.mod_user.encode(encoding)[:8])] = self.mod_user.encode(encoding)[:8]
        if self.mod_date:
            struct.pack_into('<i', result, 608, self._encode_delphi_date(self.mod_date))
        if self.mod_time:
            struct.pack_into('<i', result, 612, self._encode_delphi_time(self.mod_time))
        if self.created_date:
            struct.pack_into('<i', result, 616, self._encode_delphi_date(self.created_date))
        result[620:620 + len(self.created_user.encode(encoding)[:8])] = self.created_user.encode(encoding)[:8]

        return bytes(result)

    @staticmethod
    def _decode_delphi_date(days: int) -> datetime:
        """Convert Delphi date to Python datetime"""
        from datetime import timedelta
        base_date = datetime(1899, 12, 30)
        return base_date + timedelta(days=days)

    @staticmethod
    def _encode_delphi_date(dt: datetime) -> int:
        """Convert Python datetime to Delphi date"""
        base_date = datetime(1899, 12, 30)
        return (dt - base_date).days

    @staticmethod
    def _decode_delphi_time(milliseconds: int) -> datetime:
        """Convert Delphi time to Python datetime"""
        from datetime import timedelta
        base = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        return base + timedelta(milliseconds=milliseconds)

    @staticmethod
    def _encode_delphi_time(dt: datetime) -> int:
        """Convert Python datetime to Delphi time"""
        midnight = dt.replace(hour=0, minute=0, second=0, microsecond=0)
        return int((dt - midnight).total_seconds() * 1000)

    def validate(self) -> list[str]:
        """Validate record"""
        errors = []

        if self.gs_code <= 0:
            errors.append("GsCode must be positive")
        if not self.gs_name.strip():
            errors.append("GsName cannot be empty")
        if len(self.gs_name) > 80:
            errors.append(f"GsName too long: {len(self.gs_name)} (max 80)")
        if self.price_sell < 0:
            errors.append("Price must be non-negative")
        if self.vat_rate < 0 or self.vat_rate > 100:
            errors.append(f"Invalid VAT rate: {self.vat_rate}% (0-100)")

        return errors

    def __str__(self) -> str:
        return f"GSCAT({self.gs_code}: {self.gs_name})"