"""
Add to_bytes() method to all repositories
"""

from pathlib import Path

REPOS_DIR = Path("packages/nexdata/nexdata/repositories")

# Repository files to update
REPO_FILES = [
    "tsh_repository.py",
    "tsi_repository.py",
    "gscat_repository.py",
    "barcode_repository.py",
    "pab_repository.py",
    "mglst_repository.py",
]

# Method to add (with proper indentation)
TO_BYTES_METHOD = '''
    def to_bytes(self, record) -> bytes:
        """Convert record to bytes"""
        return record.to_bytes()
'''


def add_to_bytes_method(filepath: Path) -> bool:
    """Add to_bytes method to repository file"""

    if not filepath.exists():
        return False

    # Read file
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Check if already has to_bytes
    if "def to_bytes(self" in content:
        return False

    # Find where to insert (after from_bytes method)
    lines = content.split('\n')
    insert_index = -1

    # Find from_bytes method
    for i, line in enumerate(lines):
        if "def from_bytes(self" in line:
            # Find end of this method (next def or class end)
            for j in range(i + 1, len(lines)):
                # Look for next method or end of indented block
                if lines[j].strip().startswith("def ") and not lines[j].strip().startswith("def from_bytes"):
                    insert_index = j
                    break
                # Or if we hit a blank line followed by non-indented content
                if j < len(lines) - 1 and lines[j].strip() == "" and lines[j + 1] and not lines[j + 1].startswith(
                        "    "):
                    insert_index = j
                    break
            break

    if insert_index == -1:
        # Try alternative: insert before first method after from_bytes
        for i, line in enumerate(lines):
            if "def get_by" in line or "def search_by" in line or "def get_recent" in line:
                insert_index = i
                break

    if insert_index == -1:
        print(f"  ❌ Could not find insertion point")
        return False

    # Insert method
    method_lines = TO_BYTES_METHOD.strip('\n').split('\n')
    for line in reversed(method_lines):
        lines.insert(insert_index, line)

    # Write back
    new_content = '\n'.join(lines)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    return True


def add_to_all_repositories():
    print("=" * 60)
    print("ADD: to_bytes() method to repositories")
    print("=" * 60)

    if not REPOS_DIR.exists():
        print(f"❌ Directory not found: {REPOS_DIR}")
        return False

    print(f"\n📁 Processing repositories in: {REPOS_DIR}")
    print("-" * 60)

    added_count = 0
    skipped_count = 0

    for repo_file in REPO_FILES:
        filepath = REPOS_DIR / repo_file

        if not filepath.exists():
            print(f"⚠️  {repo_file:<30} - File not found")
            continue

        print(f"📄 {repo_file:<30}", end=" - ")

        if add_to_bytes_method(filepath):
            print("✅ Added")
            added_count += 1
        else:
            print("⚪ Already exists or skipped")
            skipped_count += 1

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY:")
    print(f"  ✅ Added:   {added_count}")
    print(f"  ⚪ Skipped: {skipped_count}")
    print(f"  📊 Total:   {len(REPO_FILES)}")
    print("=" * 60)

    if added_count > 0:
        print("\n📋 Added method:")
        print("   def to_bytes(self, record) -> bytes:")
        print("       return record.to_bytes()")

        print("\n📝 Next step:")
        print("   python scripts/test_tsh_tsi_read.py")

    return True


if __name__ == "__main__":
    success = add_to_all_repositories()
    exit(0 if success else 1)