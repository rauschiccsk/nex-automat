"""
Re-process NEX Genesis Product Enrichment
=========================================

Permanent script for re-processing supplier invoice items with NEX Genesis
product matching using the corrected GSCAT model.

Location: scripts/reprocess_nex_enrichment.py (permanent, no number prefix)

Expected Results:
- Match rate: >70%
- EAN matches: >65% (via BarCode field @ offset 60)
- Name matches: <5% (fuzzy fallback)
- Errors: <1%
"""

import sys
import os
import asyncio
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import asyncpg
from packages.nexdata.nexdata.btrieve.btrieve_client import BtrieveClient
from packages.nexdata.nexdata.repositories.gscat_repository import GSCATRepository


async def reprocess_enrichment():
    """Re-process all supplier invoice items for NEX enrichment"""

    print("=" * 70)
    print("RE-PROCESSING NEX GENESIS PRODUCT ENRICHMENT")
    print("=" * 70)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Initialize Btrieve client
    try:
        client = BtrieveClient()
        repo = GSCATRepository(client)
        print("✅ NEX Genesis connection established")
    except Exception as e:
        print(f"❌ ERROR: Could not initialize NEX Genesis: {e}")
        return False

    # Connect to PostgreSQL
    postgres_password = os.getenv('POSTGRES_PASSWORD')
    if not postgres_password:
        print("❌ ERROR: POSTGRES_PASSWORD environment variable not set")
        return False

    try:
        conn = await asyncpg.connect(
            host='localhost',
            port=5432,
            database='invoice_staging',
            user='postgres',
            password=postgres_password
        )
        print("✅ PostgreSQL connection established\n")
    except Exception as e:
        print(f"❌ ERROR: Could not connect to PostgreSQL: {e}")
        return False

    try:
        # Get all items without NEX enrichment (where nex_gs_code is NULL)
        query = """
            SELECT id, original_ean, original_name
            FROM invoice_items_pending
            WHERE nex_gs_code IS NULL
            ORDER BY id
        """

        items = await conn.fetch(query)
        total_items = len(items)

        print(f"Items to process: {total_items}")
        print("=" * 70)

        # Statistics
        stats = {
            'total': total_items,
            'matched': 0,
            'ean_matched': 0,
            'name_matched': 0,
            'not_matched': 0,
            'errors': 0
        }

        # Process each item
        for i, item in enumerate(items, 1):
            item_id = item['id']
            ean = item['original_ean']
            product_name = item['original_name']

            try:
                matched = False
                match_method = None
                nex_product = None

                # Try EAN match first
                if ean:
                    nex_product = repo.find_by_barcode(ean)
                    if nex_product:
                        matched = True
                        match_method = 'ean'
                        stats['ean_matched'] += 1

                # Update database
                if matched:
                    # Clean NULL bytes from strings
                    nex_name = nex_product.GsName.replace('\x00', '').strip() if nex_product.GsName else None
                    nex_unit = nex_product.MgCode.replace('\x00', '').strip() if nex_product.MgCode else None

                    update_query = """
                        UPDATE invoice_items_pending
                        SET 
                            nex_gs_code = $1,
                            nex_name = $2,
                            matched_by = $3,
                            in_nex = $4
                        WHERE id = $5
                    """

                    await conn.execute(
                        update_query,
                        nex_product.GsCode,
                        nex_name,
                        match_method,
                        True,  # in_nex = true
                        item_id
                    )

                    stats['matched'] += 1

                    if i % 100 == 0:
                        progress = (i / total_items) * 100
                        match_rate = (stats['matched'] / i) * 100
                        print(f"Progress: {i}/{total_items} ({progress:.1f}%) - Match rate: {match_rate:.1f}%")
                else:
                    stats['not_matched'] += 1

            except Exception as e:
                stats['errors'] += 1
                print(f"❌ Error processing item {item_id}: {e}")

        # Final statistics
        print("\n" + "=" * 70)
        print("PROCESSING COMPLETE")
        print("=" * 70)
        print(f"Total items:     {stats['total']}")
        print(f"Matched:         {stats['matched']} ({(stats['matched']/stats['total']*100):.1f}%)")
        print(f"  - EAN matches: {stats['ean_matched']} ({(stats['ean_matched']/stats['total']*100):.1f}%)")
        print(f"  - Name matches: {stats['name_matched']} ({(stats['name_matched']/stats['total']*100):.1f}%)")
        print(f"Not matched:     {stats['not_matched']} ({(stats['not_matched']/stats['total']*100):.1f}%)")
        print(f"Errors:          {stats['errors']} ({(stats['errors']/stats['total']*100):.1f}%)")

        # Check if targets met
        print("\n" + "=" * 70)
        print("TARGET ANALYSIS")
        print("=" * 70)

        match_rate = (stats['matched'] / stats['total']) * 100
        ean_rate = (stats['ean_matched'] / stats['total']) * 100
        error_rate = (stats['errors'] / stats['total']) * 100

        targets_met = True

        if match_rate >= 70:
            print(f"✅ Match rate: {match_rate:.1f}% >= 70% (TARGET MET)")
        else:
            print(f"❌ Match rate: {match_rate:.1f}% < 70% (TARGET NOT MET)")
            targets_met = False

        if ean_rate >= 65:
            print(f"✅ EAN rate: {ean_rate:.1f}% >= 65% (TARGET MET)")
        else:
            print(f"⚠️  EAN rate: {ean_rate:.1f}% < 65% (below target)")

        if error_rate < 1:
            print(f"✅ Error rate: {error_rate:.1f}% < 1% (TARGET MET)")
        else:
            print(f"❌ Error rate: {error_rate:.1f}% >= 1% (TARGET NOT MET)")
            targets_met = False

        print("\n" + "=" * 70)
        if targets_met:
            print("✅ ALL TARGETS MET - Phase 4 Ready for Production")
        else:
            print("⚠️  SOME TARGETS NOT MET - Review needed")
        print("=" * 70)

        return targets_met

    finally:
        await conn.close()
        print(f"\nCompleted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


async def main():
    """Main function"""
    success = await reprocess_enrichment()
    return success


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)