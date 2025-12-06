#!/usr/bin/env python3
"""
Script 17: Fix InvoiceService syntax error
Properly reconstruct __init__ method without config
"""

from pathlib import Path
import re

# Target file
INVOICE_SERVICE = Path("apps/supplier-invoice-editor/src/business/invoice_service.py")


def fix_invoice_service_init():
    """Fix InvoiceService __init__ method"""
    if not INVOICE_SERVICE.exists():
        print(f"❌ ERROR: File not found: {INVOICE_SERVICE}")
        return False

    content = INVOICE_SERVICE.read_text(encoding='utf-8')

    # Find __init__ method and replace
    init_pattern = r'def __init__\(self\):.*?(?=\n    def |\Z)'

    # Replacement __init__ without config
    new_init = '''def __init__(self):
        self.logger = logging.getLogger(__name__)
        # Try to initialize PostgreSQL client
        self.db_client = None
        self._init_database()'''

    # Replace __init__ method
    content = re.sub(init_pattern, new_init, content, flags=re.DOTALL)

    # Write fixed content
    INVOICE_SERVICE.write_text(content, encoding='utf-8')

    return True


def main():
    """Fix InvoiceService syntax"""
    print("=" * 60)
    print("Fixing InvoiceService syntax error")
    print("=" * 60)

    if not fix_invoice_service_init():
        return False

    print("\n✅ Fixed: InvoiceService __init__ method")

    # Verify syntax
    content = INVOICE_SERVICE.read_text(encoding='utf-8')
    try:
        compile(content, str(INVOICE_SERVICE), 'exec')
        print("✅ Python syntax valid")
    except SyntaxError as e:
        print(f"❌ Syntax error at line {e.lineno}: {e.msg}")
        if e.text:
            print(f"   {e.text.strip()}")
        return False

    print("\n" + "=" * 60)
    print("ÚSPECH: InvoiceService syntax fixed")
    print("=" * 60)
    print("\nNext step: Test application")
    print("cd apps/supplier-invoice-editor")
    print("python main.py")

    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)