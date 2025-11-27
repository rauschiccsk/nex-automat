#!/usr/bin/env python3
"""
Fix TSH and TSI repositories - rename store_id to book_id and use table names
"""

from pathlib import Path

REPOS = [
    "packages/nexdata/nexdata/repositories/tsh_repository.py",
    "packages/nexdata/nexdata/repositories/tsi_repository.py"
]


def fix_repository(repo_path: Path) -> bool:
    """Fix dynamic repository"""

    if not repo_path.exists():
        print(f"  ❌ Not found: {repo_path.name}")
        return False

    content = repo_path.read_text(encoding='utf-8')

    # Determine table prefix from filename
    table_prefix = 'tsh' if 'tsh_' in repo_path.name else 'tsi'

    # Replace store_id with book_id in __init__ signature
    content = content.replace(
        'def __init__(self, btrieve_client: BtrieveClient, store_id: str = "001"):',
        'def __init__(self, btrieve_client: BtrieveClient, book_id: str = "001"):'
    )

    # Replace store_id with book_id in docstring
    content = content.replace(
        'store_id: Store identifier (default: "001")',
        'book_id: Book identifier (default: "001")'
    )

    # Replace self.store_id assignment
    content = content.replace(
        'self.store_id = store_id',
        'self.book_id = book_id'
    )

    # Replace table_name property return value
    # Old: f"C:/NEX/YEARACT/STORES/TSHA-{self.store_id}.BTR"
    # New: f'{tsh}-{self.book_id}'

    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'return f"C:/NEX/YEARACT/STORES/TSH' in line or 'return f"C:/NEX/YEARACT/STORES/TSI' in line:
            # Replace with simple table name
            lines[i] = f'        return f\'{table_prefix}-{{self.book_id}}\''
            print(f"  ✓ Updated table_name: '{table_prefix}-{{book_id}}'")
            break

    content = '\n'.join(lines)

    # Write back
    repo_path.write_text(content, encoding='utf-8')

    print(f"  ✓ Fixed: {repo_path.name}")
    return True


def main():
    print("=" * 70)
    print("Fix Dynamic Repositories (TSH/TSI)")
    print("=" * 70)
    print()

    success = 0
    for repo_path_str in REPOS:
        repo_path = Path(repo_path_str)
        print(f"📝 Processing: {repo_path.name}")
        if fix_repository(repo_path):
            success += 1
        print()

    print("=" * 70)
    print(f"✅ Fixed: {success}/{len(REPOS)} repositories")
    print()
    print("Changes:")
    print("  • store_id → book_id")
    print("  • Full path → table name (tsh-{book_id}, tsi-{book_id})")
    print()
    print("Next: Create config/database.yaml")
    print("=" * 70)


if __name__ == "__main__":
    main()