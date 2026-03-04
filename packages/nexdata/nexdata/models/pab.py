r"""
PAB Table Model
Katalog obchodnych partnerov (dodavatelia, odberatelia)

Table: PAB00000.BTR
Location: C:\NEX\YEARACT\DIALS\PAB00000.BTR
Definition: pab.bdf
Record Size: 1269 bytes

Fix: Pascal ShortString (StrN) occupies N+1 bytes (byte 0 = length, bytes 1..N = data).
Previous parser used flat byte slicing without the length prefix, causing offset drift
and concatenated/corrupted values.
"""

import struct
from dataclasses import dataclass
from datetime import date, datetime, time as time_type, timedelta


# ---------------------------------------------------------------------------
# PAB_FIELDS: exact BDF field definitions (91 fields)
#
# Format: (field_name, field_type, byte_size)
#   - "str" fields are Pascal ShortString: byte_size = max_len + 1
#     (first byte = length, remaining = character data)
#   - Fields starting with "_" are search-index copies and will be skipped
# ---------------------------------------------------------------------------
PAB_FIELDS = [
    ("PaCode", "longint", 4),
    ("PaName", "str", 31),
    ("_PaName", "str", 31),
    ("RegName", "str", 61),
    ("SmlName", "str", 11),
    ("OldTin", "str", 16),
    ("RegIno", "str", 16),
    ("RegTin", "str", 16),
    ("RegVin", "str", 16),
    ("RegAddr", "str", 31),
    ("RegSta", "str", 3),
    ("RegCty", "str", 4),
    ("RegCtn", "str", 31),
    ("RegZip", "str", 16),
    ("RegTel", "str", 21),
    ("RegFax", "str", 21),
    ("RegEml", "str", 31),
    ("CrpAddr", "str", 31),
    ("CrpSta", "str", 3),
    ("CrpCty", "str", 4),
    ("CrpCtn", "str", 31),
    ("CrpZip", "str", 16),
    ("CrpTel", "str", 21),
    ("CrpFax", "str", 21),
    ("CrpEml", "str", 31),
    ("IvcAddr", "str", 31),
    ("IvcSta", "str", 3),
    ("IvcCty", "str", 4),
    ("IvcCtn", "str", 31),
    ("IvcZip", "str", 16),
    ("IvcTel", "str", 21),
    ("IvcFax", "str", 21),
    ("IvcEml", "str", 31),
    ("WebSite", "str", 31),
    ("ContoNum", "str", 31),
    ("BankCode", "str", 16),
    ("BankSeat", "str", 31),
    ("IbanCode", "str", 35),
    ("SwftCode", "str", 21),
    ("ContoQnt", "byte", 1),
    ("IsDscPrc", "double", 8),
    ("IsExpDay", "word", 2),
    ("IsPenPrc", "double", 8),
    ("IsPayCode", "str", 4),
    ("IsPayName", "str", 21),
    ("IsTrsCode", "str", 4),
    ("IsTrsName", "str", 21),
    ("IcDscPrc", "double", 8),
    ("IcExpDay", "word", 2),
    ("IcPenPrc", "double", 8),
    ("IcPlsNum", "word", 2),
    ("IcPayCode", "str", 4),
    ("IcPayName", "str", 19),
    ("IcPayMode", "byte", 1),
    ("IcPayBrm", "byte", 1),
    ("IcTrsCode", "str", 4),
    ("IcTrsName", "str", 21),
    ("IcSalLim", "double", 8),
    ("BuDisStat", "byte", 1),
    ("BuDisDate", "date", 4),
    ("BuDisUser", "str", 9),
    ("BuDisDesc", "str", 31),
    ("SaDisStat", "byte", 1),
    ("SaDisDate", "date", 4),
    ("SaDisUser", "str", 9),
    ("SaDisDesc", "str", 21),
    ("IcFacDay", "word", 2),
    ("IcFacPrc", "double", 8),
    ("PagCode", "word", 2),
    ("IdCode", "str", 21),
    ("VatPay", "byte", 1),
    ("SapType", "byte", 1),
    ("CusType", "byte", 1),
    ("OrgType", "byte", 1),
    ("PasQnt", "word", 2),
    ("BonClc", "byte", 1),
    ("CrtUser", "str", 9),
    ("CrtDate", "date", 4),
    ("CrtTime", "time", 4),
    ("ModNum", "word", 2),
    ("ModUser", "str", 9),
    ("ModDate", "date", 4),
    ("ModTime", "time", 4),
    ("IcAplNum", "word", 2),
    ("PgcCode", "word", 2),
    ("SrCode", "str", 16),
    ("TrdType", "byte", 1),
    ("PrnLng", "str", 3),
    ("DlrCode", "word", 2),
    ("HedName", "str", 31),
    ("RegRec", "str", 61),
    ("IcExpPrm", "word", 2),
    ("OwnPac", "longint", 4),
    ("SpeLev", "byte", 1),
    ("AdvPay", "double", 8),
]


