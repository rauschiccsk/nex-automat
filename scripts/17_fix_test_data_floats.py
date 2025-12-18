"""
Fix: Change 0 to 0.0 in test data for float columns.
Run from: C:/Development/nex-automat
"""

from pathlib import Path


def main():
    file_path = Path("apps/supplier-invoice-staging/ui/invoice_items_window.py")

    if not file_path.exists():
        print(f"ERROR: {file_path} not found")
        return False

    content = file_path.read_text(encoding="utf-8")

    # Replace integer 0 with float 0.0 for margin and price columns
    # Pattern: "margin_percent": 0, -> "margin_percent": 0.0,
    replacements = [
        ('"margin_percent": 0,', '"margin_percent": 0.0,'),
        ('"selling_price_excl_vat": 0,', '"selling_price_excl_vat": 0.0,'),
        ('"selling_price_incl_vat": 0,', '"selling_price_incl_vat": 0.0,'),
    ]

    changed = False
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
            changed = True

    if not changed:
        print("SKIP: No changes needed or already fixed")
        return True

    file_path.write_text(content, encoding="utf-8")
    print(f"OK: Fixed test data in {file_path}")
    return True


if __name__ == "__main__":
    main()