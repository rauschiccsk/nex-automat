#!/usr/bin/env python3
"""
Create config/database.yaml for Btrieve table mappings
"""

from pathlib import Path

CONFIG_DIR = Path("config")
CONFIG_FILE = CONFIG_DIR / "database.yaml"

DATABASE_YAML_CONTENT = """# NEX Genesis Btrieve Database Configuration
# Table name mappings for nexdata package

nex_genesis:
  # Root paths
  root_path: "C:\\\\NEX"
  yearact_path: "C:\\\\NEX\\\\YEARACT"

  # Table mappings
  # Format: table_name: "full_path_to_BTR_file"
  tables:
    # Static tables (STORES)
    gscat: "C:\\\\NEX\\\\YEARACT\\\\STORES\\\\GSCAT.BTR"
    barcode: "C:\\\\NEX\\\\YEARACT\\\\STORES\\\\BARCODE.BTR"
    mglst: "C:\\\\NEX\\\\YEARACT\\\\STORES\\\\MGLST.BTR"

    # Static tables (DIALS)
    pab: "C:\\\\NEX\\\\YEARACT\\\\DIALS\\\\PAB00000.BTR"

    # Dynamic tables (use {book_id} placeholder)
    # These will be resolved at runtime based on book_id parameter
    tsh: "C:\\\\NEX\\\\YEARACT\\\\STORES\\\\TSHA-{book_id}.BTR"
    tsi: "C:\\\\NEX\\\\YEARACT\\\\STORES\\\\TSIA-{book_id}.BTR"

  # Book configuration
  books:
    # Default book for delivery notes
    delivery_notes_book: "001"

    # Book type (A = Annual)
    book_type: "A"

    # Available books
    available_books:
      - "001"
      - "002"
      - "003"

# Usage examples:
# ----------------
# Static table:
#   client = BtrieveClient("config/database.yaml")
#   repo = GSCATRepository(client)
#   repo.table_name  # Returns 'gscat'
#   client.open_file('gscat')  # Resolves to C:\\NEX\\YEARACT\\STORES\\GSCAT.BTR
#
# Dynamic table:
#   repo = TSHRepository(client, book_id="001")
#   repo.table_name  # Returns 'tsh-001'
#   client.open_file('tsh-001')  # Resolves to C:\\NEX\\YEARACT\\STORES\\TSHA-001.BTR
"""


def create_config():
    """Create database.yaml configuration file"""

    print("=" * 70)
    print("Create Database Configuration")
    print("=" * 70)
    print()

    # Create config directory if it doesn't exist
    if not CONFIG_DIR.exists():
        CONFIG_DIR.mkdir(parents=True)
        print(f"✓ Created directory: {CONFIG_DIR}")
    else:
        print(f"✓ Directory exists: {CONFIG_DIR}")

    # Check if file already exists
    if CONFIG_FILE.exists():
        print(f"⚠️  File already exists: {CONFIG_FILE}")
        response = input("   Overwrite? (y/n): ")
        if response.lower() != 'y':
            print("   Skipped.")
            return False

    # Write config file
    CONFIG_FILE.write_text(DATABASE_YAML_CONTENT, encoding='utf-8')

    print(f"✓ Created: {CONFIG_FILE}")
    print()

    # Show file content
    print("📄 File content:")
    print("-" * 70)
    lines = DATABASE_YAML_CONTENT.split('\n')
    for i, line in enumerate(lines[:35], 1):  # First 35 lines
        print(f"{i:2d}: {line}")
    print("   ...")
    print("-" * 70)

    print()
    print("✅ Configuration file created successfully!")
    print()
    print("Table mappings:")
    print("  • gscat    → C:\\NEX\\YEARACT\\STORES\\GSCAT.BTR")
    print("  • barcode  → C:\\NEX\\YEARACT\\STORES\\BARCODE.BTR")
    print("  • mglst    → C:\\NEX\\YEARACT\\STORES\\MGLST.BTR")
    print("  • pab      → C:\\NEX\\YEARACT\\DIALS\\PAB00000.BTR")
    print("  • tsh-001  → C:\\NEX\\YEARACT\\STORES\\TSHA-001.BTR")
    print("  • tsi-001  → C:\\NEX\\YEARACT\\STORES\\TSIA-001.BTR")
    print()
    print("Next: Test read operations")
    print("=" * 70)

    return True


if __name__ == "__main__":
    create_config()