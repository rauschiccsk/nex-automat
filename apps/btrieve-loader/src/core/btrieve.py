"""
Singleton BtrieveClient wrapper for Btrieve-Loader REST API.

Provides connection pooling and reuse for Btrieve database access.
"""

import threading
from contextlib import contextmanager
from typing import Generator

from nexdata.btrieve.btrieve_client import BtrieveClient

from .config import settings


class BtrieveClientManager:
    """
    Thread-safe singleton manager for BtrieveClient instances.

    Provides connection pooling and automatic resource management.
    """

    _instance: "BtrieveClientManager | None" = None
    _lock = threading.Lock()

    def __new__(cls) -> "BtrieveClientManager":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        if self._initialized:
            return
        self._initialized = True
        self._client: BtrieveClient | None = None
        self._client_lock = threading.Lock()
        self._open_files: dict[str, bytes] = {}  # table_name -> position_block

    @property
    def client(self) -> BtrieveClient:
        """Get or create BtrieveClient instance."""
        if self._client is None:
            with self._client_lock:
                if self._client is None:
                    self._client = BtrieveClient(settings.btrieve_config)
        return self._client

    def open_table(self, table_name: str, owner: str = "") -> bytes:
        """
        Open a Btrieve table and cache the position block.

        Args:
            table_name: Table name (e.g., 'gscat', 'pab', 'tsh-001')
            owner: Owner password for secured files

        Returns:
            Position block bytes

        Raises:
            RuntimeError: If file cannot be opened
        """
        if table_name in self._open_files:
            return self._open_files[table_name]

        owner_name = owner or settings.btrieve_owner
        status, pos_block = self.client.open_file(table_name, owner_name=owner_name)

        if status != BtrieveClient.STATUS_SUCCESS:
            raise RuntimeError(
                f"Failed to open {table_name}: {self.client.get_status_message(status)}"
            )

        self._open_files[table_name] = pos_block
        return pos_block

    def close_table(self, table_name: str) -> None:
        """Close a cached Btrieve table."""
        if table_name in self._open_files:
            pos_block = self._open_files.pop(table_name)
            self.client.close_file(pos_block)

    def close_all(self) -> None:
        """Close all open tables."""
        for table_name in list(self._open_files.keys()):
            self.close_table(table_name)

    @contextmanager
    def table_session(self, table_name: str, owner: str = "") -> Generator[bytes, None, None]:
        """
        Context manager for table access.

        Args:
            table_name: Table name to open
            owner: Owner password

        Yields:
            Position block for table operations
        """
        pos_block = self.open_table(table_name, owner)
        try:
            yield pos_block
        finally:
            # Keep connection open for reuse (don't close)
            pass

    def get_first(self, table_name: str, key_num: int = 0) -> tuple[int, bytes]:
        """Get first record from table."""
        pos_block = self.open_table(table_name)
        return self.client.get_first(pos_block, key_num)

    def get_next(self, table_name: str) -> tuple[int, bytes]:
        """Get next record from table."""
        pos_block = self._open_files.get(table_name)
        if pos_block is None:
            raise RuntimeError(f"Table {table_name} not open")
        return self.client.get_next(pos_block)


# Global singleton instance
_manager: BtrieveClientManager | None = None


def get_btrieve_client() -> BtrieveClientManager:
    """Get the global BtrieveClientManager instance."""
    global _manager
    if _manager is None:
        _manager = BtrieveClientManager()
    return _manager


def get_btrieve_manager() -> BtrieveClientManager:
    """Alias for get_btrieve_client (FastAPI dependency)."""
    return get_btrieve_client()
