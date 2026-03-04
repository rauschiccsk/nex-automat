"""
PABLoader — UPSERT transformed PAB records into the PostgreSQL partners table.

Uses pg8000 driver (NEVER psycopg2/asyncpg).
After each INSERT/UPDATE, writes a mapping to migration_id_map.
Processes records in batches of 100.
"""

import sys
from pathlib import Path

# Ensure nex-migration root is on sys.path for config imports
_migration_root = str(Path(__file__).resolve().parent.parent)
if _migration_root not in sys.path:
    sys.path.insert(0, _migration_root)

from load.base_loader import BaseLoader

# Columns for UPSERT (all partners columns except id, created_at, created_by)
_UPSERT_COLUMNS = [
    "code",
    "name",
    "partner_type",
    "is_supplier",
    "is_customer",
    "company_id",
    "tax_id",
    "vat_id",
    "is_vat_payer",
    "street",
    "city",
    "zip_code",
    "country_code",
    "phone",
    "mobile",
    "email",
    "website",
    "contact_person",
    "payment_due_days",
    "credit_limit",
    "discount_percent",
    "payment_method",
    "currency",
    "iban",
    "bank_name",
    "swift_bic",
    "notes",
    "is_active",
]

# Columns to update on conflict (exclude code — that's the conflict key)
_UPDATE_COLUMNS = [col for col in _UPSERT_COLUMNS if col != "code"]

BATCH_SIZE = 100


def _build_upsert_sql() -> str:
    """Build the UPSERT SQL statement for partners table."""
    cols = ", ".join(_UPSERT_COLUMNS)
    placeholders = ", ".join(["%s"] * len(_UPSERT_COLUMNS))
    update_set = ", ".join(
        f"{col} = EXCLUDED.{col}" for col in _UPDATE_COLUMNS
    )

    return (
        f"INSERT INTO partners ({cols}) "
        f"VALUES ({placeholders}) "
        f"ON CONFLICT (code) DO UPDATE SET {update_set}, "
        f"updated_at = NOW(), updated_by = 'migration' "
        f"RETURNING id, (xmax = 0) AS is_insert"
    )


class PABLoader(BaseLoader):
    """Load transformed PAB records into PostgreSQL partners table."""

    def __init__(self, db_config: dict):
        super().__init__(db_config=db_config)
        self.category = "PAB"
        self._upsert_sql = _build_upsert_sql()

    # ------------------------------------------------------------------
    # Abstract method implementation
    # ------------------------------------------------------------------

    def load(self, records: list[dict]) -> None:
        """UPSERT records into partners in batches of 100."""
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
        """Process a single batch of records."""
        for idx, record in enumerate(batch):
            source_key = record.get("_source_key", "")
            try:
                values = self._extract_values(record)
                cursor.execute(self._upsert_sql, values)
                row = cursor.fetchone()

                if row:
                    target_id = str(row[0])
                    is_insert = row[1]

                    if is_insert:
                        self.stats["inserted"] += 1
                    else:
                        self.stats["updated"] += 1

                    # Write ID mapping
                    self.add_id_mapping(
                        source_table="PAB",
                        source_key=source_key,
                        target_table="partners",
                        target_id=target_id,
                    )

            except Exception as e:
                self.stats["errors"] += 1
                print(f"    ERROR [{offset + idx}] {source_key}: {e}")
                # Rollback the current transaction and start fresh
                self.conn.rollback()

    @staticmethod
    def _extract_values(record: dict) -> tuple:
        """Extract values from record dict in the order matching _UPSERT_COLUMNS."""
        return tuple(record.get(col) for col in _UPSERT_COLUMNS)
