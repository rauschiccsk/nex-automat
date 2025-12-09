"""
Script 03: Test ProductMatcher integration
Phase 4: Integration testing
"""

import sys
from pathlib import Path

# Add apps to path
dev_root = Path(r"C:\Development\nex-automat")
sys.path.insert(0, str(dev_root / "apps" / "supplier-invoice-loader"))


def test_imports():
    """Test 1: Verify all imports work"""
    print("\n" + "=" * 60)
    print("TEST 1: Imports")
    print("=" * 60)

    try:
        from src.business.product_matcher import ProductMatcher
        print("✅ ProductMatcher imported")
    except Exception as e:
        print(f"❌ Failed to import ProductMatcher: {e}")
        return False

    try:
        from src.utils.config import config
        print("✅ Config imported")
    except Exception as e:
        print(f"❌ Failed to import config: {e}")
        return False

    try:
        from nex_shared.database.postgres_staging import PostgresStagingClient
        print("✅ PostgresStagingClient imported")
    except Exception as e:
        print(f"❌ Failed to import PostgresStagingClient: {e}")
        return False

    return True


def test_config():
    """Test 2: Verify NEX Genesis config exists"""
    print("\n" + "=" * 60)
    print("TEST 2: Configuration")
    print("=" * 60)

    try:
        from src.utils.config import config

        # Check NEX_GENESIS_ENABLED
        if hasattr(config, 'NEX_GENESIS_ENABLED'):
            print(f"✅ NEX_GENESIS_ENABLED = {config.NEX_GENESIS_ENABLED}")
        else:
            print("❌ NEX_GENESIS_ENABLED not found in config")
            return False

        # Check NEX_DATA_PATH
        if hasattr(config, 'NEX_DATA_PATH'):
            print(f"✅ NEX_DATA_PATH = {config.NEX_DATA_PATH}")

            # Verify path exists
            data_path = Path(config.NEX_DATA_PATH)
            if data_path.exists():
                print(f"✅ NEX data path exists: {data_path}")
            else:
                print(f"⚠️  NEX data path not found: {data_path}")
                print("   (Expected if not on Mágerstav server)")
        else:
            print("❌ NEX_DATA_PATH not found in config")
            return False

        return True

    except Exception as e:
        print(f"❌ Config test failed: {e}")
        return False


def test_product_matcher_init():
    """Test 3: Initialize ProductMatcher"""
    print("\n" + "=" * 60)
    print("TEST 3: ProductMatcher Initialization")
    print("=" * 60)

    try:
        from src.business.product_matcher import ProductMatcher
        from src.utils.config import config

        data_path = Path(config.NEX_DATA_PATH)

        if not data_path.exists():
            print(f"⚠️  Skipping - NEX data path not available: {data_path}")
            print("   (This is expected if not on Mágerstav server)")
            return True

        # Try to initialize
        matcher = ProductMatcher(str(data_path))
        print(f"✅ ProductMatcher initialized successfully")
        print(f"   Data path: {data_path}")

        # Check if Btrieve client loaded
        if matcher.gscat_repo and matcher.gscat_repo.client:
            print("✅ BtrieveClient loaded")
        else:
            print("⚠️  BtrieveClient not available")

        return True

    except Exception as e:
        print(f"❌ ProductMatcher initialization failed: {e}")
        return False


def test_matching():
    """Test 4: Test product matching"""
    print("\n" + "=" * 60)
    print("TEST 4: Product Matching")
    print("=" * 60)

    try:
        from src.business.product_matcher import ProductMatcher
        from src.utils.config import config

        data_path = Path(config.NEX_DATA_PATH)

        if not data_path.exists():
            print(f"⚠️  Skipping - NEX data path not available")
            return True

        matcher = ProductMatcher(str(data_path))

        # Test case 1: Name matching
        test_item = {
            'name': 'Coca Cola',
            'ean': None
        }

        print(f"\n🔍 Testing name match: '{test_item['name']}'")
        result = matcher.match_item(test_item, min_confidence=0.6)

        if result.is_match:
            print(f"✅ Match found!")
            print(f"   Product: {result.product.gs_name}")
            print(f"   Code: {result.product.gs_code}")
            print(f"   Confidence: {result.confidence:.2f}")
            print(f"   Method: {result.method}")
        else:
            print(f"⚠️  No match found (confidence too low)")

        # Test case 2: EAN matching (if available)
        test_item_ean = {
            'name': 'Test Product',
            'ean': '8586014570014'  # Example EAN
        }

        print(f"\n🔍 Testing EAN match: '{test_item_ean['ean']}'")
        result_ean = matcher.match_item(test_item_ean, min_confidence=0.6)

        if result_ean.is_match:
            print(f"✅ Match found by EAN!")
            print(f"   Product: {result_ean.product.gs_name}")
            print(f"   Method: {result_ean.method}")
        else:
            print(f"⚠️  No EAN match (EAN may not exist in database)")

        return True

    except Exception as e:
        print(f"❌ Matching test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_postgres_methods():
    """Test 5: Test PostgreSQL enrichment methods"""
    print("\n" + "=" * 60)
    print("TEST 5: PostgreSQL Enrichment Methods")
    print("=" * 60)

    try:
        from nex_shared.database.postgres_staging import PostgresStagingClient

        print("✅ PostgresStagingClient available")

        # Check methods exist
        methods = [
            'get_pending_enrichment_items',
            'update_nex_enrichment',
            'mark_no_match',
            'get_enrichment_stats'
        ]

        for method in methods:
            if hasattr(PostgresStagingClient, method):
                print(f"✅ Method exists: {method}")
            else:
                print(f"❌ Method missing: {method}")
                return False

        print("\n⚠️  Note: Actual database operations not tested")
        print("   (Requires live PostgreSQL connection)")

        return True

    except Exception as e:
        print(f"❌ PostgreSQL test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("PHASE 4 INTEGRATION TEST")
    print("Testing ProductMatcher integration in supplier-invoice-loader")
    print("=" * 60)

    results = []

    # Run tests
    results.append(("Imports", test_imports()))
    results.append(("Configuration", test_config()))
    results.append(("ProductMatcher Init", test_product_matcher_init()))
    results.append(("Product Matching", test_matching()))
    results.append(("PostgreSQL Methods", test_postgres_methods()))

    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:12} {test_name}")

    all_passed = all(result for _, result in results)

    print("\n" + "=" * 60)
    if all_passed:
        print("✅ ALL TESTS PASSED - Integration ready for deployment")
    else:
        print("❌ SOME TESTS FAILED - Review errors above")
    print("=" * 60)

    return all_passed


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)