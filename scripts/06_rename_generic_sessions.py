#!/usr/bin/env python3
"""
Analyze and rename generic session files with better descriptive names.

PROBLEM:
- Niektoré session súbory majú generické názvy (napr. SESSION_2025-12-08_20251208.md)
- Ťažko sa v nich orientuje bez otvorenia

SOLUTION:
- Načíta obsah generických súborov
- Zanalyzuje title, summary, objectives
- Navrhne lepší názov
- Premenuje súbory

USAGE:
    python scripts/06_rename_generic_sessions.py
"""

import re
from pathlib import Path
from typing import Dict, List


def analyze_session_content(filepath: Path) -> Dict[str, str]:
    """Extract key information from session file."""
    content = filepath.read_text(encoding='utf-8')
    lines = content.splitlines()

    info = {
        'title': '',
        'objective': '',
        'summary': '',
        'status': ''
    }

    # Extract title (first # heading)
    for line in lines[:20]:
        if line.startswith('# ') and not line.startswith('##'):
            info['title'] = line.lstrip('#').strip()
            break

    # Look for objective/goal patterns
    objective_patterns = [
        r'\*\*Cieľ:\*\*\s*(.+)',
        r'\*\*Objective:\*\*\s*(.+)',
        r'\*\*Goal:\*\*\s*(.+)',
        r'## SESSION OBJECTIVE\s+(.+)',
    ]

    for line in lines[:50]:
        for pattern in objective_patterns:
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                info['objective'] = match.group(1).strip()
                break
        if info['objective']:
            break

    # Look for status
    status_patterns = [
        r'\*\*Status:\*\*\s*(.+)',
        r'Status:\s+(.+)',
    ]

    for line in lines[:50]:
        for pattern in status_patterns:
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                info['status'] = match.group(1).strip()
                break
        if info['status']:
            break

    # Extract summary (look for ## Summary or ### Summary)
    in_summary = False
    summary_lines = []
    for line in lines[:100]:
        if re.match(r'^##+ Summary', line, re.IGNORECASE):
            in_summary = True
            continue
        if in_summary:
            if line.startswith('#'):
                break
            if line.strip():
                summary_lines.append(line.strip())
            if len(summary_lines) >= 3:
                break

    if summary_lines:
        info['summary'] = ' '.join(summary_lines)[:200]

    return info


def suggest_filename(date: str, info: Dict[str, str], original: str) -> str:
    """Suggest a better filename based on session content."""

    # Extract key phrases from title, objective, summary
    text = f"{info['title']} {info['objective']} {info['summary']}".lower()

    # Keywords to look for
    keywords = {
        'v2.2': ['v2.2', 'v22'],
        'v2.3': ['v2.3', 'v23', 'invoice-shared', 'migration'],
        'v2.4': ['v2.4', 'v24', 'enrichment', 'product matching'],
        'analysis': ['analýza', 'analysis', 'investigation'],
        'loader': ['supplier-invoice-loader', 'loader'],
        'editor': ['supplier-invoice-editor', 'editor'],
        'deployment': ['deployment', 'deploy', 'magerstav', 'mágerstav'],
        'implementation': ['implementation', 'implementácia'],
        'planning': ['planning', 'plan', 'návrh'],
        'testing': ['testing', 'test'],
    }

    # Detect relevant keywords
    detected = []
    for key, terms in keywords.items():
        if any(term in text for term in terms):
            detected.append(key)

    # Generate slug
    if 'v2.3' in detected and 'analysis' in detected:
        slug = 'v23-loader-analysis-enrichment-planning'
    elif 'v2.4' in detected and 'implementation' in detected:
        slug = 'v24-enrichment-implementation-complete'
    elif 'v2.4' in detected and 'deployment' in detected:
        slug = 'v24-phase4-deployment'
    elif 'v2.4' in detected:
        slug = 'v24-product-enrichment'
    elif 'loader' in detected and 'analysis' in detected:
        slug = 'loader-analysis-planning'
    else:
        # Fallback: use parts of title
        title_words = re.sub(r'[^\w\s-]', '', info['title'].lower())
        title_words = re.sub(r'[-\s]+', '-', title_words)
        slug = title_words[:50] if title_words else original.replace('.md', '').split('_')[-1]

    return f"SESSION_{date}_{slug}.md"


