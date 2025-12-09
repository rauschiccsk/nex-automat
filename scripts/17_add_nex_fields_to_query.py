"""
Script 17: Add NEX fields to invoice_service.py SELECT query
Phase 4: Editor integration
"""

from pathlib import Path


def main():
    """Add NEX enrichment fields to SELECT query"""

    dev_root = Path(r"C:\Development\nex-automat")
    service_file = dev_root / "apps" / "supplier-invoice-editor" / "src" / "business" / "invoice_service.py"

    if not service_file.exists():
        print(f"❌ File not found: {service_file}")
        return False

    print(f"📝 Reading: {service_file.relative_to(dev_root)}")
    content = service_file.read_text(encoding='utf-8')

    # Check if already modified
    if 'nex_name' in content and 'matched_by' in content:
        print("⚠️  NEX fields already added to query - skipping")
        return True

    # Replace the SELECT query in _get_items_from_database method
    old_query = """        query = \"\"\"
            SELECT
                id,
                invoice_id,
                line_number,
                COALESCE(edited_name, original_name) as item_name,
                COALESCE(edited_mglst_code, 0) as category_code,
                original_unit as unit,
                original_quantity as quantity,
                COALESCE(edited_price_buy, original_price_per_unit) as unit_price,
                COALESCE(edited_discount_percent, 0.00) as rabat_percent,
                COALESCE(final_price_buy, edited_price_buy, original_price_per_unit) as price_after_rabat,
                (COALESCE(final_price_buy, edited_price_buy, original_price_per_unit) * original_quantity) as total_price,
                COALESCE(CAST(nex_gs_code AS VARCHAR), original_ean, '') as plu_code,
                original_ean,
                was_edited,
                validation_status
            FROM invoice_items_pending
            WHERE invoice_id = %s
            ORDER BY line_number
        \"\"\""""

    new_query = """        query = \"\"\"
            SELECT
                id,
                invoice_id,
                line_number,
                COALESCE(edited_name, original_name) as item_name,
                COALESCE(edited_mglst_code, 0) as category_code,
                original_unit as unit,
                original_quantity as quantity,
                COALESCE(edited_price_buy, original_price_per_unit) as unit_price,
                COALESCE(edited_discount_percent, 0.00) as rabat_percent,
                COALESCE(final_price_buy, edited_price_buy, original_price_per_unit) as price_after_rabat,
                (COALESCE(final_price_buy, edited_price_buy, original_price_per_unit) * original_quantity) as total_price,
                COALESCE(CAST(nex_gs_code AS VARCHAR), original_ean, '') as plu_code,
                original_ean,
                was_edited,
                validation_status,
                -- NEX Genesis enrichment fields
                nex_gs_code,
                nex_plu,
                nex_name,
                nex_category,
                nex_barcode_created,
                in_nex,
                matched_by
            FROM invoice_items_pending
            WHERE invoice_id = %s
            ORDER BY line_number
        \"\"\""""

    content = content.replace(old_query, new_query)

    # Write modified content
    print(f"💾 Writing modified file...")
    service_file.write_text(content, encoding='utf-8')

    print("✅ SUCCESS: invoice_service.py updated with NEX fields")
    print("\nAdded NEX fields to SELECT query:")
    print("  - nex_gs_code")
    print("  - nex_plu")
    print("  - nex_name")
    print("  - nex_category")
    print("  - nex_barcode_created")
    print("  - in_nex (match status)")
    print("  - matched_by (match method)")

    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)