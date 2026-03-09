"""
Unit tests for PABLoader — INSERT structured records into partner_catalog* (6 tables).

Tests run on Linux CI without actual database access.
Uses unittest.mock to mock pg8000 connections and cursors.

PABLoader.load() expects structured records from PABTransformer:
{
    "_source_key": "10001",
    "header": { partner_id, partner_name, ... },
    "extensions": { ... } | None,
    "addresses": [ ... ],
    "contacts": [ ... ],
    "bank_accounts": [ ... ],
    "texts": [ ... ],
}
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Add nex-migration to sys.path so we can import load/config modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "apps" / "nex-migration"))

from load.pab_loader import PABLoader, BATCH_SIZE


def _mock_db_config() -> dict:
    """Return a fake DB config for tests."""
    return {
        "host": "localhost",
        "port": 5432,
        "database": "test_db",
        "user": "test_user",
        "password": "test_pass",
    }


def _structured_record(**header_overrides) -> dict:
    """Return a minimal structured record as produced by PABTransformer."""
    header_defaults = {
        "partner_id": 10001,
        "partner_name": "Test Partner s.r.o.",
        "company_id": "12345678",
        "tax_id": "2012345678",
        "vat_id": "SK2012345678",
        "is_vat_payer": True,
        "is_supplier": False,
        "is_customer": True,
        "street": "Hlavna 1",
        "city": "Bratislava",
        "zip_code": "81101",
        "country_code": "SK",
        "partner_class": "business",
        "is_active": True,
        "created_by": "migration",
        "updated_by": "migration",
    }
    header_defaults.update(header_overrides)
    return {
        "_source_key": str(header_defaults["partner_id"]),
        "header": header_defaults,
        "extensions": {
            "sale_payment_due_days": 30,
            "sale_credit_limit": 5000.0,
            "sale_discount_percent": 2.5,
            "sale_currency_code": "EUR",
            "created_by": "migration",
            "updated_by": "migration",
        },
        "addresses": [
            {
                "address_type": "registered",
                "street": "Hlavna 1",
                "city": "Bratislava",
                "zip_code": "81101",
                "country_code": "SK",
                "created_by": "migration",
                "updated_by": "migration",
            }
        ],
        "contacts": [
            {
                "contact_type": "person",
                "last_name": "Jan Novak",
                "phone_work": "+421999888777",
                "phone_mobile": "+421999888666",
                "email": "test@partner.sk",
                "country_code": "SK",
                "created_by": "migration",
                "updated_by": "migration",
            }
        ],
        "bank_accounts": [
            {
                "iban_code": "SK3112000000198742637541",
                "bank_name": "Slovenska sporitelna",
                "swift_code": "GIBASKBX",
                "is_primary": True,
                "created_by": "migration",
                "updated_by": "migration",
            }
        ],
        "texts": [
            {
                "text_type": "notes",
                "line_number": 1,
                "language": "sk",
                "text_content": "Poznamka 1",
                "created_by": "migration",
                "updated_by": "migration",
            }
        ],
    }


class TestPABLoaderInsertSQL:
    """Test the SQL statements used by PABLoader."""

    def test_insert_header_contains_partner_catalog(self):
        """SQL should INSERT INTO partner_catalog."""
        from load.pab_loader import _INSERT_HEADER

        assert "INSERT INTO partner_catalog" in _INSERT_HEADER
        assert "RETURNING partner_id" in _INSERT_HEADER

    def test_insert_extensions_sql(self):
        """SQL should INSERT INTO partner_catalog_extensions."""
        from load.pab_loader import _INSERT_EXTENSIONS

        assert "INSERT INTO partner_catalog_extensions" in _INSERT_EXTENSIONS

    def test_insert_address_sql(self):
        """SQL should INSERT INTO partner_catalog_addresses."""
        from load.pab_loader import _INSERT_ADDRESS

        assert "INSERT INTO partner_catalog_addresses" in _INSERT_ADDRESS

    def test_insert_contact_sql(self):
        """SQL should INSERT INTO partner_catalog_contacts."""
        from load.pab_loader import _INSERT_CONTACT

        assert "INSERT INTO partner_catalog_contacts" in _INSERT_CONTACT

    def test_insert_bank_account_sql(self):
        """SQL should INSERT INTO partner_catalog_bank_accounts."""
        from load.pab_loader import _INSERT_BANK_ACCOUNT

        assert "INSERT INTO partner_catalog_bank_accounts" in _INSERT_BANK_ACCOUNT

    def test_insert_text_sql(self):
        """SQL should INSERT INTO partner_catalog_texts."""
        from load.pab_loader import _INSERT_TEXT

        assert "INSERT INTO partner_catalog_texts" in _INSERT_TEXT


class TestPABLoaderInsert:
    """Test INSERT behavior for a single record."""

    @patch("load.pab_loader.BaseLoader.check_dependencies", return_value=[])
    @patch("pg8000.connect")
    def test_insert_single_record(self, mock_connect, mock_deps):
        """A single structured record should result in 1 insert and 1 id_mapping."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        # fetchone returns (partner_id,) after INSERT RETURNING
        mock_cursor.fetchone.return_value = (10001,)

        loader = PABLoader(db_config=_mock_db_config())
        loader.conn = mock_conn
        loader.batch_id = 1

        record = _structured_record()
        loader.load([record])

        # Header INSERT should have been called
        assert mock_cursor.execute.call_count >= 1

        # Check first execute call contains INSERT INTO partner_catalog
        first_call_args = mock_cursor.execute.call_args_list[0]
        sql = first_call_args[0][0]
        assert "INSERT INTO partner_catalog" in sql

        # Stats
        assert loader.stats["inserted"] == 1

    @patch("load.pab_loader.BaseLoader.check_dependencies", return_value=[])
    @patch("pg8000.connect")
    def test_insert_writes_id_mapping(self, mock_connect, mock_deps):
        """After INSERT, add_id_mapping should be called with correct params."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        mock_cursor.fetchone.return_value = (10001,)

        loader = PABLoader(db_config=_mock_db_config())
        loader.conn = mock_conn
        loader.batch_id = 1

        record = _structured_record()
        loader.load([record])

        # Verify add_id_mapping was called (it writes to migration_id_map)
        mapping_calls = [
            c
            for c in mock_cursor.execute.call_args_list
            if "migration_id_map" in str(c)
        ]
        assert len(mapping_calls) >= 1
        assert loader.stats["mapped"] == 1


class TestPABLoaderBatching:
    """Test batch processing."""

    @patch("load.pab_loader.BaseLoader.check_dependencies", return_value=[])
    @patch("pg8000.connect")
    def test_batch_commits(self, mock_connect, mock_deps):
        """Records should be committed in batches of BATCH_SIZE."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        mock_cursor.fetchone.return_value = (99999,)

        loader = PABLoader(db_config=_mock_db_config())
        loader.conn = mock_conn
        loader.batch_id = 1

        # Create 250 records — should result in 3 commits (100+100+50)
        records = [
            _structured_record(partner_id=i, partner_name=f"Partner {i}")
            for i in range(250)
        ]
        # Fix _source_key for each
        for i, rec in enumerate(records):
            rec["_source_key"] = str(i)

        loader.load(records)

        # conn.commit should be called 3 times (100 + 100 + 50)
        assert mock_conn.commit.call_count == 3
        assert loader.stats["inserted"] == 250

    def test_batch_size_is_100(self):
        """Verify BATCH_SIZE constant is 100."""
        assert BATCH_SIZE == 100


class TestPABLoaderErrorHandling:
    """Test error handling during load."""

    @patch("load.pab_loader.BaseLoader.check_dependencies", return_value=[])
    @patch("pg8000.connect")
    def test_db_error_increments_error_count(self, mock_connect, mock_deps):
        """A DB error on a record should increment errors, not crash."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        # First execute raises, then subsequent succeed
        call_count = [0]
        original_fetchone_return = (10001,)

        def side_effect_execute(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                raise Exception("DB constraint violation")

        mock_cursor.execute.side_effect = side_effect_execute
        mock_cursor.fetchone.return_value = original_fetchone_return

        loader = PABLoader(db_config=_mock_db_config())
        loader.conn = mock_conn
        loader.batch_id = 1

        records = [
            _structured_record(partner_id=1, partner_name="Bad"),
            _structured_record(partner_id=2, partner_name="Good"),
        ]
        records[0]["_source_key"] = "BAD"
        records[1]["_source_key"] = "GOOD"

        loader.load(records)

        # At least one error should be recorded
        assert loader.stats["errors"] >= 1
