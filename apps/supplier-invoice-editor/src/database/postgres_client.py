"""
PostgreSQL Client - Database connection using pg8000 (Pure Python)
"""

import logging
from contextlib import contextmanager
from typing import Dict, List, Optional

try:
    import pg8000
    import pg8000.dbapi

    PG8000_AVAILABLE = True
except ImportError:
    PG8000_AVAILABLE = False
    pg8000 = None


class PostgresClient:
    """PostgreSQL database client using pg8000"""

    def __init__(self, config):
        """
        Initialize PostgreSQL client

        Args:
            config: Configuration object
        """
        self.config = config
        self.logger = logging.getLogger(__name__)

        if not PG8000_AVAILABLE:
            raise ImportError("pg8000 not installed. Install with: pip install pg8000")

        # Get connection parameters
        self.conn_params = self._get_connection_params()

        # Test connection
        self.logger.info("PostgreSQL client initialized with pg8000")

    def _get_connection_params(self) -> dict:
        """Get connection parameters from config"""
        # Check if config is already a connection dict (has 'host' key)
        if isinstance(self.config, dict) and "host" in self.config:
            # Direct connection params
            params = {
                "host": self.config.get("host", "localhost"),
                "port": self.config.get("port", 5432),
                "database": self.config.get("database", "supplier_invoice_editor"),
                "user": self.config.get("user", "postgres"),
                "password": self.config.get("password", ""),
            }
        else:
            # Config object - try to get nested config
            db_config = self.config.get("database.postgres", {})
            if not db_config:
                db_config = self.config.get("postgresql", {})

            params = {
                "host": db_config.get("host", "localhost"),
                "port": db_config.get("port", 5432),
                "database": db_config.get("database", "supplier_invoice_editor"),
                "user": db_config.get("user", "postgres"),
                "password": db_config.get("password", ""),
            }

        self.logger.info(
            f"Connection params: host={params['host']} port={params['port']} database={params['database']} user={params['user']}"
        )

        return params

    @contextmanager
    def get_connection(self):
        """
        Get database connection (context manager)

        Usage:
            with client.get_connection() as conn:
                cur = conn.cursor()
                cur.execute("SELECT * FROM table")
        """
        conn = None
        try:
            conn = pg8000.dbapi.connect(**self.conn_params)
            yield conn
        finally:
            if conn:
                conn.close()

    def execute_query(self, query: str, params: tuple = None, fetch: bool = True) -> list[dict] | None:
        """
        Execute SQL query

        Args:
            query: SQL query string
            params: Query parameters
            fetch: Whether to fetch results

        Returns:
            List of result dictionaries if fetch=True, None otherwise
        """
        try:
            with self.get_connection() as conn:
                cur = conn.cursor()
                cur.execute(query, params or ())

                if fetch:
                    # Get column names
                    columns = [desc[0] for desc in cur.description] if cur.description else []

                    # Fetch rows and convert to dictionaries
                    rows = cur.fetchall()
                    results = [dict(zip(columns, row)) for row in rows]

                    cur.close()
                    self.logger.debug(f"Query returned {len(results)} rows")
                    return results
                else:
                    conn.commit()
                    cur.close()
                    self.logger.debug("Query executed, no results")
                    return None

        except Exception:
            self.logger.exception(f"Query execution failed: {query}")
            raise

    def execute_many(self, query: str, params_list: list[tuple]) -> int:
        """
        Execute query with multiple parameter sets

        Args:
            query: SQL query string
            params_list: List of parameter tuples

        Returns:
            Number of affected rows
        """
        try:
            with self.get_connection() as conn:
                cur = conn.cursor()
                cur.executemany(query, params_list)
                conn.commit()
                affected = cur.rowcount
                cur.close()
                self.logger.info(f"Batch execution affected {affected} rows")
                return affected

        except Exception:
            self.logger.exception("Batch execution failed")
            raise

    @contextmanager
    def transaction(self):
        """
        Transaction context manager

        Usage:
            with client.transaction() as conn:
                cur = conn.cursor()
                cur.execute("INSERT ...")
                cur.execute("UPDATE ...")
                # Auto-commit on success, rollback on exception
        """
        conn = None
        try:
            conn = pg8000.dbapi.connect(**self.conn_params)
            yield conn
            conn.commit()
            self.logger.debug("Transaction committed")
        except Exception as e:
            if conn:
                conn.rollback()
            self.logger.error(f"Transaction rolled back: {e}")
            raise
        finally:
            if conn:
                conn.close()

    def test_connection(self) -> bool:
        """
        Test database connection

        Returns:
            True if connection successful
        """
        try:
            result = self.execute_query("SELECT 1 as test", fetch=True)
            self.logger.info("Database connection test successful")
            return result is not None
        except Exception as e:
            self.logger.error(f"Database connection test failed: {e}")
            return False

    def close(self):
        """Close connections (pg8000 connections are closed in context managers)"""
        self.logger.info("PostgreSQL client closed")
