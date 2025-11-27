"""
Create repositories for GSCAT, BARCODE, PAB, MGLST
"""

from pathlib import Path

TARGET_DIR = Path("packages/nex-shared/repositories")

GSCAT_REPOSITORY = '''"""
Repository for GSCAT (Katalóg)
"""

from typing import Optional, List
from nex_shared.repositories.base_repository import BaseRepository
from nex_shared.models.gscat import GSCATRecord
from nex_shared.btrieve.btrieve_client import BtrieveClient


class GSCATRepository(BaseRepository[GSCATRecord]):
    """Repository for accessing GSCAT records (Katalóg)"""

    @property
    def table_name(self) -> str:
        """Get table file path"""
        return "C:/NEX/GSCAT.BTR"

    def from_bytes(self, data: bytes) -> GSCATRecord:
        """Convert bytes to GSCATRecord"""
        return GSCATRecord.from_bytes(data)

    def get_by_code(self, code: str) -> Optional[GSCATRecord]:
        """
        Get GSCAT record by product code

        Args:
            code: Product code

        Returns:
            GSCATRecord if found, None otherwise
        """
        for record in self.get_all():
            if record.C_001.strip() == code.strip():
                return record
        return None

    def search_by_name(self, search_term: str) -> List[GSCATRecord]:
        """
        Search products by name

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
'''

BARCODE_REPOSITORY = '''"""
Repository for BARCODE (Čiarové kódy)
"""

from typing import Optional, List
from nex_shared.repositories.base_repository import BaseRepository
from nex_shared.models.barcode import BARCODERecord
from nex_shared.btrieve.btrieve_client import BtrieveClient


class BARCODERepository(BaseRepository[BARCODERecord]):
    """Repository for accessing BARCODE records (Čiarové kódy)"""

    @property
    def table_name(self) -> str:
        """Get table file path"""
        return "C:/NEX/BARCODE.BTR"

    def from_bytes(self, data: bytes) -> BARCODERecord:
        """Convert bytes to BARCODERecord"""
        return BARCODERecord.from_bytes(data)

    def get_by_barcode(self, barcode: str) -> Optional[BARCODERecord]:
        """
        Get BARCODE record by barcode

        Args:
            barcode: Barcode string

        Returns:
            BARCODERecord if found, None otherwise
        """
        for record in self.get_all():
            if record.C_001.strip() == barcode.strip():
                return record
        return None

    def get_by_product_code(self, product_code: str) -> List[BARCODERecord]:
        """
        Get all barcodes for product code

        Args:
            product_code: Product code

        Returns:
            List of barcode records
        """
        results = []

        for record in self.get_all():
            if record.C_002.strip() == product_code.strip():
                results.append(record)

        return results
'''

PAB_REPOSITORY = '''"""
Repository for PAB (Adresár)
"""

from typing import Optional, List
from nex_shared.repositories.base_repository import BaseRepository
from nex_shared.models.pab import PABRecord
from nex_shared.btrieve.btrieve_client import BtrieveClient


class PABRepository(BaseRepository[PABRecord]):
    """Repository for accessing PAB records (Adresár)"""

    @property
    def table_name(self) -> str:
        """Get table file path"""
        return "C:/NEX/PAB.BTR"

    def from_bytes(self, data: bytes) -> PABRecord:
        """Convert bytes to PABRecord"""
        return PABRecord.from_bytes(data)

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
'''

MGLST_REPOSITORY = '''"""
Repository for MGLST (Pohyby)
"""

from typing import Optional, List
from nex_shared.repositories.base_repository import BaseRepository
from nex_shared.models.mglst import MGLSTRecord
from nex_shared.btrieve.btrieve_client import BtrieveClient


class MGLSTRepository(BaseRepository[MGLSTRecord]):
    """Repository for accessing MGLST records (Pohyby)"""

    @property
    def table_name(self) -> str:
        """Get table file path"""
        return "C:/NEX/MGLST.BTR"

    def from_bytes(self, data: bytes) -> MGLSTRecord:
        """Convert bytes to MGLSTRecord"""
        return MGLSTRecord.from_bytes(data)

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
'''


def create_repositories():
    print("=" * 60)
    print("CREATE: GSCAT, BARCODE, PAB, MGLST Repositories")
    print("=" * 60)

    # Check target directory
    if not TARGET_DIR.exists():
        print(f"❌ Target directory not found: {TARGET_DIR}")
        return False

    print(f"\n✅ Target: {TARGET_DIR}")

    # Create files
    files = [
        ("gscat_repository.py", GSCAT_REPOSITORY),
        ("barcode_repository.py", BARCODE_REPOSITORY),
        ("pab_repository.py", PAB_REPOSITORY),
        ("mglst_repository.py", MGLST_REPOSITORY)
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
        print("   - GSCATRepository (Katalóg)")
        print("   - BARCODERepository (Čiarové kódy)")
        print("   - PABRepository (Adresár)")
        print("   - MGLSTRepository (Pohyby)")

    return success_count == len(files)


if __name__ == "__main__":
    success = create_repositories()
    exit(0 if success else 1)