"""
Field mapping configuration: Btrieve fields → PostgreSQL columns.

Source field names match the nexdata PAB model (PABRecord dataclass).
Target field names match the PostgreSQL 'partners' table schema.
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


# PAB — Partner field mappings
# source_field = nexdata PABRecord attribute names
# target_field = PostgreSQL partners table column names
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
    # PostgreSQL: varchar ('customer', 'supplier', 'both')
    FieldMapping(
        source_field="partner_type",
        target_field="partner_type",
        transform="map_partner_type_int",
        default="customer",
    ),
    # Tax / company identifiers
    FieldMapping(
        source_field="ico",
        target_field="company_id",
        transform="strip",
    ),
    FieldMapping(
        source_field="dic",
        target_field="tax_id",
        transform="strip",
    ),
    FieldMapping(
        source_field="ic_dph",
        target_field="vat_id",
        transform="strip",
    ),
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
    # PAB model has 'fax' — mapped to 'mobile' only if no dedicated mobile field
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
    FieldMapping(
        source_field="_currency",
        target_field="currency",
        default="EUR",
    ),
    # Bank info
    FieldMapping(source_field="iban", target_field="iban", transform="strip"),
    FieldMapping(source_field="bank_name", target_field="bank_name", transform="strip"),
    FieldMapping(source_field="swift", target_field="swift_bic", transform="strip"),
    # Notes — PAB has note, note2, internal_note → combined into notes
    FieldMapping(
        source_field="note",
        target_field="notes",
        transform="combine_notes",
    ),
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
