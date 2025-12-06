#!/usr/bin/env python3
"""
Script 28: Diagnose _load_invoices method
Show complete method to see where except/finally should be
"""

from pathlib import Path
import re

# Target file
MAIN_WINDOW = Path("apps/supplier-invoice-editor/src/ui/main_window.py")


def main():
    """Show _load_invoices method"""
    print("=" * 60)
    print("Diagnosing _load_invoices method")
    print("=" * 60)

    if not MAIN_WINDOW.exists():
        print(f"❌ ERROR: File not found: {MAIN_WINDOW}")
        return False

    content = MAIN_WINDOW.read_text(encoding='utf-8')

    # Find _load_invoices method
    pattern = r'def _load_invoices\(self\):.*?(?=\n    def |\Z)'
    match = re.search(pattern, content, re.DOTALL)

    if match:
        print("\n📝 _load_invoices method:")
        lines = match.group(0).split('\n')
        for i, line in enumerate(lines, 1):
            print(f"   {i:3d}: {line}")
    else:
        print("\n⚠️  _load_invoices method not found")

    print("\n" + "=" * 60)

    return True


if __name__ == "__main__":
    main()