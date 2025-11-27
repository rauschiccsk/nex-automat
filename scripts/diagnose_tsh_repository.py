#!/usr/bin/env python3
"""
Diagnose TSH repository structure
"""

from pathlib import Path

TARGET_FILE = Path("packages/nexdata/nexdata/repositories/tsh_repository.py")


def diagnose():
    if not TARGET_FILE.exists():
        print(f"❌ File not found: {TARGET_FILE}")
        return

    content = TARGET_FILE.read_text(encoding='utf-8')
    lines = content.split('\n')

    print(f"Total lines: {len(lines)}")
    print()
    print("File content:")
    print("=" * 70)

    for i, line in enumerate(lines, 1):
        print(f"{i:3d}: {line}")

    print("=" * 70)


if __name__ == "__main__":
    diagnose()