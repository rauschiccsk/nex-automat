"""
Create TSH and TSI repositories for supplier-invoice-loader
"""

from pathlib import Path

TARGET_DIR = Path("packages/nex-shared/repositories")

TSH_REPOSITORY = '''"""
Repository for TSH (Dodacie listy - Header)
"""

from typing import Optional, List
from nex_shared.repositories.base_repository import BaseRepository
from nex_shared.models.tsh import TSHRecord
from nex_shared.btrieve.btrieve_client import BtrieveClient


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
'''

TSI_REPOSITORY = '''"""
Repository for TSI (Dodacie listy - Items)
"""

from typing import Optional, List
from nex_shared.repositories.base_repository import BaseRepository
from nex_shared.models.tsi import TSIRecord
from nex_shared.btrieve.btrieve_client import BtrieveClient


class TSIRepository(BaseRepository[TSIRecord]):
    """Repository for accessing TSI records (Dodacie listy - Items)"""

    def __init__(self, btrieve_client: BtrieveClient, store_id: str = "001"):
        """
        Initialize TSI repository

        Args:
            btrieve_client: Btrieve client instance
            store_id: Store identifier (default: "001")
        """
        self.store_id = store_id
        super().__init__(btrieve_client)

    @property
    def table_name(self) -> str:
        """Get table file path"""
        return f"C:/NEX/YEARACT/STORES/TSIA-{self.store_id}.BTR"

    def from_bytes(self, data: bytes) -> TSIRecord:
        """Convert bytes to TSIRecord"""
        return TSIRecord.from_bytes(data)

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
'''


def create_repositories():
    print("=" * 60)
    print("CREATE: TSH/TSI Repositories")
    print("=" * 60)

    # Check target directory
    if not TARGET_DIR.exists():
        print(f"❌ Target directory not found: {TARGET_DIR}")
        return False

    print(f"\n✅ Target: {TARGET_DIR}")

    # Create files
    files = [
        ("tsh_repository.py", TSH_REPOSITORY),
        ("tsi_repository.py", TSI_REPOSITORY)
    ]

    success_count = 0

    print(f"\n📋 Creating {len(files)} repository files:")
    print("-" * 60)

    for filename, content in files:
        filepath = TARGET_DIR / filename

        try:
            # Write file
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)

            size = filepath.stat().st_size
            print(f"✅ {filename:<25} - Created ({size:,} bytes)")
            success_count += 1

        except Exception as e:
            print(f"❌ {filename:<25} - Error: {e}")

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY:")
    print(f"  ✅ Created: {success_count}/{len(files)}")
    print("=" * 60)

    if success_count == len(files):
        print("\n📋 Created repositories:")
        print("   - TSHRepository (Dodacie listy - Header)")
        print("   - TSIRepository (Dodacie listy - Items)")
        print("\n📝 Methods:")
        print("   TSH:")
        print("     - get_by_document_number(doc_number)")
        print("     - get_recent_documents(limit=100)")
        print("   TSI:")
        print("     - get_by_document(doc_number)")
        print("     - get_by_document_and_line(doc_number, line_number)")

    return success_count == len(files)


if __name__ == "__main__":
    success = create_repositories()
    exit(0 if success else 1)