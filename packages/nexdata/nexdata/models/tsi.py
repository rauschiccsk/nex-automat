r"""
TSI Table Model
Dodacie listy - Items (položky dokladov)

Table: TSIA-001.BTR (actual year, book 001)
Location: C:\NEX\YEARACT\STORES\TSIA-001.BTR
Definition: tsi.bdf
Record Size: ~400 bytes
"""

import struct
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class TSIRecord:
    """
    TSI record structure - Dodacie listy Items

    Obsahuje jednotlivé položky dodacieho listu.
    Viaceré TSI záznamy patria k jednému TSH záznamu (rovnaký DocNumber).
    """

    # Composite primary key
    doc_number: str  # Číslo dokladu (foreign key to TSH)
    line_number: int  # Poradové číslo položky

    # Product
    gs_code: int = 0  # Kód produktu (foreign key to GSCAT)
    gs_name: str = ""  # Názov produktu (cache)
    bar_code: str = ""  # Čiarový kód (ak bol použitý)

    # Quantity
    quantity: Decimal = Decimal("1.0")  # Množstvo
    unit: str = "ks"  # Merná jednotka
    unit_coef: Decimal = Decimal("1.0")  # Koeficient prepočtu

    # Pricing (per unit)
    price_unit: Decimal = Decimal("0.00")  # Jednotková cena bez DPH
    price_unit_vat: Decimal = Decimal("0.00")  # Jednotková cena s DPH
    vat_rate: Decimal = Decimal("20.0")  # DPH sadzba (%)
    discount_percent: Decimal = Decimal("0.0")  # Zľava v %

    # Line totals
    line_base: Decimal = Decimal("0.00")  # Základ dane (po zľave)
    line_vat: Decimal = Decimal("0.00")  # DPH
    line_total: Decimal = Decimal("0.00")  # Celkom s DPH

    # Stock
    warehouse_code: int = 1  # Kód skladu
    batch_number: str = ""  # Číslo šarže/série
    serial_number: str = ""  # Sériové číslo

    # Additional info
    note: str = ""  # Poznámka k položke

    # Supplier reference
    supplier_item_code: str = ""  # Kód produktu u dodávateľa

    # Status
    status: int = 1  # Stav položky (1=active, 2=cancelled)

    # Audit fields
    mod_user: str = ""  # Užívateľ poslednej zmeny
    mod_date: datetime | None = None  # Dátum poslednej zmeny
    mod_time: datetime | None = None  # Čas poslednej zmeny

    # Indexes (constants)
    INDEX_DOCLINE = "DocNumber,LineNumber"  # Composite primary index
    INDEX_GSCODE = "GsCode"  # Index podľa produktu
    INDEX_BARCODE = "BarCode"  # Index podľa čiarového kódu

    @classmethod
    def from_bytes(cls, data: bytes, encoding: str = "cp852") -> "TSIRecord":
        """
        Deserialize TSI record from bytes

        Field Layout (approximate, ~400 bytes):
        - DocNumber: 20 bytes (0-19) - string
        - LineNumber: 4 bytes (20-23) - longint
        - GsCode: 4 bytes (24-27) - longint
        - GsName: 80 bytes (28-107) - string
        - BarCode: 15 bytes (108-122) - string
        - Quantity: 8 bytes (123-130) - double
        - Unit: 10 bytes (131-140) - string
        - UnitCoef: 8 bytes (141-148) - double
        - PriceUnit: 8 bytes (149-156) - double
        - PriceUnitVat: 8 bytes (157-164) - double
        - VatRate: 8 bytes (165-172) - double
        - DiscountPercent: 8 bytes (173-180) - double
        - LineBase: 8 bytes (181-188) - double
        - LineVat: 8 bytes (189-196) - double
        - LineTotal: 8 bytes (197-204) - double
        - WarehouseCode: 4 bytes (205-208) - longint
        - BatchNumber: 30 bytes (209-238) - string
        - SerialNumber: 30 bytes (239-268) - string
        - Note: 100 bytes (269-368) - string
        - SupplierItemCode: 30 bytes (369-398) - string
        - Status: 4 bytes (399-402) - longint
        - ModUser: 8 bytes (403-410) - string
        - ModDate: 4 bytes (411-414) - longint
        - ModTime: 4 bytes (415-418) - longint

        Args:
            data: Raw bytes from Btrieve
            encoding: String encoding

        Returns:
            TSIRecord instance
        """
        if len(data) < 400:
            raise ValueError(f"Invalid record size: {len(data)} bytes (expected >= 400)")

        # Primary key
        doc_number = data[0:20].decode(encoding, errors="ignore").rstrip("\x00 ")
        line_number = struct.unpack("<i", data[20:24])[0]

        # Product
        gs_code = struct.unpack("<i", data[24:28])[0]
        gs_name = data[28:108].decode(encoding, errors="ignore").rstrip("\x00 ")
        bar_code = data[108:123].decode(encoding, errors="ignore").rstrip("\x00 ")

        # Quantity
        quantity = Decimal(str(round(struct.unpack("<d", data[123:131])[0], 3)))
        unit = data[131:141].decode(encoding, errors="ignore").rstrip("\x00 ")
        unit_coef = Decimal(str(struct.unpack("<d", data[141:149])[0]))

        # Pricing
        price_unit = Decimal(str(round(struct.unpack("<d", data[149:157])[0], 2)))
        price_unit_vat = Decimal(str(round(struct.unpack("<d", data[157:165])[0], 2)))
        vat_rate = Decimal(str(round(struct.unpack("<d", data[165:173])[0], 1)))
        discount_percent = Decimal(str(round(struct.unpack("<d", data[173:181])[0], 2)))

        # Line totals
        line_base = Decimal(str(round(struct.unpack("<d", data[181:189])[0], 2)))
        line_vat = Decimal(str(round(struct.unpack("<d", data[189:197])[0], 2)))
        line_total = Decimal(str(round(struct.unpack("<d", data[197:205])[0], 2)))

        # Stock
        warehouse_code = struct.unpack("<i", data[205:209])[0]
        batch_number = data[209:239].decode(encoding, errors="ignore").rstrip("\x00 ")
        serial_number = data[239:269].decode(encoding, errors="ignore").rstrip("\x00 ")

        # Additional
        note = data[269:369].decode(encoding, errors="ignore").rstrip("\x00 ")
        supplier_item_code = data[369:399].decode(encoding, errors="ignore").rstrip("\x00 ")

        # Status
        status = struct.unpack("<i", data[399:403])[0]

        # Audit
        mod_user = ""
        mod_date = None
        mod_time = None
        if len(data) >= 419:
            mod_user = data[403:411].decode(encoding, errors="ignore").rstrip("\x00 ")
            mod_date_int = struct.unpack("<i", data[411:415])[0]
            mod_date = cls._decode_delphi_date(mod_date_int) if mod_date_int > 0 else None
            mod_time_int = struct.unpack("<i", data[415:419])[0]
            mod_time = cls._decode_delphi_time(mod_time_int) if mod_time_int >= 0 else None

        return cls(
            doc_number=doc_number,
            line_number=line_number,
            gs_code=gs_code,
            gs_name=gs_name,
            bar_code=bar_code,
            quantity=quantity,
            unit=unit,
            unit_coef=unit_coef,
            price_unit=price_unit,
            price_unit_vat=price_unit_vat,
            vat_rate=vat_rate,
            discount_percent=discount_percent,
            line_base=line_base,
            line_vat=line_vat,
            line_total=line_total,
            warehouse_code=warehouse_code,
            batch_number=batch_number,
            serial_number=serial_number,
            note=note,
            supplier_item_code=supplier_item_code,
            status=status,
            mod_user=mod_user,
            mod_date=mod_date,
            mod_time=mod_time,
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

    def calculate_line_totals(self) -> None:
        """
        Calculate line totals based on quantity, price, discount, and VAT
        Updates line_base, line_vat, and line_total
        """
        # Calculate base after discount
        subtotal = self.quantity * self.price_unit
        discount_amount = subtotal * (self.discount_percent / Decimal("100"))
        self.line_base = subtotal - discount_amount

        # Calculate VAT
        self.line_vat = self.line_base * (self.vat_rate / Decimal("100"))

        # Calculate total
        self.line_total = self.line_base + self.line_vat

        # Round to 2 decimals
        self.line_base = round(self.line_base, 2)
        self.line_vat = round(self.line_vat, 2)
        self.line_total = round(self.line_total, 2)

    def validate(self) -> list[str]:
        """Validate record"""
        errors = []

        if not self.doc_number.strip():
            errors.append("DocNumber cannot be empty")
        if self.line_number <= 0:
            errors.append("LineNumber must be positive")
        if self.gs_code <= 0:
            errors.append("GsCode must be positive")
        if self.quantity <= 0:
            errors.append("Quantity must be positive")
        if self.price_unit < 0:
            errors.append("PriceUnit cannot be negative")
        if self.discount_percent < 0 or self.discount_percent > 100:
            errors.append(f"Invalid discount: {self.discount_percent}%")

        # Check calculation
        expected_total = self.line_base + self.line_vat
        if abs(expected_total - self.line_total) > Decimal("0.01"):
            errors.append(f"Invalid line total: {self.line_total} != {expected_total}")

        return errors

    def __str__(self) -> str:
        return f"TSI({self.doc_number}/{self.line_number}: {self.gs_name}, {self.quantity} {self.unit})"
