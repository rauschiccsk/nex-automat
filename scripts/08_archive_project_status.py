#!/usr/bin/env python3
"""
Archive PROJECT_STATUS.md-old as historical snapshot.

DECISION:
- PROJECT_STATUS.md-old je zastaralý (v2.1, 2.12.2025)
- Presunieme do archive/ s datovaným názvom
- Pridáme archive notice do headeru
- Nový PROJECT_STATUS.md vytvoríme až po spracovaní všetkých .md-old

USAGE:
    python scripts/08_archive_project_status.py
"""

from pathlib import Path
from datetime import datetime


def main():
    print("=" * 80)
    print("ARCHIVE PROJECT_STATUS.md-old")
    print("=" * 80)

    # Paths
    old_file = Path("docs/PROJECT_STATUS.md-old")
    archive_file = Path("docs/archive/PROJECT_STATUS_v2.1_2025-12-02.md")

    # Check if source exists
    if not old_file.exists():
        print(f"\n❌ ERROR: {old_file} not found!")
        return

    print(f"\n📂 Source: {old_file}")
    print(f"📦 Archive: {archive_file}")

    # Read content
    print("\n📖 Reading content...")
    content = old_file.read_text(encoding='utf-8')

    print(f"   Size: {len(content):,} bytes")
    print(f"   Lines: {len(content.splitlines()):,}")

    # Add archive notice
    archive_notice = """---
**⚠️ ARCHIVED DOCUMENT**

This document represents the project status as of **v2.1 (2025-12-02)**.

**This document is OUTDATED:**
- Does not include v2.2 (BaseGrid cleanup)
- Does not include v2.3 (invoice-shared migration)
- Does not include v2.4 (NEX Genesis enrichment - marked "PLANNED" but actually COMPLETE)

**For current status, see:**
- `docs/strategic/PROJECT_STATUS.md` (will be created after .md-old migration)
- `docs/PROJECT_ARCHIVE.md` or `docs/archive/sessions/` (detailed history)

**Archived:** {date}  
**Reason:** Historical snapshot (v2.1)

---

""".format(date=datetime.now().strftime('%Y-%m-%d'))

    # Insert notice after first heading
    lines = content.splitlines(keepends=True)

    # Find first heading
    first_heading_idx = 0
    for i, line in enumerate(lines):
        if line.startswith('# '):
            first_heading_idx = i + 1
            break

    # Insert notice
    new_content = (
            ''.join(lines[:first_heading_idx]) +
            archive_notice +
            ''.join(lines[first_heading_idx:])
    )

    # Create archive directory
    archive_file.parent.mkdir(parents=True, exist_ok=True)

    # Write archived file
    print("\n💾 Writing archive file...")
    archive_file.write_text(new_content, encoding='utf-8')
    print(f"   ✅ Created: {archive_file}")

    # Delete original
    print("\n🗑️  Removing original...")
    old_file.unlink()
    print(f"   ✅ Deleted: {old_file}")

    print("\n" + "=" * 80)
    print("✅ DONE!")
    print("=" * 80)

    print(f"\n📊 Archive Summary:")
    print(f"   Archived: PROJECT_STATUS_v2.1_2025-12-02.md")
    print(f"   Size: {len(new_content):,} bytes")
    print(f"   Location: docs/archive/")

    print("\n💡 Next steps:")
    print("   1. Continue processing .md-old files")
    print("   2. After all .md-old processed → create NEW PROJECT_STATUS.md")
    print("   3. Update archive index")

    # List remaining .md-old files
    remaining = list(Path("docs").rglob("*.md-old"))
    print(f"\n📂 Remaining .md-old files: {len(remaining)}")


if __name__ == "__main__":
    main()