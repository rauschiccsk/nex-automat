"""
Script 20: Update Archive Index with Batch 3 Session
Adds SESSION_2025-12-15_documentation-migration-batch3.md to archive index
"""

from pathlib import Path


def update_archive_index():
    """Update archive index with batch 3 session"""

    repo_root = Path(r"C:\Development\nex-automat")
    archive_index = repo_root / "docs" / "archive" / "00_ARCHIVE_INDEX.md"

    print("🔄 Updating Archive Index with Batch 3 Session...")
    print()

    if not archive_index.exists():
        print(f"❌ Archive index not found: {archive_index}")
        return

    with open(archive_index, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if batch 3 session already exists
    if "SESSION_2025-12-15_documentation-migration-batch3.md" in content:
        print("✓ Batch 3 session already in index")
        return

    # Find the session history section
    lines = content.split('\n')

    # Find "**2025-12-09:**" and add new date section before it
    insert_idx = None
    for i, line in enumerate(lines):
        if line.strip() == "**2025-12-09:**":
            insert_idx = i
            break

    if insert_idx:
        # Insert new date section
        new_entries = [
            "**2025-12-15:**",
            "",
            "- [Documentation Migration Batch 3](sessions/SESSION_2025-12-15_documentation-migration-batch3.md)",
            "- [Documentation Migration Batch 2](sessions/SESSION_2025-12-15_documentation-migration-batch2.md)",
            ""
        ]

        # Insert before 2025-12-09
        for entry in reversed(new_entries):
            lines.insert(insert_idx, entry)

        # Update total sessions count
        for i, line in enumerate(lines):
            if line.startswith("**Total Sessions:**"):
                lines[i] = "**Total Sessions:** 9"
                break

        content = '\n'.join(lines)

        with open(archive_index, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✅ Updated: {archive_index.relative_to(repo_root)}")
        print("   Added batch 2 and batch 3 sessions")
        print("   Updated session count: 9")
    else:
        print("⚠️ Could not find insertion point")

    print()
    print("=" * 60)
    print("✅ UPDATE COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    update_archive_index()