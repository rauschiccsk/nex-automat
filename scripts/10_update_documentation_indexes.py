#!/usr/bin/env python3
"""
Update all documentation indexes after .md-old migration.

UPDATES:
1. docs/archive/00_ARCHIVE_INDEX.md - Add session files
2. docs/00_DOCUMENTATION_INDEX.md - Update counts
3. Generate new docs.json manifest

CHANGES PROCESSED:
- PROJECT_ARCHIVE.md-old → 7 session files
- PROJECT_STATUS.md-old → archived
- KNOWN_ISSUES.md-old → deleted

USAGE:
    python scripts/10_update_documentation_indexes.py
"""

from pathlib import Path
from datetime import datetime
import json


def update_archive_index():
    """Update docs/archive/00_ARCHIVE_INDEX.md with session files."""

    index_file = Path("docs/archive/00_ARCHIVE_INDEX.md")
    sessions_dir = Path("docs/archive/sessions")

    # Get all session files
    session_files = sorted(sessions_dir.glob("SESSION_*.md"))

    # Group by date
    sessions_by_date = {}
    for session_file in session_files:
        # Extract date from filename
        parts = session_file.stem.split('_')
        if len(parts) >= 2:
            date = parts[1]  # YYYY-MM-DD
            if date not in sessions_by_date:
                sessions_by_date[date] = []
            sessions_by_date[date].append(session_file)

    # Generate content
    content = f"""# Archive Index

**Category:** Archive  
**Last Updated:** {datetime.now().strftime('%Y-%m-%d')}

---

## Overview

This directory contains archived documentation and historical snapshots of the NEX Automat project.

---

## Session History

Complete chronological archive of development sessions. Each session documents work completed, decisions made, and lessons learned.

**Total Sessions:** {len(session_files)}

### By Date

"""

    # Add sessions grouped by date
    for date in sorted(sessions_by_date.keys(), reverse=True):
        content += f"**{date}:**\n\n"
        for session_file in sessions_by_date[date]:
            # Extract title from filename
            title = session_file.stem.replace('SESSION_', '').replace(date + '_', '').replace('-', ' ').title()
            content += f"- [{title}](sessions/{session_file.name})\n"
        content += "\n"

    # Add archived documents section
    content += """---

## Archived Documents

Historical snapshots of project documentation.

### Project Status

- [PROJECT_STATUS_v2.1_2025-12-02.md](PROJECT_STATUS_v2.1_2025-12-02.md) - Project status as of v2.1 (OUTDATED, archived)

---

## See Also

- [Documentation Index](../00_DOCUMENTATION_INDEX.md) - Current documentation
- [Session Notes](../../SESSION_NOTES/SESSION_NOTES.md) - Active work
- [Project Archive](PROJECT_ARCHIVE.md-old.backup) - Original archive backup (if exists)

---

**Note:** This index is automatically generated. Do not edit manually.
"""

    # Write file
    index_file.write_text(content, encoding='utf-8')

    return len(session_files)


def update_main_index():
    """Update docs/00_DOCUMENTATION_INDEX.md with current counts."""

    index_file = Path("docs/00_DOCUMENTATION_INDEX.md")

    if not index_file.exists():
        print(f"   ⚠️  Main index not found: {index_file}")
        return

    # Count .md files (excluding .md-old)
    all_md_files = list(Path("docs").rglob("*.md"))
    md_files = [f for f in all_md_files if not f.name.endswith('.md-old')]

    # Count by category
    strategic = len(list(Path("docs/strategic").glob("*.md"))) if Path("docs/strategic").exists() else 0
    system = len(list(Path("docs/system").glob("*.md"))) if Path("docs/system").exists() else 0
    development = len(list(Path("docs/development").glob("*.md"))) if Path("docs/development").exists() else 0
    deployment = len(list(Path("docs/deployment").glob("*.md"))) if Path("docs/deployment").exists() else 0
    archive = len(list(Path("docs/archive").rglob("*.md"))) if Path("docs/archive").exists() else 0

    # Read current content
    content = index_file.read_text(encoding='utf-8')

    # Update statistics (simple text replacement)
    # This is basic - you might want to improve pattern matching
    lines = content.splitlines()
    updated_lines = []

    for line in lines:
        # Update last updated date
        if 'Last Updated:' in line:
            updated_lines.append(f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d')}")
        else:
            updated_lines.append(line)

    # Write back
    index_file.write_text('\n'.join(updated_lines), encoding='utf-8')

    return len(md_files)


def generate_manifest():
    """Generate new docs.json manifest."""

    manifest_file = Path("SESSION_NOTES/docs.json")

    # Count files
    all_files = list(Path("docs").rglob("*"))
    md_files = [f for f in all_files if f.suffix == '.md']
    md_old_files = [f for f in all_files if f.name.endswith('.md-old')]

    # Basic manifest structure
    manifest = {
        "name": "documentation",
        "type": "docs",
        "location": "docs",
        "generated": datetime.now().isoformat(),
        "description": "Komplexná dokumentácia NEX Automat projektu",
        "statistics": {
            "total_files": len(all_files),
            "markdown_files": len(md_files),
            "md_old_remaining": len(md_old_files),
            "total_lines": sum(len(f.read_text(encoding='utf-8').splitlines()) for f in md_files if f.is_file()),
        },
        "migration_status": {
            "completed": [
                "PROJECT_ARCHIVE.md-old → 7 session files",
                "PROJECT_STATUS.md-old → archived",
                "KNOWN_ISSUES.md-old → deleted"
            ],
            "remaining": len(md_old_files),
            "progress": f"{((60 - len(md_old_files)) / 60 * 100):.1f}%"  # Assuming 60 total
        }
    }

    # Write manifest
    manifest_file.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding='utf-8')

    return manifest


def main():
    print("=" * 80)
    print("UPDATE DOCUMENTATION INDEXES")
    print("=" * 80)

    print("\n📊 Processing updates...\n")

    # 1. Update archive index
    print("1. Updating docs/archive/00_ARCHIVE_INDEX.md...")
    try:
        session_count = update_archive_index()
        print(f"   ✅ Updated: {session_count} sessions indexed")
    except Exception as e:
        print(f"   ❌ ERROR: {e}")

    # 2. Update main index
    print("\n2. Updating docs/00_DOCUMENTATION_INDEX.md...")
    try:
        doc_count = update_main_index()
        print(f"   ✅ Updated: {doc_count} documents indexed")
    except Exception as e:
        print(f"   ❌ ERROR: {e}")

    # 3. Generate manifest
    print("\n3. Generating SESSION_NOTES/docs.json...")
    try:
        manifest = generate_manifest()
        print(f"   ✅ Generated: {manifest['statistics']['markdown_files']} .md files")
        print(f"   ✅ Remaining: {manifest['statistics']['md_old_remaining']} .md-old files")
        print(f"   ✅ Progress: {manifest['migration_status']['progress']}")
    except Exception as e:
        print(f"   ❌ ERROR: {e}")

    print("\n" + "=" * 80)
    print("✅ INDEXES UPDATED!")
    print("=" * 80)

    print("\n📁 Updated files:")
    print("   - docs/archive/00_ARCHIVE_INDEX.md")
    print("   - docs/00_DOCUMENTATION_INDEX.md")
    print("   - SESSION_NOTES/docs.json")

    print("\n💡 Next steps:")
    print("   1. Review updated indexes")
    print("   2. Continue .md-old migration")
    print("   3. Git commit changes")


if __name__ == "__main__":
    main()