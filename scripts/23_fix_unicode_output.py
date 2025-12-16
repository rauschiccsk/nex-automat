#!/usr/bin/env python
"""
Script 23: Fix Unicode Output for Windows Console
Replaces Unicode characters with ASCII equivalents.
"""

from pathlib import Path

# Files to fix
FILES_TO_FIX = [
    "tools/rag/database.py",
    "tools/rag/embeddings.py",
    "tools/rag/__main__.py",
    "tools/rag/init_prompt_helper.py",
    "tools/rag/api.py",
]

# Replacements: Unicode -> ASCII
REPLACEMENTS = {
    "✓": "[OK]",
    "✅": "[OK]",
    "❌": "[ERROR]",
    "⚠": "[WARN]",
    "🔍": "[SEARCH]",
    "📊": "[STATS]",
    "📄": "[DOC]",
    "📚": "[DOCS]",
    "🟢": "[HIGH]",
    "🟡": "[MED]",
    "🔴": "[LOW]",
    "🤖": "[BOT]",
    "👋": "",
    "💥": "[!]",
    "✨": "[*]",
    "📌": "[>]",
}


def fix_file(filepath: Path) -> bool:
    """Fix Unicode in a single file."""
    if not filepath.exists():
        print(f"  [SKIP] Not found: {filepath}")
        return False

    content = filepath.read_text(encoding='utf-8')
    original = content

    for unicode_char, ascii_replacement in REPLACEMENTS.items():
        content = content.replace(unicode_char, ascii_replacement)

    if content != original:
        filepath.write_text(content, encoding='utf-8')
        changes = sum(1 for u in REPLACEMENTS if u in original)
        print(f"  [OK] Fixed: {filepath} ({changes} replacement types)")
        return True
    else:
        print(f"  [--] No changes: {filepath}")
        return False


def main():
    print("=" * 50)
    print("Fixing Unicode characters for Windows console")
    print("=" * 50)
    print()

    project_root = Path(__file__).parent.parent
    fixed = 0

    for rel_path in FILES_TO_FIX:
        filepath = project_root / rel_path
        if fix_file(filepath):
            fixed += 1

    print()
    print(f"Fixed {fixed}/{len(FILES_TO_FIX)} files")
    print()
    print("[OK] Done! Run tests again:")
    print("   python -m tools.rag --stats")


if __name__ == "__main__":
    main()