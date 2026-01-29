"""
Test database functionality
"""

import sys
from pathlib import Path

import pytest

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def test_database_module_exists():
    """Test that database module exists"""
    # Check if there are database-related modules
    db_dir = Path(__file__).parent.parent / "database"
    assert db_dir.exists(), "Database directory not found"


def test_postgres_staging_import():
    """Test PostgreSQL staging client import"""
    try:
        from invoice_shared.database.postgres_staging import PostgresStagingClient

        assert PostgresStagingClient is not None
    except ImportError as e:
        pytest.fail(f"Failed to import PostgresStagingClient: {e}")


@pytest.mark.skip(reason="Requires PostgreSQL connection")
def test_postgres_connection():
    """Test PostgreSQL connection (requires running database)"""

    # Would need actual database config
    pass
