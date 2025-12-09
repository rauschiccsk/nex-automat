"""
Test EAN lookup v NEX Genesis databáze
Otestuje vzorku EAN kódov z faktúr
"""

import sys
from pathlib import Path

# Pridať paths pre import
root_path = Path(__file__).parent.parent
loader_path = root_path / "apps" / "supplier-invoice-loader"
packages_path = root_path / "packages"

sys.path.insert(0, str(loader_path))
sys.path.insert(0, str(packages_path))

from src.utils.config import config
from nex_shared.database.postgres_staging import PostgresStagingClient
from nexdata.btrieve.btrieve_client import BtrieveClient
from nexdata.repositories.gscat_repository import GSCATRepository
from nexdata.repositories.barcode_repository import BARCODERepository


def test_ean_codes():
    """Test EAN codes from invoices against NEX Genesis"""

    print("=" * 70)
    print("EAN Lookup Test - NEX Genesis")
    print("=" * 70)

    # PostgreSQL config
    pg_config = {
        'host': config.POSTGRES_HOST,
        'port': config.POSTGRES_PORT,
        'database': config.POSTGRES_DATABASE,
        'user': config.POSTGRES_USER,
        'password': config.POSTGRES_PASSWORD
    }

    # NEX data path
    nex_data_path = getattr(config, 'NEX_DATA_PATH', r"C:\NEX\YEARACT\STORES")

    # Inicializovať Btrieve
    print(f"\n1. Inicializácia Btrieve...")
    print(f"   Path: {nex_data_path}")

    btrieve_config = {'database_path': nex_data_path}
    btrieve = BtrieveClient(config_or_path=btrieve_config)

    gscat_repo = GSCATRepository(btrieve)
    barcode_repo = BARCODERepository(btrieve)

    print(f"   ✓ Btrieve pripravený")

    # Načítať vzorku EAN kódov z PostgreSQL
    print(f"\n2. Načítanie EAN kódov z faktúr...")

    with PostgresStagingClient(pg_config) as client:
        rows = client.get_pending_enrichment_items(limit=20)

        print(f"   ✓ Našlo sa {len(rows)} items")

        # Test každý EAN
        print(f"\n3. Testovanie EAN kódov v NEX Genesis...")
        print("-" * 70)

        stats = {
            'total': 0,
            'has_ean': 0,
            'found_gscat': 0,
            'found_barcode': 0,
            'not_found': 0
        }

        for item in rows:
            ean = item.get('original_ean')
            name = item.get('original_name', '')

            if not ean or ean.upper() == 'N/A':
                continue

            stats['total'] += 1
            stats['has_ean'] += 1

            print(f"\nEAN: {ean}")
            print(f"Name: {name}")

            # Test v GSCAT (pomocou find_by_barcode)
            try:
                gscat_result = gscat_repo.find_by_barcode(ean)
                if gscat_result:
                    stats['found_gscat'] += 1
                    print(f"  ✓ FOUND in GSCAT")
                    print(f"    Code: {gscat_result.gs_code}")
                    print(f"    Name: {gscat_result.gs_name.replace(chr(0), '').strip()}")
                    continue
            except Exception as e:
                print(f"  ✗ GSCAT search failed: {e}")

            # Test v BARCODE
            try:
                barcode_result = barcode_repo.find_by_barcode(ean)
                if barcode_result:
                    stats['found_barcode'] += 1
                    print(f"  ✓ FOUND in BARCODE")
                    print(f"    GS Code: {barcode_result.gs_code}")

                    # Načítať GSCAT record
                    gscat = gscat_repo.find_by_code(barcode_result.gs_code)
                    if gscat:
                        print(f"    Name: {gscat.gs_name.replace(chr(0), '').strip()}")
                    continue
            except Exception as e:
                print(f"  ✗ BARCODE error: {e}")

            # Not found
            stats['not_found'] += 1
            print(f"  ✗ NOT FOUND in NEX Genesis")

        # Štatistika
        print("\n" + "=" * 70)
        print("VÝSLEDKY TESTOVANIA")
        print("=" * 70)
        print(f"Celkom items:        {len(rows)}")
        print(f"S EAN kódom:         {stats['has_ean']}")
        print(f"Found in GSCAT:      {stats['found_gscat']}")
        print(f"Found in BARCODE:    {stats['found_barcode']}")
        print(f"NOT FOUND:           {stats['not_found']}")
        print()

        if stats['has_ean'] > 0:
            found_total = stats['found_gscat'] + stats['found_barcode']
            success_rate = found_total / stats['has_ean'] * 100
            print(f"SUCCESS RATE:        {success_rate:.1f}%")

            if success_rate < 50:
                print(f"\n⚠ PROBLÉM: Väčšina EAN kódov nie je v NEX Genesis!")
                print(f"  Možné príčiny:")
                print(f"  - Faktúry od dodávateľov mimo NEX sortimentu")
                print(f"  - NEX Genesis nemá vyplnené EAN kódy")
                print(f"  - Iný formát EAN kódov (EAN13 vs EAN8)")

        print("=" * 70)


if __name__ == "__main__":
    test_ean_codes()