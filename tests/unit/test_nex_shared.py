"""
Unit tests for nex-shared package utilities.

Tests cover:
- text_utils.clean_string
- grid_settings utilities
- general shared functionality
"""

import os
import sqlite3

# Import from nex-shared package
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "packages" / "nex-shared"))

from utils.text_utils import clean_string


class TestCleanString:
    """Tests for clean_string() function."""

    def test_removes_null_bytes(self):
        """Should remove null bytes from string."""
        input_str = "Hello\x00World\x00"
        result = clean_string(input_str)
        assert result == "HelloWorld"
        assert "\x00" not in result

    def test_removes_control_characters(self):
        """Should remove control characters except newline and tab."""
        input_str = "Hello\x01\x02\x03World"
        result = clean_string(input_str)
        assert result == "HelloWorld"

    def test_preserves_newline_and_tab(self):
        """Should preserve newline and tab characters."""
        input_str = "Hello\n\tWorld"
        result = clean_string(input_str)
        assert result == "Hello\n\tWorld"

    def test_strips_whitespace(self):
        """Should strip leading and trailing whitespace."""
        input_str = "   Hello World   "
        result = clean_string(input_str)
        assert result == "Hello World"

    def test_returns_none_for_none_input(self):
        """Should return None when input is None."""
        result = clean_string(None)
        assert result is None

    def test_returns_non_string_unchanged(self):
        """Should return non-string values unchanged."""
        assert clean_string(123) == 123
        assert clean_string(45.67) == 45.67
        assert clean_string([1, 2, 3]) == [1, 2, 3]

    def test_returns_none_for_empty_after_cleaning(self):
        """Should return None if string is empty after cleaning."""
        input_str = "\x00\x00\x00"
        result = clean_string(input_str)
        assert result is None

    def test_handles_btrieve_padding(self):
        """Should handle NEX Genesis Btrieve null-padded fields."""
        # Simulates typical Btrieve field padding
        input_str = "ProductName\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        result = clean_string(input_str)
        assert result == "ProductName"

    def test_handles_mixed_content(self):
        """Should handle strings with mixed problematic characters."""
        input_str = "  \x00Hello\x01\x00World\x02  "
        result = clean_string(input_str)
        assert result == "HelloWorld"

    def test_unicode_characters_preserved(self):
        """Should preserve Unicode characters."""
        input_str = "Čokoláda špeciálna"
        result = clean_string(input_str)
        assert result == "Čokoláda špeciálna"


class TestGridSettingsPath:
    """Tests for grid settings path utilities."""

    def test_get_grid_settings_db_path_format(self):
        """Should return path in expected format."""
        from utils.grid_settings import get_grid_settings_db_path

        path = get_grid_settings_db_path()

        assert path.endswith("grid_settings.db")
        assert "SQLITE" in path

    def test_get_current_user_id_returns_string(self):
        """Should return a string user ID."""
        from utils.grid_settings import get_current_user_id

        user_id = get_current_user_id()

        assert isinstance(user_id, str)
        assert len(user_id) > 0

    def test_get_current_user_id_uses_username(self):
        """Should use USERNAME environment variable."""
        from utils.grid_settings import get_current_user_id

        with patch.dict(os.environ, {"USERNAME": "test_user"}):
            user_id = get_current_user_id()
            assert user_id == "test_user"


class TestGridSettingsDatabase:
    """Tests for grid settings database operations."""

    def test_init_grid_settings_creates_tables(self, temp_sqlite_db):
        """Should create required tables on init."""
        from utils.grid_settings import init_grid_settings_db

        with patch("utils.grid_settings.get_grid_settings_db_path", return_value=temp_sqlite_db):
            init_grid_settings_db()

            # Verify tables exist
            conn = sqlite3.connect(temp_sqlite_db)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = {row[0] for row in cursor.fetchall()}
            conn.close()

            assert "grid_column_settings" in tables
            assert "grid_settings" in tables

    def test_save_and_load_column_settings(self, temp_sqlite_db):
        """Should save and load column settings correctly."""
        from utils.grid_settings import (
            init_grid_settings_db,
            load_column_settings,
            save_column_settings,
        )

        with patch("utils.grid_settings.get_grid_settings_db_path", return_value=temp_sqlite_db):
            columns = [
                {"column_name": "id", "width": 50, "visual_index": 0, "visible": True},
                {"column_name": "name", "width": 200, "visual_index": 1, "visible": True},
                {"column_name": "hidden", "width": 100, "visual_index": 2, "visible": False},
            ]

            result = save_column_settings("test_window", "test_grid", columns, user_id="test_user")
            assert result is True

            loaded = load_column_settings("test_window", "test_grid", user_id="test_user")
            assert len(loaded) == 3
            assert loaded[0]["column_name"] == "id"
            assert loaded[0]["width"] == 50
            assert loaded[2]["visible"] is False

    def test_load_column_settings_empty_for_nonexistent(self, temp_sqlite_db):
        """Should return empty list for non-existent settings."""
        from utils.grid_settings import load_column_settings

        with patch("utils.grid_settings.get_grid_settings_db_path", return_value=temp_sqlite_db):
            loaded = load_column_settings("nonexistent", "nonexistent", user_id="nobody")
            assert loaded == []

    def test_save_and_load_grid_settings(self, temp_sqlite_db):
        """Should save and load grid-level settings."""
        from utils.grid_settings import (
            init_grid_settings_db,
            load_grid_settings,
            save_grid_settings,
        )

        with patch("utils.grid_settings.get_grid_settings_db_path", return_value=temp_sqlite_db):
            result = save_grid_settings("test_window", "test_grid", 2, user_id="test_user")
            assert result is True

            loaded = load_grid_settings("test_window", "test_grid", user_id="test_user")
            assert loaded is not None
            assert loaded["active_column_index"] == 2

    def test_load_grid_settings_none_for_nonexistent(self, temp_sqlite_db):
        """Should return None for non-existent grid settings."""
        from utils.grid_settings import load_grid_settings

        with patch("utils.grid_settings.get_grid_settings_db_path", return_value=temp_sqlite_db):
            loaded = load_grid_settings("nonexistent", "nonexistent", user_id="nobody")
            assert loaded is None


class TestInvoiceDataFixture:
    """Tests using shared invoice data fixtures."""

    def test_sample_invoice_data_structure(self, sample_invoice_data):
        """Should have correct invoice data structure."""
        assert "invoice_head" in sample_invoice_data
        assert "invoice_items" in sample_invoice_data

        head = sample_invoice_data["invoice_head"]
        assert head["id"] == 1
        assert head["supplier_name"] == "Test Supplier s.r.o."
        assert head["currency"] == "EUR"

    def test_sample_invoice_items_count(self, sample_invoice_data):
        """Should have multiple invoice items."""
        items = sample_invoice_data["invoice_items"]
        assert len(items) == 3

    def test_sample_invoice_item_with_ean(self, sample_invoice_data):
        """Should have item with EAN code."""
        items = sample_invoice_data["invoice_items"]
        item_with_ean = items[0]
        assert item_with_ean["original_ean"] is not None
        assert len(item_with_ean["original_ean"]) == 13

    def test_sample_invoice_item_without_ean(self, sample_invoice_data):
        """Should have item without EAN code."""
        items = sample_invoice_data["invoice_items"]
        item_without_ean = items[2]
        assert item_without_ean["original_ean"] is None
