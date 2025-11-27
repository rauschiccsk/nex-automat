#!/usr/bin/env python3
"""
Diagnose syntax error in btrieve_client.py
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
    print("Lines around error (85-105):")
    print("=" * 70)

    for i in range(85, min(105, len(lines))):
        line = lines[i]
        marker = " <<<" if i == 95 else ""  # Line 96 (0-indexed = 95)
        print(f"{i + 1:3d}: {line}{marker}")

    print("=" * 70)


if __name__ == "__main__":
    diagnose()