def main():
    print("=" * 80)
    print("SESSION FILENAME OPTIMIZER")
    print("=" * 80)

    sessions_dir = Path("docs/archive/sessions")

    if not sessions_dir.exists():
        print(f"❌ ERROR: {sessions_dir} not found!")
        return

    # Find all session files
    all_files = list(sessions_dir.glob("SESSION_*.md"))

    print(f"\n📂 Found {len(all_files)} session files")

    # Identify generic filenames (contain date twice or 'session-NN')
    generic_patterns = [
        r'SESSION_\d{4}-\d{2}-\d{2}_\d{8}\.md',  # SESSION_YYYY-MM-DD_YYYYMMDD.md
        r'SESSION_session-\d+_',  # SESSION_session-NN_
    ]

    generic_files = []
    for filepath in all_files:
        filename = filepath.name
        if any(re.search(pattern, filename) for pattern in generic_patterns):
            generic_files.append(filepath)

    if not generic_files:
        print("\n✅ No generic filenames found! All files have descriptive names.")
        return

    print(f"\n🔍 Found {len(generic_files)} generic filenames:")
    for f in generic_files:
        print(f"   - {f.name}")

    # Analyze and suggest renames
    renames = []

    print("\n📊 Analyzing sessions...")
    for filepath in generic_files:
        print(f"\n{'=' * 60}")
        print(f"Analyzing: {filepath.name}")

        # Extract date from filename
        date_match = re.search(r'(\d{4}-\d{2}-\d{2})', filepath.name)
        date_str = date_match.group(1) if date_match else 'unknown'

        # Analyze content
        info = analyze_session_content(filepath)

        print(f"   Title: {info['title'][:70]}...")
        print(f"   Objective: {info['objective'][:70]}...")
        print(f"   Status: {info['status']}")

        # Suggest new filename
        new_filename = suggest_filename(date_str, info, filepath.name)

        if new_filename != filepath.name:
            renames.append({
                'old': filepath,
                'new': filepath.parent / new_filename,
                'info': info
            })
            print(f"   ✨ Suggested: {new_filename}")
        else:
            print(f"   ✅ Filename already optimal")

    if not renames:
        print("\n✅ All filenames are already optimal!")
        return

    # Ask for confirmation
    print("\n" + "=" * 80)
    print("RENAME SUMMARY")
    print("=" * 80)
    print(f"\n📝 Proposed renames ({len(renames)} files):\n")

    for i, rename in enumerate(renames, 1):
        print(f"{i}. {rename['old'].name}")
        print(f"   → {rename['new'].name}")
        print()

    response = input("Proceed with renaming? (yes/no): ").strip().lower()

    if response not in ['yes', 'y']:
        print("\n❌ Rename cancelled.")
        return

    # Perform renames
    print("\n🔄 Renaming files...")
    for rename in renames:
        old_path = rename['old']
        new_path = rename['new']

        try:
            old_path.rename(new_path)
            print(f"✅ Renamed: {new_path.name}")
        except Exception as e:
            print(f"❌ ERROR renaming {old_path.name}: {e}")

    print("\n" + "=" * 80)
    print("✅ DONE!")
    print("=" * 80)
    print(f"\n📁 Renamed {len(renames)} files in: docs/archive/sessions/")
    print("\n💡 Next steps:")
    print("   1. Review renamed files")
    print("   2. Update archive index if needed")
    print("   3. Commit changes to Git")


if __name__ == "__main__":
    main()