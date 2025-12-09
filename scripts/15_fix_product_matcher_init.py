"""
Session Script 15: Fix ProductMatcher Initialization
Create BtrieveClient before passing to repositories
"""
from pathlib import Path


def main():
    matcher_file = Path(r"C:\Development\nex-automat\apps\supplier-invoice-loader\src\business\product_matcher.py")

    print("=" * 60)
    print("Fixing ProductMatcher Initialization")
    print("=" * 60)

    with open(matcher_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Add BtrieveClient import
    if 'from nexdata.btrieve.client import BtrieveClient' not in content:
        # Find import section
        import_pos = content.find('from nexdata.repositories')
        if import_pos > 0:
            content = content[:import_pos] + 'from nexdata.btrieve.client import BtrieveClient\n' + content[import_pos:]
            print("✅ Added BtrieveClient import")

    # Fix __init__ method
    old_init = '''    def __init__(self, nex_data_path: str):
        """
        Initialize matcher with NEX Genesis data

        Args:
            nex_data_path: Path to NEX Genesis data directory
        """
        self.gscat_repo = GSCATRepository(nex_data_path)
        self.barcode_repo = BARCODERepository(nex_data_path)'''

    new_init = '''    def __init__(self, nex_data_path: str):
        """
        Initialize matcher with NEX Genesis data

        Args:
            nex_data_path: Path to NEX Genesis data directory
        """
        self.btrieve = BtrieveClient(nex_data_path)
        self.gscat_repo = GSCATRepository(self.btrieve)
        self.barcode_repo = BARCODERepository(self.btrieve)'''

    if old_init in content:
        content = content.replace(old_init, new_init)

        with open(matcher_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print("✅ Fixed __init__ method")
        print("\nChanges:")
        print("  - Created BtrieveClient instance")
        print("  - Pass BtrieveClient to repositories (not path string)")
    else:
        print("⚠️  __init__ already fixed or pattern not found")

    print("\n" + "=" * 60)
    print("✅ Fix complete!")
    print("=" * 60)

    return 0


if __name__ == '__main__':
    import sys

    sys.exit(main())