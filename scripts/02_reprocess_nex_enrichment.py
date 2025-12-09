"""
Re-process NEX enrichment pre existujúce faktúry v2.3
Spustí ProductMatcher na všetky záznamy s in_nex = FALSE alebo NULL
"""

import sys
from pathlib import Path

# Pridať paths pre import (spúšťané zo scripts/)
root_path = Path(__file__).parent.parent
loader_path = root_path / "apps" / "supplier-invoice-loader"
packages_path = root_path / "packages"

# Pridať loader_path priamo, aby sme mohli importovať z src/
sys.path.insert(0, str(loader_path))
sys.path.insert(0, str(packages_path))

# Import z src/ (supplier-invoice-loader je teraz v sys.path)
from src.business.product_matcher import ProductMatcher
from src.utils.config import config
from nex_shared.database.postgres_staging import PostgresStagingClient


def reprocess_items(limit: int = None):
    """Re-process items without NEX enrichment"""

    print("=" * 70)
    print("NEX Enrichment Re-processor")
    print("=" * 70)

    # Inicializovať ProductMatcher
    print("\n1. Inicializácia ProductMatcher...")
    try:
        # Načítať NEX data path z config
        nex_data_path = getattr(config, 'NEX_DATA_PATH', r"C:\NEX\YEARACT\STORES")
        print(f"   NEX data path: {nex_data_path}")

        matcher = ProductMatcher(nex_data_path=nex_data_path)
        print(f"   ✓ ProductMatcher pripravený")
    except Exception as e:
        print(f"   ✗ CHYBA pri inicializácii ProductMatcher: {e}")
        return

    # PostgreSQL config
    pg_config = {
        'host': config.POSTGRES_HOST,
        'port': config.POSTGRES_PORT,
        'database': config.POSTGRES_DATABASE,
        'user': config.POSTGRES_USER,
        'password': config.POSTGRES_PASSWORD
    }

    # Pripojiť PostgreSQL
    print("\n2. Pripojenie na PostgreSQL...")
    try:
        with PostgresStagingClient(pg_config) as client:
            print(f"   ✓ PostgreSQL pripravený")

            # Načítať items na re-process pomocou get_pending_enrichment_items
            print("\n3. Načítanie items na re-process...")

            # Metóda vráti items s in_nex IS NULL alebo FALSE
            rows = client.get_pending_enrichment_items(limit=limit)
            total = len(rows)

            if total == 0:
                print("   ℹ Žiadne items na re-process")
                return

            print(f"   ✓ Našlo sa {total} items")

            # Re-process každý item
            print(f"\n4. Re-processing {total} items...")
            print("-" * 70)

            stats = {
                "total": total,
                "matched_ean": 0,
                "matched_name": 0,
                "not_matched": 0,
                "errors": 0
            }

            for idx, item in enumerate(rows, 1):
                item_id = item['id']
                original_name = item['original_name']
                original_ean = item.get('original_ean')

                print(f"\n[{idx}/{total}] Item ID: {item_id}")
                print(f"  Name: {original_name}")
                print(f"  EAN:  {original_ean or 'N/A'}")

                try:
                    # Pripraviť item_data dict pre ProductMatcher
                    item_data = {
                        'original_name': original_name,
                        'original_ean': original_ean
                    }

                    # Matchovať cez ProductMatcher
                    result = matcher.match_item(item_data)

                    # Skontrolovať či sa našiel match
                    if result.is_match and result.product:
                        # Sanitizovať gs_name - odstrániť NULL bytes
                        gs_name = result.product.gs_name
                        if gs_name:
                            gs_name = gs_name.replace('\x00', '').strip()

                        # Matched - manuálny UPDATE s ošetrenými dátami
                        cursor = client._conn.cursor()
                        cursor.execute("""
                            UPDATE invoice_items_pending
                            SET nex_gs_code = %s,
                                nex_name = %s,
                                nex_category = %s,
                                in_nex = TRUE,
                                matched_by = %s,
                                validation_status = 'valid',
                                validation_message = 'Matched with NEX Genesis'
                            WHERE id = %s
                        """, (
                            result.product.gs_code,
                            gs_name,
                            result.product.mglst_code,
                            result.method,
                            item_id
                        ))
                        cursor.close()

                        if result.method == "ean":
                            stats["matched_ean"] += 1
                            print(f"  ✓ MATCHED (EAN): {result.product.gs_code} - {gs_name}")
                        else:
                            stats["matched_name"] += 1
                            print(f"  ✓ MATCHED (Name): {result.product.gs_code} - {gs_name}")
                            print(f"    Confidence: {result.confidence:.2f} ({result.confidence_level})")
                    else:
                        # Not matched - manuálny UPDATE namiesto mark_no_match
                        # (mark_no_match používa neplatný validation_status)
                        cursor = client._conn.cursor()
                        cursor.execute("""
                            UPDATE invoice_items_pending
                            SET in_nex = FALSE,
                                matched_by = NULL,
                                validation_status = 'warning',
                                validation_message = 'No matching product found'
                            WHERE id = %s
                        """, (item_id,))
                        cursor.close()

                        stats["not_matched"] += 1
                        print(f"  ✗ NO MATCH")

                except Exception as e:
                    stats["errors"] += 1
                    print(f"  ✗ ERROR: {e}")
                    import traceback
                    traceback.print_exc()

            # Štatistika
            print("\n" + "=" * 70)
            print("VÝSLEDKY RE-PROCESSINGU")
            print("=" * 70)
            print(f"Celkom items:        {stats['total']}")
            print(f"Matched (EAN):       {stats['matched_ean']} ({stats['matched_ean']/stats['total']*100:.1f}%)")
            print(f"Matched (Name):      {stats['matched_name']} ({stats['matched_name']/stats['total']*100:.1f}%)")
            print(f"Not matched:         {stats['not_matched']} ({stats['not_matched']/stats['total']*100:.1f}%)")
            print(f"Errors:              {stats['errors']}")
            print()

            total_matched = stats['matched_ean'] + stats['matched_name']
            match_rate = total_matched / stats['total'] * 100
            print(f"MATCH RATE:          {match_rate:.1f}%")

            if match_rate >= 70:
                print(f"✓ Cieľ splnený (>70%)")
            else:
                print(f"✗ Cieľ nesplnený (<70%)")

            print("=" * 70)

    except Exception as e:
        print(f"   ✗ CHYBA: {e}")
        import traceback
        traceback.print_exc()
        return

    print("\n✓ PostgreSQL odpojený")


def main():
    """Main entry point"""

    # Limit pre testovanie (None = všetky)
    limit = None  # Spustiť na všetky items

    print(f"\nRe-processing limit: {limit if limit else 'ALL'}")
    print("POZOR: Toto prepíše existujúce NEX údaje!\n")

    response = input("Pokračovať? (y/n): ")
    if response.lower() != 'y':
        print("Zrušené")
        return

    reprocess_items(limit=limit)


if __name__ == "__main__":
    main()