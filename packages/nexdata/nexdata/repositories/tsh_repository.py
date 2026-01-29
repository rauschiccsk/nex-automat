"""
Repository for TSH (Dodacie listy - Header)
"""

from nexdata.btrieve.btrieve_client import BtrieveClient
from nexdata.models.tsh import TSHRecord
from nexdata.repositories.base_repository import BaseRepository


class TSHRepository(BaseRepository[TSHRecord]):
    """Repository for accessing TSH records (Dodacie listy - Header)"""

    def __init__(self, btrieve_client: BtrieveClient, book_id: str = "001"):
        """
        Initialize TSH repository

        Args:
            btrieve_client: Btrieve client instance
            book_id: Book identifier (default: "001")
        """
        self.book_id = book_id
        super().__init__(btrieve_client)

    @property
    def table_name(self) -> str:
        """Get table file path"""
        return f"tsh-{self.book_id}"

    def from_bytes(self, data: bytes) -> TSHRecord:
        """Convert bytes to TSHRecord"""
        return TSHRecord.from_bytes(data)

    def to_bytes(self, record) -> bytes:
        """Convert record to bytes"""
        return record.to_bytes()

    def get_by_document_number(self, doc_number: str) -> TSHRecord | None:
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

    def get_recent_documents(self, limit: int = 100) -> list[TSHRecord]:
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
