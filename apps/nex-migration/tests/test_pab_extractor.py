"""
Unit tests for PABExtractor — M4 (Btrieve PAB → JSON).

Tests run on Linux CI without nexdata installed.
Uses unittest.mock and types.SimpleNamespace to simulate nexdata records.
"""

import json
import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

# Add nex-migration to sys.path so we can import extract/config modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "apps" / "nex-migration"))

from extract.pab_extractor import PABExtractor


def _make_pab_record(**overrides) -> SimpleNamespace:
    """Create a fake PABRecord with sensible defaults."""
    defaults = {
        "pab_code": "10001",
        "name1": "  Test Partner s.r.o.  ",
        "partner_type": 2,
        "ico": "  12345678  ",
        "dic": " 2012345678 ",
        "ic_dph": " SK2012345678 ",
        "vat_payer": 1,
        "street": " Hlavná 1 ",
        "city": " Bratislava ",
        "zip_code": " 81101 ",
        "country": "SK",
        "phone": " +421999888777 ",
        "fax": " +421999888666 ",
        "email": " test@partner.sk ",
        "web": " www.partner.sk ",
        "contact_person": " Ján Novák ",
        "payment_terms": 30,
        "credit_limit": "5000.00",
        "discount_percent": "2.5",
        "iban": " SK3112000000198742637541 ",
        "bank_name": " Slovenská sporiteľňa ",
        "swift": " GIBASKBX ",
        "note": " Poznámka 1 ",
        "note2": " Poznámka 2 ",
        "internal_note": "",
        "active": 1,
        # Fields that don't exist in PAB — defaults from FieldMapping
        "_payment_method": None,
        "_currency": None,
    }
    defaults.update(overrides)
    return SimpleNamespace(**defaults)


class TestMapRecordBasic:
    """test_map_record_basic — field mapping and _source_key presence."""

    def test_map_record_basic(self):
        """Verify field mapping and _source_key for a standard PAB record."""
        extractor = PABExtractor(data_dir="/tmp/test_pab_data")
        record = _make_pab_record()
        mapped = extractor._map_record(record)

        # _source_key must be present and correct
        assert "_source_key" in mapped
        assert mapped["_source_key"] == "10001"

        # Required fields
        assert mapped["code"] == "10001"
        assert mapped["name"] == "Test Partner s.r.o."

        # Partner type mapping (2 → customer)
        assert mapped["partner_type"] == "customer"
        assert mapped["is_customer"] is True
        assert mapped["is_supplier"] is False

        # Tax fields — stripped
        assert mapped["company_id"] == "12345678"
        assert mapped["tax_id"] == "2012345678"
        assert mapped["vat_id"] == "SK2012345678"
        assert mapped["is_vat_payer"] is True

        # Address — stripped
        assert mapped["street"] == "Hlavná 1"
        assert mapped["city"] == "Bratislava"
        assert mapped["zip_code"] == "81101"
        assert mapped["country_code"] == "SK"

        # Contact — stripped
        assert mapped["phone"] == "+421999888777"
        assert mapped["email"] == "test@partner.sk"

        # Business terms — type conversions
        assert mapped["payment_due_days"] == 30
        assert isinstance(mapped["credit_limit"], float)
        assert mapped["credit_limit"] == 5000.0
        assert mapped["discount_percent"] == 2.5

        # Bank — stripped
        assert mapped["iban"] == "SK3112000000198742637541"

        # Notes — combined
        assert "Poznámka 1" in mapped["notes"]
        assert "Poznámka 2" in mapped["notes"]

        # Defaults for missing fields
        assert mapped["payment_method"] == "transfer"
        assert mapped["currency"] == "EUR"

    def test_map_record_supplier_type(self):
        """partner_type=1 should map to supplier."""
        extractor = PABExtractor(data_dir="/tmp/test_pab_data")
        record = _make_pab_record(partner_type=1)
        mapped = extractor._map_record(record)

        assert mapped["partner_type"] == "supplier"
        assert mapped["is_supplier"] is True
        assert mapped["is_customer"] is False

    def test_map_record_both_type(self):
        """partner_type=3 should map to 'both'."""
        extractor = PABExtractor(data_dir="/tmp/test_pab_data")
        record = _make_pab_record(partner_type=3)
        mapped = extractor._map_record(record)

        assert mapped["partner_type"] == "both"
        assert mapped["is_supplier"] is True
        assert mapped["is_customer"] is True


class TestOutputStructure:
    """test_output_structure — mock nexdata, verify JSON output structure."""

    def test_output_structure(self, tmp_path):
        """Extract with mocked nexdata → verify JSON structure."""
        # Create fake records
        fake_records = [
            _make_pab_record(pab_code="001", name1="Partner A"),
            _make_pab_record(pab_code="002", name1="Partner B"),
            _make_pab_record(pab_code="003", name1="Partner C"),
        ]

        # Mock nexdata module
        mock_nexdata = MagicMock()
        mock_pab_instance = MagicMock()
        mock_pab_instance.read_all.return_value = fake_records
        mock_nexdata.PAB.return_value = mock_pab_instance

        extractor = PABExtractor(data_dir=str(tmp_path))

        # Patch nexdata in the extract() method
        with patch.dict(sys.modules, {"nexdata": mock_nexdata}):
            output_file = extractor.extract()

        # Verify file exists
        assert output_file.exists()
        assert output_file.name == "PAB.json"

        # Load and verify structure
        with open(output_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert data["category"] == "PAB"
        assert "extracted_at" in data
        assert data["total_source"] == 3
        assert data["total_extracted"] == 3
        assert data["error_count"] == 0
        assert isinstance(data["records"], list)
        assert len(data["records"]) == 3
        assert isinstance(data["errors"], list)
        assert len(data["errors"]) == 0

        # Verify each record has _source_key
        for rec in data["records"]:
            assert "_source_key" in rec
            assert "code" in rec
            assert "name" in rec
