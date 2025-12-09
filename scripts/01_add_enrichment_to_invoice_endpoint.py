"""
Script 01: Add ProductMatcher enrichment to /invoice endpoint
Phase 4: Integration
"""

import os
from pathlib import Path


def main():
    """Modify main.py to add automatic enrichment"""

    # Paths
    dev_root = Path(r"C:\Development\nex-automat")
    main_py = dev_root / "apps" / "supplier-invoice-loader" / "main.py"

    if not main_py.exists():
        print(f"❌ File not found: {main_py}")
        return False

    print(f"📝 Reading: {main_py}")
    content = main_py.read_text(encoding='utf-8')

    # Check if already modified
    if 'from src.business.product_matcher import ProductMatcher' in content:
        print("⚠️  ProductMatcher already imported - skipping")
        return True

    # 1. Add import after existing imports (after logging import)
    import_section = 'from src.utils.logger import setup_logging'
    new_import = '''from src.utils.logger import setup_logging
from src.business.product_matcher import ProductMatcher'''

    content = content.replace(import_section, new_import)

    # 2. Add global product_matcher variable after app creation
    app_creation = 'app = FastAPI(title="Supplier Invoice Loader")'
    new_global = '''app = FastAPI(title="Supplier Invoice Loader")

# Global ProductMatcher instance
product_matcher: Optional[ProductMatcher] = None'''

    content = content.replace(app_creation, new_global)

    # 3. Modify startup event to initialize ProductMatcher
    startup_old = '''@app.on_event("startup")
async def startup_event():
    setup_logging(config.LOG_LEVEL)
    logger.info("Supplier Invoice Loader API started")
    logger.info(f"Upload directory: {config.UPLOAD_DIR}")'''

    startup_new = '''@app.on_event("startup")
async def startup_event():
    global product_matcher
    setup_logging(config.LOG_LEVEL)
    logger.info("Supplier Invoice Loader API started")
    logger.info(f"Upload directory: {config.UPLOAD_DIR}")

    # Initialize ProductMatcher if NEX Genesis is enabled
    if config.NEX_GENESIS_ENABLED:
        try:
            product_matcher = ProductMatcher(config.NEX_DATA_PATH)
            logger.info(f"✅ ProductMatcher initialized: {config.NEX_DATA_PATH}")
        except Exception as e:
            logger.error(f"❌ Failed to initialize ProductMatcher: {e}")
            product_matcher = None
    else:
        logger.info("⚠️  NEX Genesis enrichment disabled")'''

    content = content.replace(startup_old, startup_new)

    # 4. Add enrichment function before /invoice endpoint
    enrichment_function = '''

async def enrich_invoice_items(invoice_id: int):
    """
    Automatic enrichment of invoice items with NEX Genesis data

    Args:
        invoice_id: ID of invoice to enrich
    """
    if not product_matcher:
        logger.warning(f"ProductMatcher not available for invoice {invoice_id}")
        return

    try:
        pg_client = PostgresStagingClient(config.POSTGRES)
        items = pg_client.get_pending_enrichment_items(invoice_id, limit=100)

        logger.info(f"🔍 Enriching {len(items)} items for invoice {invoice_id}")

        matched_count = 0
        no_match_count = 0

        for item in items:
            try:
                # Prepare item data for matching
                item_data = {
                    'name': item.get('edited_name') or item.get('original_name'),
                    'ean': item.get('edited_ean') or item.get('original_ean')
                }

                # Match with NEX Genesis
                result = product_matcher.match_item(item_data, min_confidence=0.6)

                if result.is_match:
                    # Save match to database
                    pg_client.update_nex_enrichment(
                        item_id=item['id'],
                        gscat_record=result.product,
                        matched_by=result.method
                    )
                    matched_count += 1
                    logger.debug(f"  ✅ Item {item['id']}: {result.product.gs_name} (confidence: {result.confidence:.2f})")
                else:
                    # Mark as no match
                    pg_client.mark_no_match(
                        item_id=item['id'],
                        reason=f"No match found (min confidence: 0.6)"
                    )
                    no_match_count += 1
                    logger.debug(f"  ⚠️  Item {item['id']}: No match")

            except Exception as e:
                logger.error(f"  ❌ Error enriching item {item['id']}: {e}")
                continue

        # Log statistics
        stats = pg_client.get_enrichment_stats(invoice_id)
        logger.info(f"✅ Enrichment complete: {matched_count} matched, {no_match_count} no match")
        logger.info(f"📊 Stats - Total: {stats['total']}, Matched: {stats['matched']}, Pending: {stats['pending']}")

    except Exception as e:
        logger.error(f"❌ Failed to enrich invoice {invoice_id}: {e}")


'''

    # Find the /invoice endpoint and add enrichment call
    invoice_endpoint_marker = '    return invoice_data'

    # Check if enrichment already added
    if 'await enrich_invoice_items(invoice_id)' in content:
        print("⚠️  Enrichment already added to /invoice endpoint")
    else:
        # Add enrichment function before endpoint
        endpoint_start = '@app.post("/invoice"'
        content = content.replace(endpoint_start, enrichment_function + endpoint_start)

        # Add enrichment call before return in /invoice endpoint
        new_return_section = '''    
    # Automatic enrichment with NEX Genesis
    if product_matcher and invoice_id:
        logger.info(f"🚀 Starting enrichment for invoice {invoice_id}")
        await enrich_invoice_items(invoice_id)

    return invoice_data'''

        content = content.replace('    return invoice_data', new_return_section)

    # Write modified content
    print(f"💾 Writing modified file...")
    main_py.write_text(content, encoding='utf-8')

    print("✅ SUCCESS: main.py modified with ProductMatcher integration")
    print("\nChanges:")
    print("  1. Added ProductMatcher import")
    print("  2. Added global product_matcher variable")
    print("  3. Modified startup_event to initialize ProductMatcher")
    print("  4. Added enrich_invoice_items() function")
    print("  5. Added enrichment call to /invoice endpoint")

    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)