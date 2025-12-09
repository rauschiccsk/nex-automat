"""
Script 09: Fix Unicode Issues in main.py
=========================================

Purpose: Remove emojis from main.py startup event handler

Usage:
    python scripts/09_fix_unicode_main.py
"""

from pathlib import Path


def main():
    main_py_path = Path("C:/Development/nex-automat/apps/supplier-invoice-loader/main.py")

    if not main_py_path.exists():
        print(f"[ERROR] File not found: {main_py_path}")
        return

    print("=" * 70)
    print("FIXING main.py - REMOVE EMOJI UNICODE")
    print("=" * 70)

    # Read current file
    with open(main_py_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Show the problematic lines (around 556, 576, 578, 584)
    print("\n[DEBUG] Checking lines around startup event handler...")

    modified = False
    for i, line in enumerate(lines, 1):
        # Check for emoji Unicode characters in print statements
        if 'print(f"' in line and any(emoji in line for emoji in ['✅', '❌', '🔍', '🚀']):
            print(f"[FOUND] Line {i}: {line.strip()[:60]}...")

            # Replace emojis
            new_line = line
            new_line = new_line.replace('✅', '[OK]')
            new_line = new_line.replace('❌', '[ERROR]')
            new_line = new_line.replace('🔍', '[SEARCH]')
            new_line = new_line.replace('🚀', '[ROCKET]')

            if new_line != line:
                lines[i - 1] = new_line
                modified = True
                print(f"[FIXED] Line {i}: {new_line.strip()[:60]}...")

    if modified:
        # Write back
        with open(main_py_path, 'w', encoding='utf-8', newline='') as f:
            f.writelines(lines)

        print(f"\n[OK] File updated: {main_py_path}")
    else:
        print("\n[INFO] No emoji characters found")

    print("\n[NEXT] Run test again")


if __name__ == "__main__":
    main()