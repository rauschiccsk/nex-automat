"""Base Repository Pattern"""

from typing import Generic, TypeVar, Optional, List, Callable
from abc import ABC, abstractmethod
from nex_shared.btrieve.btrieve_client import BtrieveClient
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
        """Table name for BtrieveClient"""
        pass
    
    @abstractmethod
    def from_bytes(self, data: bytes) -> T:
        """Convert raw Btrieve bytes to model instance"""
        pass
    
    def open(self) -> bool:
        """Open Btrieve table"""
        if self._is_open:
            return True
        status, pos_block = self.client.open_file(self.table_name)
        if status == BtrieveClient.STATUS_SUCCESS:
            self._is_open = True
            self._pos_block = pos_block
            return True
        return False
    
    def close(self):
        """Close Btrieve table"""
        if self._is_open and hasattr(self, '_pos_block'):
            self.client.close_file(self._pos_block)
            self._is_open = False
    
    def get_first(self) -> Optional[T]:
        """Get first record"""
        if not self._is_open:
            if not self.open():
                return None
        status, data = self.client.get_first(self._pos_block)
        if status == BtrieveClient.STATUS_SUCCESS:
            try:
                return self.from_bytes(data)
            except Exception as e:
                logger.error(f"Failed to deserialize: {e}")
                return None
        return None
    
    def get_next(self) -> Optional[T]:
        """Get next record"""
        if not self._is_open:
            return None
        status, data = self.client.get_next(self._pos_block)
        if status == BtrieveClient.STATUS_SUCCESS:
            try:
                return self.from_bytes(data)
            except Exception as e:
                logger.error(f"Failed to deserialize: {e}")
                return None
        return None
    
    def get_all(self, max_records: int = 10000) -> List[T]:
        """Get all records"""
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
        return records
