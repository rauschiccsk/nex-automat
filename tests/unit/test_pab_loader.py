"""
Unit tests for PABLoader — M5 (UPSERT into PostgreSQL partners table).

Tests run on Linux CI without actual database access.
Uses unittest.mock to mock pg8000 connections and cursors.
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch, call
from uuid import uuid4

import pytest

# Add nex-migration to sys.path so we can import load/config modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "apps" / "nex-migration"))

from load.pab_loader import PABLoader, _UPSERT_COLUMNS, _build_upsert_sql, BATCH_SIZE


def _mock_db_config() -> dict:
    """Return a fake DB config for tests."""
    return {
        "host": "localhost",
        "port": 5432,
        "database": "test_db",
        "user": "test_user",
        "password": "test_pass",
    }


def _valid_record(**overrides) -> dict:
    """Return a minimal valid record ready for loading."""
    defaults = {
        "_source_key": "10001",
        "code": "10001",
        "name": "Test Partner s.r.o.",
        "partner_type": "customer",
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


class TestPABLoaderUpsertSQL:
    """Test the generated UPSERT SQL statement."""

    def test_upsert_sql_contains_insert(self):
        """SQL should contain INSERT INTO partners."""
        sql = _build_upsert_sql()
        assert "INSERT INTO partners" in sql

    def test_upsert_sql_contains_on_conflict(self):
        """SQL should contain ON CONFLICT (code) DO UPDATE."""
        sql = _build_upsert_sql()
        assert "ON CONFLICT (code) DO UPDATE" in sql

    def test_upsert_sql_contains_returning(self):
        """SQL should contain RETURNING to get back the id and insert/update flag."""
        sql = _build_upsert_sql()
        assert "RETURNING id" in sql

    def test_upsert_sql_updates_updated_at(self):
        """SQL should set updated_at and updated_by on conflict."""
        sql = _build_upsert_sql()
        assert "updated_at = NOW()" in sql
        assert "updated_by = 'migration'" in sql

    def test_upsert_columns_complete(self):
        """All expected columns should be in the UPSERT column list."""
        expected = [
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
        for col in expected:
            assert col in _UPSERT_COLUMNS, f"Missing column: {col}"


class TestPABLoaderInsert:
    """Test UPSERT behavior — INSERT path."""

    @patch("load.pab_loader.BaseLoader.check_dependencies", return_value=[])
    @patch("pg8000.connect")
    def test_insert_single_record(self, mock_connect, mock_deps):
        """A single new record should result in 1 insert and 1 id_mapping."""
        target_uuid = str(uuid4())

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        # fetchone returns (uuid, True) for INSERT — xmax=0 means True
        mock_cursor.fetchone.return_value = (target_uuid, True)

        loader = PABLoader(db_config=_mock_db_config())
        loader.conn = mock_conn
        loader.batch_id = 1

        record = _valid_record()
        loader.load([record])

        # UPSERT should have been called once
        assert mock_cursor.execute.call_count >= 1

        # Check first execute call contains INSERT INTO partners
        first_call_args = mock_cursor.execute.call_args_list[0]
        sql = first_call_args[0][0]
        assert "INSERT INTO partners" in sql

        # Stats
        assert loader.stats["inserted"] == 1
        assert loader.stats["updated"] == 0

    @patch("load.pab_loader.BaseLoader.check_dependencies", return_value=[])
    @patch("pg8000.connect")
    def test_insert_writes_id_mapping(self, mock_connect, mock_deps):
        """After INSERT, add_id_mapping should be called with correct params."""
        target_uuid = str(uuid4())

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        mock_cursor.fetchone.return_value = (target_uuid, True)

        loader = PABLoader(db_config=_mock_db_config())
        loader.conn = mock_conn
        loader.batch_id = 1

        record = _valid_record(_source_key="10001")
        loader.load([record])

        # Verify add_id_mapping was called (it writes to migration_id_map)
        # The mapping execute call should contain migration_id_map
        mapping_calls = [
            c
            for c in mock_cursor.execute.call_args_list
            if "migration_id_map" in str(c)
        ]
        assert len(mapping_calls) >= 1
        assert loader.stats["mapped"] == 1


class TestPABLoaderUpdate:
    """Test UPSERT behavior — UPDATE path."""

    @patch("load.pab_loader.BaseLoader.check_dependencies", return_value=[])
    @patch("pg8000.connect")
    def test_update_existing_record(self, mock_connect, mock_deps):
        """An existing record (conflict) should increment updated counter."""
        target_uuid = str(uuid4())

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        # fetchone returns (uuid, False) for UPDATE — xmax != 0
        mock_cursor.fetchone.return_value = (target_uuid, False)

        loader = PABLoader(db_config=_mock_db_config())
        loader.conn = mock_conn
        loader.batch_id = 1

        record = _valid_record()
        loader.load([record])

        assert loader.stats["updated"] == 1
        assert loader.stats["inserted"] == 0


class TestPABLoaderBatching:
    """Test batch processing."""

    @patch("load.pab_loader.BaseLoader.check_dependencies", return_value=[])
    @patch("pg8000.connect")
    def test_batch_commits(self, mock_connect, mock_deps):
        """Records should be committed in batches of BATCH_SIZE."""
        target_uuid = str(uuid4())

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        mock_cursor.fetchone.return_value = (target_uuid, True)

        loader = PABLoader(db_config=_mock_db_config())
        loader.conn = mock_conn
        loader.batch_id = 1

        # Create 250 records — should result in 3 commits (100+100+50)
        records = [
            _valid_record(_source_key=f"P{i:04d}", code=f"P{i:04d}") for i in range(250)
        ]
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

        # First execute raises, subsequent ones succeed
        target_uuid = str(uuid4())
        mock_cursor.execute.side_effect = [
            Exception("DB constraint violation"),  # first record fails
            None,  # second record UPSERT
            (target_uuid, True),  # second record fetchone (via execute)
        ]
        # Reset to allow fetchone to work after the error
        mock_cursor.execute.side_effect = None
        mock_cursor.execute.side_effect = [
            Exception("DB constraint violation"),
            None,
        ]
        mock_cursor.fetchone.return_value = (target_uuid, True)

        loader = PABLoader(db_config=_mock_db_config())
        loader.conn = mock_conn
        loader.batch_id = 1

        records = [
            _valid_record(_source_key="BAD", code="BAD"),
            _valid_record(_source_key="GOOD", code="GOOD"),
        ]
        loader.load(records)

        # At least one error should be recorded
        assert loader.stats["errors"] >= 1


class TestPABLoaderExtractValues:
    """Test the _extract_values helper."""

    def test_extract_values_correct_order(self):
        """Values should be extracted in the order of _UPSERT_COLUMNS."""
        record = _valid_record()
        values = PABLoader._extract_values(record)

        assert isinstance(values, tuple)
        assert len(values) == len(_UPSERT_COLUMNS)

        # First value should be code
        assert values[0] == record["code"]
        # Second value should be name
        assert values[1] == record["name"]

    def test_extract_values_missing_field_returns_none(self):
        """Missing fields should return None."""
        record = {"code": "X", "name": "Y"}
        values = PABLoader._extract_values(record)

        # partner_type (3rd column) should be None since it's missing
        assert values[2] is None
