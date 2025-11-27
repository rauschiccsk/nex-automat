"""
Repository for TSH (Dodacie listy - Header)
"""

from typing import Optional, List
from nexdata.repositories.base_repository import BaseRepository
from nexdata.models.tsh import TSHRecord
from nexdata.btrieve.btrieve_client import BtrieveClient


class TSHRepository(BaseRepository[TSHRecord]):
    """Repository for accessing TSH records (Dodacie listy - Header)"""

    def __init__(self, btrieve_client: BtrieveClient, store_id: str = "001"):
        """
        Initialize TSH repository

        Args:
            btrieve_client: Btrieve client instance
            store_id: Store identifier (default: "001")
        """
        self.store_id = store_id
        super().__init__(btrieve_client)

    @property
    def table_name(self) -> str:
        """Get table file path"""
        return f"C:/NEX/YEARACT/STORES/TSHA-{self.store_id}.BTR"

    def from_bytes(self, data: bytes) -> TSHRecord:
        """Convert bytes to TSHRecord"""
        return TSHRecord.from_bytes(data)

    def to_bytes(self, record) -> bytes:
        """Convert record to bytes"""
        return record.to_bytes()
    def get_by_document_number(self, doc_number: str) -> Optional[TSHRecord]:
        """
        Get TSH record by document number

        Args:
            doc_number: Document number (e.g., "240001")

        Returns:
            TSHRecord if found, None otherwise
        """
        # Search through all records
        for record in self.get_all():
            if record.C_001 == doc_number:
                return record
        return None

    def get_recent_documents(self, limit: int = 100) -> List[TSHRecord]:
        """
        Get recent documents (limited)

        Args:
            limit: Maximum number of records to return

        Returns:
            List of TSH records
        """
        records = []
        count = 0

        for record in self.get_all():
            records.append(record)
            count += 1
            if count >= limit:
                break

        return records
