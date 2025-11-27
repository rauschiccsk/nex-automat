"""
Repository for PAB (Adresár)
"""

from typing import Optional, List
from nexdata.repositories.base_repository import BaseRepository
from nexdata.models.pab import PABRecord
from nexdata.btrieve.btrieve_client import BtrieveClient


class PABRepository(BaseRepository[PABRecord]):
    """Repository for accessing PAB records (Adresár)"""

    @property
    def table_name(self) -> str:
        """Get table file path"""
        return 'pab'

    def from_bytes(self, data: bytes) -> PABRecord:
        """Convert bytes to PABRecord"""
        return PABRecord.from_bytes(data)

    def to_bytes(self, record) -> bytes:
        """Convert record to bytes"""
        return record.to_bytes()
    def get_by_code(self, code: str) -> Optional[PABRecord]:
        """
        Get PAB record by code

        Args:
            code: Address code

        Returns:
            PABRecord if found, None otherwise
        """
        for record in self.get_all():
            if record.C_001.strip() == code.strip():
                return record
        return None

    def search_by_name(self, search_term: str) -> List[PABRecord]:
        """
        Search addresses by name

        Args:
            search_term: Search term

        Returns:
            List of matching records
        """
        results = []
        search_lower = search_term.lower()

        for record in self.get_all():
            if search_lower in record.C_002.lower():
                results.append(record)

        return results

    def get_suppliers(self) -> List[PABRecord]:
        """
        Get all supplier records

        Returns:
            List of supplier records
        """
        results = []

        for record in self.get_all():
            # P_004 = Supplier flag
            if record.P_004 == 1:
                results.append(record)

        return results