# ---------------------------------------------------------------------------
# Low-level binary parsers for Pascal/Delphi types
# ---------------------------------------------------------------------------


def _parse_pascal_string(buf: bytes, offset: int, max_len: int) -> str:
    """
    Parse a Pascal ShortString from binary buffer.

    Pascal ShortString[N] occupies N+1 bytes:
      byte 0      = actual length (0..N)
      bytes 1..N  = character data

    Args:
        buf: Raw binary buffer
        offset: Start offset in buffer (points to the length byte)
        max_len: Maximum string length (N), so the field occupies max_len+1 bytes

    Returns:
        Decoded string (cp1250, stripped)
    """
    length = buf[offset]
    if length > max_len:
        length = max_len
    raw = buf[offset + 1 : offset + 1 + length]
    try:
        return raw.decode("cp1250").strip()
    except Exception:
        return raw.decode("latin-1", errors="replace").strip()


def _parse_pascal_date(buf: bytes, offset: int) -> date | None:
    """
    Parse Delphi TDateTime date part (int32, days since 1899-12-30).

    Returns:
        date object or None if value <= 0
    """
    value = struct.unpack_from("<i", buf, offset)[0]
    if value <= 0:
        return None
    try:
        return date(1899, 12, 30) + timedelta(days=value)
    except Exception:
        return None


def _parse_pascal_time(buf: bytes, offset: int) -> time_type | None:
    """
    Parse Delphi time value (int32, milliseconds since midnight).

    Returns:
        time object or None if value <= 0
    """
    value = struct.unpack_from("<i", buf, offset)[0]
    if value <= 0:
        return None
    try:
        total_seconds = value // 1000
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return time_type(hours % 24, minutes, seconds)
    except Exception:
        return None


def parse_pab_record(raw_bytes: bytes) -> dict:
    """
    Parse a raw PAB binary record into a dict using PAB_FIELDS definition.

    Correctly handles Pascal ShortString format where each StrN field
    occupies N+1 bytes (1 length byte + N data bytes).

    Fields starting with '_' are skipped (search-index copies).

    Args:
        raw_bytes: Raw binary record from Btrieve

    Returns:
        Dict with field_name -> parsed_value
    """
    offset = 0
    record: dict = {}

    for field_name, field_type, field_size in PAB_FIELDS:
        if offset + field_size > len(raw_bytes):
            break

        if field_name.startswith("_"):
            # Skip search-index copy fields
            offset += field_size
            continue

        if field_type == "str":
            # Pascal ShortString: field_size = max_len + 1
            record[field_name] = _parse_pascal_string(raw_bytes, offset, field_size - 1)
        elif field_type == "longint":
            record[field_name] = struct.unpack_from("<i", raw_bytes, offset)[0]
        elif field_type == "word":
            record[field_name] = struct.unpack_from("<H", raw_bytes, offset)[0]
        elif field_type == "byte":
            record[field_name] = raw_bytes[offset]
        elif field_type == "double":
            record[field_name] = round(
                struct.unpack_from("<d", raw_bytes, offset)[0], 6
            )
        elif field_type == "date":
            record[field_name] = _parse_pascal_date(raw_bytes, offset)
        elif field_type == "time":
            record[field_name] = _parse_pascal_time(raw_bytes, offset)

        offset += field_size

    return record


# ---------------------------------------------------------------------------
# PABRecord dataclass (preserves existing API)
# ---------------------------------------------------------------------------


