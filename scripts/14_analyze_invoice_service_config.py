#!/usr/bin/env python3
"""
Script 14: Analyze InvoiceService config requirements
Find what config attributes InvoiceService needs
"""

from pathlib import Path
import re

# Target file
INVOICE_SERVICE = Path("apps/supplier-invoice-editor/src/business/invoice_service.py")


def find_config_usages(content: str) -> list:
    """Find all config.xxx usages"""
    # Find patterns like config.xxx or self.config.xxx
    pattern = r'(?:self\.)?config\.[a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)*'
    matches = re.findall(pattern, content)
    return sorted(set(matches))


def main():
    """Analyze config usage in InvoiceService"""
    print("=" * 60)
    print("Analyzing InvoiceService config requirements")
    print("=" * 60)

    if not INVOICE_SERVICE.exists():
        print(f"❌ ERROR: File not found: {INVOICE_SERVICE}")
        return False

    # Read content
    content = INVOICE_SERVICE.read_text(encoding='utf-8')

    # Find config usages
    usages = find_config_usages(content)

    if not usages:
        print("\n⚠️  No config.xxx usages found")
    else:
        print(f"\n📝 Found {len(usages)} config attribute usages:")
        for usage in usages:
            print(f"   - {usage}")

    # Find __init__ method
    init_start = content.find('def __init__')
    if init_start != -1:
        init_end = content.find('\n    def ', init_start + 1)
        if init_end == -1:
            init_end = len(content)

        init_method = content[init_start:init_end]
        print("\n📋 __init__ method:")
        lines = init_method.split('\n')
        for line in lines:
            print(f"   {line}")

    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE")
    print("=" * 60)

    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)