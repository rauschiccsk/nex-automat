"""
Unit tests for PABTransformer — M5 (JSON → PostgreSQL-ready structured dicts).

Tests run on Linux CI without database access.
Uses unittest.mock and tmp directories to simulate extracted JSON data.

Transformer output is structured:
{
    "_source_key": "...",
    "header": { ... partner_catalog columns ... },
    "extensions": { ... partner_catalog_extensions ... } | None,
    "addresses": [ ... ],
    "contacts": [ ... ],
    "bank_accounts": [ ... ],
    "texts": [ ... ],
}
"""

import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

# Add nex-migration to sys.path so we can import transform/config modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "apps" / "nex-migration"))


from transform.pab_transformer import PABTransformer


def _make_pab_json(records: list[dict], tmp_path: Path) -> Path:
    """Create a fake data/PAB/PAB.json in tmp_path."""
    pab_dir = tmp_path / "PAB"
    pab_dir.mkdir(parents=True, exist_ok=True)
    data = {
        "category": "PAB",
        "extracted_at": "2025-01-01T00:00:00",
        "total_source": len(records),
        "total_extracted": len(records),
        "error_count": 0,
        "records": records,
        "errors": [],
    }
    json_file = pab_dir / "PAB.json"
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    return json_file


def _valid_raw_record(**overrides) -> dict:
    """Return a minimal valid raw record as it would appear in PAB.json."""
    defaults = {
        "_source_key": "10001",
        "code": "10001",
        "name": "Test Partner s.r.o.",
        "partner_type": 2,
        "is_supplier": False,
        "is_customer": True,
        "company_id": "12345678",
        "tax_id": "2012345678",
        "vat_id": "SK2012345678",
        "is_vat_payer": True,
        "street": "Hlavna 1",
        "city": "Bratislava",
        "zip_code": "81101",
        "country_code": "SK",
        "phone": "+421999888777",
        "mobile": "+421999888666",
        "email": "test@partner.sk",
        "website": "www.partner.sk",
        "contact_person": "Jan Novak",
        "payment_due_days": 30,
        "credit_limit": 5000.0,
        "discount_percent": 2.5,
        "payment_method": "transfer",
        "currency": "EUR",
        "iban": "SK3112000000198742637541",
        "bank_name": "Slovenska sporitelna",
        "swift_bic": "GIBASKBX",
        "notes": "Poznamka 1",
        "is_active": True,
    }
    defaults.update(overrides)
    return defaults


