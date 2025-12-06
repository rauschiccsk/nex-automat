#!/usr/bin/env python3
"""
Script 16: Fix MainWindow syntax error
Properly reconstruct __init__ method without config
"""

from pathlib import Path
import re

# Target file
MAIN_WINDOW = Path("apps/supplier-invoice-editor/src/ui/main_window.py")


def fix_main_window_init():
    """Fix MainWindow __init__ method"""
    if not MAIN_WINDOW.exists():
        print(f"❌ ERROR: File not found: {MAIN_WINDOW}")
        return False

    content = MAIN_WINDOW.read_text(encoding='utf-8')

    # Find __init__ method
    init_pattern = r'def __init__\(self[^)]*\):.*?(?=\n    def |\Z)'

    # Replacement __init__ without config
    new_init = '''def __init__(self, parent=None):
        super().__init__(
            window_name=WINDOW_MAIN,
            default_size=(1400, 900),
            default_pos=(100, 100)
        )
        self.logger = logging.getLogger(__name__)
        self.invoice_service = InvoiceService()

        self._setup_ui()
        self._create_menu_bar()
        self._create_toolbar()
        self._create_status_bar()
        self._connect_signals()

        # Load initial data
        QTimer.singleShot(0, self._load_invoices)'''

    # Replace __init__ method
    content = re.sub(init_pattern, new_init, content, flags=re.DOTALL)

    # Write fixed content
    MAIN_WINDOW.write_text(content, encoding='utf-8')

    return True


def main():
    """Fix MainWindow syntax"""
    print("=" * 60)
    print("Fixing MainWindow syntax error")
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