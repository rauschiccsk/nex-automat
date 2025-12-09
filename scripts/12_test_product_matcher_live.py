"""
Session Script 12: Test ProductMatcher with Real Btrieve Data
Tests LIVE queries against real NEX Genesis database
"""
import sys
import traceback
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'apps' / 'supplier-invoice-loader' / 'src'))

from business.product_matcher import ProductMatcher

def main():
    print("=" * 60)
    print("Testing ProductMatcher with LIVE Btrieve Data")
    print("=" * 60)

    # Initialize matcher
    nex_data_path = r"C:\NEX\YEARACT\STORES"

    print(f"\nInitializing ProductMatcher...")
    print(f"NEX Data Path: {nex_data_path}")

    try:
        matcher = ProductMatcher(nex_data_path)
        print("✅ ProductMatcher initialized")
    except Exception as e:
        print(f"❌ Failed to initialize: {e}")
        print("\nFull traceback:")
        traceback.print_exc()
        return 1

    # Test 1: EAN matching
    print("\n" + "=" * 60)
    print("TEST 1: EAN Matching")
    print("=" * 60)

    test_ean = "8586017850028"  # Example EAN - replace with real one

    print(f"\nSearching for EAN: {test_ean}")

    item_data = {
        'original_name': 'Test Product',
        'original_ean': test_ean
    }

    try:
        result = matcher.match_item(item_data)

        if result.is_match:
            print(f"✅ Match found!")
            print(f"   Product: {result.product.gs_name}")
            print(f"   GS Code: {result.product.gs_code}")
            print(f"   Category: {result.product.mglst_code}")
            print(f"   Confidence: {result.confidence:.2%}")
            print(f"   Method: {result.method}")
        else:
            print(f"⚠️  No match found")
            print(f"   Confidence: {result.confidence}")
    except Exception as e:
        print(f"❌ Error during matching: {e}")
        traceback.print_exc()
        return 1

    # Test 2: Name matching
    print("\n" + "=" * 60)
    print("TEST 2: Name Matching")
    print("=" * 60)

    test_name = "Coca Cola"  # Example name - replace with real one

    print(f"\nSearching for name: {test_name}")

    item_data = {
        'original_name': test_name,
        'original_ean': ''
    }

    try:
        result = matcher.match_item(item_data, min_confidence=0.6)

        if result.is_match:
            print(f"✅ Match found!")
            print(f"   Product: {result.product.gs_name}")
            print(f"   GS Code: {result.product.gs_code}")
            print(f"   Confidence: {result.confidence:.2%}")
            print(f"   Method: {result.method}")

            if result.alternatives:
                print(f"\n   Alternatives ({len(result.alternatives)}):")
                for alt_product, alt_score in result.alternatives[:3]:
                    print(f"   - {alt_product.gs_name} ({alt_score:.2%})")
        else:
            print(f"⚠️  No match found")
            print(f"   Confidence: {result.confidence}")
    except Exception as e:
        print(f"❌ Error during matching: {e}")
        traceback.print_exc()
        return 1

    print("\n" + "=" * 60)
    print("✅ All tests completed!")
    print("=" * 60)

    return 0

if __name__ == '__main__':
    sys.exit(main())