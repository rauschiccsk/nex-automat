"""
Session Script 11: Add Repository Methods for LIVE Queries
Adds find_by_barcode(), get_by_code(), search_by_name()
"""
from pathlib import Path

def main():
    nexdata_path = Path(r"C:\Development\nex-automat\packages\nexdata\nexdata")
    barcode_repo = nexdata_path / "repositories" / "barcode_repository.py"
    gscat_repo = nexdata_path / "repositories" / "gscat_repository.py"

    print("=" * 60)
    print("Phase 3: Adding Repository Methods")
    print("=" * 60)

    # 1. Add find_by_barcode to BARCODERepository
    print("\n[1/2] Updating barcode_repository.py...")

    with open(barcode_repo, 'r', encoding='utf-8') as f:
        barcode_content = f.read()

    if 'find_by_barcode' not in barcode_content:
        barcode_method = '''
    def find_by_barcode(self, barcode: str) -> Optional[BarcodeRecord]:
        """
        Find barcode record by barcode string - LIVE query
        
        Args:
            barcode: Barcode string to search for
            
        Returns:
            BarcodeRecord if found, None otherwise
        """
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
'''

        # Find end of class and insert before last line
        insert_pos = barcode_content.rfind('\n')
        barcode_content = barcode_content[:insert_pos] + barcode_method + '\n' + barcode_content[insert_pos:]

        # Add Optional import if not present
        if 'from typing import Optional' not in barcode_content:
            if 'from typing import List' in barcode_content:
                barcode_content = barcode_content.replace(
                    'from typing import List',
                    'from typing import List, Optional'
                )

        with open(barcode_repo, 'w', encoding='utf-8') as f:
            f.write(barcode_content)

        print("  ✅ Added find_by_barcode()")
    else:
        print("  ⚠️  find_by_barcode() already exists")

    # 2. Add methods to GSCATRepository
    print("\n[2/2] Updating gscat_repository.py...")

    with open(gscat_repo, 'r', encoding='utf-8') as f:
        gscat_content = f.read()

    methods_to_add = []

    if 'get_by_code' not in gscat_content:
        methods_to_add.append('''
    def get_by_code(self, gs_code: int) -> Optional[GSCATRecord]:
        """
        Get product by GS_CODE - LIVE query
        
        Args:
            gs_code: Product code
            
        Returns:
            GSCATRecord if found, None otherwise
        """
        try:
            # Open GSCAT file
            file = self.btrieve.open(self.gscat_file)
            
            # Search by GS_CODE (primary key)
            result = file.get_equal(gs_code.to_bytes(4, byteorder='little'))
            
            if result:
                return self._parse_record(result)
            
            return None
            
        except Exception as e:
            return None
        finally:
            if file:
                file.close()
''')

    if 'search_by_name' not in gscat_content:
        methods_to_add.append('''
    def search_by_name(self, search_term: str, limit: int = 20) -> List[GSCATRecord]:
        """
        Search products by name - LIVE query
        
        Performs case-insensitive search on GS_NAME field
        Returns active products only
        
        Args:
            search_term: Search string (already normalized)
            limit: Maximum number of results
            
        Returns:
            List of matching GSCATRecord objects
        """
        results = []
        
        try:
            # Open GSCAT file
            file = self.btrieve.open(self.gscat_file)
            
            # Get first record
            record = file.get_first()
            
            # Iterate through all records
            while record and len(results) < limit:
                try:
                    product = self._parse_record(record)
                    
                    # Skip discontinued products
                    if product.discontinued:
                        record = file.get_next()
                        continue
                    
                    # Check if name contains search term (case-insensitive)
                    product_name = product.gs_name.lower()
                    if search_term.lower() in product_name:
                        results.append(product)
                    
                    record = file.get_next()
                    
                except Exception:
                    # Skip malformed records
                    record = file.get_next()
                    continue
            
            return results
            
        except Exception as e:
            return results
        finally:
            if file:
                file.close()
''')

    if methods_to_add:
        # Insert methods
        insert_pos = gscat_content.rfind('\n')
        for method in methods_to_add:
            gscat_content = gscat_content[:insert_pos] + method + '\n' + gscat_content[insert_pos:]

        # Add Optional import if not present
        if 'from typing import Optional' not in gscat_content:
            if 'from typing import List' in gscat_content:
                gscat_content = gscat_content.replace(
                    'from typing import List',
                    'from typing import List, Optional'
                )

        with open(gscat_repo, 'w', encoding='utf-8') as f:
            f.write(gscat_content)

        print("  ✅ Added get_by_code()")
        print("  ✅ Added search_by_name()")
    else:
        print("  ⚠️  Methods already exist")

    print("\n" + "=" * 60)
    print("✅ Repository methods added!")
    print("=" * 60)
    print("\nAdded LIVE query methods:")
    print("  - BARCODERepository.find_by_barcode()")
    print("  - GSCATRepository.get_by_code()")
    print("  - GSCATRepository.search_by_name()")

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())