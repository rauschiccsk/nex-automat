#!/usr/bin/env python3
"""
Script 04: Check logger configuration in base_window.py
Overí nastavenie loggera a zmení DEBUG logy na print()
"""

from pathlib import Path
import re


def check_and_fix_logging():
    """Skontroluje logger config a zmení DEBUG na print() pre istotu"""

    base_window_path = Path("packages/nex-shared/ui/base_window.py")

    if not base_window_path.exists():
        print(f"❌ File not found: {base_window_path}")
        return False

    content = base_window_path.read_text(encoding='utf-8')
    lines = content.split('\n')

    print("=" * 80)
    print("LOGGER CONFIGURATION CHECK")
    print("=" * 80)

    # Hľadaj logger definíciu
    for i, line in enumerate(lines[:50], 1):  # Prvých 50 riadkov
        if 'logger' in line.lower() and ('getLogger' in line or 'Logger' in line):
            print(f"{i:4d}: {line}")

    print("\n" + "=" * 80)
    print("CHANGING logger.debug() to print() for visibility")
    print("=" * 80)

    # Zmeň všetky logger.debug na print s prefixom
    content = re.sub(
        r'logger\.debug\(f"🔍 ([^"]+)"\)',
        r'print(f"🔍 DEBUG: \1")',
        content
    )

    # Aj pre prípad iného formátovania
    content = re.sub(
        r'logger\.debug\(f\'🔍 ([^\']+)\'\)',
        r'print(f"🔍 DEBUG: \1")',
        content
    )

    base_window_path.write_text(content, encoding='utf-8')

    print("✅ Changed logger.debug() to print() for DEBUG messages")
    print("\n📝 Count of changes:")

    # Spočítaj počet DEBUG printov
    debug_count = content.count('print(f"🔍 DEBUG:')
    print(f"   Total DEBUG prints: {debug_count}")

    return True


if __name__ == "__main__":
    success = check_and_fix_logging()
    if success:
        print("\n" + "=" * 80)
        print("NEXT: Test again")
        print("=" * 80)
        print("cd apps/supplier-invoice-editor")
        print("python main.py")
        print("→ Teraz by sa mali DEBUG správy zobrazovať v console!")