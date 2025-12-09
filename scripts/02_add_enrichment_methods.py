"""
Session Script 02: Add Enrichment Methods to PostgresStagingClient
Adds 4 new methods for NEX Genesis enrichment
"""
from pathlib import Path


def main():
    target_file = Path(r"C:\Development\nex-automat\packages\nex-shared\database\postgres_staging.py")

    print("=" * 60)
    print("Phase 1: Adding Enrichment Methods")
    print("=" * 60)

    # Read current file
    with open(target_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # New methods to add
    new_methods = '''
    def get_pending_enrichment_items(
        self, 
        invoice_id: Optional[int] = None,
        limit: int = 100
    ) -> List[Dict]:
        """
        Get items WHERE in_nex IS NULL OR in_nex = FALSE

        Args:
            invoice_id: Optional invoice ID to filter by
            limit: Maximum number of items to return

        Returns:
            List of items with original and edited data
        """
        cursor = self._conn.cursor()

        if invoice_id:
            cursor.execute("""
                SELECT 
                    id, invoice_id, line_number,
                    original_name, original_ean,
                    original_quantity, original_unit,
                    original_price_per_unit, original_vat_rate,
                    edited_name, edited_ean,
                    was_edited,
                    nex_gs_code, in_nex
                FROM invoice_items_pending
                WHERE invoice_id = %s
                  AND (in_nex IS NULL OR in_nex = FALSE)
                ORDER BY line_number
                LIMIT %s
            """, (invoice_id, limit))
        else:
            cursor.execute("""
                SELECT 
                    id, invoice_id, line_number,
                    original_name, original_ean,
                    original_quantity, original_unit,
                    original_price_per_unit, original_vat_rate,
                    edited_name, edited_ean,
                    was_edited,
                    nex_gs_code, in_nex
                FROM invoice_items_pending
                WHERE in_nex IS NULL OR in_nex = FALSE
                ORDER BY invoice_id, line_number
                LIMIT %s
            """, (limit,))

        rows = cursor.fetchall()
        cursor.close()

        columns = [
            'id', 'invoice_id', 'line_number',
            'original_name', 'original_ean',
            'original_quantity', 'original_unit',
            'original_price_per_unit', 'original_vat_rate',
            'edited_name', 'edited_ean',
            'was_edited',
            'nex_gs_code', 'in_nex'
        ]

        return [dict(zip(columns, row)) for row in rows]

    def update_nex_enrichment(
        self,
        item_id: int,
        gscat_record,
        matched_by: str = 'ean'
    ) -> bool:
        """
        Update item with NEX Genesis data

        Args:
            item_id: Item ID to update
            gscat_record: GSCATRecord from nexdata with product data
            matched_by: Method used for matching ('ean', 'name', 'manual')

        Returns:
            True if update successful
        """
        cursor = self._conn.cursor()

        cursor.execute("""
            UPDATE invoice_items_pending SET
                nex_gs_code = %s,
                nex_plu = %s,
                nex_name = %s,
                nex_category = %s,
                in_nex = TRUE,
                nex_barcode_created = FALSE,
                validation_status = %s,
                validation_message = %s
            WHERE id = %s
        """, (
            gscat_record.gs_code,
            gscat_record.gs_code,
            gscat_record.gs_name,
            gscat_record.mglst_code,
            'matched',
            f'Auto-matched by {matched_by}',
            item_id
        ))

        success = cursor.rowcount > 0
        cursor.close()
        return success

    def mark_no_match(
        self,
        item_id: int,
        reason: str = 'No matching product found'
    ) -> bool:
        """
        Mark item as not found in NEX Genesis

        Args:
            item_id: Item ID to mark
            reason: Reason for no match

        Returns:
            True if update successful
        """
        cursor = self._conn.cursor()

        cursor.execute("""
            UPDATE invoice_items_pending SET
                in_nex = FALSE,
                validation_status = 'needs_review',
                validation_message = %s
            WHERE id = %s
        """, (reason, item_id))

        success = cursor.rowcount > 0
        cursor.close()
        return success

    def get_enrichment_stats(
        self,
        invoice_id: Optional[int] = None
    ) -> Dict:
        """
        Get enrichment statistics

        Args:
            invoice_id: Optional invoice ID to filter by

        Returns:
            Dictionary with enrichment statistics
        """
        cursor = self._conn.cursor()

        if invoice_id:
            cursor.execute("""
                SELECT 
                    COUNT(*) FILTER (WHERE in_nex = TRUE) as enriched,
                    COUNT(*) FILTER (WHERE in_nex = FALSE) as not_found,
                    COUNT(*) FILTER (WHERE in_nex IS NULL) as pending,
                    COUNT(*) as total
                FROM invoice_items_pending
                WHERE invoice_id = %s
            """, (invoice_id,))
        else:
            cursor.execute("""
                SELECT 
                    COUNT(*) FILTER (WHERE in_nex = TRUE) as enriched,
                    COUNT(*) FILTER (WHERE in_nex = FALSE) as not_found,
                    COUNT(*) FILTER (WHERE in_nex IS NULL) as pending,
                    COUNT(*) as total
                FROM invoice_items_pending
            """)

        row = cursor.fetchone()
        cursor.close()

        return {
            'enriched': row[0] or 0,
            'not_found': row[1] or 0,
            'pending': row[2] or 0,
            'total': row[3] or 0
        }
'''

    # Find the right place to insert (before the last line or at the end of class)
    # We'll insert before the last method or at the end

    # Check if methods already exist
    if 'get_pending_enrichment_items' in content:
        print("⚠️  Methods already exist in file")
        return 1

    # Add imports at top if not present
    if 'from typing import Optional, List, Dict' not in content:
        # Find existing typing imports and extend them
        if 'from typing import' in content:
            content = content.replace(
                'from typing import Dict',
                'from typing import Dict, Optional, List',
                1
            )
        else:
            # Add new import after other imports
            import_pos = content.find('\nimport psycopg2')
            if import_pos > 0:
                content = content[:import_pos] + '\nfrom typing import Optional, List, Dict' + content[import_pos:]

    # Find the class and add methods before the last line
    # Look for the last method in PostgresStagingClient class
    class_start = content.find('class PostgresStagingClient')
    if class_start == -1:
        print("❌ PostgresStagingClient class not found")
        return 1

    # Find the end of the class (before next class or end of file)
    # We'll add methods at the end of the class, properly indented
    next_class = content.find('\nclass ', class_start + 1)
    if next_class == -1:
        # No next class, add at end
        insert_pos = len(content)
    else:
        insert_pos = next_class

    # Insert methods
    content = content[:insert_pos] + new_methods + '\n' + content[insert_pos:]

    # Write back
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ Added 4 enrichment methods to {target_file.name}")
    print("\nMethods added:")
    print("  - get_pending_enrichment_items()")
    print("  - update_nex_enrichment()")
    print("  - mark_no_match()")
    print("  - get_enrichment_stats()")

    print("\n" + "=" * 60)
    print("✅ Phase 1 Step 1 complete!")
    print("=" * 60)

    return 0


if __name__ == '__main__':
    import sys

    sys.exit(main())