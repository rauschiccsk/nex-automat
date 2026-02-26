"""PostgreSQL database connection using pg8000.

Provides a FastAPI dependency that yields a database connection
with cursor per request, with automatic commit/rollback.
"""

import os
from contextlib import contextmanager

import pg8000.dbapi


def _get_conn_params() -> dict:
    """Build connection parameters from environment variables."""
    return {
        "host": os.getenv("POSTGRES_HOST", "localhost"),
        "port": int(os.getenv("POSTGRES_PORT", "5432")),
        "database": os.getenv("POSTGRES_DB", "nex_automat"),
        "user": os.getenv("POSTGRES_USER", "nex_admin"),
        "password": os.getenv("POSTGRES_PASSWORD", ""),
    }


@contextmanager
def get_connection():
    """Context manager for a pg8000 database connection."""
    conn = None
    try:
        conn = pg8000.dbapi.connect(**_get_conn_params())
        yield conn
        conn.commit()
    except Exception:
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()


def get_db():
    """FastAPI dependency — yields a pg8000 connection with auto-commit/rollback."""
    with get_connection() as conn:
        yield conn
