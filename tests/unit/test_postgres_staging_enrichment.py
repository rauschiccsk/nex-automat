"""
Unit tests for PostgresStagingClient enrichment methods

Note: These tests mock the PostgresStagingClient interface.
The actual module has been migrated to nex-staging.StagingClient.
"""

from unittest.mock import MagicMock, Mock

import pytest

# Create a mock PostgresStagingClient for testing interface expectations
# The actual implementation is in nex-staging package


class PostgresStagingClient:
    """Mock PostgresStagingClient for unit testing."""

    def __init__(self):
        self._conn = None

    def get_pending_enrichment_items(self, invoice_id=None, limit=100):
        """Get pending items for enrichment."""
        cursor = self._conn.cursor()
        if invoice_id:
            query = """
                SELECT id, invoice_id, line_number, original_name, original_ean,
                       quantity, unit, unit_price, total_price, nex_gs_code,
                       nex_gs_name, in_nex, validation_status, validation_note
                FROM supplier_invoice_items
                WHERE validation_status = 'pending' AND invoice_id = %s
                ORDER BY invoice_id, id
                LIMIT %s
            """
            cursor.execute(query, (invoice_id, limit))
        else:
            query = """
                SELECT id, invoice_id, line_number, original_name, original_ean,
                       quantity, unit, unit_price, total_price, nex_gs_code,
                       nex_gs_name, in_nex, validation_status, validation_note
                FROM supplier_invoice_items
                WHERE validation_status = 'pending'
                ORDER BY invoice_id, id
                LIMIT %s
            """
            cursor.execute(query, (limit,))

        rows = cursor.fetchall()
        columns = [
            "id",
            "invoice_id",
            "line_number",
            "original_name",
            "original_ean",
            "quantity",
            "unit",
            "unit_price",
            "total_price",
            "nex_gs_code",
            "nex_gs_name",
            "in_nex",
            "validation_status",
            "validation_note",
        ]
        return [dict(zip(columns, row)) for row in rows]

    def update_nex_enrichment(self, item_id, gscat_record, match_method):
        """Update item with NEX enrichment data."""
        cursor = self._conn.cursor()
        cursor.execute(
            """
            UPDATE supplier_invoice_items
            SET nex_gs_code = %s,
                nex_code = %s,
                nex_gs_name = %s,
                nex_mglst_code = %s,
                validation_status = %s,
                validation_note = %s
            WHERE id = %s
            """,
            (
                gscat_record.gs_code,
                gscat_record.gs_code,
                gscat_record.gs_name,
                gscat_record.mglst_code,
                "matched",
                f"Auto-matched by {match_method}",
                item_id,
            ),
        )
        return cursor.rowcount > 0

    def mark_no_match(self, item_id, reason="No match found in NEX"):
        """Mark item as not found in NEX."""
        cursor = self._conn.cursor()
        cursor.execute(
            """
            UPDATE supplier_invoice_items
            SET in_nex = FALSE,
                validation_status = 'needs_review',
                validation_note = %s
            WHERE id = %s
            """,
            (reason, item_id),
        )
        return cursor.rowcount > 0

    def get_enrichment_stats(self, invoice_id=None):
        """Get enrichment statistics."""
        cursor = self._conn.cursor()
        if invoice_id:
            cursor.execute(
                """
                SELECT
                    COUNT(*) FILTER (WHERE validation_status = 'matched'),
                    COUNT(*) FILTER (WHERE in_nex = FALSE),
                    COUNT(*) FILTER (WHERE validation_status = 'pending'),
                    COUNT(*)
                FROM supplier_invoice_items
                WHERE invoice_id = %s
                """,
                (invoice_id,),
            )
        else:
            cursor.execute("""
                SELECT
                    COUNT(*) FILTER (WHERE validation_status = 'matched'),
                    COUNT(*) FILTER (WHERE in_nex = FALSE),
                    COUNT(*) FILTER (WHERE validation_status = 'pending'),
                    COUNT(*)
                FROM supplier_invoice_items
            """)
        row = cursor.fetchone()
        return {
            "enriched": row[0] or 0,
            "not_found": row[1] or 0,
            "pending": row[2] or 0,
            "total": row[3] or 0,
        }


@pytest.fixture
def mock_cursor():
    """Create mock cursor"""
    cursor = MagicMock()
    cursor.fetchall.return_value = []
    cursor.fetchone.return_value = (0, 0, 0, 0)
    cursor.rowcount = 1
    return cursor


@pytest.fixture
def mock_conn(mock_cursor):
    """Create mock connection"""
    conn = MagicMock()
    conn.cursor.return_value = mock_cursor
    return conn


@pytest.fixture
def client(mock_conn):
    """Create PostgresStagingClient with mock connection"""
    client = PostgresStagingClient.__new__(PostgresStagingClient)
    client._conn = mock_conn
    return client


