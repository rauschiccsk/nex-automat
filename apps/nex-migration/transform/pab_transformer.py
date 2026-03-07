"""
PABTransformer — validates and normalizes extracted PAB JSON records
for the normalized partner_catalog* schema (6 tables).

Reads data/PAB/PAB.json (produced by PABExtractor on Windows).
Records in JSON are already field-mapped to intermediate column names.
This transformer validates required fields, normalizes types, and returns
structured records ready for PABLoader INSERT into partner_catalog* tables.

Output per record:
{
    "header": { ... partner_catalog columns ... },
    "extensions": { ... partner_catalog_extensions columns ... } | None,
    "addresses": [ { ... partner_catalog_addresses row ... } ],
    "contacts": [ { ... partner_catalog_contacts row ... } ],
    "bank_accounts": [ { ... partner_catalog_bank_accounts row ... } ],
    "texts": [ { ... partner_catalog_texts row ... } ],
}
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
    """Validate and normalize extracted PAB records for partner_catalog* tables."""

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
            structured = self._build_structured_record(raw, idx)
            if structured is not None:
                results.append(structured)
                self.stats["valid"] += 1

        return results

    def validate_record(self, record: dict, index: int) -> bool:
        """Validate a raw record. Returns True if valid."""
        source_key = record.get("_source_key", f"idx:{index}")

        # code is required and must be numeric (used as partner_id)
        code = record.get("code")
        if not code or not str(code).strip():
            self.add_error(index, source_key, "code", "Missing or empty partner code")
            return False

        try:
            int(str(code).strip())
        except (ValueError, TypeError):
            self.add_error(
                index, source_key, "code", f"Non-numeric partner code: '{code}'"
            )
            return False

        # name is required
        name = record.get("name")
        if not name or not str(name).strip():
            self.add_error(index, source_key, "name", "Missing or empty partner name")
            return False

        # partner_type must be valid
        partner_type = record.get("partner_type", "customer")
        if partner_type not in ("customer", "supplier", "both"):
            self.add_warning(
                index,
                source_key,
                "partner_type",
                f"Invalid partner_type '{partner_type}', defaulting to 'customer'",
            )
            record["partner_type"] = "customer"

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

    # Max field lengths matching PostgreSQL partner_catalog schema
    _HEADER_MAX_LEN: dict[str, int] = {
        "partner_code": 30,
        "partner_name": 100,
        "company_id": 20,
        "tax_id": 20,
        "vat_id": 20,
        "street": 100,
        "city": 100,
        "zip_code": 20,
        "country_code": 2,
    }

    def _truncate_fields(self, record: dict, max_lens: dict[str, int]) -> dict:
        """Truncate string fields to match PostgreSQL column max lengths."""
        for fld, max_len in max_lens.items():
            val = record.get(fld)
            if isinstance(val, str) and len(val) > max_len:
                record[fld] = val[:max_len]
        return record

    def _build_structured_record(self, raw: dict, index: int) -> dict | None:
        """Build a structured record from a raw PAB.json entry.

        Returns None if validation fails.
        """
        if not self.validate_record(raw, index):
            return None

        source_key = raw.get("_source_key", f"idx:{index}")
        partner_type = self._normalize_partner_type(raw.get("partner_type"))
        country_code = self._normalize_country_code(raw.get("country_code", "SK"))

        # --- Header (partner_catalog) ---
        header = {
            "partner_id": int(str(raw["code"]).strip()),
            "partner_code": transforms.to_str_strip(raw.get("code")),
            "partner_name": transforms.strip(raw.get("name")),
            "company_id": transforms.strip(raw.get("company_id")),
            "tax_id": transforms.strip(raw.get("tax_id")),
            "vat_id": transforms.strip(raw.get("vat_id")),
            "is_vat_payer": self._derive_vat_payer(raw),
            "is_supplier": partner_type in ("supplier", "both"),
            "is_customer": partner_type in ("customer", "both"),
            "street": transforms.strip(raw.get("street")),
            "city": transforms.strip(raw.get("city")),
            "zip_code": transforms.strip(raw.get("zip_code")),
            "country_code": country_code,
            "partner_class": "business",
            "is_active": transforms.to_bool(raw.get("is_active", True)),
            "created_by": "migration",
            "updated_by": "migration",
        }
        self._truncate_fields(header, self._HEADER_MAX_LEN)

        # --- Extensions (partner_catalog_extensions) ---
        extensions = self._build_extensions(raw)

        # --- Addresses (partner_catalog_addresses) ---
        addresses = self._build_addresses(raw, country_code)

        # --- Contacts (partner_catalog_contacts) ---
        contacts = self._build_contacts(raw, country_code)

        # --- Bank Accounts (partner_catalog_bank_accounts) ---
        bank_accounts = self._build_bank_accounts(raw)

        # --- Texts (partner_catalog_texts) ---
        texts = self._build_texts(raw)

        return {
            "_source_key": source_key,
            "header": header,
            "extensions": extensions,
            "addresses": addresses,
            "contacts": contacts,
            "bank_accounts": bank_accounts,
            "texts": texts,
        }

    def _build_extensions(self, raw: dict) -> dict | None:
        """Build extensions dict if any business terms are present."""
        payment_due_days = transforms.to_int(raw.get("payment_due_days"), default=0)
        credit_limit = transforms.to_decimal(raw.get("credit_limit"), default=0.0)
        discount_percent = transforms.to_decimal(
            raw.get("discount_percent"), default=0.0
        )
        currency = transforms.strip(raw.get("currency")) or "EUR"

        # Only create extensions if there's meaningful data
        has_data = (
            payment_due_days > 0
            or credit_limit > 0
            or discount_percent > 0
            or currency != "EUR"
        )

        if not has_data:
            # Still create with defaults — all partners need extensions
            return {
                "sale_payment_due_days": 14,
                "sale_credit_limit": 0,
                "sale_discount_percent": 0,
                "sale_currency_code": "EUR",
                "created_by": "migration",
                "updated_by": "migration",
            }

        return {
            "sale_payment_due_days": payment_due_days if payment_due_days > 0 else 14,
            "sale_credit_limit": credit_limit,
            "sale_discount_percent": discount_percent,
            "sale_currency_code": currency,
            "created_by": "migration",
            "updated_by": "migration",
        }

    def _build_addresses(self, raw: dict, country_code: str) -> list[dict]:
        """Build address list from raw record."""
        street = transforms.strip(raw.get("street"))
        city = transforms.strip(raw.get("city"))
        zip_code = transforms.strip(raw.get("zip_code"))

        # Only create if at least one address field is present
        if not any([street, city, zip_code]):
            return []

        return [
            {
                "address_type": "registered",
                "street": street,
                "city": city,
                "zip_code": zip_code,
                "country_code": country_code,
                "created_by": "migration",
                "updated_by": "migration",
            }
        ]

    def _build_contacts(self, raw: dict, country_code: str) -> list[dict]:
        """Build contact list from raw record."""
        phone = transforms.strip(raw.get("phone"))
        mobile = transforms.strip(raw.get("mobile"))
        email = transforms.strip(raw.get("email"))
        contact_person = transforms.strip(raw.get("contact_person"))

        # Only create if at least one contact field is present
        if not any([phone, mobile, email, contact_person]):
            return []

        return [
            {
                "contact_type": "person",
                "last_name": contact_person,
                "phone_work": phone,
                "phone_mobile": mobile,
                "email": email,
                "country_code": country_code,
                "created_by": "migration",
                "updated_by": "migration",
            }
        ]

    @staticmethod
    def _build_bank_accounts(raw: dict) -> list[dict]:
        """Build bank account list from raw record."""
        iban = transforms.strip(raw.get("iban"))
        bank_name = transforms.strip(raw.get("bank_name"))
        swift_bic = transforms.strip(raw.get("swift_bic"))

        # Only create if at least IBAN or bank_name is present
        if not any([iban, bank_name]):
            return []

        return [
            {
                "iban_code": iban,
                "bank_name": bank_name,
                "swift_code": swift_bic,
                "is_primary": True,
                "created_by": "migration",
                "updated_by": "migration",
            }
        ]

    @staticmethod
    def _build_texts(raw: dict) -> list[dict]:
        """Build text list from raw record."""
        notes = raw.get("notes")
        if notes:
            sanitized = transforms.strip(notes)
            if sanitized:
                return [
                    {
                        "text_type": "notes",
                        "line_number": 1,
                        "language": "sk",
                        "text_content": sanitized,
                        "created_by": "migration",
                        "updated_by": "migration",
                    }
                ]
        return []

    @staticmethod
    def _derive_vat_payer(raw: dict) -> bool:
        """Derive is_vat_payer from vat_id presence.

        The Btrieve extractor sets is_vat_payer=False for all records,
        but partners with a non-empty vat_id are VAT payers.
        A valid vat_id must have a country prefix + at least 8 digits
        (e.g. 'SK2020399139').
        """
        # Explicit flag takes priority (if it was ever True)
        if transforms.to_bool(raw.get("is_vat_payer", False)):
            return True
        # Derive from vat_id
        vat_id = transforms.strip(raw.get("vat_id"))
        if not vat_id or vat_id in ("", "SK"):
            return False
        # Must have at least a country prefix + some digits
        return len(vat_id) >= 4

    @staticmethod
    def _normalize_partner_type(value) -> str:
        """Ensure partner_type is a valid enum string."""
        if isinstance(value, str) and value in ("customer", "supplier", "both"):
            return value
        if isinstance(value, (int, float)):
            return transforms.map_partner_type_int(value)
        return "customer"

    # Slovak district codes → ISO country codes.
    # PAB.json country_code field contains okres/district codes from Btrieve,
    # not ISO 3166-1 alpha-2 country codes.
    _DISTRICT_TO_COUNTRY: dict[str, str] = {
        "26": "SK",  # Old Komárno district number
        "BA": "SK",  # Bratislava
        "BB": "SK",  # Banská Bystrica
        "BJ": "SK",  # Bardejov
        "C1": "CN",  # China (Guangzhou)
        "DK": "SK",  # Dolný Kubín
        "GP": "SK",  # Gemerská Poloma area
        "HA": "SK",  # Haniska
        "HB": "CZ",  # Havlíčův Brod
        "HC": "SK",  # Hlohovec
        "HK": "CZ",  # Hradec Králové
        "KE": "SK",  # Košice
        "KK": "SK",  # Kežmarok
        "KN": "SK",  # Komárno
        "LC": "SK",  # Lučenec
        "LJ": "SK",  # Liptovský Ján area
        "MA": "SK",  # Malacky
        "MI": "SK",  # Michalovce
        "NI": "SK",  # Nitra
        "NO": "SK",  # Námestovo
        "NZ": "SK",  # Nové Zámky
        "PD": "SK",  # Prievidza
        "PR": "CZ",  # Praha
        "PU": "SK",  # Púchov
        "RD": "SK",  # Radoľa area (Kysuce)
        "RK": "SK",  # Ružomberok
        "SF": "US",  # San Francisco
        "SK": "SK",  # Slovakia
        "SV": "SK",  # Snina
        "TA": "SK",  # Trnava
    }

    @classmethod
    def _normalize_country_code(cls, value) -> str:
        """Convert district/county code to ISO 3166-1 alpha-2 country code.

        PAB.json stores Slovak district codes (KN, BA, KE, ...) in the
        country_code field instead of ISO country codes (SK, CZ, ...).
        """
        if value is None:
            return "SK"
        s = str(value).strip().upper()
        # First check district-to-country map (covers all known PAB values)
        if s in cls._DISTRICT_TO_COUNTRY:
            return cls._DISTRICT_TO_COUNTRY[s]
        # Fallback: if it looks like a valid ISO country code, use it
        if len(s) == 2 and s.isalpha():
            return s
        return transforms.country_code(value, default="SK")
