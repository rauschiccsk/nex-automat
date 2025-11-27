#!/usr/bin/env python3
"""
Show complete open_file method
"""

from pathlib import Path

TARGET_FILE = Path("packages/nexdata/nexdata/btrieve/btrieve_client.py")


def show_method():
    if not TARGET_FILE.exists():
        print(f"❌ File not found: {TARGET_FILE}")
        return

    content = TARGET_FILE.read_text(encoding='utf-8')
    lines = content.split('\n')

    # Find open_file method
    in_method = False
    method_lines = []

    for i, line in enumerate(lines, 1):
        if 'def open_file(self, filename: str' in line:
            in_method = True
            print(f"Found open_file() at line {i}")
            print()

        if in_method:
            method_lines.append((i, line))

            # Check if we left the method (next def at same indent)
            if i > method_lines[0][0] and line.strip().startswith('def '):
                current_indent = len(line) - len(line.lstrip())
                start_indent = len(method_lines[0][1]) - len(method_lines[0][1].lstrip())
                if current_indent <= start_indent:
                    break

    print("open_file() method content:")
    print("=" * 70)
    for line_num, line_content in method_lines:
        print(f"{line_num:3d}: {line_content}")
    print("=" * 70)


if __name__ == "__main__":
    show_method()