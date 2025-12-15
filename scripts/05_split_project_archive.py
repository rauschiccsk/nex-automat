#!/usr/bin/env python3
"""
Split PROJECT_ARCHIVE.md-old into individual session files.

PROBLEM:
- PROJECT_ARCHIVE.md-old je 4500+ riadkov (126 KB)
- Ťažko sa načítava do Claude chatu
- Chceme každú session v samostatnom súbore

SOLUTION:
- Rozdelí na sessions pomocou regex
- Vytvorí docs/archive/sessions/ adresár
- Každá session = samostatný .md súbor

NAMING:
- SESSION_2025-12-06_basegrid-persistence.md
- SESSION_2025-12-08_v2.2-cleanup.md
- Atď.

USAGE:
    python scripts/05_split_project_archive.py
"""

import re
from pathlib import Path
from datetime import datetime


def main():
    print("=" * 80)
    print("PROJECT ARCHIVE SPLITTER")
    print("=" * 80)

    # Paths
    archive_file = Path("docs/PROJECT_ARCHIVE.md-old")
    sessions_dir = Path("docs/archive/sessions")

    # Check if archive exists
    if not archive_file.exists():
        print(f"❌ ERROR: {archive_file} not found!")
        return

    print(f"\n📂 Reading: {archive_file}")
    content = archive_file.read_text(encoding='utf-8')

    print(f"   Size: {len(content):,} bytes")
    print(f"   Lines: {len(content.splitlines()):,}")

    # Extract document header (everything before first session)
    first_session_match = re.search(
        r'^(## Session \d{4}-\d{2}-\d{2}:|# PROJECT ARCHIVE SESSION)',
        content,
        re.MULTILINE
    )

    if not first_session_match:
        print("❌ ERROR: No sessions found in archive!")
        return

    header = content[:first_session_match.start()].strip()
    sessions_content = content[first_session_match.start():]

    print(f"\n📋 Document header: {len(header)} bytes")

    # Split into sessions using regex
    # Matches both:
    # ## Session 2025-12-06: Title
    # # PROJECT ARCHIVE SESSION - Title
    pattern = r'^(## Session \d{4}-\d{2}-\d{2}:.*?$|# PROJECT ARCHIVE SESSION.*?$)'
    session_starts = list(re.finditer(pattern, sessions_content, re.MULTILINE))

    print(f"\n🔍 Found {len(session_starts)} sessions")

    # Create sessions directory
    sessions_dir.mkdir(parents=True, exist_ok=True)
    print(f"\n📁 Created directory: {sessions_dir}")

    # Split sessions
    sessions = []
    for i, match in enumerate(session_starts):
        start = match.start()
        end = session_starts[i + 1].start() if i + 1 < len(session_starts) else len(sessions_content)

        session_content = sessions_content[start:end].strip()
        session_title = match.group(0)

        sessions.append({
            'title': session_title,
            'content': session_content
        })

    # Generate filenames and write files
    created_files = []

    for i, session in enumerate(sessions):
        # Extract date and title from session header
        title_line = session['title']

        # Try to extract date from title
        date_match = re.search(r'(\d{4}-\d{2}-\d{2})', title_line)
        if date_match:
            date_str = date_match.group(1)
        else:
            # Fallback: use index
            date_str = f"session-{i + 1:02d}"

        # Extract descriptive part (sanitize for filename)
        if 'Session' in title_line:
            # ## Session 2025-12-06: BaseGrid Persistence Implementation
            title_part = title_line.split(':', 1)[1].strip() if ':' in title_line else f"session-{i + 1}"
        else:
            # # PROJECT ARCHIVE SESSION - v2.3 Migration
            title_part = title_line.replace('# PROJECT ARCHIVE SESSION', '').replace('-', '').strip()
            if not title_part:
                title_part = f"session-{i + 1}"

        # Sanitize filename
        title_slug = re.sub(r'[^\w\s-]', '', title_part.lower())
        title_slug = re.sub(r'[-\s]+', '-', title_slug)
        title_slug = title_slug[:50]  # Limit length

        # Create filename
        filename = f"SESSION_{date_str}_{title_slug}.md"
        filepath = sessions_dir / filename

        # Write session file
        session_header = f"""# {session['title'].lstrip('#').strip()}

**Extracted from:** PROJECT_ARCHIVE.md-old  
**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

"""

        full_content = session_header + session['content']
        filepath.write_text(full_content, encoding='utf-8')

        created_files.append({
            'filename': filename,
            'size': len(full_content),
            'lines': len(full_content.splitlines())
        })

        print(f"\n✅ Created: {filename}")
        print(f"   Size: {len(full_content):,} bytes")
        print(f"   Lines: {len(full_content.splitlines()):,}")

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"\n📊 Created {len(created_files)} session files:")

    total_size = sum(f['size'] for f in created_files)
    total_lines = sum(f['lines'] for f in created_files)

    print(f"\n   Total size: {total_size:,} bytes")
    print(f"   Total lines: {total_lines:,}")
    print(f"   Original size: {len(content):,} bytes")
    print(f"   Original lines: {len(content.splitlines()):,}")

    print("\n📁 Files created in: docs/archive/sessions/")
    for f in created_files:
        print(f"   - {f['filename']}")

    print("\n✅ DONE!")
    print("\n💡 Next steps:")
    print("   1. Review generated session files")
    print("   2. Optionally rename files for better organization")
    print("   3. Update documentation indexes")
    print("   4. Delete PROJECT_ARCHIVE.md-old (backup first!)")


if __name__ == "__main__":
    main()