"""
PABLoader — UPSERT structured PAB records into the normalized partner_catalog* schema.

Target tables (6):
  - partner_catalog          (header — INTEGER PK partner_id from PAB code)
  - partner_catalog_extensions (business terms — 1:1 with header)
  - partner_catalog_addresses  (1:N — UNIQUE on partner_id+address_type)
  - partner_catalog_contacts   (1:N — no natural unique → DELETE+INSERT)
  - partner_catalog_bank_accounts (1:N — no natural unique → DELETE+INSERT)
  - partner_catalog_texts      (1:N — UNIQUE on partner_id+text_type+line_number+language)

Uses pg8000 driver (NEVER psycopg2/asyncpg).
After INSERT/UPDATE, writes mapping to migration_id_map (UPSERT — see base_loader).

Re-runnable: ON CONFLICT DO UPDATE on tables with natural unique keys; DELETE + INSERT
for child tables without (contacts, bank_accounts). xmax==0 detects insert-vs-update.

Triggers:
  - trg_partner_catalog_init_version (AFTER INSERT) — initial history row
  - trg_partner_catalog_versioning (BEFORE UPDATE WHEN key fields change) — history row on update
  Both fire correctly under UPSERT pattern.

Processes records in batches.
"""

import sys
from pathlib import Path

from nex_config.limits import PAB_BATCH_SIZE

# Ensure nex-migration root is on sys.path for config imports
_migration_root = str(Path(__file__).resolve().parent.parent)
if _migration_root not in sys.path:
    sys.path.insert(0, _migration_root)

from load.base_loader import BaseLoader

BATCH_SIZE = PAB_BATCH_SIZE

# ---------------------------------------------------------------------------
# SQL statements — UPSERT pattern for re-runnable migration
# ---------------------------------------------------------------------------

_UPSERT_HEADER = """
    INSERT INTO partner_catalog (
        partner_id, partner_name, company_id, tax_id, vat_id,
        is_vat_payer, is_supplier, is_customer, street, city, zip_code,
        country_code, partner_class, is_active, created_by, updated_by
    ) VALUES (
        %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s
    )
    ON CONFLICT (partner_id) DO UPDATE SET
        partner_name = EXCLUDED.partner_name,
        company_id = EXCLUDED.company_id,
        tax_id = EXCLUDED.tax_id,
        vat_id = EXCLUDED.vat_id,
        is_vat_payer = EXCLUDED.is_vat_payer,
        is_supplier = EXCLUDED.is_supplier,
        is_customer = EXCLUDED.is_customer,
        street = EXCLUDED.street,
        city = EXCLUDED.city,
        zip_code = EXCLUDED.zip_code,
        country_code = EXCLUDED.country_code,
        partner_class = EXCLUDED.partner_class,
        is_active = EXCLUDED.is_active,
        updated_by = EXCLUDED.updated_by
    RETURNING partner_id, (xmax = 0) AS was_inserted
"""

_UPSERT_EXTENSIONS = """
    INSERT INTO partner_catalog_extensions (
        partner_id, sale_payment_due_days, sale_credit_limit,
        sale_discount_percent, sale_currency_code, created_by, updated_by
    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (partner_id) DO UPDATE SET
        sale_payment_due_days = EXCLUDED.sale_payment_due_days,
        sale_credit_limit = EXCLUDED.sale_credit_limit,
        sale_discount_percent = EXCLUDED.sale_discount_percent,
        sale_currency_code = EXCLUDED.sale_currency_code,
        updated_by = EXCLUDED.updated_by
"""

_UPSERT_ADDRESS = """
    INSERT INTO partner_catalog_addresses (
        partner_id, address_type, street, city, zip_code,
        country_code, created_by, updated_by
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (partner_id, address_type) DO UPDATE SET
        street = EXCLUDED.street,
        city = EXCLUDED.city,
        zip_code = EXCLUDED.zip_code,
        country_code = EXCLUDED.country_code,
        updated_by = EXCLUDED.updated_by
"""

