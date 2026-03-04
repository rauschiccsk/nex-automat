"""
PABTransformer — validates and normalizes extracted PAB JSON records for PostgreSQL.

Reads data/PAB/PAB.json (produced by PABExtractor on Windows).
Records in JSON are already field-mapped to target column names by the extractor.
This transformer validates required fields, normalizes types, and returns
records ready for PABLoader UPSERT into the partners table.
"""

import sys
from pathlib import Path

# Ensure nex-migration root is on sys.path for config imports
_migration_root = str(Path(__file__).resolve().parent.parent)
if _migration_root not in sys.path:
    sys.path.insert(0, _migration_root)

from transform.base_transformer import BaseTransformer
from transform import transforms


class PABTransformer(BaseTransformer):
    """Validate and normalize extracted PAB records for partners table."""

    def __init__(self, data_dir: str = "data"):
        super().__init__(data_dir=data_dir)
        self.category = "PAB"

    # ------------------------------------------------------------------
    # Abstract method implementations
    # ------------------------------------------------------------------

    def transform(self) -> list[dict]:
        """Read PAB.json and validate/normalize each record."""
        raw_records = self.read_extracted_data("PAB")
        self.stats["total"] = len(raw_records)

        results: list[dict] = []
        for idx, raw in enumerate(raw_records):
            normalized = self._normalize_record(raw, idx)
            if normalized is not None:
                results.append(normalized)
                self.stats["valid"] += 1

        return results

    def validate_record(self, record: dict, index: int) -> bool:
        """Validate a record. Returns True if valid."""
        source_key = record.get("_source_key", f"idx:{index}")

        # code is required
        code = record.get("code")
        if not code or not str(code).strip():
            self.add_error(index, source_key, "code", "Missing or empty partner code")
            return False

        # name is required
        name = record.get("name")
        if not name or not str(name).strip():
            self.add_error(index, source_key, "name", "Missing or empty partner name")
            return False

        # partner_type must be valid enum value
        partner_type = record.get("partner_type", "customer")
        if partner_type not in ("customer", "supplier", "both"):
            self.add_warning(
                index,
                source_key,
                "partner_type",
                f"Invalid partner_type '{partner_type}', defaulting to 'customer'",
            )
            record["partner_type"] = "customer"

        # payment_method must be valid enum value
        payment_method = record.get("payment_method", "transfer")
        if payment_method not in ("transfer", "cash", "cod"):
            self.add_warning(
                index,
                source_key,
                "payment_method",
                f"Invalid payment_method '{payment_method}', defaulting to 'transfer'",
            )
            record["payment_method"] = "transfer"

        # country_code — must be 2 chars
        country_code = record.get("country_code", "SK")
        if country_code and len(str(country_code)) != 2:
            self.add_warning(
                index,
                source_key,
                "country_code",
                f"Invalid country_code '{country_code}', defaulting to 'SK'",
            )
            record["country_code"] = "SK"

        return True

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    # Max field lengths matching PostgreSQL partners table schema
    _FIELD_MAX_LEN: dict[str, int] = {
        "code": 30,
        "name": 100,
        "partner_type": 20,
        "company_id": 20,
        "tax_id": 20,
        "vat_id": 20,
        "street": 100,
        "city": 100,
        "zip_code": 20,
        "country_code": 2,
        "phone": 50,
        "mobile": 50,
        "email": 255,
        "website": 255,
        "contact_person": 255,
        "payment_method": 50,
        "currency": 3,
        "iban": 34,
        "bank_name": 255,
        "swift_bic": 11,
    }

    def _truncate_fields(self, record: dict) -> dict:
        """Truncate string fields to match PostgreSQL column max lengths."""
        for field, max_len in self._FIELD_MAX_LEN.items():
            val = record.get(field)
            if isinstance(val, str) and len(val) > max_len:
                record[field] = val[:max_len]
        return record

    def _normalize_record(self, raw: dict, index: int) -> dict | None:
        """Normalize types and validate a single record from PAB.json.

        Records in JSON are already field-mapped by PABExtractor.
        Field names are target column names (code, name, partner_type, etc.).
        This method ensures correct Python types for PostgreSQL.
        """
        source_key = raw.get("_source_key", f"idx:{index}")

        partner_type = self._normalize_partner_type(raw.get("partner_type"))

        result: dict = {
            "_source_key": source_key,
            # Required string fields
            "code": transforms.to_str_strip(raw.get("code")),
            "name": transforms.strip(raw.get("name")),
            # Partner type — derive booleans from normalized partner_type string
            "partner_type": partner_type,
            "is_supplier": partner_type in ("supplier", "both"),
            "is_customer": partner_type in ("customer", "both"),
            # Tax / company identifiers
            "company_id": transforms.strip(raw.get("company_id")),
            "tax_id": transforms.strip(raw.get("tax_id")),
            "vat_id": transforms.strip(raw.get("vat_id")),
            "is_vat_payer": transforms.to_bool(raw.get("is_vat_payer", False)),
            # Address
            "street": transforms.strip(raw.get("street")),
            "city": transforms.strip(raw.get("city")),
            "zip_code": transforms.strip(raw.get("zip_code")),
            "country_code": self._normalize_country_code(raw.get("country_code", "SK")),
            # Contact
            "phone": transforms.strip(raw.get("phone")),
            "mobile": transforms.strip(raw.get("mobile")),
            "email": transforms.strip(raw.get("email")),
            "website": transforms.strip(raw.get("website")),
            "contact_person": transforms.strip(raw.get("contact_person")),
            # Business terms
            "payment_due_days": transforms.to_int(
                raw.get("payment_due_days"), default=14
            ),
            "credit_limit": transforms.to_decimal(raw.get("credit_limit"), default=0.0),
            "discount_percent": transforms.to_decimal(
                raw.get("discount_percent"), default=0.0
            ),
            "payment_method": self._normalize_payment_method(
                raw.get("payment_method", "transfer")
            ),
            "currency": transforms.strip(raw.get("currency")) or "EUR",
            # Bank info
            "iban": transforms.strip(raw.get("iban")),
            "bank_name": transforms.strip(raw.get("bank_name")),
            "swift_bic": transforms.strip(raw.get("swift_bic")),
            # Notes
            "notes": self._normalize_notes(raw),
            # Status
            "is_active": transforms.to_bool(raw.get("is_active", True)),
        }

        self._truncate_fields(result)

        if not self.validate_record(result, index):
            return None

        return result

    @staticmethod
    def _normalize_partner_type(value) -> str:
        """Ensure partner_type is a valid enum string."""
        if isinstance(value, str) and value in ("customer", "supplier", "both"):
            return value
        if isinstance(value, (int, float)):
            return transforms.map_partner_type_int(value)
        return "customer"

    @staticmethod
    def _normalize_country_code(value) -> str:
        """Ensure country_code is a 2-char ISO code."""
        if value is None:
            return "SK"
        s = str(value).strip()
        if len(s) == 2:
            return s.upper()
        return transforms.country_code(value, default="SK")

    @staticmethod
    def _normalize_payment_method(value) -> str:
        """Ensure payment_method is a valid enum string."""
        if isinstance(value, str) and value in ("transfer", "cash", "cod"):
            return value
        return transforms.map_payment_method(value)

    @staticmethod
    def _normalize_notes(raw: dict) -> str | None:
        """Normalize notes — use existing notes field or combine note fields."""
        # If JSON has pre-combined notes, sanitize and use that
        notes = raw.get("notes")
        if notes:
            sanitized = transforms.strip(notes)
            if sanitized:
                return sanitized
        # Otherwise try to combine from individual fields
        note = raw.get("note")
        note2 = raw.get("note2")
        internal_note = raw.get("internal_note")
        return transforms.combine_notes(note, note2, internal_note)
