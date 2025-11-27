"""
Repository for TSI (Dodacie listy - Items)
"""

from typing import Optional, List
from nexdata.repositories.base_repository import BaseRepository
from nexdata.models.tsi import TSIRecord
from nexdata.btrieve.btrieve_client import BtrieveClient


class TSIRepository(BaseRepository[TSIRecord]):
    """Repository for accessing TSI records (Dodacie listy - Items)"""

    def __init__(self, btrieve_client: BtrieveClient, book_id: str = "001"):
        """
        Initialize TSI repository

        Args:
            btrieve_client: Btrieve client instance
            book_id: Book identifier (default: "001")
        """
        self.book_id = book_id
        super().__init__(btrieve_client)

    @property
    def table_name(self) -> str:
        """Get table file path"""
        return f'tsi-{self.book_id}'

    def from_bytes(self, data: bytes) -> TSIRecord:
        """Convert bytes to TSIRecord"""
        return TSIRecord.from_bytes(data)

    def to_bytes(self, record) -> bytes:
        """Convert record to bytes"""
        return record.to_bytes()
    def get_by_document(self, doc_number: str) -> List[TSIRecord]:
        """
        Get all items for specific document

        Args:
            doc_number: Document number (e.g., "240001")

        Returns:
            List of TSI records for the document
        """
        items = []

        for record in self.get_all():
            if record.C_001 == doc_number:
                items.append(record)

        return items

    def get_by_document_and_line(
        self, 
        doc_number: str, 
        line_number: int
    ) -> Optional[TSIRecord]:
        """
        Get specific item by document and line number

        Args:
            doc_number: Document number
            line_number: Line number within document

        Returns:
            TSIRecord if found, None otherwise
        """
        for record in self.get_all():
            if record.C_001 == doc_number and record.P_001 == line_number:
                return record

        return None