_INSERT_CONTACT = """
    INSERT INTO partner_catalog_contacts (
        partner_id, contact_type, last_name, phone_work, phone_mobile,
        email, country_code, created_by, updated_by
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

_INSERT_BANK_ACCOUNT = """
    INSERT INTO partner_catalog_bank_accounts (
        partner_id, iban_code, bank_name, swift_code,
        is_primary, created_by, updated_by
    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

_UPSERT_TEXT = """
    INSERT INTO partner_catalog_texts (
        partner_id, text_type, line_number, language,
        text_content, created_by, updated_by
    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (partner_id, text_type, line_number, language) DO UPDATE SET
        text_content = EXCLUDED.text_content,
        updated_by = EXCLUDED.updated_by
"""

_DELETE_CONTACTS_FOR_PARTNER = (
    "DELETE FROM partner_catalog_contacts WHERE partner_id = %s"
)
_DELETE_BANK_ACCOUNTS_FOR_PARTNER = (
    "DELETE FROM partner_catalog_bank_accounts WHERE partner_id = %s"
)


class PABLoader(BaseLoader):
    """Load structured PAB records into normalized partner_catalog* tables."""

    def __init__(self, db_config: dict):
        super().__init__(db_config=db_config)
        self.category = "PAB"

    # ------------------------------------------------------------------
    # Abstract method implementation
    # ------------------------------------------------------------------

    def load(self, records: list[dict]) -> None:
        """UPSERT records into partner_catalog* in batches."""
        total = len(records)
        cursor = self.conn.cursor()

        for batch_start in range(0, total, BATCH_SIZE):
            batch = records[batch_start : batch_start + BATCH_SIZE]
            self._load_batch(cursor, batch, batch_start)
            self.conn.commit()

            loaded = min(batch_start + BATCH_SIZE, total)
            print(f"    Batch {loaded}/{total} committed")

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _load_batch(self, cursor, batch: list[dict], offset: int) -> None:
        """Process a single batch of structured records."""
        for idx, record in enumerate(batch):
            source_key = record.get("_source_key", "")
            try:
                partner_id, was_inserted = self._upsert_record(cursor, record)

                if was_inserted:
                    self.stats["inserted"] += 1
                else:
                    self.stats["updated"] += 1

                # Write ID mapping (already UPSERT in base_loader.add_id_mapping)
                self.add_id_mapping(
                    source_table="PAB",
                    source_key=source_key,
                    target_table="partner_catalog",
                    target_id=str(partner_id),
                )

            except Exception as e:
                self.stats["errors"] += 1
                print(f"    ERROR [{offset + idx}] {source_key}: {e}")
                # Rollback the current transaction and start fresh
                self.conn.rollback()

    def _upsert_record(self, cursor, record: dict) -> tuple[int, bool]:
        """UPSERT a single structured record into all partner_catalog* tables.

        Returns (partner_id, was_inserted) where was_inserted=True for fresh rows.
        """
        header = record["header"]

        # 1. UPSERT header → partner_catalog
        #    INSERT trigger creates history, BEFORE-UPDATE trigger creates new
        #    history entry when key fields change.
        cursor.execute(
            _UPSERT_HEADER,
            (
                header["partner_id"],
                header["partner_name"],
                header.get("company_id"),
                header.get("tax_id"),
                header.get("vat_id"),
                header.get("is_vat_payer", False),
                header.get("is_supplier", False),
                header.get("is_customer", True),
                header.get("street"),
                header.get("city"),
                header.get("zip_code"),
                header.get("country_code", "SK"),
                header.get("partner_class", "business"),
                header.get("is_active", True),
                header.get("created_by", "migration"),
                header.get("updated_by", "migration"),
            ),
        )
        row = cursor.fetchone()
        partner_id = row[0]
        was_inserted = bool(row[1])

        # 2. UPSERT extensions → partner_catalog_extensions (PK = partner_id)
        extensions = record.get("extensions")
        if extensions:
            cursor.execute(
                _UPSERT_EXTENSIONS,
                (
                    partner_id,
                    extensions.get("sale_payment_due_days", 14),
                    extensions.get("sale_credit_limit", 0),
                    extensions.get("sale_discount_percent", 0),
                    extensions.get("sale_currency_code", "EUR"),
                    extensions.get("created_by", "migration"),
                    extensions.get("updated_by", "migration"),
                ),
            )

        # 3. Reset 1:N children that have no natural unique key.
        #    Re-runs would otherwise duplicate or orphan rows.
        cursor.execute(_DELETE_CONTACTS_FOR_PARTNER, (partner_id,))
        cursor.execute(_DELETE_BANK_ACCOUNTS_FOR_PARTNER, (partner_id,))

        # 4. UPSERT addresses (UNIQUE on partner_id, address_type)
        for addr in record.get("addresses", []):
            cursor.execute(
                _UPSERT_ADDRESS,
                (
                    partner_id,
                    addr.get("address_type", "registered"),
                    addr.get("street"),
                    addr.get("city"),
                    addr.get("zip_code"),
                    addr.get("country_code", "SK"),
                    addr.get("created_by", "migration"),
                    addr.get("updated_by", "migration"),
                ),
            )

        # 5. INSERT contacts (children deleted in step 3, fresh insert)
        for contact in record.get("contacts", []):
            cursor.execute(
                _INSERT_CONTACT,
                (
                    partner_id,
                    contact.get("contact_type", "main"),
                    contact.get("last_name"),
                    contact.get("phone_work"),
                    contact.get("phone_mobile"),
                    contact.get("email"),
                    contact.get("country_code", "SK"),
                    contact.get("created_by", "migration"),
                    contact.get("updated_by", "migration"),
                ),
            )

        # 6. INSERT bank accounts + set bank_account_count to actual count
        bank_accounts = record.get("bank_accounts", [])
        for bank in bank_accounts:
            cursor.execute(
                _INSERT_BANK_ACCOUNT,
                (
                    partner_id,
                    bank.get("iban_code"),
                    bank.get("bank_name"),
                    bank.get("swift_code"),
                    bank.get("is_primary", True),
                    bank.get("created_by", "migration"),
                    bank.get("updated_by", "migration"),
                ),
            )
        # Set bank_account_count atomically (instead of incrementing — re-runs
        # with the increment pattern would double-count).
        cursor.execute(
            "UPDATE partner_catalog SET bank_account_count = %s WHERE partner_id = %s",
            (len(bank_accounts), partner_id),
        )

        # 7. UPSERT texts (UNIQUE on partner_id, text_type, line_number, language)
        for text in record.get("texts", []):
            cursor.execute(
                _UPSERT_TEXT,
                (
                    partner_id,
                    text.get("text_type", "notes"),
                    text.get("line_number", 1),
                    text.get("language", "sk"),
                    text.get("text_content"),
                    text.get("created_by", "migration"),
                    text.get("updated_by", "migration"),
                ),
            )

        return partner_id, was_inserted
