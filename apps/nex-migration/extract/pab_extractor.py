"""
PABExtractor — extracts partner records from Btrieve PAB table via nexdata.

Lazy-imports nexdata inside extract methods so that the module
can be imported and tested on Linux CI without nexdata installed.

Output: data/PAB/PAB.json
"""

import json
from datetime import datetime
from decimal import Decimal
from pathlib import Path

from config.field_mappings import PAB_FIELD_MAPPINGS
from extract.base_extractor import BaseExtractor, DateTimeEncoder


class PABExtractor(BaseExtractor):
    """Extracts partners from Btrieve PAB table and saves as JSON."""

    def __init__(self, data_dir: str = "data", data_root: str | None = None):
        super().__init__(data_dir=data_dir, data_root=data_root)
        self.category = "PAB"

    def get_source_tables(self) -> list[str]:
        return ["PAB"]

    def _build_btrieve_config(self) -> dict:
        """Build BtrieveClient config dict with table path derived from data_root."""
        pab_path = str(self.data_root / "YEARACT" / "DIALS" / "PAB00000.BTR")
        return {
            "data_root": str(self.data_root),
            "nex_genesis": {
                "tables": {
                    "pab": pab_path,
                },
            },
        }

    def extract_table(self, table_name: str) -> list[dict]:
        """Extract records from PAB Btrieve table via nexdata (lazy import)."""
        # Lazy import — nexdata is only available on Windows with 32-bit Python
        import nexdata  # noqa: F811

        config = self._build_btrieve_config()
        client = nexdata.BtrieveClient(config)
        repo = nexdata.PABRepository(client)
        try:
            repo.open()
            raw_records = repo.get_all()
        finally:
            repo.close()
        return [self._map_record(rec) for rec in raw_records]

    # ------------------------------------------------------------------
    # Field mapping
    # ------------------------------------------------------------------

    def _map_record(self, record) -> dict:
        """Map a single nexdata PABRecord to output dict using PAB_FIELD_MAPPINGS."""
        mapped: dict = {}
        for fm in PAB_FIELD_MAPPINGS:
            value = getattr(record, fm.source_field, fm.default)
            if value is None:
                value = fm.default
            if fm.transform and value is not None:
                value = self._apply_transform(fm.transform, value, record)
            mapped[fm.target_field] = value

        # Primary key from Btrieve — always pab_code
        mapped["_source_key"] = self._source_key(record)
        return mapped

    def _source_key(self, record) -> str:
        """Return string primary key for the PAB record."""
        raw = getattr(record, "pab_code", "")
        return str(raw).strip()

    # ------------------------------------------------------------------
    # Transforms
    # ------------------------------------------------------------------

    @staticmethod
    def _apply_transform(transform: str, value, record=None):
        """Apply a named transform to a field value."""
        if transform == "strip":
            return str(value).strip() if value else ""
        if transform == "to_str_strip":
            return str(value).strip()
        if transform == "to_int":
            try:
                return int(value)
            except (TypeError, ValueError):
                return 0
        if transform == "to_decimal":
            try:
                return float(Decimal(str(value)))
            except (TypeError, ValueError):
                return 0.0
        if transform == "to_bool":
            if isinstance(value, bool):
                return value
            if isinstance(value, (int, float)):
                return bool(value)
            if isinstance(value, str):
                return value.strip().lower() in ("1", "true", "yes", "y", "a")
            return False
        if transform == "map_partner_type_int":
            mapping = {1: "supplier", 2: "customer", 3: "both"}
            try:
                return mapping.get(int(value), "customer")
            except (TypeError, ValueError):
                return "customer"
        if transform == "is_supplier_from_type":
            try:
                return int(value) in (1, 3)
            except (TypeError, ValueError):
                return False
        if transform == "is_customer_from_type":
            try:
                return int(value) in (2, 3)
            except (TypeError, ValueError):
                return True
        if transform == "country_code":
            code = str(value).strip().upper()
            return code if len(code) == 2 else "SK"
        if transform == "combine_notes":
            parts = [str(value).strip()] if value else []
            if record is not None:
                for extra_field in ("note2", "internal_note"):
                    extra = getattr(record, extra_field, None)
                    if extra:
                        parts.append(str(extra).strip())
            return " | ".join(parts) if parts else ""
        # Unknown transform — return as-is
        return value

    # ------------------------------------------------------------------
    # Override run() to produce the flat JSON output format from task spec
    # ------------------------------------------------------------------

    def extract(self) -> Path:
        """
        High-level extraction: read PAB via nexdata, map fields, write JSON.

        Returns the path to the output JSON file.
        """
        output_dir = self.data_dir / self.category
        output_dir.mkdir(parents=True, exist_ok=True)

        records: list[dict] = []
        errors: list[dict] = []
        total_source = 0

        # Lazy import nexdata
        import nexdata  # noqa: F811

        config = self._build_btrieve_config()
        client = nexdata.BtrieveClient(config)
        repo = nexdata.PABRepository(client)
        try:
            repo.open()
            raw_records = repo.get_all()
        finally:
            repo.close()
        total_source = len(raw_records)

        for raw in raw_records:
            try:
                mapped = self._map_record(raw)
                records.append(mapped)
            except Exception as e:
                errors.append(
                    {
                        "source_key": self._source_key(raw),
                        "error": str(e),
                    }
                )

        output_file = output_dir / "PAB.json"
        payload = {
            "category": self.category,
            "extracted_at": datetime.now().isoformat(),
            "total_source": total_source,
            "total_extracted": len(records),
            "error_count": len(errors),
            "records": records,
            "errors": errors,
        }
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(payload, f, cls=DateTimeEncoder, ensure_ascii=False, indent=2)

        print(f"PABExtractor: {len(records)}/{total_source} records → {output_file}")
        if errors:
            print(f"  Errors: {len(errors)}")

        return output_file
