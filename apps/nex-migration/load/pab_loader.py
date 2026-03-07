"""
PABLoader — INSERT structured PAB records into the normalized partner_catalog* schema.

Target tables (6):
  - partner_catalog          (header — INTEGER PK partner_id from PAB code)
  - partner_catalog_extensions (business terms — 1:1 with header)
  - partner_catalog_addresses  (registered address — 1:N)
  - partner_catalog_contacts   (phone/email/person — 1:N)
  - partner_catalog_bank_accounts (IBAN/SWIFT — 1:N)
  - partner_catalog_texts      (notes — 1:N)

Uses pg8000 driver (NEVER psycopg2/asyncpg).
After INSERT, writes mapping to migration_id_map.
INSERT trigger partner_catalog_init_version auto-creates history — NO manual insert.
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
# SQL statements
# ---------------------------------------------------------------------------

_INSERT_HEADER = """
    INSERT INTO partner_catalog (
        partner_id, partner_name, company_id, tax_id, vat_id,
        is_vat_payer, is_supplier, is_customer, street, city, zip_code,
        country_code, partner_class, is_active, created_by, updated_by
    ) VALUES (
        %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s
    )
    RETURNING partner_id
"""

_INSERT_EXTENSIONS = """
    INSERT INTO partner_catalog_extensions (
        partner_id, sale_payment_due_days, sale_credit_limit,
        sale_discount_percent, sale_currency_code, created_by, updated_by
    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

_INSERT_ADDRESS = """
    INSERT INTO partner_catalog_addresses (
        partner_id, address_type, street, city, zip_code,
        country_code, created_by, updated_by
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
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

_INSERT_TEXT = """
    INSERT INTO partner_catalog_texts (
        partner_id, text_type, line_number, language,
        text_content, created_by, updated_by
    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
"""


class PABLoader(BaseLoader):
    """Load structured PAB records into normalized partner_catalog* tables."""

    def __init__(self, db_config: dict):
        super().__init__(db_config=db_config)
        self.category = "PAB"

    # ------------------------------------------------------------------
    # Abstract method implementation
    # ------------------------------------------------------------------

    def load(self, records: list[dict]) -> None:
        """INSERT records into partner_catalog* in batches."""
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
                partner_id = self._insert_record(cursor, record)

                self.stats["inserted"] += 1

                # Write ID mapping
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

    def _insert_record(self, cursor, record: dict) -> int:
        """Insert a single structured record into all partner_catalog* tables.

        Returns the partner_id.
        """
        header = record["header"]

        # 1. Insert header → partner_catalog
        #    Trigger partner_catalog_init_version auto-creates history entry
        cursor.execute(
            _INSERT_HEADER,
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

        # 2. Insert extensions → partner_catalog_extensions
        extensions = record.get("extensions")
        if extensions:
            cursor.execute(
                _INSERT_EXTENSIONS,
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

        # 3. Insert addresses → partner_catalog_addresses
        for addr in record.get("addresses", []):
            cursor.execute(
                _INSERT_ADDRESS,
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

        # 4. Insert contacts → partner_catalog_contacts
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

        # 5. Insert bank accounts → partner_catalog_bank_accounts
        for bank in record.get("bank_accounts", []):
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

            # Update bank_account_count on partner_catalog
            cursor.execute(
                "UPDATE partner_catalog SET bank_account_count = "
                "bank_account_count + 1 WHERE partner_id = %s",
                (partner_id,),
            )

        # 6. Insert texts → partner_catalog_texts
        for text in record.get("texts", []):
            cursor.execute(
                _INSERT_TEXT,
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

        return partner_id
