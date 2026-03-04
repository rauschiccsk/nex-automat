"""
Base extractor — abstraktná trieda pre všetky extractory.
Beží na Windows CC s venv32 (32-bit Python pre Btrieve).
Výstup: JSON súbory v data/{category}/ adresári.
"""

import json
from abc import ABC, abstractmethod
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path


class DateTimeEncoder(json.JSONEncoder):
    """JSON encoder pre datetime, date, Decimal a bytes."""

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, date):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, bytes):
            return obj.decode("utf-8", errors="replace")
        return super().default(obj)


class BaseExtractor(ABC):
    r"""
    Abstraktná trieda pre extrakciu dát z Btrieve tabuliek.

    Subclass musí implementovať:
    - get_source_tables() → list tabuľkových mien
    - extract_table(table_name) → list dict záznamov

    Args:
        data_dir: Output directory for JSON files.
        data_root: Base path to NEX Genesis data (e.g. C:\NEX, C:\DEPTEST\NEX).
    """

    DEFAULT_DATA_ROOT = r"C:\NEX"

    def __init__(self, data_dir: str = "data", data_root: str | None = None):
        self.data_dir = Path(data_dir)
        self.data_root = Path(data_root) if data_root else Path(self.DEFAULT_DATA_ROOT)
        self.category: str = ""
        self.stats: dict[str, int] = {}

    @abstractmethod
    def get_source_tables(self) -> list[str]:
        """Vráti zoznam Btrieve tabuliek na extrakciu."""
        ...

    @abstractmethod
    def extract_table(self, table_name: str) -> list[dict]:
        """Extrahuje všetky záznamy z jednej Btrieve tabuľky."""
        ...

    def run(self) -> dict[str, int]:
        """Spustí extrakciu všetkých tabuliek a uloží JSON súbory."""
        output_dir = self.data_dir / self.category
        output_dir.mkdir(parents=True, exist_ok=True)

        print(f"\n{'=' * 60}")
        print(f"EXTRACT: {self.category}")
        print(f"DATA ROOT: {self.data_root}")
        print(f"{'=' * 60}")

        for table_name in self.get_source_tables():
            print(f"\n  Extracting {table_name}...", end=" ")
            try:
                records = self.extract_table(table_name)
                count = len(records)
                output_file = output_dir / f"{table_name}.json"
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(
                        {
                            "table": table_name,
                            "category": self.category,
                            "extracted_at": datetime.now().isoformat(),
                            "count": count,
                            "records": records,
                        },
                        f,
                        cls=DateTimeEncoder,
                        ensure_ascii=False,
                        indent=2,
                    )
                self.stats[table_name] = count
                print(f"OK ({count} records)")
            except Exception as e:
                self.stats[table_name] = -1
                print(f"FAILED: {e}")

        print(f"\n{'=' * 60}")
        print(f"EXTRACT SUMMARY: {self.category}")
        for table, count in self.stats.items():
            status = f"{count} records" if count >= 0 else "FAILED"
            print(f"  {table}: {status}")
        total = sum(c for c in self.stats.values() if c >= 0)
        failed = sum(1 for c in self.stats.values() if c < 0)
        print(f"  TOTAL: {total} records, {failed} failures")
        print(f"{'=' * 60}\n")

        return self.stats
