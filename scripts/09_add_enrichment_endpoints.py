"""
Session Script 09: Add Enrichment API Endpoints
Adds 3 enrichment endpoints to main.py
"""
from pathlib import Path


def main():
    main_file = Path(r"C:\Development\nex-automat\apps\supplier-invoice-loader\main.py")

    print("=" * 60)
    print("Phase 3: Adding API Endpoints")
    print("=" * 60)

    with open(main_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if already added
    if 'product_matcher' in content:
        print("⚠️  Enrichment endpoints already exist")
        return 1

    # 1. Add import at top
    import_line = "from src.business.product_matcher import ProductMatcher, MatchResult\n"

    # Find the imports section (after other src imports)
    import_pos = content.find('from src.utils import config')
    if import_pos == -1:
        print("❌ Could not find import section")
        return 1

    # Insert after this line
    next_newline = content.find('\n', import_pos)
    content = content[:next_newline + 1] + import_line + content[next_newline + 1:]

    # 2. Add global variable after app initialization
    global_var = """
# Global ProductMatcher instance
product_matcher: Optional[ProductMatcher] = None
"""

    # Find app = FastAPI() and add after it
    app_pos = content.find('app = FastAPI(')
    if app_pos == -1:
        print("❌ Could not find app initialization")
        return 1

    # Find end of that block (next blank line)
    next_blank = content.find('\n\n', app_pos)
    content = content[:next_blank] + global_var + content[next_blank:]

    # 3. Add ProductMatcher initialization to startup event
    startup_code = """
    # Initialize ProductMatcher if NEX Genesis is enabled
    if config.NEX_GENESIS_ENABLED:
        try:
            global product_matcher
            product_matcher = ProductMatcher(config.NEX_DATA_PATH)
            logger.info("[OK] ProductMatcher initialized")
        except Exception as e:
            logger.warning(f"[WARN] ProductMatcher init failed: {e}")
"""

    # Find startup event
    startup_pos = content.find('@app.on_event("startup")')
    if startup_pos == -1:
        print("❌ Could not find startup event")
        return 1

    # Find end of startup function
    # Look for next @app or end of file
    next_decorator = content.find('\n@app.', startup_pos + 1)
    if next_decorator == -1:
        next_decorator = len(content)

    # Insert before the next decorator
    content = content[:next_decorator] + startup_code + '\n' + content[next_decorator:]

    # 4. Add the 3 endpoints at the end
    endpoints_code = '''

# ==============================================================================
# NEX GENESIS ENRICHMENT ENDPOINTS
# ==============================================================================

@app.post("/enrich/invoice/{invoice_id}")
async def enrich_invoice_items(
    invoice_id: int,
    min_confidence: float = 0.6,
    api_key: str = Depends(verify_api_key)
):
    """
    Enrich invoice items with NEX Genesis product data

    Args:
        invoice_id: Invoice ID to enrich
        min_confidence: Minimum confidence threshold for name matching (0.0-1.0)

    Returns:
        Enrichment statistics
    """
    if not product_matcher:
        raise HTTPException(
            status_code=503,
            detail="ProductMatcher not initialized. Check NEX_GENESIS_ENABLED config."
        )

    # Create PostgreSQL client
    pg_config = {
        'host': config.POSTGRES_HOST,
        'port': config.POSTGRES_PORT,
        'database': config.POSTGRES_DATABASE,
        'user': config.POSTGRES_USER,
        'password': config.POSTGRES_PASSWORD
    }

    stats = {
        'invoice_id': invoice_id,
        'total': 0,
        'matched': 0,
        'matched_ean': 0,
        'matched_name': 0,
        'not_found': 0,
        'errors': 0,
        'min_confidence': min_confidence
    }

    try:
        with PostgresStagingClient(pg_config) as pg_client:
            # Get pending items
            items = pg_client.get_pending_enrichment_items(invoice_id=invoice_id)
            stats['total'] = len(items)

            logger.info(f"Enriching {stats['total']} items for invoice {invoice_id}")

            # Process each item
            for item in items:
                try:
                    # Try to match
                    match_result = product_matcher.match_item(item, min_confidence)

                    if match_result.product:
                        # Update with matched product
                        success = pg_client.update_nex_enrichment(
                            item['id'],
                            match_result.product,
                            match_result.method
                        )

                        if success:
                            stats['matched'] += 1
                            if match_result.method == 'ean':
                                stats['matched_ean'] += 1
                            else:
                                stats['matched_name'] += 1

                            logger.debug(
                                f"Matched item {item['id']}: {item.get('original_name')} "
                                f"-> {match_result.product.gs_name} "
                                f"(confidence: {match_result.confidence:.2f}, method: {match_result.method})"
                            )
                    else:
                        # Mark as not found
                        pg_client.mark_no_match(
                            item['id'],
                            f"No match found (min_confidence={min_confidence})"
                        )
                        stats['not_found'] += 1

                        logger.debug(f"No match for item {item['id']}: {item.get('original_name')}")

                except Exception as e:
                    logger.error(f"Error enriching item {item['id']}: {e}")
                    stats['errors'] += 1

            logger.info(
                f"Enrichment complete: {stats['matched']}/{stats['total']} matched "
                f"(EAN: {stats['matched_ean']}, Name: {stats['matched_name']}, "
                f"Not found: {stats['not_found']}, Errors: {stats['errors']})"
            )

    except Exception as e:
        logger.error(f"Enrichment failed: {e}")
        raise HTTPException(status_code=500, detail=f"Enrichment failed: {str(e)}")

    return {
        'success': True,
        'message': f"Enriched {stats['matched']}/{stats['total']} items",
        'statistics': stats
    }


@app.get("/enrich/stats/{invoice_id}")
async def get_enrichment_stats(
    invoice_id: int,
    api_key: str = Depends(verify_api_key)
):
    """
    Get enrichment statistics for an invoice

    Args:
        invoice_id: Invoice ID

    Returns:
        Enrichment statistics
    """
    pg_config = {
        'host': config.POSTGRES_HOST,
        'port': config.POSTGRES_PORT,
        'database': config.POSTGRES_DATABASE,
        'user': config.POSTGRES_USER,
        'password': config.POSTGRES_PASSWORD
    }

    try:
        with PostgresStagingClient(pg_config) as pg_client:
            stats = pg_client.get_enrichment_stats(invoice_id=invoice_id)

            # Add percentage
            if stats['total'] > 0:
                stats['enriched_percent'] = round(stats['enriched'] / stats['total'] * 100, 1)
            else:
                stats['enriched_percent'] = 0.0

            return {
                'success': True,
                'invoice_id': invoice_id,
                'statistics': stats
            }

    except Exception as e:
        logger.error(f"Failed to get stats: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")


@app.get("/pending/items")
async def get_pending_items(
    invoice_id: Optional[int] = None,
    limit: int = 100,
    api_key: str = Depends(verify_api_key)
):
    """
    Get pending enrichment items

    Args:
        invoice_id: Optional invoice ID to filter by
        limit: Maximum number of items to return (1-1000)

    Returns:
        List of pending items
    """
    if limit < 1 or limit > 1000:
        raise HTTPException(status_code=400, detail="Limit must be between 1 and 1000")

    pg_config = {
        'host': config.POSTGRES_HOST,
        'port': config.POSTGRES_PORT,
        'database': config.POSTGRES_DATABASE,
        'user': config.POSTGRES_USER,
        'password': config.POSTGRES_PASSWORD
    }

    try:
        with PostgresStagingClient(pg_config) as pg_client:
            items = pg_client.get_pending_enrichment_items(
                invoice_id=invoice_id,
                limit=limit
            )

            return {
                'success': True,
                'count': len(items),
                'invoice_id': invoice_id,
                'items': items
            }

    except Exception as e:
        logger.error(f"Failed to get pending items: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get pending items: {str(e)}")
'''

    # Append endpoints at the end
    content += endpoints_code

    # Write back
    with open(main_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ Updated {main_file.name}")
    print("\nAdded:")
    print("  - ProductMatcher import")
    print("  - Global product_matcher variable")
    print("  - ProductMatcher initialization in startup")
    print("  - POST /enrich/invoice/{invoice_id}")
    print("  - GET /enrich/stats/{invoice_id}")
    print("  - GET /pending/items")

    print("\n" + "=" * 60)
    print("✅ Phase 3 Step 1 complete!")
    print("=" * 60)

    return 0


if __name__ == '__main__':
    import sys

    sys.exit(main())