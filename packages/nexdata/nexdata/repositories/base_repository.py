"""
Base Repository Pattern
Fix: Replace BtrStatus with BtrieveClient status codes
"""

from typing import Generic, TypeVar, Optional, List, Callable
from abc import ABC, abstractmethod
from nexdata.btrieve.btrieve_client import BtrieveClient
import logging

logger = logging.getLogger(__name__)

T = TypeVar('T')


class BaseRepository(Generic[T], ABC):
    """Base repository providing common CRUD operations"""

    def __init__(self, btrieve_client: BtrieveClient):
        """Initialize repository with Btrieve client"""
        self.client = btrieve_client
        self._is_open = False

    @property
    @abstractmethod
    def table_name(self) -> str:
        """Table name for BtrieveClient (e.g., 'gscat', 'barcode')"""
        pass

    @abstractmethod
    def from_bytes(self, data: bytes) -> T:
        """Convert raw Btrieve bytes to model instance"""
        pass

    @abstractmethod
    def to_bytes(self, record: T) -> bytes:
        """Convert model instance to raw Btrieve bytes"""
        pass

    def open(self) -> bool:
        """Open Btrieve table"""
        if self._is_open:
            return True

        status, pos_block = self.client.open_file(self.table_name)
        if status == BtrieveClient.STATUS_SUCCESS:
            self._is_open = True
            self._pos_block = pos_block
            logger.debug(f"Opened table: {self.table_name}")
            return True
        else:
            logger.error(f"Failed to open table {self.table_name}: {status}")
            return False

    def close(self):
        """Close Btrieve table"""
        if self._is_open and hasattr(self, '_pos_block'):
            self.client.close_file(self._pos_block)
            self._is_open = False
            logger.debug(f"Closed table: {self.table_name}")

    def __enter__(self):
        """Context manager entry"""
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()

    def get_first(self) -> Optional[T]:
        """Get first record in table"""
        if not self._is_open:
            if not self.open():
                return None

        status, data = self.client.get_first(self._pos_block)
        if status == BtrieveClient.STATUS_SUCCESS:
            try:
                return self.from_bytes(data)
            except Exception as e:
                logger.error(f"Failed to deserialize record: {e}")
                return None
        else:
            return None

    def get_next(self) -> Optional[T]:
        """Get next record in current position"""
        if not self._is_open:
            return None

        status, data = self.client.get_next(self._pos_block)
        if status == BtrieveClient.STATUS_SUCCESS:
            try:
                return self.from_bytes(data)
            except Exception as e:
                logger.error(f"Failed to deserialize record: {e}")
                return None
        else:
            return None

    def get_all(self, max_records: int = 10000) -> List[T]:
        """Get all records from table"""
        records = []

        if not self._is_open:
            if not self.open():
                return records

        record = self.get_first()
        if record:
            records.append(record)
        else:
            return records

        while len(records) < max_records:
            record = self.get_next()
            if record is None:
                break
            records.append(record)

        logger.info(f"Retrieved {len(records)} records from {self.table_name}")
        return records

    def find(self, predicate: Callable[[T], bool], max_results: int = 100) -> List[T]:
        """Find records matching predicate"""
        results = []

        if not self._is_open:
            if not self.open():
                return results

        record = self.get_first()
        while record and len(results) < max_results:
            if predicate(record):
                results.append(record)
            record = self.get_next()

        logger.debug(f"Found {len(results)} matching records in {self.table_name}")
        return results

    def find_one(self, predicate: Callable[[T], bool]) -> Optional[T]:
        """Find first record matching predicate"""
        if not self._is_open:
            if not self.open():
                return None

        record = self.get_first()
        while record:
            if predicate(record):
                return record
            record = self.get_next()

        return None

    def exists(self, predicate: Callable[[T], bool]) -> bool:
        """Check if any record matches predicate"""
        return self.find_one(predicate) is not None


class ReadOnlyRepository(BaseRepository[T], ABC):
    """Read-only repository (no write operations)"""

    def insert(self, record: T):
        """Not implemented for read-only repository"""
        raise NotImplementedError("Insert not allowed on read-only repository")

    def update(self, record: T):
        """Not implemented for read-only repository"""
        raise NotImplementedError("Update not allowed on read-only repository")


class CRUDRepository(BaseRepository[T], ABC):
    """Full CRUD repository with write operations"""

    def insert(self, record: T) -> bool:
        """Insert new record"""
        if not self._is_open:
            if not self.open():
                return False

        # Validate before insert
        if hasattr(record, 'validate'):
            errors = record.validate()
            if errors:
                logger.error(f"Validation failed: {errors}")
                return False

        try:
            data = self.to_bytes(record)
            # Note: Actual Btrieve insert operation needs implementation
            logger.info(f"Insert to {self.table_name} (stub)")
            return True
        except Exception as e:
            logger.error(f"Insert error: {e}")
            return False

    def update(self, record: T) -> bool:
        """Update existing record"""
        if not self._is_open:
            if not self.open():
                return False

        # Validate before update
        if hasattr(record, 'validate'):
            errors = record.validate()
            if errors:
                logger.error(f"Validation failed: {errors}")
                return False

        try:
            data = self.to_bytes(record)
            # Note: Actual Btrieve update operation needs implementation
            logger.info(f"Update in {self.table_name} (stub)")
            return True
        except Exception as e:
            logger.error(f"Update error: {e}")
            return False
