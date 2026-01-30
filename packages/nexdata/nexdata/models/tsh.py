r"""
TSH Table Model
Dodacie listy - Header (hlavičky dokladov)

Table: TSHA-001.BTR (actual year, book 001)
Location: C:\NEX\YEARACT\STORES\TSHA-001.BTR
Definition: tsh.bdf
Record Size: variable (Pascal ShortString format)

NEX Genesis uses Pascal ShortString format:
- [1-byte length][N-bytes data]
"""

import struct
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal


@dataclass
class TSHRecord:
    """
    TSH record structure - Dodacie listy Header

    Obsahuje hlavičku dodacieho listu (zákazník, dátumy, sumy).
    Položky sú v TSI tabuľke (TSI records s rovnakým DocNumber).

    Uses Pascal ShortString format for string fields:
    - First byte contains length
    - Followed by actual string data
    """

    # Primary key
    doc_number: str  # Číslo dokladu (napr. "DD2600100001") - primary key

    # Document info
    doc_type: int = 1  # Typ dokladu (1=príjem, 2=výdaj, 3=transfer)
    doc_date: date | None = None  # Dátum vystavenia
    delivery_date: date | None = None  # Dátum dodania
    due_date: date | None = None  # Dátum splatnosti

    # Reference
    reference: str = ""  # Referenčné číslo (napr. "2026000183")

    # Partner
    pab_code: int = 0  # Kód partnera (foreign key to PAB)
    pab_name: str = ""  # Názov partnera (cache)
    pab_ico: str = ""  # IČO partnera (cache)
    pab_dic: str = ""  # DIČ partnera (cache)
    pab_ic_dph: str = ""  # IČ DPH partnera (cache)
    pab_address: str = ""  # Adresa partnera (cache)
    pab_city: str = ""  # Mesto partnera
    pab_zip: str = ""  # PSČ partnera

    # Payment
    payment_name: str = ""  # Názov spôsobu platby (napr. "Hotovosť")
    payment_method: int = 1  # Spôsob platby (1=hotovosť, 2=prevodom, 3=karta)
    payment_terms: int = 14  # Platobné podmienky (dni)
    paid: bool = False  # Zaplatené
    paid_date: date | None = None  # Dátum platby
    paid_amount: Decimal = Decimal("0.00")  # Zaplatená suma

    # Financial
    currency: str = "EUR"  # Mena (EUR, USD, CZK, etc.)
    exchange_rate: Decimal = Decimal("1.0")  # Výmenný kurz

    # Amounts (in document currency)
    amount_base: Decimal = Decimal("0.00")  # Základ dane
    amount_vat: Decimal = Decimal("0.00")  # DPH
    amount_total: Decimal = Decimal("0.00")  # Celkom s DPH

    # VAT breakdown
    vat_20_base: Decimal = Decimal("0.00")  # Základ DPH 20%
    vat_20_amount: Decimal = Decimal("0.00")  # DPH 20%
    vat_10_base: Decimal = Decimal("0.00")  # Základ DPH 10%
    vat_10_amount: Decimal = Decimal("0.00")  # DPH 10%
    vat_0_base: Decimal = Decimal("0.00")  # Základ DPH 0%

    # References
    invoice_number: str = ""  # Číslo faktúry (ak relevantné)
    order_number: str = ""  # Číslo objednávky
    internal_note: str = ""  # Interná poznámka
    public_note: str = ""  # Verejná poznámka (pre zákazníka)

    # Status
    status: int = 1  # Stav (1=draft, 2=confirmed, 3=shipped, 4=cancelled)
    locked: bool = False  # Uzamknutý (nemožno upravovať)
    posted: bool = False  # Zaúčtovaný

    # Warehouse
    warehouse_code: int = 1  # Kód skladu

    # Audit fields
    mod_user: str = ""  # Užívateľ poslednej zmeny
    mod_date: datetime | None = None  # Dátum poslednej zmeny
    mod_time: datetime | None = None  # Čas poslednej zmeny
    created_date: datetime | None = None  # Dátum vytvorenia
    created_user: str = ""  # Užívateľ vytvorenia

    # Raw data for debugging
    _raw_offset: int = 0  # Last parsed offset

    # Indexes (constants)
    INDEX_DOCNUMBER = "DocNumber"  # Primary index
    INDEX_PABCODE = "PabCode"  # Index podľa partnera
    INDEX_DOCDATE = "DocDate"  # Index podľa dátumu
    INDEX_STATUS = "Status"  # Index podľa stavu

    @staticmethod
    def _read_pascal_string(data: bytes, offset: int, encoding: str = "cp852") -> tuple[str, int]:
        """
        Read Pascal ShortString from bytes.

        Pascal ShortString format:
        - First byte: length (0-255)
        - Following bytes: string data

        Args:
            data: Raw bytes
            offset: Starting offset
            encoding: String encoding

        Returns:
            Tuple of (string_value, new_offset)
        """
        if offset >= len(data):
            return "", offset

        length = data[offset]
        if length == 0:
            return "", offset + 1

        end = offset + 1 + length
        if end > len(data):
            # Not enough data, read what we can
            end = len(data)

        try:
            value = data[offset + 1 : end].decode(encoding, errors="replace").rstrip("\x00")
        except Exception:
            value = ""

        return value, offset + 1 + length

    @staticmethod
    def _read_int32(data: bytes, offset: int) -> tuple[int, int]:
        """Read 4-byte little-endian integer."""
        if offset + 4 > len(data):
            return 0, offset + 4
        value = struct.unpack("<i", data[offset : offset + 4])[0]
        return value, offset + 4

    @staticmethod
    def _read_int16(data: bytes, offset: int) -> tuple[int, int]:
        """Read 2-byte little-endian integer."""
        if offset + 2 > len(data):
            return 0, offset + 2
        value = struct.unpack("<h", data[offset : offset + 2])[0]
        return value, offset + 2

    @staticmethod
    def _read_double(data: bytes, offset: int) -> tuple[float, int]:
        """Read 8-byte little-endian double."""
        if offset + 8 > len(data):
            return 0.0, offset + 8
        value = struct.unpack("<d", data[offset : offset + 8])[0]
        return value, offset + 8

    @staticmethod
    def _read_byte(data: bytes, offset: int) -> tuple[int, int]:
        """Read single byte."""
        if offset >= len(data):
            return 0, offset + 1
        return data[offset], offset + 1

    @staticmethod
    def _read_uint16(data: bytes, offset: int) -> tuple[int, int]:
        """Read 2-byte little-endian unsigned integer."""
        if offset + 2 > len(data):
            return 0, offset + 2
        value = struct.unpack("<H", data[offset : offset + 2])[0]
        return value, offset + 2

    @staticmethod
    def _read_uint32(data: bytes, offset: int) -> tuple[int, int]:
        """Read 4-byte little-endian unsigned integer."""
        if offset + 4 > len(data):
            return 0, offset + 4
        value = struct.unpack("<I", data[offset : offset + 4])[0]
        return value, offset + 4

    @staticmethod
    def _read_fixed_pascal_string(
        data: bytes, offset: int, buffer_size: int, encoding: str = "cp852"
    ) -> tuple[str, int]:
        """
        Read fixed-width buffer with length prefix (hybrid format).

        NEX Genesis hybrid format:
        - [1-byte length prefix][fixed-width buffer]
        - Length prefix indicates "active" part, but full text is in buffer
        - We read the entire buffer and strip nulls from BOTH sides

        Args:
            data: Raw bytes
            offset: Starting offset (at length prefix byte)
            buffer_size: Total buffer size INCLUDING length prefix byte
            encoding: String encoding

        Returns:
            Tuple of (string_value, new_offset after buffer)
        """
        if offset + buffer_size > len(data):
            return "", offset + buffer_size

        # Skip the length prefix byte, read the rest of the buffer
        raw = data[offset + 1 : offset + buffer_size]

        try:
            # Strip nulls from BOTH sides (fixes "\x00\x00\x0044298684" -> "44298684")
            value = raw.decode(encoding, errors="replace").strip("\x00").strip()
        except Exception:
            value = ""

        return value, offset + buffer_size

    @staticmethod
    def _decode_delphi_datetime(double_val: float) -> date | None:
        """
        Convert Delphi TDateTime (double) to Python date.

        Delphi TDateTime is a double where:
        - Integer part = days since 1899-12-30
        - Fractional part = time of day

        Args:
            double_val: Delphi TDateTime as double

        Returns:
            Python date or None if invalid
        """
        from datetime import timedelta

        if double_val <= 0:
            return None

        try:
            # Extract just the date part (integer portion)
            days = int(double_val)
            # Delphi epoch is 1899-12-30
            base_date = datetime(1899, 12, 30)
            result = base_date + timedelta(days=days)
            # Validate reasonable date range (1990-2100)
            if 1990 <= result.year <= 2100:
                return result.date()
        except (ValueError, OverflowError):
            pass

        return None

    @classmethod
    def from_bytes(cls, data: bytes, encoding: str = "cp852") -> "TSHRecord":
        """
        Deserialize TSH record from bytes.

        Field sequence (based on hex dump analysis):
        Offset  Size  Type                Field
        0x0000  4     int32               doc_id (internal, skip)
        0x0004  1+12  pascal string       doc_number
        0x0011  1+10  pascal string       reference
        0x001c  2     padding             skip
        0x001e  8     double              doc_date (Delphi TDateTime as double)
        0x0026  30    fixed pascal        pab_name1 (hybrid: length + fixed buffer)
        0x0044  30    fixed pascal        pab_name2
        0x0062  30    fixed pascal        pab_address
        ...     ...   fixed pascal        ICO, DIC, IC_DPH, city, ZIP, etc.
        ...     ...   doubles             amounts at the end

        Hybrid format: [1-byte length][fixed-width buffer]
        - Length prefix indicates "active" part
        - Full text is in the fixed-width buffer

        Args:
            data: Raw bytes from Btrieve
            encoding: String encoding (cp852 for Czech/Slovak)

        Returns:
            TSHRecord instance
        """
        if len(data) < 50:
            raise ValueError(f"Invalid record size: {len(data)} bytes (expected >= 50)")

        offset = 0

        # 0x0000: doc_id (int32) - internal ID, skip
        _doc_id, offset = cls._read_uint32(data, offset)

        # 0x0004: doc_number (pascal string, len=12)
        doc_number, offset = cls._read_pascal_string(data, offset, encoding)

        # 0x0011: reference (pascal string, len=10)
        reference, offset = cls._read_pascal_string(data, offset, encoding)

        # 0x001c: 2 bytes padding
        offset += 2

        # 0x001e: Skip 8 bytes - contains unknown value (not doc_date)
        # doc_date will be extracted from reference or found elsewhere
        offset += 8
        doc_date = None  # TODO: find actual doc_date location

        # 0x0026: pab_name1 (30 bytes - hybrid fixed pascal)
        pab_name, offset = cls._read_fixed_pascal_string(data, offset, 30, encoding)

        # 0x0044: pab_name2 (30 bytes - normalized name)
        pab_name2, offset = cls._read_fixed_pascal_string(data, offset, 30, encoding)
        # Use pab_name2 if pab_name is empty
        if not pab_name and pab_name2:
            pab_name = pab_name2

        # 0x0062: pab_address (30 bytes)
        pab_address, offset = cls._read_fixed_pascal_string(data, offset, 30, encoding)

        # 0x0080: pab_city (20 bytes)
        pab_city, offset = cls._read_fixed_pascal_string(data, offset, 20, encoding)

        # 0x0094: pab_zip (10 bytes)
        pab_zip, offset = cls._read_fixed_pascal_string(data, offset, 10, encoding)

        # 0x009e: pab_ico (15 bytes)
        pab_ico, offset = cls._read_fixed_pascal_string(data, offset, 15, encoding)

        # 0x00ad: pab_dic (15 bytes)
        pab_dic, offset = cls._read_fixed_pascal_string(data, offset, 15, encoding)

        # 0x00bc: pab_ic_dph (15 bytes)
        pab_ic_dph, offset = cls._read_fixed_pascal_string(data, offset, 15, encoding)

        # 0x00cb: payment_name (20 bytes)
        payment_name, offset = cls._read_fixed_pascal_string(data, offset, 20, encoding)

        # Amounts at hardcoded offsets (from hex dump analysis)
        # These are NOT 4-byte aligned, so we use exact offsets
        amount_base = Decimal("0.00")
        amount_vat = Decimal("0.00")
        amount_total = Decimal("0.00")

        # Offset 0x0215: amount_base (8 bytes double)
        # Offset 0x023d: amount_vat (8 bytes double)
        # Offset 0x0245: amount_total (8 bytes double)
        if len(data) >= 0x024D:  # Minimum size for all amounts
            try:
                base_val = struct.unpack("<d", data[0x0215 : 0x0215 + 8])[0]
                vat_val = struct.unpack("<d", data[0x023D : 0x023D + 8])[0]
                total_val = struct.unpack("<d", data[0x0245 : 0x0245 + 8])[0]

                # Validate amounts are reasonable
                if 0 <= base_val < 10_000_000 and 0 <= vat_val < 10_000_000:
                    amount_base = Decimal(str(round(base_val, 2)))
                    amount_vat = Decimal(str(round(vat_val, 2)))
                    amount_total = Decimal(str(round(total_val, 2)))
            except (struct.error, ValueError):
                pass

        # Fields not yet mapped - will be identified in future analysis
        doc_type = 1
        delivery_date = None
        due_date = None
        pab_code = 0

        return cls(
            doc_number=doc_number,
            reference=reference,
            doc_type=doc_type,
            doc_date=doc_date,
            delivery_date=delivery_date,
            due_date=due_date,
            pab_code=pab_code,
            pab_name=pab_name,
            pab_ico=pab_ico,
            pab_dic=pab_dic,
            pab_ic_dph=pab_ic_dph,
            pab_address=pab_address,
            pab_city=pab_city,
            pab_zip=pab_zip,
            payment_name=payment_name,
            amount_base=amount_base,
            amount_vat=amount_vat,
            amount_total=amount_total,
            _raw_offset=offset,
        )

    @classmethod
    def _find_amounts(cls, data: bytes, start_offset: int) -> tuple[Decimal, Decimal, Decimal] | None:
        """
        Find and parse amount fields (base, vat, total).

        Looks for three consecutive reasonable double values.
        """
        # Search in the last portion of the record where amounts typically are
        search_start = max(start_offset, len(data) - 200)

        for offset in range(search_start, len(data) - 24, 1):
            try:
                val1 = struct.unpack("<d", data[offset : offset + 8])[0]
                val2 = struct.unpack("<d", data[offset + 8 : offset + 16])[0]
                val3 = struct.unpack("<d", data[offset + 16 : offset + 24])[0]

                # Check if values look like amounts (positive, reasonable range)
                if all(0 <= v < 1_000_000 for v in [val1, val2, val3]):
                    # Check if total ≈ base + vat (within tolerance)
                    if abs(val1 + val2 - val3) < 0.02 or abs(val3) < 0.01:
                        return (
                            Decimal(str(round(val1, 2))),
                            Decimal(str(round(val2, 2))),
                            Decimal(str(round(val3, 2))),
                        )
            except (struct.error, ValueError):
                continue

        return None

    @classmethod
    def _find_dates(cls, data: bytes, start_offset: int) -> tuple[date | None, date | None, date | None] | None:
        """
        Find and parse date fields.

        Looks for Delphi date integers (days since 1899-12-30).
        Valid dates should be roughly 40000-50000 (years 2009-2036).
        """
        for offset in range(start_offset, min(start_offset + 100, len(data) - 12), 1):
            try:
                val1 = struct.unpack("<i", data[offset : offset + 4])[0]
                val2 = struct.unpack("<i", data[offset + 4 : offset + 8])[0]
                val3 = struct.unpack("<i", data[offset + 8 : offset + 12])[0]

                # Check if values look like Delphi dates (2000-2040 range)
                if all(36526 <= v <= 51501 or v == 0 for v in [val1, val2, val3]):
                    return (
                        cls._decode_delphi_date(val1) if val1 > 0 else None,
                        cls._decode_delphi_date(val2) if val2 > 0 else None,
                        cls._decode_delphi_date(val3) if val3 > 0 else None,
                    )
            except (struct.error, ValueError):
                continue

        return None

    @staticmethod
    def _decode_delphi_date(days: int) -> date:
        """Convert Delphi date to Python date"""
        from datetime import timedelta

        base_date = datetime(1899, 12, 30)
        return (base_date + timedelta(days=days)).date()

    def validate(self) -> list[str]:
        """Validate record"""
        errors = []

        if not self.doc_number.strip():
            errors.append("DocNumber cannot be empty")
        if self.pab_code < 0:
            errors.append("PabCode cannot be negative")
        if self.amount_total < 0:
            errors.append("AmountTotal cannot be negative")

        return errors

    def __str__(self) -> str:
        return f"TSH({self.doc_number}: {self.pab_name}, {self.amount_total} {self.currency})"


# Helper function for external use
def read_pascal_string(data: bytes, offset: int, encoding: str = "cp852") -> tuple[str, int]:
    """
    Read Pascal ShortString from bytes.

    Pascal ShortString format:
    - First byte: length (0-255)
    - Following bytes: string data

    Args:
        data: Raw bytes
        offset: Starting offset
        encoding: String encoding

    Returns:
        Tuple of (string_value, new_offset)
    """
    return TSHRecord._read_pascal_string(data, offset, encoding)
