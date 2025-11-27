"""
Simple test - GSCAT Repository
Test reading product catalog from C:/NEX/GSCAT.BTR
"""

from nexdata import BtrieveClient, GSCATRepository


def test_gscat():
    print("=" * 60)
    print("TEST: GSCAT Repository (Product Catalog)")
    print("=" * 60)

    try:
        # Initialize Btrieve client
        print("\n📡 Connecting to Btrieve...")
        client = BtrieveClient(config_or_path={})
        print("✅ Btrieve client initialized")

        # Create GSCAT repository
        print("\n📦 Creating GSCAT repository...")
        gscat_repo = GSCATRepository(client)
        print(f"✅ Repository created: {gscat_repo.table_name}")

        # Read first 10 products
        print("\n📋 Reading first 10 products...")

        # Open table manually to see status
        if not gscat_repo.open():
            print("❌ Failed to open GSCAT table")
            return False

        print("✅ Table opened successfully")

        # Get first product
        print("\n🔍 Reading first product...")
        first_product = gscat_repo.get_first()

        if not first_product:
            print("⚠️  No products found")
            gscat_repo.close()
            return False

        print(f"✅ First product found: {first_product.gs_name}")

        # Get next 9 products
        products = [first_product]
        for i in range(9):
            product = gscat_repo.get_next()
            if product:
                products.append(product)
            else:
                break

        print(f"✅ Found {len(products)} products\n")

        # Display products
        print("-" * 60)
        print(f"{'Code':<8} {'Name':<40} {'Price':>10} {'Unit':<6}")
        print("-" * 60)

        for product in products:
            code = str(product.gs_code)
            name = product.gs_name[:40]
            price = f"{product.price_sell:.2f}"
            unit = product.unit

            print(f"{code:<8} {name:<40} {price:>10} {unit:<6}")

        print("-" * 60)

        # Close table
        gscat_repo.close()
        print("\n✅ Table closed")

        return True

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    print("\n" + "=" * 60)
    print("NEX GENESIS - GSCAT READ TEST".center(60))
    print("=" * 60)

    success = test_gscat()

    print("\n" + "=" * 60)
    if success:
        print("✅ TEST PASSED")
        print("\n📝 Next: Try TSH/TSI test again")
        print("   python scripts/test_tsh_tsi_read.py")
    else:
        print("❌ TEST FAILED")
    print("=" * 60)


if __name__ == "__main__":
    main()