#!/usr/bin/env python3
"""
Script 20: Diagnose _init_database method
Find where self.config is used in InvoiceService
"""

from pathlib import Path
import re

# Target file
INVOICE_SERVICE = Path("apps/supplier-invoice-editor/src/business/invoice_service.py")


def find_init_database():
    """Find _init_database method"""
    if not INVOICE_SERVICE.exists():
        print(f"❌ ERROR: File not found: {INVOICE_SERVICE}")
        return False

    content = INVOICE_SERVICE.read_text(encoding='utf-8')

    # Find _init_database method
    pattern = r'def _init_database\(self\):.*?(?=\n    def |\Z)'
    match = re.search(pattern, content, re.DOTALL)

    if match:
        print("\n📝 _init_database method:")
        lines = match.group(0).split('\n')
        for i, line in enumerate(lines, 1):
            print(f"   {i:3d}: {line}")
    else:
        print("\n⚠️  _init_database method not found")

    # Find all self.config usages in the file
    config_usages = re.findall(r'self\.config\.[a-zA-Z_][a-zA-Z0-9_.]*', content)
    if config_usages:
        print(f"\n⚠️  Found {len(config_usages)} self.config usages:")
        for usage in sorted(set(config_usages)):
            print(f"   - {usage}")

    return True


def main():
    """Diagnose _init_database"""
    print("=" * 60)
    print("Diagnosing _init_database method")
    print("=" * 60)

    find_init_database()

    print("\n" + "=" * 60)
    print("DIAGNOSIS COMPLETE")
    print("=" * 60)

    return True


if __name__ == "__main__":
    main()