"""
Script 14: Check PostgreSQL client in editor - verify it loads nex_* fields
"""

from pathlib import Path


def main():
    """Check postgres_client.py in editor"""

    dev_root = Path(r"C:\Development\nex-automat")
    postgres_file = dev_root / "apps" / "supplier-invoice-editor" / "src" / "database" / "postgres_client.py"

    if not postgres_file.exists():
        print(f"❌ File not found: {postgres_file}")
        return False

    print(f"📝 Analyzing: {postgres_file.relative_to(dev_root)}")
    print("=" * 60)

    content = postgres_file.read_text(encoding='utf-8')

    # Check if nex_* fields are in SELECT queries
    nex_fields = [
        'nex_gs_code',
        'nex_plu',
        'nex_name',
        'nex_category',
        'nex_barcode_created',
        'in_nex',
        'matched_by'
    ]

    print("\n1. Checking for NEX fields in SELECT queries:")
    for field in nex_fields:
        if field in content:
            print(f"   ✅ {field} found")
        else:
            print(f"   ❌ {field} NOT FOUND")

    # Find get_invoice or similar method
    print("\n2. Looking for invoice loading methods:")
    if 'def get_invoice' in content:
        print("   ✅ get_invoice() method found")

        # Extract the method to see the SELECT query
        lines = content.split('\n')
        in_method = False
        method_lines = []

        for line in lines:
            if 'def get_invoice' in line:
                in_method = True

            if in_method:
                method_lines.append(line)

                # Stop at next method or end of indentation
                if len(method_lines) > 1 and line and not line[0].isspace() and line.strip():
                    break

        print("\n   Method preview:")
        for i, line in enumerate(method_lines[:30], 1):  # Show first 30 lines
            print(f"   {i:3d}: {line}")

    # Check if items are loaded
    print("\n3. Checking item loading:")
    if 'invoice_items_pending' in content or 'get_invoice_items' in content:
        print("   ✅ Items loading method found")
    else:
        print("   ⚠️  Items loading method not clear")

    print("\n" + "=" * 60)
    print("RECOMMENDATION:")
    print("=" * 60)

    all_found = all(field in content for field in nex_fields)

    if all_found:
        print("✅ All NEX fields are present in postgres_client.py")
        print("   No modification needed")
    else:
        print("❌ Some NEX fields are missing")
        print("   Need to update SELECT query to include all NEX fields")

    return True


if __name__ == "__main__":
    main()