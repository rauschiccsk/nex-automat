"""
Script 20: Properly add ProductMatcher to main.py
Add import, global variable, and startup initialization
"""

from pathlib import Path


def main():
    """Add ProductMatcher properly to main.py"""

    dev_root = Path(r"C:\Development\nex-automat")
    main_py = dev_root / "apps" / "supplier-invoice-loader" / "main.py"

    if not main_py.exists():
        print(f"❌ File not found: {main_py}")
        return False

    print(f"📝 Reading: {main_py}")
    content = main_py.read_text(encoding='utf-8')

    # Check if already added
    if 'from src.business.product_matcher import ProductMatcher' in content:
        print("⚠️  ProductMatcher import already exists")
    else:
        # Add import after other src.business imports
        import_location = 'from src.api import models'
        new_import = '''from src.api import models
from src.business.product_matcher import ProductMatcher'''
        content = content.replace(import_location, new_import)
        print("✅ Added ProductMatcher import")

    # Check for global variable
    if 'product_matcher: Optional[ProductMatcher] = None' in content:
        print("⚠️  Global product_matcher already exists")
    else:
        # Add after app creation
        app_location = 'app = FastAPI('
        # Find the end of app = FastAPI(...) block
        lines = content.split('\n')
        new_lines = []
        app_found = False
        added = False

        for i, line in enumerate(lines):
            new_lines.append(line)

            if 'app = FastAPI(' in line and not added:
                app_found = True

            # Add after the closing ) of FastAPI
            if app_found and ')' in line and 'FastAPI' not in line and not added:
                new_lines.append('')
                new_lines.append('# Global ProductMatcher instance')
                new_lines.append('product_matcher: Optional[ProductMatcher] = None')
                added = True
                print("✅ Added global product_matcher variable")

        content = '\n'.join(new_lines)

    # Add ProductMatcher initialization in startup_event
    if 'product_matcher = ProductMatcher' in content:
        print("⚠️  ProductMatcher initialization already in startup_event")
    else:
        # Find startup_event and add ProductMatcher init
        startup_marker = '    print("=" * 60)\n\n\n@app.on_event("shutdown")'

        if startup_marker in content:
            productmatcher_init = '''    print("=" * 60)

    # Initialize ProductMatcher if NEX Genesis is enabled
    global product_matcher
    if config.NEX_GENESIS_ENABLED:
        try:
            product_matcher = ProductMatcher(config.NEX_DATA_PATH)
            print(f"✅ ProductMatcher initialized: {config.NEX_DATA_PATH}")
        except Exception as e:
            print(f"❌ Failed to initialize ProductMatcher: {e}")
            product_matcher = None
    else:
        print("⚠️  NEX Genesis enrichment disabled")


@app.on_event("shutdown")'''

            content = content.replace(startup_marker, productmatcher_init)
            print("✅ Added ProductMatcher initialization to startup_event")
        else:
            print("❌ Could not find startup_event marker")
            return False

    # Write modified content
    print(f"💾 Writing modified file...")
    main_py.write_text(content, encoding='utf-8')

    print("✅ SUCCESS: ProductMatcher properly added to main.py")

    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)