class TestPABTransformerValidRecord:
    """Test that valid records are correctly transformed."""

    def test_valid_record_returns_dict(self, tmp_path):
        """A valid record should produce a non-None transformed dict."""
        records = [_valid_raw_record()]
        _make_pab_json(records, tmp_path)

        transformer = PABTransformer(data_dir=str(tmp_path))
        result, stats = transformer.run()

        assert len(result) == 1
        assert stats["valid"] == 1
        assert stats["errors"] == 0
        assert stats["total"] == 1

    def test_valid_record_has_structured_output(self, tmp_path):
        """Transformed record should have structured format with header, extensions, etc."""
        records = [_valid_raw_record()]
        _make_pab_json(records, tmp_path)

        transformer = PABTransformer(data_dir=str(tmp_path))
        result, _ = transformer.run()
        rec = result[0]

        # Structured output must have these keys
        assert "_source_key" in rec
        assert rec["_source_key"] == "10001"
        assert "header" in rec
        assert "extensions" in rec
        assert "addresses" in rec
        assert "contacts" in rec
        assert "bank_accounts" in rec
        assert "texts" in rec

    def test_valid_record_header_has_correct_types(self, tmp_path):
        """Header should have correct Python types matching partner_catalog schema."""
        records = [_valid_raw_record()]
        _make_pab_json(records, tmp_path)

        transformer = PABTransformer(data_dir=str(tmp_path))
        result, _ = transformer.run()
        header = result[0]["header"]

        # Integer fields
        assert isinstance(header["partner_id"], int)
        assert header["partner_id"] == 10001

        # String fields
        assert isinstance(header["partner_name"], str)
        assert header["partner_name"] == "Test Partner s.r.o."

        # Boolean fields — derived from partner_type=2 (customer)
        assert isinstance(header["is_supplier"], bool)
        assert isinstance(header["is_customer"], bool)
        assert header["is_customer"] is True
        assert header["is_supplier"] is False
        assert isinstance(header["is_vat_payer"], bool)
        assert isinstance(header["is_active"], bool)

    def test_partner_type_supplier(self, tmp_path):
        """partner_type=1 should map to supplier flags in header."""
        records = [_valid_raw_record(partner_type=1)]
        _make_pab_json(records, tmp_path)

        transformer = PABTransformer(data_dir=str(tmp_path))
        result, _ = transformer.run()
        header = result[0]["header"]

        assert header["is_supplier"] is True
        assert header["is_customer"] is False

    def test_partner_type_both(self, tmp_path):
        """partner_type=3 should map to both supplier and customer."""
        records = [_valid_raw_record(partner_type=3)]
        _make_pab_json(records, tmp_path)

        transformer = PABTransformer(data_dir=str(tmp_path))
        result, _ = transformer.run()
        header = result[0]["header"]

        assert header["is_supplier"] is True
        assert header["is_customer"] is True

    def test_multiple_records(self, tmp_path):
        """Multiple valid records should all be transformed."""
        records = [
            _valid_raw_record(_source_key="001", code="001", name="Partner A"),
            _valid_raw_record(_source_key="002", code="002", name="Partner B"),
            _valid_raw_record(_source_key="003", code="003", name="Partner C"),
        ]
        _make_pab_json(records, tmp_path)

        transformer = PABTransformer(data_dir=str(tmp_path))
        result, stats = transformer.run()

        assert len(result) == 3
        assert stats["valid"] == 3
        assert stats["total"] == 3

    def test_extensions_created(self, tmp_path):
        """Extensions should be created with business terms."""
        records = [_valid_raw_record()]
        _make_pab_json(records, tmp_path)

        transformer = PABTransformer(data_dir=str(tmp_path))
        result, _ = transformer.run()
        ext = result[0]["extensions"]

        assert ext is not None
        assert "sale_payment_due_days" in ext
        assert "sale_currency_code" in ext


class TestPABTransformerInvalidRecord:
    """Test that invalid records are rejected."""

    def test_missing_code_returns_none(self, tmp_path):
        """Record without code should be rejected."""
        records = [_valid_raw_record(code="", _source_key="")]
        _make_pab_json(records, tmp_path)

        transformer = PABTransformer(data_dir=str(tmp_path))
        result, stats = transformer.run()

        assert len(result) == 0
        assert stats["errors"] == 1
        assert stats["valid"] == 0

    def test_missing_name_returns_none(self, tmp_path):
        """Record without name should be rejected."""
        records = [_valid_raw_record(name="")]
        _make_pab_json(records, tmp_path)

        transformer = PABTransformer(data_dir=str(tmp_path))
        result, stats = transformer.run()

        assert len(result) == 0
        assert stats["errors"] == 1

    def test_none_code_returns_none(self, tmp_path):
        """Record with None code should be rejected."""
        records = [_valid_raw_record(code=None, _source_key="")]
        _make_pab_json(records, tmp_path)

        transformer = PABTransformer(data_dir=str(tmp_path))
        result, stats = transformer.run()

        assert len(result) == 0
        assert stats["errors"] >= 1

    def test_mixed_valid_invalid(self, tmp_path):
        """Mix of valid and invalid records — only valid ones pass."""
        records = [
            _valid_raw_record(_source_key="001", code="001", name="OK Partner"),
            _valid_raw_record(_source_key="", code="", name="Bad Partner"),
            _valid_raw_record(_source_key="003", code="003", name="Another OK"),
        ]
        _make_pab_json(records, tmp_path)

        transformer = PABTransformer(data_dir=str(tmp_path))
        result, stats = transformer.run()

        assert len(result) == 2
        assert stats["valid"] == 2
        assert stats["errors"] == 1


class TestPABTransformerFileNotFound:
    """Test behavior when extract file is missing."""

    def test_missing_json_raises_error(self, tmp_path):
        """Transformer should raise FileNotFoundError if PAB.json doesn't exist."""
        transformer = PABTransformer(data_dir=str(tmp_path))

        with pytest.raises(FileNotFoundError):
            transformer.run()
