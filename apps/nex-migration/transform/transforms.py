"""
Transformačné funkcie pre field mapping.

Každá funkcia sa volá podľa názvu v FieldMapping.transform.
Vstup: raw hodnota z Btrieve extraktu.
Výstup: PostgreSQL-ready hodnota.
"""

import re


def _sanitize(value: str) -> str:
    """Remove null bytes and non-printable control chars (except \\n, \\t) from Btrieve data."""
    # Remove null bytes first
    s = value.replace("\x00", "")
    # Remove other non-printable control chars (keep \n=0x0a, \t=0x09, \r=0x0d)
    s = re.sub(r"[\x01-\x08\x0b\x0c\x0e-\x1f\x7f]", "", s)
    return s


COUNTRY_MAP = {
    "slovensko": "SK",
    "slovakia": "SK",
    "sk": "SK",
    "česko": "CZ",
    "česká republika": "CZ",
    "czech republic": "CZ",
    "cz": "CZ",
    "maďarsko": "HU",
    "hungary": "HU",
    "hu": "HU",
    "rakúsko": "AT",
    "austria": "AT",
    "at": "AT",
    "nemecko": "DE",
    "germany": "DE",
    "de": "DE",
    "poľsko": "PL",
    "poland": "PL",
    "pl": "PL",
    "": "SK",
}


def strip(value) -> str | None:
    """Orezanie whitespace + sanitizácia null bytes, vráti None ak je výsledok prázdny."""
    if value is None:
        return None
    s = _sanitize(str(value)).strip()
    return s if s else None


def to_str_strip(value) -> str | None:
    """Konverzia na string + strip + sanitizácia null bytes (pre číselné kódy)."""
    if value is None:
        return None
    s = _sanitize(str(value)).strip()
    return s if s else None


def to_bool(value) -> bool:
    """Konverzia na boolean — podporuje int, str, bool."""
    if value is None:
        return False
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    s = _sanitize(str(value)).strip().lower()
    return s in ("true", "1", "yes", "áno", "ano", "t", "y")


def to_int(value, default: int = 0) -> int:
    """Konverzia na int, default ak sa nepodarí."""
    if value is None:
        return default
    try:
        return int(float(value))
    except (ValueError, TypeError):
        return default


def to_decimal(value, default: float = 0.0) -> float:
    """Konverzia na float/decimal, default ak sa nepodarí."""
    if value is None:
        return default
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def country_code(value, default: str = "SK") -> str:
    """Konverzia názvu krajiny na ISO 3166-1 alpha-2 kód."""
    if value is None:
        return default
    s = _sanitize(str(value)).strip().lower()
    return COUNTRY_MAP.get(s, default)


def map_partner_type_int(value) -> str:
    """
    Konverzia PAB partner_type int na PostgreSQL enum string.

    Btrieve: 1=supplier, 2=customer, 3=both
    PostgreSQL: 'supplier', 'customer', 'both'
    """
    if value is None:
        return "customer"
    try:
        val = int(value)
    except (ValueError, TypeError):
        return "customer"

    mapping = {
        1: "supplier",
        2: "customer",
        3: "both",
    }
    return mapping.get(val, "customer")


def is_supplier_from_type(value) -> bool:
    """Zisti či je partner dodávateľ z partner_type int."""
    if value is None:
        return False
    try:
        val = int(value)
    except (ValueError, TypeError):
        return False
    return val in (1, 3)


def is_customer_from_type(value) -> bool:
    """Zisti či je partner odberateľ z partner_type int."""
    if value is None:
        return True
    try:
        val = int(value)
    except (ValueError, TypeError):
        return True
    return val in (2, 3)


def map_partner_type(is_customer: bool, is_supplier: bool) -> str:
    """Pomocná funkcia — kombinácia flagov na partner_type string."""
    if is_customer and is_supplier:
        return "both"
    if is_supplier:
        return "supplier"
    return "customer"


def map_payment_method(value) -> str:
    """Konverzia platobnej metódy zo slovenčiny na PostgreSQL enum."""
    if value is None:
        return "transfer"
    s = _sanitize(str(value)).strip().lower()
    mapping = {
        "prevod": "transfer",
        "prevodom": "transfer",
        "transfer": "transfer",
        "hotovosť": "cash",
        "hotovost": "cash",
        "cash": "cash",
        "dobierka": "cod",
        "cod": "cod",
    }
    return mapping.get(s, "transfer")


def combine_notes(
    note: str | None, note2: str | None = None, internal_note: str | None = None
) -> str | None:
    """Skombinuje PAB note polia do jedného text poľa."""
    parts = []
    if note:
        n = _sanitize(str(note)).strip()
        if n:
            parts.append(n)
    if note2:
        n2 = _sanitize(str(note2)).strip()
        if n2:
            parts.append(n2)
    if internal_note:
        n3 = _sanitize(str(internal_note)).strip()
        if n3:
            parts.append(f"[internal] {n3}")
    return "\n".join(parts) if parts else None