@dataclass
class PABRecord:
    """
    PAB record structure - Obchodni partneri

    Evidencia vsetkych obchodnych partnerov (dodavatelia, odberatelia, ostatni).
    """

    # Primary key
    pab_code: int  # Kod partnera - primary key

    # Basic info
    name1: str = ""  # Nazov firmy (riadok 1)
    name2: str = ""  # Nazov firmy (riadok 2) / RegName
    short_name: str = ""  # Skrateny nazov

    # Address
    street: str = ""  # Ulica a cislo
    city: str = ""  # Mesto
    zip_code: str = ""  # PSC
    country: str = ""  # Krajina

    # Contact
    phone: str = ""  # Telefon
    fax: str = ""  # Fax
    email: str = ""  # Email
    web: str = ""  # Web stranka
    contact_person: str = ""  # Kontaktna osoba

    # Tax info
    ico: str = ""  # ICO (identifikacne cislo organizacie)
    dic: str = ""  # DIC (danove identifikacne cislo)
    ic_dph: str = ""  # IC DPH (identifikacne cislo pre DPH)

    # Bank info
    bank_account: str = ""  # Cislo uctu
    bank_code: str = ""  # Kod banky
    bank_name: str = ""  # Nazov banky
    iban: str = ""  # IBAN
    swift: str = ""  # SWIFT/BIC

    # Business info
    partner_type: int = 0  # Typ partnera (1=dodavatel, 2=odberatel, 3=oboje)
    payment_terms: int = 14  # Platobne podmienky (dni)
    credit_limit: float = 0.0  # Kreditny limit
    discount_percent: float = 0.0  # Zlava v percentach

    # Status
    active: bool = True  # Aktivny partner
    vat_payer: bool = True  # Platitel DPH

    # Notes
    note: str = ""  # Poznamka
    note2: str = ""  # Poznamka 2
    internal_note: str = ""  # Interna poznamka

    # Audit fields
    mod_user: str = ""  # Uzivatel poslednej zmeny
    mod_date: datetime | None = None  # Datum poslednej zmeny
    mod_time: datetime | None = None  # Cas poslednej zmeny
    created_date: datetime | None = None  # Datum vytvorenia
    created_user: str = ""  # Uzivatel vytvorenia

    # Raw parsed fields from BDF (all 91 fields minus underscore-prefixed)
    raw_fields: dict | None = None

    # Indexes (constants)
    INDEX_PABCODE = "PabCode"  # Primary index
    INDEX_NAME = "Name1"  # Index podla nazvu
    INDEX_ICO = "ICO"  # Index podla ICO
    INDEX_TYPE = "PartnerType"  # Index podla typu partnera

    @classmethod
    def from_bytes(cls, data: bytes) -> "PABRecord":
        """
        Deserialize PAB record from raw Btrieve bytes using BDF field definitions.

        Uses parse_pab_record() which correctly handles Pascal ShortString format
        (StrN = N+1 bytes: 1 length byte + N character bytes).

        Args:
            data: Raw bytes from Btrieve

        Returns:
            PABRecord instance
        """
        # Record size per BDF header is 1269 bytes; fields total 1277
        # (AdvPay was added later). Accept >= 1269 for backwards compat.
        expected_size = 1269
        if len(data) < expected_size:
            raise ValueError(
                f"Invalid record size: {len(data)} bytes (expected >= {expected_size})"
            )

        r = parse_pab_record(data)

        return cls(
            pab_code=r.get("PaCode", 0),
            name1=r.get("PaName", ""),
            name2=r.get("RegName", ""),
            short_name=r.get("SmlName", ""),
            street=r.get("RegAddr", ""),
            city=r.get("RegCtn", ""),
            zip_code=r.get("RegZip", ""),
            country=r.get("RegCty", ""),
            phone=r.get("RegTel", ""),
            fax=r.get("RegFax", ""),
            email=r.get("RegEml", ""),
            web=r.get("WebSite", ""),
            contact_person=r.get("HedName", ""),
            ico=r.get("RegIno", ""),
            dic=r.get("RegTin", ""),
            ic_dph=r.get("RegVin", ""),
            bank_account=r.get("ContoNum", ""),
            bank_code=r.get("BankCode", ""),
            bank_name=r.get("BankSeat", ""),
            iban=r.get("IbanCode", ""),
            swift=r.get("SwftCode", ""),
            partner_type=r.get("CusType", 0),
            payment_terms=r.get("IcExpDay", 14),
            credit_limit=r.get("IcSalLim", 0.0),
            discount_percent=r.get("IcDscPrc", 0.0),
            active=r.get("BuDisStat", 0) == 0,  # 0 = active, >0 = disabled
            vat_payer=bool(r.get("VatPay", 0)),
            note=r.get("BuDisDesc", ""),
            note2=r.get("SaDisDesc", ""),
            internal_note="",
            mod_user=r.get("ModUser", ""),
            mod_date=r.get("ModDate"),
            mod_time=r.get("ModTime"),
            created_date=r.get("CrtDate"),
            created_user=r.get("CrtUser", ""),
            raw_fields=r,
        )

    def validate(self) -> list[str]:
        """Validate record"""
        errors = []

        if self.pab_code <= 0:
            errors.append("PabCode must be positive")
        if not self.name1.strip():
            errors.append("Name1 cannot be empty")
        if self.ico and len(self.ico) not in [8, 10, 12]:
            errors.append(f"Invalid ICO length: {len(self.ico)} (expected 8, 10 or 12)")
        if self.payment_terms < 0:
            errors.append("PaymentTerms cannot be negative")
        if self.credit_limit < 0:
            errors.append("CreditLimit cannot be negative")

        return errors

    def get_full_name(self) -> str:
        """Get full company name (Name1 + Name2)"""
        if self.name2:
            return f"{self.name1} {self.name2}".strip()
        return self.name1

    def get_full_address(self) -> str:
        """Get full address as single line"""
        parts = [self.street, self.city, self.zip_code, self.country]
        return ", ".join([p for p in parts if p])

    def is_supplier(self) -> bool:
        """Check if partner is supplier"""
        return self.partner_type in [1, 3]  # 1=supplier, 3=both

    def is_customer(self) -> bool:
        """Check if partner is customer"""
        return self.partner_type in [2, 3]  # 2=customer, 3=both

    def __str__(self) -> str:
        return f"PAB({self.pab_code}: {self.name1})"
