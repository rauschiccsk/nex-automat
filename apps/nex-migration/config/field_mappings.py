"""
Field mapping configuration: PAB.json fields → partner_catalog* columns.

PAB.json records are already field-mapped by PABExtractor (Windows).
These mappings define how JSON keys map to the normalized partner_catalog schema:
  - partner_catalog (header)
  - partner_catalog_extensions (business terms)
  - partner_catalog_addresses (registered address)
  - partner_catalog_contacts (phone, email, contact person)
  - partner_catalog_bank_accounts (IBAN, SWIFT, bank)
  - partner_catalog_texts (notes)
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class FieldMapping:
    source_field: str
    target_field: str
    transform: str | None = None
    required: bool = False
    default: Any = None


# ---------------------------------------------------------------------------
# partner_catalog — hlavná tabuľka
# ---------------------------------------------------------------------------
PAB_HEADER_MAPPINGS: list[FieldMapping] = [
    FieldMapping(
        source_field="code",
        target_field="partner_id",
        required=True,
        transform="to_int",
    ),
    FieldMapping(
        source_field="name",
        target_field="partner_name",
        required=True,
        transform="strip",
    ),
    FieldMapping(
        source_field="company_id",
        target_field="company_id",
        transform="strip",
    ),
    FieldMapping(
        source_field="tax_id",
        target_field="tax_id",
        transform="strip",
    ),
    FieldMapping(
        source_field="vat_id",
        target_field="vat_id",
        transform="strip",
    ),
    FieldMapping(
        source_field="is_vat_payer",
        target_field="is_vat_payer",
        transform="to_bool",
        default=False,
    ),
    # is_supplier / is_customer derived from partner_type in transformer
    FieldMapping(
        source_field="street",
        target_field="street",
        transform="strip",
    ),
    FieldMapping(
        source_field="city",
        target_field="city",
        transform="strip",
    ),
    FieldMapping(
        source_field="zip_code",
        target_field="zip_code",
        transform="strip",
    ),
    FieldMapping(
        source_field="country_code",
        target_field="country_code",
        transform="country_code",
        default="SK",
    ),
    FieldMapping(
        source_field="is_active",
        target_field="is_active",
        transform="to_bool",
        default=True,
    ),
]


# ---------------------------------------------------------------------------
# partner_catalog_extensions — obchodné podmienky
# ---------------------------------------------------------------------------
PAB_EXTENSIONS_MAPPINGS: list[FieldMapping] = [
    FieldMapping(
        source_field="payment_due_days",
        target_field="sale_payment_due_days",
        transform="to_int",
        default=14,
    ),
    FieldMapping(
        source_field="credit_limit",
        target_field="sale_credit_limit",
        transform="to_decimal",
        default=0,
    ),
    FieldMapping(
        source_field="discount_percent",
        target_field="sale_discount_percent",
        transform="to_decimal",
        default=0,
    ),
    FieldMapping(
        source_field="currency",
        target_field="sale_currency_code",
        transform="strip",
        default="EUR",
    ),
]


# ---------------------------------------------------------------------------
# partner_catalog_addresses — adresy (type = 'registered')
# ---------------------------------------------------------------------------
PAB_ADDRESS_MAPPINGS: list[FieldMapping] = [
    FieldMapping(
        source_field="street",
        target_field="street",
        transform="strip",
    ),
    FieldMapping(
        source_field="city",
        target_field="city",
        transform="strip",
    ),
    FieldMapping(
        source_field="zip_code",
        target_field="zip_code",
        transform="strip",
    ),
    FieldMapping(
        source_field="country_code",
        target_field="country_code",
        transform="country_code",
        default="SK",
    ),
]


# ---------------------------------------------------------------------------
# partner_catalog_contacts — kontakty (type = 'main')
# ---------------------------------------------------------------------------
PAB_CONTACT_MAPPINGS: list[FieldMapping] = [
    FieldMapping(
        source_field="phone",
        target_field="phone_work",
        transform="strip",
    ),
    FieldMapping(
        source_field="mobile",
        target_field="phone_mobile",
        transform="strip",
    ),
    FieldMapping(
        source_field="email",
        target_field="email",
        transform="strip",
    ),
    FieldMapping(
        source_field="contact_person",
        target_field="last_name",
        transform="strip",
    ),
]


# ---------------------------------------------------------------------------
# partner_catalog_bank_accounts
# ---------------------------------------------------------------------------
PAB_BANK_ACCOUNT_MAPPINGS: list[FieldMapping] = [
    FieldMapping(
        source_field="iban",
        target_field="iban_code",
        transform="strip",
    ),
    FieldMapping(
        source_field="bank_name",
        target_field="bank_name",
        transform="strip",
    ),
    FieldMapping(
        source_field="swift_bic",
        target_field="swift_code",
        transform="strip",
    ),
]


# ---------------------------------------------------------------------------
# Backward-compatible aggregate (for code that imports FIELD_MAPPINGS)
# ---------------------------------------------------------------------------
FIELD_MAPPINGS = {
    "header": PAB_HEADER_MAPPINGS,
    "extensions": PAB_EXTENSIONS_MAPPINGS,
    "addresses": PAB_ADDRESS_MAPPINGS,
    "contacts": PAB_CONTACT_MAPPINGS,
    "bank_accounts": PAB_BANK_ACCOUNT_MAPPINGS,
}


# ---------------------------------------------------------------------------
# PAB_FIELD_MAPPINGS — Btrieve→JSON extraction mappings (used by PABExtractor).
# source_field = nexdata PABRecord attribute name
# target_field = intermediate JSON field name (consumed by PABTransformer)
# ---------------------------------------------------------------------------
PAB_FIELD_MAPPINGS: list[FieldMapping] = [
    # Primary key / identification
    FieldMapping(
        source_field="pab_code",
        target_field="code",
        required=True,
        transform="to_str_strip",
    ),
    FieldMapping(
        source_field="name1",
        target_field="name",
        required=True,
        transform="strip",
    ),
    # Partner type — Btrieve: int (1=supplier, 2=customer, 3=both)
    FieldMapping(
        source_field="partner_type",
        target_field="partner_type",
        transform="map_partner_type_int",
        default="customer",
    ),
    # Tax / company identifiers
    FieldMapping(source_field="ico", target_field="company_id", transform="strip"),
    FieldMapping(source_field="dic", target_field="tax_id", transform="strip"),
    FieldMapping(source_field="ic_dph", target_field="vat_id", transform="strip"),
    FieldMapping(
        source_field="vat_payer",
        target_field="is_vat_payer",
        transform="to_bool",
        default=False,
    ),
    # Address
    FieldMapping(source_field="street", target_field="street", transform="strip"),
    FieldMapping(source_field="city", target_field="city", transform="strip"),
    FieldMapping(source_field="zip_code", target_field="zip_code", transform="strip"),
    FieldMapping(
        source_field="country",
        target_field="country_code",
        transform="country_code",
        default="SK",
    ),
    # Contact
    FieldMapping(source_field="phone", target_field="phone", transform="strip"),
    FieldMapping(source_field="fax", target_field="mobile", transform="strip"),
    FieldMapping(source_field="email", target_field="email", transform="strip"),
    FieldMapping(source_field="web", target_field="website", transform="strip"),
    FieldMapping(
        source_field="contact_person",
        target_field="contact_person",
        transform="strip",
    ),
    # Business terms
    FieldMapping(
        source_field="payment_terms",
        target_field="payment_due_days",
        transform="to_int",
        default=14,
    ),
    FieldMapping(
        source_field="credit_limit",
        target_field="credit_limit",
        transform="to_decimal",
        default=0,
    ),
    FieldMapping(
        source_field="discount_percent",
        target_field="discount_percent",
        transform="to_decimal",
        default=0,
    ),
    # Payment / currency — PAB nemá priamo tieto polia, použijeme default
    FieldMapping(
        source_field="_payment_method",
        target_field="payment_method",
        default="transfer",
    ),
    FieldMapping(source_field="_currency", target_field="currency", default="EUR"),
    # Bank info
    FieldMapping(source_field="iban", target_field="iban", transform="strip"),
    FieldMapping(source_field="bank_name", target_field="bank_name", transform="strip"),
    FieldMapping(source_field="swift", target_field="swift_bic", transform="strip"),
    # Notes — PAB has note, note2, internal_note → combined into notes
    FieldMapping(source_field="note", target_field="notes", transform="combine_notes"),
    # Status
    FieldMapping(
        source_field="active",
        target_field="is_active",
        transform="to_bool",
        default=True,
    ),
    # Derived flags from partner_type int
    FieldMapping(
        source_field="partner_type",
        target_field="is_supplier",
        transform="is_supplier_from_type",
        default=False,
    ),
    FieldMapping(
        source_field="partner_type",
        target_field="is_customer",
        transform="is_customer_from_type",
        default=True,
    ),
]
