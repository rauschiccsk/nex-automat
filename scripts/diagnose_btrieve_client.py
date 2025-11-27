#!/usr/bin/env python3
"""
Diagnose btrieve_client.py structure
"""

from pathlib import Path

TARGET_FILE = Path("packages/nexdata/nexdata/btrieve/btrieve_client.py")


def diagnose():
    if not TARGET_FILE.exists():
        print(f"❌ File not found: {TARGET_FILE}")
        return

    content = TARGET_FILE.read_text(encoding='utf-8')
    lines = content.split('\n')

    print(f"Total lines: {len(lines)}")
    print()
    print("Methods found:")
    print("=" * 70)

    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith('def '):
            print(f"Line {i:3d}: {line}")

    print()
    print("=" * 70)
    print()
    print("Looking for 'open' related methods:")
    for i, line in enumerate(lines, 1):
        if 'open' in line.lower() and 'def ' in line:
            print(f"Line {i:3d}: {line}")


if __name__ == "__main__":
    diagnose()