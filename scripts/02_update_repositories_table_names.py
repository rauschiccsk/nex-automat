#!/usr/bin/env python3
"""
Update all repositories to use table names instead of full paths
"""

from pathlib import Path

REPOS_DIR = Path("packages/nexdata/nexdata/repositories")

# Mapping: filename -> table_name
REPO_UPDATES = {
    "gscat_repository.py": "gscat",
    "barcode_repository.py": "barcode",
    "mglst_repository.py": "mglst",
    "pab_repository.py": "pab",
}

# Dynamic repositories (need special handling for book_id)
DYNAMIC_REPOS = {
    "tsh_repository.py": "tsh",
    "tsi_repository.py": "tsi",
}


def update_static_repository(repo_file: Path, table_name: str) -> bool:
    """Update static repository to return table name"""

    if not repo_file.exists():
        print(f"  ❌ Not found: {repo_file.name}")
        return False

    content = repo_file.read_text(encoding='utf-8')
    lines = content.split('\n')

    # Find table_name property
    property_found = False
    for i, line in enumerate(lines):
        if '@property' in line:
            # Check next line for table_name
            if i + 1 < len(lines) and 'def table_name(self)' in lines[i + 1]:
                property_found = True
                # Find return statement (should be 2-3 lines after)
                for j in range(i + 2, min(i + 5, len(lines))):
                    if 'return' in lines[j]:
                        # Update return statement
                        lines[j] = f"        return '{table_name}'"
                        print(f"  ✓ Updated: {repo_file.name} → '{table_name}'")
                        break
                break

    if not property_found:
        print(f"  ⚠️  Could not find table_name property in {repo_file.name}")
        return False

    # Write back
    content = '\n'.join(lines)
    repo_file.write_text(content, encoding='utf-8')

    return True


def update_dynamic_repository(repo_file: Path, table_prefix: str) -> bool:
    """Update dynamic repository (TSH/TSI) with book_id support"""

    if not repo_file.exists():
        print(f"  ❌ Not found: {repo_file.name}")
        return False

    content = repo_file.read_text(encoding='utf-8')
    lines = content.split('\n')

    # 1. Find and update __init__ to accept book_id
    init_found = False
    for i, line in enumerate(lines):
        if 'def __init__(self, btrieve_client: BtrieveClient)' in line:
            # Update signature to include book_id
            lines[i] = '    def __init__(self, btrieve_client: BtrieveClient, book_id: str = "001"):'

            # Add book_id assignment after super().__init__
            for j in range(i + 1, min(i + 5, len(lines))):
                if 'super().__init__(btrieve_client)' in lines[j]:
                    # Insert book_id assignment before super
                    indent = ' ' * 8
                    lines.insert(j, f"{indent}self.book_id = book_id")
                    init_found = True
                    print(f"  ✓ Updated __init__ in {repo_file.name}")
                    break
            break

    if not init_found:
        print(f"  ⚠️  Could not update __init__ in {repo_file.name}")
        return False

    # 2. Update table_name property to use book_id
    property_found = False
    for i, line in enumerate(lines):
        if '@property' in line:
            # Check next line for table_name
            if i + 1 < len(lines) and 'def table_name(self)' in lines[i + 1]:
                property_found = True
                # Find return statement
                for j in range(i + 2, min(i + 5, len(lines))):
                    if 'return' in lines[j]:
                        # Update to use f-string with book_id
                        lines[j] = f"        return f'{table_prefix}-{{self.book_id}}'"
                        print(f"  ✓ Updated table_name in {repo_file.name} → '{table_prefix}-{{book_id}}'")
                        break
                break

    if not property_found:
        print(f"  ⚠️  Could not find table_name property in {repo_file.name}")
        return False

    # Write back
    content = '\n'.join(lines)
    repo_file.write_text(content, encoding='utf-8')

    return True


def main():
    print("=" * 70)
    print("Update Repositories - Table Names")
    print("=" * 70)
    print()

    if not REPOS_DIR.exists():
        print(f"❌ Repositories directory not found: {REPOS_DIR}")
        return

    print(f"📂 Directory: {REPOS_DIR}")
    print()

    # Update static repositories
    print("🔧 Updating static repositories...")
    static_success = 0
    for filename, table_name in REPO_UPDATES.items():
        repo_file = REPOS_DIR / filename
        if update_static_repository(repo_file, table_name):
            static_success += 1

    print()

    # Update dynamic repositories
    print("🔧 Updating dynamic repositories (TSH/TSI)...")
    dynamic_success = 0
    for filename, table_prefix in DYNAMIC_REPOS.items():
        repo_file = REPOS_DIR / filename
        if update_dynamic_repository(repo_file, table_prefix):
            dynamic_success += 1

    print()
    print("=" * 70)
    print(f"✅ Updated: {static_success}/{len(REPO_UPDATES)} static repositories")
    print(f"✅ Updated: {dynamic_success}/{len(DYNAMIC_REPOS)} dynamic repositories")
    print()
    print("Next: Create config/database.yaml")
    print("=" * 70)


if __name__ == "__main__":
    main()