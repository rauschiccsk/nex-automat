#!/usr/bin/env python3
"""
Script 26: Diagnose syntax error around line 171
Show context around the error
"""

from pathlib import Path

# Target file
MAIN_WINDOW = Path("apps/supplier-invoice-editor/src/ui/main_window.py")


def main():
    """Show context around error"""
    print("=" * 60)
    print("Diagnosing syntax error around line 171")
    print("=" * 60)

    if not MAIN_WINDOW.exists():
        print(f"❌ ERROR: File not found: {MAIN_WINDOW}")
        return False

    content = MAIN_WINDOW.read_text(encoding='utf-8')
    lines = content.split('\n')

    # Show lines 160-180
    print("\n📝 Lines 160-180:")
    for i in range(159, min(180, len(lines))):
        marker = " >>>>" if i == 170 else "     "
        print(f"{marker} {i + 1:3d}: {lines[i]}")

    # Try to find unmatched try blocks
    print("\n🔍 Looking for try/except structure issues:")
    indent_stack = []
    for i, line in enumerate(lines[:180], 1):
        stripped = line.lstrip()
        if stripped.startswith('try:'):
            indent = len(line) - len(stripped)
            indent_stack.append((i, indent, 'try'))
            print(f"   Line {i:3d}: Found try: at indent {indent}")
        elif stripped.startswith('except'):
            if indent_stack and indent_stack[-1][2] == 'try':
                matched = indent_stack.pop()
                print(f"   Line {i:3d}: Matched except for try at line {matched[0]}")
            else:
                print(f"   Line {i:3d}: ⚠️ Unmatched except!")

    if indent_stack:
        print("\n⚠️ Unmatched try blocks:")
        for line_num, indent, block_type in indent_stack:
            print(f"   Line {line_num}: {block_type} at indent {indent}")

    print("\n" + "=" * 60)

    return True


if __name__ == "__main__":
    main()