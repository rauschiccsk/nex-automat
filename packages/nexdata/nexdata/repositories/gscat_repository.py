"""
Repository for GSCAT (Katalóg)
"""

from nexdata.models.gscat import GSCATRecord
from nexdata.repositories.base_repository import BaseRepository


class GSCATRepository(BaseRepository[GSCATRecord]):
    """Repository for accessing GSCAT records (Katalóg)"""

    @property
    def table_name(self) -> str:
        """Get table file path"""
        return "gscat"

    def from_bytes(self, data: bytes) -> GSCATRecord:
        """Convert bytes to GSCATRecord"""
        return GSCATRecord.from_bytes(data)

    def to_bytes(self, record) -> bytes:
        """Convert record to bytes"""
        return record.to_bytes()

    def get_by_code(self, code: str) -> GSCATRecord | None:
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

    def search_by_name(self, search_term: str, limit: int = 20) -> list[GSCATRecord]:
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
            if search_lower in record.gs_name.lower():
                results.append(record)

        return results

    def find_by_barcode(self, barcode: str) -> GSCATRecord | None:
        """
        Find product by primary barcode in GSCAT - LIVE query

        Most products (95%) have only one barcode stored in GSCAT.
        This is faster than searching BARCODE table.

        Args:
            barcode: Barcode string to search for

        Returns:
            GSCATRecord if found, None otherwise
        """
        try:
            # Search all products for matching barcode
            for product in self.get_all():
                if product.BarCode and product.BarCode.strip() == barcode:
                    return product

            return None

        except Exception:
            return None
