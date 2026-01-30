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

    @classmethod
    def from_bytes(cls, data: bytes, encoding: str = "cp852") -> "TSHRecord":
        """
        Deserialize TSH record from bytes using Pascal ShortString format.

        Field sequence (based on MAGER hex dump analysis):
        1. doc_id (int32) - internal ID
        2. doc_number (pascal string) - document number
        3. reference (pascal string) - reference number
        4. pab_code (int32) - partner code
        5. doc_type (int16) - document type
        6. pab_name (pascal string) - partner name
        ... more string fields (ICO, DIC, IC_DPH, address, city, ZIP, payment)
        ... amounts as doubles at the end

        Args:
            data: Raw bytes from Btrieve
            encoding: String encoding (cp852 for Czech/Slovak)

        Returns:
            TSHRecord instance
        """
        if len(data) < 50:
            raise ValueError(f"Invalid record size: {len(data)} bytes (expected >= 50)")

        offset = 0

        # 1. doc_id (int32) - internal ID, skip
        doc_id, offset = cls._read_int32(data, offset)

        # 2. doc_number (pascal string)
        doc_number, offset = cls._read_pascal_string(data, offset, encoding)

        # 3. reference (pascal string)
        reference, offset = cls._read_pascal_string(data, offset, encoding)

        # 4. pab_code (int32)
        pab_code, offset = cls._read_int32(data, offset)

        # 5. doc_type (int16)
        doc_type, offset = cls._read_int16(data, offset)

        # 6. pab_name (pascal string)
        pab_name, offset = cls._read_pascal_string(data, offset, encoding)

        # 7-9. ICO, DIC, IC_DPH (pascal strings)
        pab_ico, offset = cls._read_pascal_string(data, offset, encoding)
        pab_dic, offset = cls._read_pascal_string(data, offset, encoding)
        pab_ic_dph, offset = cls._read_pascal_string(data, offset, encoding)

        # 10-12. address, city, ZIP (pascal strings)
        pab_address, offset = cls._read_pascal_string(data, offset, encoding)
        pab_city, offset = cls._read_pascal_string(data, offset, encoding)
        pab_zip, offset = cls._read_pascal_string(data, offset, encoding)

        # 13. payment_name (pascal string)
        payment_name, offset = cls._read_pascal_string(data, offset, encoding)

        # Try to find the amount section (look for doubles near end of record)
        # Amounts are typically 8-byte doubles at specific positions
        amount_base = Decimal("0.00")
        amount_vat = Decimal("0.00")
        amount_total = Decimal("0.00")

        # Search for amounts in the remaining data
        # They should be near the end as consecutive doubles
        amounts_found = cls._find_amounts(data, offset)
        if amounts_found:
            amount_base, amount_vat, amount_total = amounts_found

        # Parse dates if present
        doc_date = None
        delivery_date = None
        due_date = None

        # Try to find date section (usually after some fields)
        dates_found = cls._find_dates(data, offset)
        if dates_found:
            doc_date, delivery_date, due_date = dates_found

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