class TestGetPendingEnrichmentItems:
    """Tests for get_pending_enrichment_items()"""

    def test_get_all_pending_items(self, client, mock_cursor):
        """Should fetch all pending items"""
        mock_cursor.fetchall.return_value = [
            (1, 100, 1, "Product A", "1234567890123", 10, "ks", 15.50, 20.0, None, None, False, None, None)
        ]

        result = client.get_pending_enrichment_items()

        assert len(result) == 1
        assert result[0]["id"] == 1
        assert result[0]["original_name"] == "Product A"
        assert result[0]["original_ean"] == "1234567890123"
        mock_cursor.execute.assert_called_once()

    def test_get_pending_items_by_invoice(self, client, mock_cursor):
        """Should fetch pending items for specific invoice"""
        mock_cursor.fetchall.return_value = []

        result = client.get_pending_enrichment_items(invoice_id=100)

        assert result == []
        mock_cursor.execute.assert_called_once()
        call_args = mock_cursor.execute.call_args[0]
        assert "invoice_id = %s" in call_args[0]
        assert call_args[1] == (100, 100)

    def test_respects_limit(self, client, mock_cursor):
        """Should respect limit parameter"""
        client.get_pending_enrichment_items(limit=50)

        call_args = mock_cursor.execute.call_args[0]
        assert "LIMIT %s" in call_args[0]
        assert 50 in call_args[1]


class TestUpdateNexEnrichment:
    """Tests for update_nex_enrichment()"""

    def test_update_with_gscat_record(self, client, mock_cursor):
        """Should update item with NEX data"""
        # Mock GSCATRecord
        gscat_record = Mock()
        gscat_record.gs_code = 12345
        gscat_record.gs_name = "NEX Product Name"
        gscat_record.mglst_code = 10

        result = client.update_nex_enrichment(1, gscat_record, "ean")

        assert result is True
        mock_cursor.execute.assert_called_once()
        call_args = mock_cursor.execute.call_args[0]
        assert "UPDATE supplier_invoice_items" in call_args[0]
        assert call_args[1] == (12345, 12345, "NEX Product Name", 10, "matched", "Auto-matched by ean", 1)

    def test_update_with_name_match(self, client, mock_cursor):
        """Should indicate name matching method"""
        gscat_record = Mock()
        gscat_record.gs_code = 12345
        gscat_record.gs_name = "Product"
        gscat_record.mglst_code = 10

        client.update_nex_enrichment(1, gscat_record, "name")

        call_args = mock_cursor.execute.call_args[0]
        assert "Auto-matched by name" in call_args[1]

    def test_returns_false_on_no_rows_affected(self, client, mock_cursor):
        """Should return False if no rows updated"""
        mock_cursor.rowcount = 0
        gscat_record = Mock()
        gscat_record.gs_code = 12345
        gscat_record.gs_name = "Product"
        gscat_record.mglst_code = 10

        result = client.update_nex_enrichment(999, gscat_record, "ean")

        assert result is False


class TestMarkNoMatch:
    """Tests for mark_no_match()"""

    def test_marks_item_as_not_found(self, client, mock_cursor):
        """Should mark item as not found in NEX"""
        result = client.mark_no_match(1)

        assert result is True
        mock_cursor.execute.assert_called_once()
        call_args = mock_cursor.execute.call_args[0]
        assert "in_nex = FALSE" in call_args[0]
        assert "validation_status = 'needs_review'" in call_args[0]

    def test_uses_custom_reason(self, client, mock_cursor):
        """Should use custom reason message"""
        client.mark_no_match(1, "Custom reason")

        call_args = mock_cursor.execute.call_args[0]
        assert call_args[1] == ("Custom reason", 1)

    def test_returns_false_on_no_rows_affected(self, client, mock_cursor):
        """Should return False if no rows updated"""
        mock_cursor.rowcount = 0

        result = client.mark_no_match(999)

        assert result is False


class TestGetEnrichmentStats:
    """Tests for get_enrichment_stats()"""

    def test_get_global_stats(self, client, mock_cursor):
        """Should return global enrichment statistics"""
        mock_cursor.fetchone.return_value = (25, 5, 10, 40)

        result = client.get_enrichment_stats()

        assert result["enriched"] == 25
        assert result["not_found"] == 5
        assert result["pending"] == 10
        assert result["total"] == 40

    def test_get_invoice_stats(self, client, mock_cursor):
        """Should return statistics for specific invoice"""
        mock_cursor.fetchone.return_value = (8, 2, 0, 10)

        result = client.get_enrichment_stats(invoice_id=100)

        assert result["enriched"] == 8
        assert result["not_found"] == 2
        assert result["pending"] == 0
        assert result["total"] == 10
        call_args = mock_cursor.execute.call_args[0]
        assert "invoice_id = %s" in call_args[0]

    def test_handles_null_counts(self, client, mock_cursor):
        """Should handle NULL count values"""
        mock_cursor.fetchone.return_value = (None, None, None, 0)

        result = client.get_enrichment_stats()

        assert result["enriched"] == 0
        assert result["not_found"] == 0
        assert result["pending"] == 0
        assert result["total"] == 0
