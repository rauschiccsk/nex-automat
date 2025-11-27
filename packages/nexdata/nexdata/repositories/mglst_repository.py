"""
Repository for MGLST (Pohyby)
"""

from typing import Optional, List
from nexdata.repositories.base_repository import BaseRepository
from nexdata.models.mglst import MGLSTRecord
from nexdata.btrieve.btrieve_client import BtrieveClient


class MGLSTRepository(BaseRepository[MGLSTRecord]):
    """Repository for accessing MGLST records (Pohyby)"""

    @property
    def table_name(self) -> str:
        """Get table file path"""
        return 'mglst'

    def from_bytes(self, data: bytes) -> MGLSTRecord:
        """Convert bytes to MGLSTRecord"""
        return MGLSTRecord.from_bytes(data)

    def to_bytes(self, record) -> bytes:
        """Convert record to bytes"""
        return record.to_bytes()
    def get_by_product_code(self, product_code: str) -> List[MGLSTRecord]:
        """
        Get all movements for product code

        Args:
            product_code: Product code

        Returns:
            List of movement records
        """
        results = []

        for record in self.get_all():
            if record.C_001.strip() == product_code.strip():
                results.append(record)

        return results

    def get_recent_movements(self, limit: int = 100) -> List[MGLSTRecord]:
        """
        Get recent movements (limited)

        Args:
            limit: Maximum number of records

        Returns:
            List of movement records
        """
        results = []
        count = 0

        for record in self.get_all():
            results.append(record)
            count += 1
            if count >= limit:
                break

        return results
