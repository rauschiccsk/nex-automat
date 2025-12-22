"""PostgreSQL connection manager."""

from contextlib import contextmanager
from dataclasses import dataclass
from typing import Optional, Generator, Any
import os

import psycopg2
from psycopg2.extras import RealDictCursor


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

    @contextmanager
    def get_cursor(self, dict_cursor: bool = True) -> Generator[Any, None, None]:
        """Context manager for database cursor.

        Args:
            dict_cursor: If True, returns RealDictCursor for dict-like rows

        Yields:
            Database cursor

        Example:
            with db.get_cursor() as cur:
                cur.execute("SELECT * FROM table")
                rows = cur.fetchall()
        """
        conn = None
        try:
            conn = psycopg2.connect(
                host=self.config.host,
                port=self.config.port,
                database=self.config.database,
                user=self.config.user,
                password=self.config.password,
            )
            cursor_factory = RealDictCursor if dict_cursor else None
            cursor = conn.cursor(cursor_factory=cursor_factory)
            yield cursor
            conn.commit()
        except Exception:
            if conn:
                conn.rollback()
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
