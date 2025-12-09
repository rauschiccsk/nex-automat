"""
Test EAN Lookup in NEX Genesis GSCAT
====================================

Permanent test script for verifying EAN barcode matching functionality.
Tests known EAN codes that exist in NEX Genesis database.

Location: scripts/test_ean_lookup.py (permanent, no number prefix)
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from packages.nexdata.nexdata.repositories.gscat_repository import GSCATRepository
from packages.nexdata.nexdata.btrieve.btrieve_client import BtrieveClient


# Known EAN codes that exist in NEX Genesis (manually verified)
VERIFIED_EANS = [
    "8715743018251",
    "5203473211316",
    "3838847028515",
]

# Additional test EAN codes (may or may not exist)
TEST_EANS = [
    "8594004592804",
    "8594004592811",
    "8594004592828",
    "8594004592835",
    "8594004592842",
    "8594004592859",
    "8594004592866",
    "8594004592873",
    "8594004592880",
    "8594004592897",
    "8594004592903",
    "8594004592910",
    "8594004592927",
    "8594004592934",
    "8594004592941",
    "8594004592958",
    "8594004592965",
]


def test_ean_lookup():
    """Test EAN lookup functionality"""
    print("=" * 70)
    print("TEST EAN LOOKUP - NEX GENESIS GSCAT")
    print("=" * 70)

    # Initialize Btrieve client with default config
    try:
        client = BtrieveClient()  # Uses default config/database.yaml
        print("✅ BtrieveClient initialized (default config)")
    except Exception as e:
        print(f"❌ ERROR: Could not initialize BtrieveClient: {e}")
        print("   Make sure config/database.yaml exists")
        return False

    # Initialize repository
    try:
        repo = GSCATRepository(client)
        print("✅ GSCATRepository initialized")
    except Exception as e:
        print(f"❌ ERROR: Could not initialize repository: {e}")
        return False

    # Test verified EAN codes
    print("\n" + "=" * 70)
    print("TESTING VERIFIED EAN CODES (should be found)")
    print("=" * 70)

    verified_found = 0
    for ean in VERIFIED_EANS:
        try:
            product = repo.find_by_barcode(ean)
            if product:
                print(f"✅ {ean}: FOUND")
                print(f"   Code: {product.GsCode}")
                print(f"   Name: {product.GsName}")
                print(f"   Unit: {product.MgCode}")
                verified_found += 1
            else:
                print(f"❌ {ean}: NOT FOUND (expected to be found!)")
        except Exception as e:
            print(f"❌ {ean}: ERROR - {e}")

    print(f"\nVerified EANs found: {verified_found}/{len(VERIFIED_EANS)}")

    # Test additional EAN codes
    print("\n" + "=" * 70)
    print("TESTING ADDITIONAL EAN CODES")
    print("=" * 70)

    additional_found = 0
    for ean in TEST_EANS:
        try:
            product = repo.find_by_barcode(ean)
            if product:
                print(f"✅ {ean}: FOUND")
                print(f"   Code: {product.GsCode}")
                print(f"   Name: {product.GsName}")
                additional_found += 1
            else:
                print(f"⚪ {ean}: not found")
        except Exception as e:
            print(f"❌ {ean}: ERROR - {e}")

    print(f"\nAdditional EANs found: {additional_found}/{len(TEST_EANS)}")

    # Summary
    total_tested = len(VERIFIED_EANS) + len(TEST_EANS)
    total_found = verified_found + additional_found
    success_rate = (total_found / total_tested * 100) if total_tested > 0 else 0

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Total tested: {total_tested}")
    print(f"Total found: {total_found}")
    print(f"Success rate: {success_rate:.1f}%")
    print(f"Verified found: {verified_found}/{len(VERIFIED_EANS)}")
    print(f"Additional found: {additional_found}/{len(TEST_EANS)}")

    # Expected results
    print("\n" + "=" * 70)
    print("EXPECTED VS ACTUAL")
    print("=" * 70)

    # All verified EANs should be found
    if verified_found == len(VERIFIED_EANS):
        print("✅ All verified EANs found (expected)")
    else:
        print(f"⚠️  Only {verified_found}/{len(VERIFIED_EANS)} verified EANs found")
        print("   This indicates a problem with BarCode field access")

    # Overall success rate
    if success_rate >= 15:
        print(f"✅ Success rate {success_rate:.1f}% >= 15% (expected)")
    else:
        print(f"⚠️  Success rate {success_rate:.1f}% < 15% (expected >=15%)")

    # Return success if all verified EANs found
    return verified_found == len(VERIFIED_EANS)


def main():
    """Main test function"""
    print("\n")
    success = test_ean_lookup()

    if success:
        print("\n" + "=" * 70)
        print("✅ TEST PASSED")
        print("=" * 70)
        print("\nNext Step:")
        print("Run: python scripts/reprocess_nex_enrichment.py")
        print("Expected: >70% match rate")
    else:
        print("\n" + "=" * 70)
        print("❌ TEST FAILED")
        print("=" * 70)
        print("\nPossible issues:")
        print("1. BarCode field not properly loaded from Btrieve")
        print("2. Field name mismatch in GSCATRecord model")
        print("3. Encoding issues (should be cp852)")

    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)