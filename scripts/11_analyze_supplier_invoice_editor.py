"""
Script 11: Analyze supplier-invoice-editor structure
Find main files that need modification for NEX enrichment display
"""

from pathlib import Path
import re


def main():
    """Analyze editor structure"""

    dev_root = Path(r"C:\Development\nex-automat")
    editor_root = dev_root / "apps" / "supplier-invoice-editor"

    print("=" * 60)
    print("SUPPLIER-INVOICE-EDITOR ANALYSIS")
    print("=" * 60)

    # Find main window file
    print("\n1. Looking for main window file...")
    main_files = list(editor_root.rglob("*main*.py"))
    for f in main_files:
        if f.is_file():
            print(f"   Found: {f.relative_to(dev_root)}")

    # Find invoice grid/table files
    print("\n2. Looking for invoice grid/table files...")
    grid_files = []
    for pattern in ["*grid*.py", "*table*.py", "*item*.py", "*invoice_detail*.py"]:
        grid_files.extend(list(editor_root.rglob(pattern)))

    seen = set()
    for f in grid_files:
        if f.is_file() and f not in seen:
            seen.add(f)
            print(f"   Found: {f.relative_to(dev_root)}")

    # Find UI files
    print("\n3. Looking for UI definition files...")
    ui_files = list(editor_root.rglob("*.ui"))
    for f in ui_files[:5]:  # Show first 5
        print(f"   Found: {f.relative_to(dev_root)}")

    # Show src structure
    print("\n4. Source directory structure:")
    src_dir = editor_root / "src"
    if src_dir.exists():
        for item in sorted(src_dir.iterdir()):
            if item.is_dir():
                py_files = list(item.glob("*.py"))
                print(f"   {item.name}/ ({len(py_files)} Python files)")
                for py in py_files[:3]:  # Show first 3
                    print(f"      - {py.name}")

    # Find invoice detail window (most likely place for grid)
    print("\n5. Analyzing invoice detail files...")
    detail_files = list(editor_root.rglob("*detail*.py"))
    for f in detail_files:
        if f.is_file():
            print(f"\n   File: {f.relative_to(dev_root)}")
            content = f.read_text(encoding='utf-8')

            # Check for QTableWidget or grid-related code
            if 'QTableWidget' in content or 'QTableView' in content:
                print(f"      ✅ Contains table/grid widget")

            # Check for item-related code
            if 'invoice_items' in content.lower():
                print(f"      ✅ Handles invoice items")

            # Check for PostgreSQL
            if 'PostgresStagingClient' in content or 'get_invoice' in content:
                print(f"      ✅ Uses PostgreSQL")

    # Find models
    print("\n6. Looking for data models...")
    model_files = list(editor_root.rglob("*model*.py"))
    for f in model_files:
        if f.is_file():
            print(f"   Found: {f.relative_to(dev_root)}")

    print("\n" + "=" * 60)
    print("RECOMMENDATION:")
    print("=" * 60)
    print("Main files to modify:")
    print("1. Invoice detail window (grid with items)")
    print("2. Item model/data structure")
    print("3. Possibly: validation before approval")

    return True


if __name__ == "__main__":
    main()