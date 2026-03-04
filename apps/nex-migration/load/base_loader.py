"""
Base loader — UPSERT transformovaných dát do PostgreSQL.
Používa pg8000 driver (NIKDY psycopg2, asyncpg).
"""

import json
from abc import ABC, abstractmethod

import pg8000


class BaseLoader(ABC):
    """
    Abstraktná trieda pre loading dát do PostgreSQL.

    Subclass musí implementovať:
    - load(records) → None
    """

    def __init__(self, db_config: dict):
        self.db_config = db_config
        self.category: str = ""
        self.batch_id: int | None = None
        self.conn: pg8000.Connection | None = None
        self.stats = {"inserted": 0, "updated": 0, "errors": 0, "mapped": 0}

    def connect(self):
        """Pripoj sa k PostgreSQL cez pg8000."""
        self.conn = pg8000.connect(**self.db_config)
        self.conn.autocommit = False

    def close(self):
        """Zatvor spojenie."""
        if self.conn:
            self.conn.close()

    def start_batch(self, source_count: int) -> int:
        """Vytvor nový migration batch a vráť jeho ID."""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO migration_batches (category, status, source_count) "
            "VALUES (%s, 'running', %s) RETURNING id",
            (self.category, source_count),
        )
        self.batch_id = cursor.fetchone()[0]
        self.conn.commit()
        return self.batch_id

    def complete_batch(self, error_log: list[dict] | None = None):
        """Označ batch ako dokončený."""
        cursor = self.conn.cursor()
        cursor.execute(
            """UPDATE migration_batches
               SET status = 'completed', target_count = %s, error_count = %s,
                   completed_at = NOW(), error_log = %s
               WHERE id = %s""",
            (
                self.stats["inserted"] + self.stats["updated"],
                self.stats["errors"],
                json.dumps(error_log) if error_log else None,
                self.batch_id,
            ),
        )
        cursor.execute(
            """UPDATE migration_category_status
               SET status = 'completed', last_batch_id = %s,
                   record_count = %s, last_migrated_at = NOW(),
                   first_migrated_at = COALESCE(first_migrated_at, NOW())
               WHERE category = %s""",
            (self.batch_id, self.stats["inserted"] + self.stats["updated"], self.category),
        )
        self.conn.commit()

    def fail_batch(self, error_message: str):
        """Označ batch ako neúspešný."""
        if self.conn and self.batch_id:
            cursor = self.conn.cursor()
            cursor.execute(
                "UPDATE migration_batches SET status = 'failed', "
                "completed_at = NOW(), error_log = %s WHERE id = %s",
                (json.dumps([{"error": error_message}]), self.batch_id),
            )
            cursor.execute(
                "UPDATE migration_category_status SET status = 'failed' "
                "WHERE category = %s",
                (self.category,),
            )
            self.conn.commit()

    def add_id_mapping(
        self, source_table: str, source_key: str, target_table: str, target_id: str
    ):
        """Pridaj mapovanie Btrieve key → PostgreSQL UUID."""
        cursor = self.conn.cursor()
        cursor.execute(
            """INSERT INTO migration_id_map
               (batch_id, category, source_table, source_key, target_table, target_id)
               VALUES (%s, %s, %s, %s, %s, %s)
               ON CONFLICT (category, source_table, source_key)
               DO UPDATE SET target_id = EXCLUDED.target_id, migrated_at = NOW()""",
            (self.batch_id, self.category, source_table, source_key, target_table, target_id),
        )
        self.stats["mapped"] += 1

    def get_mapped_id(self, source_table: str, source_key: str) -> str | None:
        """Nájdi existujúce UUID mapovanie pre Btrieve kľúč."""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT target_id FROM migration_id_map "
            "WHERE source_table = %s AND source_key = %s",
            (source_table, source_key),
        )
        row = cursor.fetchone()
        return str(row[0]) if row else None

    def check_dependencies(self) -> list[str]:
        """Skontroluj či sú všetky závislosti migrované."""
        import sys
        from pathlib import Path

        sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
        from config.categories import get_category

        category = get_category(self.category)
        missing = []
        cursor = self.conn.cursor()
        for dep in category.dependencies:
            cursor.execute(
                "SELECT status FROM migration_category_status WHERE category = %s",
                (dep,),
            )
            row = cursor.fetchone()
            if not row or row[0] != "completed":
                missing.append(dep)
        return missing

    @abstractmethod
    def load(self, records: list[dict]) -> None:
        """UPSERT transformované záznamy do PostgreSQL."""
        ...

    def run(self, records: list[dict]) -> dict:
        """Spustí loading pipeline: connect → check deps → batch → load → complete."""
        print(f"\n{'=' * 60}")
        print(f"LOAD: {self.category}")
        print(f"{'=' * 60}")
        try:
            self.connect()

            missing = self.check_dependencies()
            if missing:
                raise ValueError(f"Missing dependencies for {self.category}: {missing}")

            self.start_batch(len(records))
            print(f"  Batch #{self.batch_id} started, {len(records)} records to load")

            self.load(records)
            self.complete_batch()

            print("\n  LOAD SUMMARY:")
            print(f"  Inserted: {self.stats['inserted']}")
            print(f"  Updated:  {self.stats['updated']}")
            print(f"  Errors:   {self.stats['errors']}")
            print(f"  Mapped:   {self.stats['mapped']}")
            print(f"{'=' * 60}\n")
        except Exception as e:
            print(f"  LOAD FAILED: {e}")
            self.fail_batch(str(e))
            if self.conn:
                self.conn.rollback()
            raise
        finally:
            self.close()
        return self.stats
