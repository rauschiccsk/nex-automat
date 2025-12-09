"""
Script 12: Show invoice_items_grid.py structure
"""

from pathlib import Path


def main():
    """Display invoice items grid file"""

    dev_root = Path(r"C:\Development\nex-automat")
    grid_file = dev_root / "apps" / "supplier-invoice-editor" / "src" / "ui" / "widgets" / "invoice_items_grid.py"

    if not grid_file.exists():
        print(f"❌ File not found: {grid_file}")
        return False

    print(f"📝 Content of: {grid_file.relative_to(dev_root)}")
    print("=" * 60)

    content = grid_file.read_text(encoding='utf-8')
    lines = content.split('\n')

    # Show full file with line numbers
    for i, line in enumerate(lines, 1):
        print(f"{i:3d}: {line}")

    print("=" * 60)
    print(f"Total lines: {len(lines)}")

    return True


if __name__ == "__main__":
    main()