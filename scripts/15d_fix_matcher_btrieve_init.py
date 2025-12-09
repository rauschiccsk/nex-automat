"""
Session Script 15d: Fix ProductMatcher BtrieveClient Init
Pass config dict instead of path string
"""
from pathlib import Path


def main():
    matcher_file = Path(r"C:\Development\nex-automat\apps\supplier-invoice-loader\src\business\product_matcher.py")

    print("=" * 60)
    print("Fixing BtrieveClient Initialization")
    print("=" * 60)

    with open(matcher_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix __init__ - pass config dict
    old_init = '''    def __init__(self, nex_data_path: str):
        """
        Initialize matcher with NEX Genesis data

        Args:
            nex_data_path: Path to NEX Genesis data directory
        """
        self.btrieve = BtrieveClient(nex_data_path)
        self.gscat_repo = GSCATRepository(self.btrieve)
        self.barcode_repo = BARCODERepository(self.btrieve)'''

    new_init = '''    def __init__(self, nex_data_path: str):
        """
        Initialize matcher with NEX Genesis data

        Args:
            nex_data_path: Path to NEX Genesis data directory
        """
        # Create BtrieveClient with config
        btrieve_config = {
            'database_path': nex_data_path
        }
        self.btrieve = BtrieveClient(config_or_path=btrieve_config)
        self.gscat_repo = GSCATRepository(self.btrieve)
        self.barcode_repo = BARCODERepository(self.btrieve)'''

    if old_init in content:
        content = content.replace(old_init, new_init)

        with open(matcher_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print("✅ Fixed BtrieveClient initialization")
        print("\nChange:")
        print("  - Create config dict with database_path")
        print("  - Pass config_or_path=btrieve_config")
    else:
        print("⚠️  Already fixed or pattern not found")

    print("\n" + "=" * 60)
    print("✅ Fix complete!")
    print("=" * 60)

    return 0


if __name__ == '__main__':
    import sys

    sys.exit(main())