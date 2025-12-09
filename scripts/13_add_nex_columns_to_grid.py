"""
Script 13: Add NEX enrichment columns to invoice_items_grid.py
Phase 4: Editor integration
"""

from pathlib import Path


def main():
    """Add NEX columns and coloring to invoice items grid"""

    dev_root = Path(r"C:\Development\nex-automat")
    grid_file = dev_root / "apps" / "supplier-invoice-editor" / "src" / "ui" / "widgets" / "invoice_items_grid.py"

    if not grid_file.exists():
        print(f"❌ File not found: {grid_file}")
        return False

    print(f"📝 Reading: {grid_file.relative_to(dev_root)}")
    content = grid_file.read_text(encoding='utf-8')

    # Check if already modified
    if 'nex_gs_code' in content:
        print("⚠️  NEX columns already added - skipping")
        return True

    # 1. Replace COLUMNS definition (lines 27-37)
    old_columns = """    COLUMNS = [
        ('PLU', 'plu_code', False),           # Not editable
        ('Názov', 'item_name', True),         # Editable
        ('Kategória', 'category_code', True), # Editable
        ('MJ', 'unit', True),                 # Editable
        ('Množstvo', 'quantity', True),       # Editable
        ('Cena', 'unit_price', True),         # Editable
        ('Rabat %', 'rabat_percent', True),   # Editable
        ('Po rabate', 'price_after_rabat', False),  # Calculated
        ('Suma', 'total_price', False)        # Calculated
    ]"""

    new_columns = """    COLUMNS = [
        ('PLU', 'plu_code', False),           # Not editable
        ('Názov', 'item_name', True),         # Editable
        ('Kategória', 'category_code', True), # Editable
        ('MJ', 'unit', True),                 # Editable
        ('Množstvo', 'quantity', True),       # Editable
        ('Cena', 'unit_price', True),         # Editable
        ('Rabat %', 'rabat_percent', True),   # Editable
        ('Po rabate', 'price_after_rabat', False),  # Calculated
        ('Suma', 'total_price', False),       # Calculated
        # NEX Genesis enrichment columns
        ('NEX Kód', 'nex_gs_code', False),    # From enrichment
        ('NEX Názov', 'nex_name', False),     # From enrichment
        ('NEX Kat.', 'nex_category', False),  # From enrichment
        ('Match', 'in_nex', False)            # Match status
    ]"""

    content = content.replace(old_columns, new_columns)

    # 2. Update BackgroundRole to add NEX coloring (replace lines 97-102)
    old_background = """        elif role == Qt.BackgroundRole:
            # Highlight calculated columns
            column_key = self.COLUMNS[index.column()][1]
            if column_key in ('price_after_rabat', 'total_price'):
                from PyQt5.QtGui import QColor
                return QColor(240, 240, 240)"""

    new_background = """        elif role == Qt.BackgroundRole:
            from PyQt5.QtGui import QColor
            column_key = self.COLUMNS[index.column()][1]

            # Highlight calculated columns
            if column_key in ('price_after_rabat', 'total_price'):
                return QColor(240, 240, 240)

            # Color rows based on NEX match status
            in_nex = item.get('in_nex')
            if in_nex is True:
                # Matched - light green
                return QColor(200, 255, 200)
            elif in_nex is False:
                # No match - light red
                return QColor(255, 200, 200)
            elif in_nex is None:
                # Pending - light yellow
                return QColor(255, 255, 200)"""

    content = content.replace(old_background, new_background)

    # 3. Add ToolTipRole for match method (add after BackgroundRole section)
    tooltip_code = """
        elif role == Qt.ToolTipRole:
            # Show match method for NEX enriched items
            in_nex = item.get('in_nex')
            matched_by = item.get('matched_by')

            if in_nex is True and matched_by:
                match_method = 'EAN' if matched_by == 'ean' else 'Názov'
                return f"Matched by {match_method}"
            elif in_nex is False:
                return "No match found in NEX Genesis"
            elif in_nex is None:
                return "Pending enrichment"
"""

    # Insert tooltip code before "return QVariant()" at end of data() method
    # Find the return QVariant() that's at the end of data() method (around line 104)
    lines = content.split('\n')
    new_lines = []
    inserted = False

    for i, line in enumerate(lines):
        # Look for "return QVariant()" that's at the end of data() method
        # It should be after BackgroundRole and before setData method
        if 'return QVariant()' in line and not inserted and i > 90 and i < 110:
            # Insert tooltip code before this return
            for tooltip_line in tooltip_code.split('\n'):
                new_lines.append(tooltip_line)
            inserted = True

        new_lines.append(line)

    content = '\n'.join(new_lines)

    # Write modified content
    print(f"💾 Writing modified file...")
    grid_file.write_text(content, encoding='utf-8')

    print("✅ SUCCESS: invoice_items_grid.py updated with NEX columns")
    print("\nChanges:")
    print("  1. Added 4 NEX columns: NEX Kód, NEX Názov, NEX Kat., Match")
    print("  2. Added color coding:")
    print("     - Green = matched (in_nex = TRUE)")
    print("     - Red = no match (in_nex = FALSE)")
    print("     - Yellow = pending (in_nex = NULL)")
    print("  3. Added tooltips showing match method")

    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)