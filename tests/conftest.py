"""
NEX Automat - Shared Test Fixtures

This module provides common fixtures for all tests in the test suite.
"""

import os
from unittest.mock import AsyncMock, MagicMock

import pytest

# ============================================================================
# Database Fixtures
# ============================================================================


@pytest.fixture
def db_session():
    """
    PostgreSQL test connection fixture.

    Returns a mock database session for unit tests.
    For integration tests, set TEST_DATABASE_URL environment variable.
    """
    mock_session = MagicMock()
    mock_session.execute = MagicMock(return_value=MagicMock(fetchall=lambda: []))
    mock_session.commit = MagicMock()
    mock_session.rollback = MagicMock()
    mock_session.close = MagicMock()

    # Context manager support
    mock_session.__enter__ = MagicMock(return_value=mock_session)
    mock_session.__exit__ = MagicMock(return_value=False)

    return mock_session


@pytest.fixture
def mock_cursor():
    """Create a mock database cursor."""
    cursor = MagicMock()
    cursor.fetchall.return_value = []
    cursor.fetchone.return_value = None
    cursor.rowcount = 0
    cursor.execute = MagicMock()
    return cursor


@pytest.fixture
def mock_connection(mock_cursor):
    """Create a mock database connection with cursor."""
    conn = MagicMock()
    conn.cursor.return_value = mock_cursor
    conn.commit = MagicMock()
    conn.rollback = MagicMock()
    conn.close = MagicMock()
    return conn


# ============================================================================
# FastAPI / Async Fixtures
# ============================================================================


@pytest.fixture
def async_client():
    """
    FastAPI TestClient fixture for async API testing.

    Returns a mock async client. For real API tests,
    import the actual app and use httpx.AsyncClient.
    """
    client = AsyncMock()
    client.get = AsyncMock(return_value=MagicMock(status_code=200, json=lambda: {}))
    client.post = AsyncMock(return_value=MagicMock(status_code=201, json=lambda: {}))
    client.put = AsyncMock(return_value=MagicMock(status_code=200, json=lambda: {}))
    client.delete = AsyncMock(return_value=MagicMock(status_code=204))

    # Context manager support for async with
    client.__aenter__ = AsyncMock(return_value=client)
    client.__aexit__ = AsyncMock(return_value=False)

    return client


# ============================================================================
# Invoice Data Fixtures
# ============================================================================


@pytest.fixture
def sample_invoice_data():
    """
    Sample invoice data for testing invoice processing.

    Returns a dictionary with realistic invoice test data.
    """
    return {
        "invoice_head": {
            "id": 1,
            "supplier_id": 100,
            "supplier_name": "Test Supplier s.r.o.",
            "invoice_number": "FV-2024-001",
            "invoice_date": "2024-01-15",
            "due_date": "2024-02-14",
            "total_amount": 1200.00,
            "vat_amount": 200.00,
            "currency": "EUR",
            "status": "pending",
        },
        "invoice_items": [
            {
                "id": 1,
                "invoice_id": 1,
                "original_name": "Coca Cola 0.5L",
                "original_ean": "5449000000996",
                "quantity": 24,
                "unit": "ks",
                "unit_price": 0.85,
                "total_price": 20.40,
                "vat_rate": 20.0,
            },
            {
                "id": 2,
                "invoice_id": 1,
                "original_name": "Sprite 0.5L",
                "original_ean": "5449000014535",
                "quantity": 12,
                "unit": "ks",
                "unit_price": 0.80,
                "total_price": 9.60,
                "vat_rate": 20.0,
            },
            {
                "id": 3,
                "invoice_id": 1,
                "original_name": "Unknown Product",
                "original_ean": None,
                "quantity": 5,
                "unit": "ks",
                "unit_price": 2.50,
                "total_price": 12.50,
                "vat_rate": 20.0,
            },
        ],
    }


@pytest.fixture
def sample_invoice_item():
    """Single invoice item for granular testing."""
    return {
        "id": 1,
        "invoice_id": 100,
        "original_name": "Test Product",
        "original_ean": "1234567890123",
        "quantity": 10,
        "unit": "ks",
        "unit_price": 5.00,
        "total_price": 50.00,
        "vat_rate": 20.0,
        "nex_gs_code": None,
        "validation_status": "pending",
    }


# ============================================================================
# Environment Fixtures
# ============================================================================


@pytest.fixture
def mock_env(monkeypatch):
    """
    Fixture to set up test environment variables.

    Usage:
        def test_something(mock_env):
            mock_env("DATABASE_URL", "postgresql://test:test@localhost/test")
    """

    def _set_env(key, value):
        monkeypatch.setenv(key, value)

    return _set_env


@pytest.fixture
def temp_sqlite_db(tmp_path):
    """
    Create a temporary SQLite database for testing.

    Returns the path to the temporary database file.
    """
    db_path = tmp_path / "test.db"
    return str(db_path)
