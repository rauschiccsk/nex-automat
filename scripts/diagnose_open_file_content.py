#!/usr/bin/env python3
"""
Show content of open_file method
"""

from pathlib import Path

TARGET_FILE = Path("packages/nexdata/nexdata/btrieve/btrieve_client.py")


def diagnose():
    if not TARGET_FILE.exists():
        print(f"❌ File not found: {TARGET_FILE}")
        return

    content = TARGET_FILE.read_text(encoding='utf-8')
    lines = content.split('\n')

    # Find open_file method
    in_method = False
    method_lines = []
    indent_level = 0

    for i, line in enumerate(lines, 1):
        if 'def open_file(self, filename: str' in line:
            in_method = True
            indent_level = len(line) - len(line.lstrip())
            print(f"Found open_file at line {i}")
            print()

        if in_method:
            method_lines.append((i, line))

            # Check if we left the method (next def at same or lower indent)
            if line.strip().startswith('def ') and i > 161:
                current_indent = len(line) - len(line.lstrip())
                if current_indent <= indent_level:
                    break

    print("open_file method content:")
    print("=" * 70)
    for line_num, line_content in method_lines[:50]:  # First 50 lines
        print(f"{line_num:3d}: {line_content}")
    print("=" * 70)


if __name__ == "__main__":
    diagnose()