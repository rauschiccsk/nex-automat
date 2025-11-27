#!/usr/bin/env python3
"""
Show complete __init__ method
"""

from pathlib import Path

TARGET_FILE = Path("packages/nexdata/nexdata/btrieve/btrieve_client.py")


def show_init():
    if not TARGET_FILE.exists():
        print(f"❌ File not found: {TARGET_FILE}")
        return

    content = TARGET_FILE.read_text(encoding='utf-8')
    lines = content.split('\n')

    # Find __init__ method
    in_method = False
    method_lines = []
    indent_level = 0

    for i, line in enumerate(lines, 1):
        if 'def __init__(self' in line:
            in_method = True
            indent_level = len(line) - len(line.lstrip())
            print(f"Found __init__ at line {i}")
            print()

        if in_method:
            method_lines.append((i, line))

            # Check if we left the method (next def at same or lower indent)
            if i > 48 and line.strip().startswith('def '):
                current_indent = len(line) - len(line.lstrip())
                if current_indent <= indent_level:
                    print(f"End of __init__ at line {i - 1}")
                    break

    print("__init__ method content:")
    print("=" * 70)
    for line_num, line_content in method_lines:
        print(f"{line_num:3d}: {line_content}")
    print("=" * 70)


if __name__ == "__main__":
    show_init()