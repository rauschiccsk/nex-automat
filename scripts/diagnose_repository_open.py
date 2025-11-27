#!/usr/bin/env python3
"""
Show BaseRepository.open() method
"""

from pathlib import Path

TARGET_FILE = Path("packages/nexdata/nexdata/repositories/base_repository.py")


def show_open_method():
    if not TARGET_FILE.exists():
        print(f"❌ File not found: {TARGET_FILE}")
        return

    content = TARGET_FILE.read_text(encoding='utf-8')
    lines = content.split('\n')

    # Find open method
    in_method = False
    method_lines = []

    for i, line in enumerate(lines, 1):
        if 'def open(self)' in line:
            in_method = True
            print(f"Found open() at line {i}")
            print()

        if in_method:
            method_lines.append((i, line))

            # Check if we left the method
            if line.strip().startswith('def ') and i > method_lines[0][0]:
                break

    print("open() method content:")
    print("=" * 70)
    for line_num, line_content in method_lines:
        print(f"{line_num:3d}: {line_content}")
    print("=" * 70)


if __name__ == "__main__":
    show_open_method()