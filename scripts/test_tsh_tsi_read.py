"""
Test Read Operations - TSH/TSI from NEX Genesis
Priority 3: Test reading delivery documents from Btrieve
"""

from nexdata import BtrieveClient, TSHRepository, TSIRepository


def print_separator(title: str = ""):
    """Print separator line"""
    if title:
        print(f"\n{'=' * 60}")
        print(f"{title:^60}")
        print('=' * 60)
    else:
        print('-' * 60)


def test_tsh_read():
    """Test reading TSH records (Delivery Headers)"""

    print_separator("TEST: TSH Repository (Delivery Headers)")

    try:
        # Initialize Btrieve client (with empty config - only DLL needed)
        print("\n📡 Connecting to Btrieve...")
        client = BtrieveClient(config_or_path={})
        print("✅ Btrieve client initialized")

        # Create TSH repository
        print("\n📦 Creating TSH repository...")
        tsh_repo = TSHRepository(client, store_id="001")
        print(f"✅ Repository created: {tsh_repo.table_name}")

        # Read recent documents
        print("\n📋 Reading recent TSH documents (limit: 5)...")
        documents = tsh_repo.get_recent_documents(limit=5)

        if not documents:
            print("⚠️  No TSH documents found")
            return None

        print(f"✅ Found {len(documents)} documents\n")

        # Display documents
        print_separator()
        print(f"{'Doc Number':<15} {'Date':<12} {'Partner':<30} {'Total':>12}")
        print_separator()

        for doc in documents:
            doc_date = doc.doc_date.strftime('%Y-%m-%d') if doc.doc_date else 'N/A'
            partner = doc.pab_name[:30] if doc.pab_name else f"PAB#{doc.pab_code}"
            total = f"{doc.amount_total} {doc.currency}"

            print(f"{doc.doc_number:<15} {doc_date:<12} {partner:<30} {total:>12}")

        print_separator()

        # Return first document for TSI test
        return documents[0] if documents else None

    except Exception as e:
        print(f"❌ Error reading TSH: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_tsi_read(doc_number: str):
    """Test reading TSI records (Delivery Items)"""

    print_separator(f"TEST: TSI Repository (Items for {doc_number})")

    try:
        # Initialize Btrieve client (with empty config - only DLL needed)
        print("\n📡 Connecting to Btrieve...")
        client = BtrieveClient(config_or_path={})
        print("✅ Btrieve client initialized")

        # Create TSI repository
        print("\n📦 Creating TSI repository...")
        tsi_repo = TSIRepository(client, store_id="001")
        print(f"✅ Repository created: {tsi_repo.table_name}")

        # Read items for document
        print(f"\n📋 Reading TSI items for document: {doc_number}...")
        items = tsi_repo.get_by_document(doc_number)

        if not items:
            print(f"⚠️  No items found for document {doc_number}")
            return

        print(f"✅ Found {len(items)} items\n")

        # Display items
        print_separator()
        print(f"{'Line':<6} {'Product':<40} {'Qty':>8} {'Unit':<6} {'Price':>10} {'Total':>12}")
        print_separator()

        for item in items:
            product = item.gs_name[:40] if item.gs_name else f"GS#{item.gs_code}"
            qty = f"{item.quantity:.2f}"
            price = f"{item.price_unit:.2f}"
            total = f"{item.line_total:.2f}"

            print(f"{item.line_number:<6} {product:<40} {qty:>8} {item.unit:<6} {price:>10} {total:>12}")

        print_separator()

        # Calculate totals
        total_qty = sum(item.quantity for item in items)
        total_amount = sum(item.line_total for item in items)

        print(f"\n📊 Summary:")
        print(f"   Lines: {len(items)}")
        print(f"   Total Quantity: {total_qty:.2f}")
        print(f"   Total Amount: {total_amount:.2f}")

    except Exception as e:
        print(f"❌ Error reading TSI: {e}")
        import traceback
        traceback.print_exc()


def test_tsh_by_document_number():
    """Test finding specific document"""

    print_separator("TEST: Find TSH by Document Number")

    doc_number = input("\n📝 Enter document number (or press Enter to skip): ").strip()

    if not doc_number:
        print("⚪ Skipped")
        return

    try:
        print(f"\n🔍 Searching for document: {doc_number}...")

        client = BtrieveClient(config_or_path={})
        tsh_repo = TSHRepository(client, store_id="001")

        document = tsh_repo.get_by_document_number(doc_number)

        if not document:
            print(f"❌ Document not found: {doc_number}")
            return

        print(f"✅ Document found!\n")
        print_separator()
        print(f"Document Number: {document.doc_number}")
        print(f"Date:           {document.doc_date}")
        print(f"Partner:        {document.pab_name} (#{document.pab_code})")
        print(f"Address:        {document.pab_address}")
        print(f"ICO:            {document.pab_ico}")
        print(f"Currency:       {document.currency}")
        print(f"Amount Base:    {document.amount_base}")
        print(f"Amount VAT:     {document.amount_vat}")
        print(f"Amount Total:   {document.amount_total}")
        print(f"Payment:        {'PAID' if document.paid else 'UNPAID'}")
        print(f"Status:         {document.status}")
        print_separator()

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


def main():
    print("=" * 60)
    print("NEX GENESIS - TSH/TSI READ TEST".center(60))
    print("=" * 60)

    # Test 1: Read TSH documents
    first_doc = test_tsh_read()

    # Test 2: Read TSI items for first document
    if first_doc:
        test_tsi_read(first_doc.doc_number)

    # Test 3: Find specific document (optional)
    test_tsh_by_document_number()

    # Final summary
    print_separator("TEST COMPLETE")
    print("\n✅ All read operations tested")
    print("\n📝 Next steps:")
    print("   - Test other repositories (GSCAT, PAB, etc.)")
    print("   - Integrate into GUI")
    print("   - Add write operations")


if __name__ == "__main__":
    main()