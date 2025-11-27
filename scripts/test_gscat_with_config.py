"""
Test GSCAT with proper config
"""

from nexdata import BtrieveClient, GSCATRepository

# Config from nex-genesis-server
CONFIG = {
    'nex_genesis': {
        'tables': {
            'gscat': r'C:\NEX\YEARACT\STORES\GSCAT.BTR',
            'barcode': r'C:\NEX\YEARACT\STORES\BARCODE.BTR',
            'mglst': r'C:\NEX\YEARACT\STORES\MGLST.BTR',
            'pab': r'C:\NEX\YEARACT\DIALS\PAB00000.BTR',
        }
    }
}


def test_gscat():
    print("=" * 60)
    print("TEST: GSCAT with Config")
    print("=" * 60)

    try:
        # Initialize with config
        print("\n📡 Connecting to Btrieve with config...")
        client = BtrieveClient(config_or_path=CONFIG)
        print("✅ Btrieve client initialized")

        # Create repository
        print("\n📦 Creating GSCAT repository...")

        # Temporarily fix repository to return just table name
        class GSCATRepositoryFixed(GSCATRepository):
            @property
            def table_name(self) -> str:
                return 'gscat'  # Just the name, not path!

        gscat_repo = GSCATRepositoryFixed(client)
        print(f"✅ Repository created: {gscat_repo.table_name}")

        # Try to open
        print("\n📋 Opening GSCAT table...")
        if not gscat_repo.open():
            print("❌ Failed to open")
            return False

        print("✅ Table opened!")

        # Read first product
        print("\n🔍 Reading first product...")
        product = gscat_repo.get_first()

        if not product:
            print("⚠️  No products found")
            gscat_repo.close()
            return False

        print(f"✅ Product: {product.gs_name}")
        print(f"   Code: {product.gs_code}")
        print(f"   Price: {product.price_sell} {product.unit}")

        gscat_repo.close()
        return True

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_gscat()

    print("\n" + "=" * 60)
    if success:
        print("🎉 SUCCESS!")
        print("\nNext: Fix all repositories to use table names only")
    else:
        print("❌ FAILED")
    print("=" * 60)