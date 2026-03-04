"""
Base transformer — konverzia extrahovaných JSON dát na PostgreSQL-ready records.
"""

import json
from abc import ABC, abstractmethod
from pathlib import Path


class BaseTransformer(ABC):
    """
    Abstraktná trieda pre transformáciu extrahovaných dát.

    Subclass musí implementovať:
    - transform() → list transformovaných záznamov
    - validate_record(record, index) → bool
    """

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.category: str = ""
        self.errors: list[dict] = []
        self.warnings: list[dict] = []
        self.stats = {"total": 0, "valid": 0, "errors": 0, "warnings": 0}

    def read_extracted_data(self, table_name: str) -> list[dict]:
        """Načíta extrahované JSON dáta pre danú tabuľku."""
        json_file = self.data_dir / self.category / f"{table_name}.json"
        if not json_file.exists():
            raise FileNotFoundError(f"Extract file not found: {json_file}")
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data["records"]

    @abstractmethod
    def transform(self) -> list[dict]:
        """Transformuj extrahované dáta na PostgreSQL-ready záznamy."""
        ...

    @abstractmethod
    def validate_record(self, record: dict, index: int) -> bool:
        """Validuj jeden transformovaný záznam. Vráti True ak je validný."""
        ...

    def add_error(self, index: int, source_key: str, field: str, message: str):
        """Pridaj chybu do error logu."""
        self.errors.append(
            {"index": index, "source_key": source_key, "field": field, "message": message}
        )
        self.stats["errors"] += 1

    def add_warning(self, index: int, source_key: str, field: str, message: str):
        """Pridaj varovanie do warning logu."""
        self.warnings.append(
            {"index": index, "source_key": source_key, "field": field, "message": message}
        )
        self.stats["warnings"] += 1

    def run(self) -> tuple[list[dict], dict]:
        """Spustí transformáciu a vráti (záznamy, štatistiky)."""
        print(f"\n{'=' * 60}")
        print(f"TRANSFORM: {self.category}")
        print(f"{'=' * 60}")

        records = self.transform()

        print(f"\n  TRANSFORM SUMMARY:")
        print(f"  Total source: {self.stats['total']}")
        print(f"  Valid:        {self.stats['valid']}")
        print(f"  Errors:       {self.stats['errors']}")
        print(f"  Warnings:     {self.stats['warnings']}")
        if self.errors:
            print(f"\n  ERRORS (first 10):")
            for err in self.errors[:10]:
                print(f"    [{err['index']}] {err['source_key']}.{err['field']}: {err['message']}")
        print(f"{'=' * 60}\n")

        return records, self.stats
