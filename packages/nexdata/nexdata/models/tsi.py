r"""
TSI Table Model
Dodacie listy - Items (položky dokladov)

Table: TSIA-001.BTR (actual year, book 001)
Location: C:\NEX\YEARACT\STORES\TSIA-001.BTR
Definition: tsi.bdf
Record Size: ~200+ bytes (based on BDF analysis)
Encoding: Kamenický (KEYBCS2)

TSI.bdf field structure (verified offsets):
Offset  Size  Type      Field
0       13    Str12     DocNum (1 length + 12 data)
13      2     word      ItmNum (line number)
15      2     word      MgCode (measure unit code)
17      4     longint   GsCode (PLU)
21      31    Str30     GsName (1 length + 30 data)
52      16    Str15     BarCode
68      16    Str15     StkCode
84      31    Str30     Notice
115     4     longint   PackGs
119     2     Str1      GsType
121     2     word      StkNum (warehouse)
123     11    Str10     MsName (unit name)
134     8     double    GsQnt (quantity) ← IMPORTANT
142     8     double    VatPrc (VAT rate %)
150     8     double    DscPrc (discount %)
158     8     double    AcSPrice (unit price) ← IMPORTANT
"""

import struct
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from ..utils.encoding import decode_keybcs2

# Control characters to strip from string fields (0x00-0x1F)
_CONTROL_CHARS = "".join(chr(i) for i in range(32))


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

    # Minimum record size based on BDF (need at least up to AcSPrice at offset 158 + 8 bytes)
    MIN_RECORD_SIZE = 166  # Up to and including AcSPrice field

    @staticmethod
    def _read_fixed_pascal_string(data: bytes, offset: int, buffer_size: int) -> tuple[str, int]:
        """
        Read fixed-width buffer with length prefix (hybrid format).

        NEX Genesis hybrid format:
        - [1-byte length prefix][fixed-width buffer]
        - Length prefix indicates "active" part, but full text is in buffer
        - We read the entire buffer and strip control chars

        Args:
            data: Raw bytes
            offset: Starting offset (at length prefix byte)
            buffer_size: Total buffer size INCLUDING length prefix byte

        Returns:
            Tuple of (string_value, new_offset after buffer)
        """
        if offset + buffer_size > len(data):
            return "", offset + buffer_size

        # Skip the length prefix byte, read the rest of the buffer
        raw = data[offset + 1 : offset + buffer_size]

        try:
            value = decode_keybcs2(raw)
            # Strip control chars (0x00-0x1F) from BOTH sides
            value = value.strip(_CONTROL_CHARS).strip()
        except Exception:
            value = ""

        return value, offset + buffer_size

    @classmethod
    def from_bytes(cls, data: bytes) -> "TSIRecord":
        """
        Deserialize TSI record from bytes (Kamenický encoding)

        Uses HARDCODED OFFSETS from TSI.bdf specification:
        Offset  Size  Type      Field
        0       13    Str12     DocNum
        13      2     word      ItmNum
        15      2     word      MgCode
        17      4     longint   GsCode
        21      31    Str30     GsName
        52      16    Str15     BarCode
        68      16    Str15     StkCode
        84      31    Str30     Notice
        115     4     longint   PackGs
        119     2     Str1      GsType
        121     2     word      StkNum
        123     11    Str10     MsName (unit)
        134     8     double    GsQnt (quantity)
        142     8     double    VatPrc (VAT %)
        150     8     double    DscPrc (discount %)
        158     8     double    AcSPrice (unit price)

        Args:
            data: Raw bytes from Btrieve (Kamenický/KEYBCS2 encoding)

        Returns:
            TSIRecord instance
        """
        if len(data) < cls.MIN_RECORD_SIZE:
            raise ValueError(f"Invalid record size: {len(data)} bytes (expected >= {cls.MIN_RECORD_SIZE})")

        # === HARDCODED OFFSETS from TSI.bdf ===

        # Offset 0: DocNum (Str12 - 13 bytes)
        doc_number, _ = cls._read_fixed_pascal_string(data, 0, 13)

        # Offset 13: ItmNum (word - 2 bytes)
        line_number = struct.unpack("<H", data[13:15])[0]

        # Offset 17: GsCode (longint - 4 bytes)
        gs_code = struct.unpack("<i", data[17:21])[0]

        # Offset 21: GsName (Str30 - 31 bytes)
        gs_name, _ = cls._read_fixed_pascal_string(data, 21, 31)

        # Offset 52: BarCode (Str15 - 16 bytes)
        bar_code, _ = cls._read_fixed_pascal_string(data, 52, 16)

        # Offset 84: Notice (Str30 - 31 bytes) - použijeme ako note
        note, _ = cls._read_fixed_pascal_string(data, 84, 31)

        # Offset 121: StkNum (word - 2 bytes) - warehouse code
        warehouse_code = struct.unpack("<H", data[121:123])[0]

        # Offset 123: MsName (Str10 - 11 bytes) - unit name
        unit, _ = cls._read_fixed_pascal_string(data, 123, 11)
        if not unit:
            unit = "ks"

        # Offset 134: GsQnt (double - 8 bytes) - QUANTITY
        quantity = Decimal("0")
        try:
            qty_val = struct.unpack("<d", data[134:142])[0]
            if 0 <= qty_val < 1_000_000:  # Sanity check
                quantity = Decimal(str(round(qty_val, 3)))
        except (struct.error, ValueError):
            pass

        # Offset 142: VatPrc (double - 8 bytes) - VAT rate
        vat_rate = Decimal("20.0")
        try:
            vat_val = struct.unpack("<d", data[142:150])[0]
            if 0 <= vat_val <= 100:  # Sanity check
                vat_rate = Decimal(str(round(vat_val, 1)))
        except (struct.error, ValueError):
            pass

        # Offset 150: DscPrc (double - 8 bytes) - discount %
        discount_percent = Decimal("0.0")
        try:
            dsc_val = struct.unpack("<d", data[150:158])[0]
            if 0 <= dsc_val <= 100:  # Sanity check
                discount_percent = Decimal(str(round(dsc_val, 2)))
        except (struct.error, ValueError):
            pass

        # Offset 158: AcSPrice (double - 8 bytes) - UNIT PRICE
        price_unit = Decimal("0.00")
        try:
            price_val = struct.unpack("<d", data[158:166])[0]
            if 0 <= price_val < 10_000_000:  # Sanity check
                price_unit = Decimal(str(round(price_val, 2)))
        except (struct.error, ValueError):
            pass

        # Calculate line totals
        if quantity > 0 and price_unit > 0:
            # Apply discount
            subtotal = quantity * price_unit
            discount_amount = subtotal * (discount_percent / Decimal("100"))
            line_base = subtotal - discount_amount
            line_vat = line_base * (vat_rate / Decimal("100"))
            line_total = line_base + line_vat
        else:
            line_base = Decimal("0.00")
            line_vat = Decimal("0.00")
            line_total = Decimal("0.00")

        return cls(
            doc_number=doc_number,
            line_number=line_number,
            gs_code=gs_code,
            gs_name=gs_name,
            bar_code=bar_code,
            quantity=quantity,
            unit=unit,
            unit_coef=Decimal("1.0"),
            price_unit=price_unit,
            price_unit_vat=price_unit * (1 + vat_rate / Decimal("100")),
            vat_rate=vat_rate,
            discount_percent=discount_percent,
            line_base=round(line_base, 2),
            line_vat=round(line_vat, 2),
            line_total=round(line_total, 2),
            warehouse_code=warehouse_code if warehouse_code > 0 else 1,
            batch_number="",
            serial_number="",
            note=note,
            supplier_item_code="",
            status=1,
            mod_user="",
            mod_date=None,
            mod_time=None,
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
