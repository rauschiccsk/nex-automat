"""
Repository for BARCODE (Čiarové kódy)
"""

from typing import Optional, List
from nexdata.repositories.base_repository import BaseRepository
from nexdata.models.barcode import BarcodeRecord
from nexdata.btrieve.btrieve_client import BtrieveClient


class BARCODERepository(BaseRepository[BarcodeRecord]):
    """Repository for accessing BARCODE records (Čiarové kódy)"""

    @property
    def table_name(self) -> str:
        """Get table file path"""
        return 'barcode'

    def from_bytes(self, data: bytes) -> BarcodeRecord:
        """Convert bytes to BarcodeRecord"""
        return BarcodeRecord.from_bytes(data)

    def to_bytes(self, record) -> bytes:
        """Convert record to bytes"""
        return record.to_bytes()
    def get_by_barcode(self, barcode: str) -> Optional[BarcodeRecord]:
        """
        Get BARCODE record by barcode

        Args:
            barcode: Barcode string

        Returns:
            BarcodeRecord if found, None otherwise
        """
        for record in self.get_all():
            if record.C_001.strip() == barcode.strip():
                return record
        return None

    def get_by_product_code(self, product_code: str) -> List[BarcodeRecord]:
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
    def find_by_barcode(self, barcode: str) -> Optional[BarcodeRecord]:
        """
        Find barcode record by barcode string - LIVE query
        
        Args:
            barcode: Barcode string to search for
            
        Returns:
            BarcodeRecord if found, None otherwise
        """
        file = None
        try:
            # Open BARCODE file
            file = self.btrieve.open(self.barcode_file)
            
            # Search by barcode (BAR_CODE field)
            result = file.get_equal(barcode.encode('cp852'))
            
            if result:
                return self._parse_record(result)
            
            return None
            
        except Exception as e:
            # Record not found or other error
            return None
        finally:
            if file:
                file.close()


