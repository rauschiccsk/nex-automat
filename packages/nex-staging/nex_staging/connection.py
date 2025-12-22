"""PostgreSQL connection manager using pg8000."""

from contextlib import contextmanager
from dataclasses import dataclass
from typing import Optional, Generator, Any
import os

import pg8000.native


@dataclass
class DatabaseConfig:
    """Database connection configuration."""
    host: str = "localhost"
    port: int = 5432
    database: str = "nex_automat"
    user: str = "nex"
    password: str = ""

    @classmethod
    def from_env(cls) -> "DatabaseConfig":
        """Create config from environment variables."""
        return cls(
            host=os.getenv("POSTGRES_HOST", "localhost"),
            port=int(os.getenv("POSTGRES_PORT", "5432")),
            database=os.getenv("POSTGRES_DATABASE", "nex_automat"),
            user=os.getenv("POSTGRES_USER", "nex"),
            password=os.getenv("POSTGRES_PASSWORD", ""),
        )


class DatabaseConnection:
    """PostgreSQL connection manager with context manager support."""

    def __init__(
        self,
        host: str = "localhost",
        port: int = 5432,
        database: str = "nex_automat",
        user: str = "nex",
        password: Optional[str] = None,
        config: Optional[DatabaseConfig] = None,
    ):
        if config:
            self.config = config
        else:
            self.config = DatabaseConfig(
                host=host,
                port=port,
                database=database,
                user=user,
                password=password or os.getenv("POSTGRES_PASSWORD", ""),
            )

    def _create_connection(self) -> pg8000.native.Connection:
        """Create a new pg8000 connection."""
        return pg8000.native.Connection(
            host=self.config.host,
            port=self.config.port,
            database=self.config.database,
            user=self.config.user,
            password=self.config.password,
        )

    @contextmanager
    def get_cursor(self, dict_cursor: bool = True) -> Generator[Any, None, None]:
        """Context manager for database cursor.

        Args:
            dict_cursor: If True, returns rows as dicts (default behavior)

        Yields:
            Pg8000Cursor wrapper

        Example:
            with db.get_cursor() as cur:
                cur.execute("SELECT * FROM table")
                rows = cur.fetchall()
        """
        conn = None
        try:
            conn = self._create_connection()
            cursor = Pg8000Cursor(conn, dict_cursor=dict_cursor)
            yield cursor
            # pg8000.native auto-commits, but we call it explicitly for clarity
        except Exception:
            raise
        finally:
            if conn:
                conn.close()

    def test_connection(self) -> tuple[bool, str]:
        """Test database connection.

        Returns:
            Tuple of (success, message)
        """
        try:
            with self.get_cursor() as cur:
                cur.execute("SELECT 1")
                return True, "Connection OK"
        except Exception as e:
            return False, str(e)


class Pg8000Cursor:
    """Cursor wrapper for pg8000.native to provide psycopg2-like interface."""

    def __init__(self, conn: pg8000.native.Connection, dict_cursor: bool = True):
        self._conn = conn
        self._dict_cursor = dict_cursor
        self._columns: list = []
        self._rows: list = []
        self._row_index: int = 0

    def execute(self, query: str, params: tuple = None):
        """Execute a query."""
        if params:
            # pg8000.native uses :name or positional, convert %s to positional
            # Replace %s with $1, $2, etc.
            converted_query = query
            param_index = 1
            while "%s" in converted_query:
                converted_query = converted_query.replace("%s", f"${param_index}", 1)
                param_index += 1
            result = self._conn.run(converted_query, list(params))
        else:
            result = self._conn.run(query)

        # Store column names if available
        if self._conn.columns:
            self._columns = [col["name"] for col in self._conn.columns]
        else:
            self._columns = []

        self._rows = result if result else []
        self._row_index = 0

    def fetchone(self):
        """Fetch one row."""
        if self._row_index >= len(self._rows):
            return None
        row = self._rows[self._row_index]
        self._row_index += 1
        if self._dict_cursor and self._columns:
            return dict(zip(self._columns, row))
        return row

    def fetchall(self):
        """Fetch all remaining rows."""
        rows = self._rows[self._row_index:]
        self._row_index = len(self._rows)
        if self._dict_cursor and self._columns:
            return [dict(zip(self._columns, row)) for row in rows]
        return rows

    @property
    def rowcount(self) -> int:
        """Return number of affected rows."""
        return self._conn.row_count if self._conn.row_count else 0

    def close(self):
        """Close cursor (no-op for pg8000.native)."""
        pass
