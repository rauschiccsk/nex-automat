#!/usr/bin/env python3
"""
Script 18: Remove DEBUG logs from base_window.py
Odstráni všetky DEBUG print() volania
"""

from pathlib import Path


def remove_debug_logs():
    """Odstráni všetky DEBUG printy z base_window.py"""

    base_window_path = Path("packages/nex-shared/ui/base_window.py")

    if not base_window_path.exists():
        print(f"❌ File not found: {base_window_path}")
        return False

    content = base_window_path.read_text(encoding='utf-8')
    lines = content.split('\n')

    print("=" * 80)
    print("REMOVING DEBUG LOGS")
    print("=" * 80)

    # Nájdi všetky DEBUG riadky
    debug_lines = []
    for i, line in enumerate(lines, 1):
        if '🔍 DEBUG:' in line and 'print(' in line:
            debug_lines.append((i, line.strip()))

    print(f"Found {len(debug_lines)} DEBUG print statements:")
    for i, line in debug_lines:
        print(f"  {i:4d}: {line[:80]}")

    # Odstráň DEBUG riadky
    new_lines = []
    removed_count = 0

    for line in lines:
        if '🔍 DEBUG:' in line and 'print(' in line:
            removed_count += 1
            continue
        new_lines.append(line)

    # Ulož súbor
    content = '\n'.join(new_lines)
    base_window_path.write_text(content, encoding='utf-8')

    print(f"\n✅ Removed {removed_count} DEBUG print statements")

    return True


if __name__ == "__main__":
    success = remove_debug_logs()
    if success:
        print("\n" + "=" * 80)
        print("FINAL TEST")
        print("=" * 80)
        print("cd apps/supplier-invoice-editor")
        print("python main.py")
        print("\n→ Console by mal byť ČISTÝ (bez 🔍 DEBUG logov)")