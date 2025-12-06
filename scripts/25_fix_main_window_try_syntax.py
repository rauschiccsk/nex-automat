#!/usr/bin/env python3
"""
Script 25: Fix MainWindow try block syntax
Properly reconstruct __init__ with config
"""

from pathlib import Path
import re

# Target file
MAIN_WINDOW = Path("apps/supplier-invoice-editor/src/ui/main_window.py")


def fix_main_window_init():
    """Fix MainWindow __init__ properly"""
    if not MAIN_WINDOW.exists():
        print(f"❌ ERROR: File not found: {MAIN_WINDOW}")
        return False

    content = MAIN_WINDOW.read_text(encoding='utf-8')

    # Find current broken __init__
    init_start = content.find('def __init__(self, config, parent=None):')
    if init_start == -1:
        print("⚠️  __init__ not found")
        return False

    # Find end of __init__ (next method or end)
    init_end = content.find('\n    def ', init_start + 1)
    if init_end == -1:
        init_end = len(content)

    # Extract parts before and after __init__
    before_init = content[:init_start]
    after_init = content[init_end:]

    # Create correct __init__
    correct_init = '''def __init__(self, config, parent=None):
        super().__init__(
            window_name=WINDOW_MAIN,
            default_size=(1400, 900),
            default_pos=(100, 100)
        )
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.invoice_service = InvoiceService(config)

        self._setup_ui()
        self._create_menu_bar()
        self._create_toolbar()
        self._create_status_bar()
        self._connect_signals()

        # Load initial data
        QTimer.singleShot(0, self._load_invoices)
'''

    # Reconstruct file
    new_content = before_init + correct_init + after_init

    # Write
    MAIN_WINDOW.write_text(new_content, encoding='utf-8')

    return True


def main():
    """Fix MainWindow syntax"""
    print("=" * 60)
    print("Fixing MainWindow try block syntax")
    print("=" * 60)

    if not fix_main_window_init():
        return False

    print("\n✅ Fixed: MainWindow __init__ method")

    # Verify syntax
    content = MAIN_WINDOW.read_text(encoding='utf-8')
    try:
        compile(content, str(MAIN_WINDOW), 'exec')
        print("✅ Python syntax valid")
    except SyntaxError as e:
        print(f"❌ Syntax error at line {e.lineno}: {e.msg}")
        if e.text:
            print(f"   {e.text.strip()}")
        return False

    print("\n" + "=" * 60)
    print("ÚSPECH: MainWindow syntax fixed")
    print("=" * 60)
    print("\nNext step: Test application")
    print("cd apps/supplier-invoice-editor")
    print("python main.py")

    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)