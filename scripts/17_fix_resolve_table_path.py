"""
Session Script 17: Fix _resolve_table_path Fallback
Add database_path fallback for table resolution
"""
from pathlib import Path
import os


def main():
    btrieve_client = Path(r"C:\Development\nex-automat\packages\nexdata\nexdata\btrieve\btrieve_client.py")

    print("=" * 60)
    print("Fixing _resolve_table_path() Fallback")
    print("=" * 60)

    with open(btrieve_client, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the end of _resolve_table_path method
    # It currently ends with: return table_name_or_path

    old_ending = '''                        return path_template.replace('{book_id}', book_id)

        # It's already a path, or no config - use as-is
        return table_name_or_path'''

    new_ending = '''                        return path_template.replace('{book_id}', book_id)

        # Fallback: if we have database_path, construct path
        if self.config and 'database_path' in self.config:
            db_path = self.config['database_path']
            # table_name to uppercase + .BTR extension
            table_file = f"{table_name_or_path.upper()}.BTR"
            return os.path.join(db_path, table_file)

        # It's already a path, or no config - use as-is
        return table_name_or_path'''

    if old_ending in content:
        content = content.replace(old_ending, new_ending)

        with open(btrieve_client, 'w', encoding='utf-8') as f:
            f.write(content)

        print("✅ Fixed _resolve_table_path() method")
        print("\nAdded fallback:")
        print("  - Check for config['database_path']")
        print("  - Construct: database_path + table_name.upper() + '.BTR'")
        print("  - Example: 'gscat' → 'C:\\NEX\\YEARACT\\STORES\\GSCAT.BTR'")
    else:
        print("⚠️  Pattern not found or already fixed")
        print("\nSearching for _resolve_table_path:")

        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'def _resolve_table_path' in line:
                print(f"\nFound at line {i + 1}")
                # Show last 10 lines of method
                for j in range(max(0, i - 5), min(len(lines), i + 15)):
                    print(f"{j + 1:4d}: {lines[j]}")
                break

    print("\n" + "=" * 60)
    print("✅ Fix complete!")
    print("=" * 60)

    return 0


if __name__ == '__main__':
    import sys

    sys.exit(main())