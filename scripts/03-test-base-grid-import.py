"""
Script 03: Test BaseGrid import from nex-shared

Otestuje či BaseGrid funguje správne.

Spustenie:
    python scripts\03-test-base-grid-import.py
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "packages" / "nex-shared"))

def main():
    print("=" * 80)
    print("TESTING BaseGrid IMPORT")
    print("=" * 80)

    # Test import
    print("\n1. Testing import...")
    try:
        from nex_shared.ui import BaseGrid, GreenHeaderView
        print("   ✓ BaseGrid imported successfully")
        print("   ✓ GreenHeaderView imported successfully")
    except ImportError as e:
        print(f"   ✗ Import failed: {e}")
        return

    # Inspect BaseGrid
    print("\n2. BaseGrid inspection:")
    print(f"   Module: {BaseGrid.__module__}")
    print(f"   Base classes: {[c.__name__ for c in BaseGrid.__mro__]}")

    # Check __init__ signature
    import inspect
    sig = inspect.signature(BaseGrid.__init__)
    print(f"   __init__ signature: {sig}")

    # List public methods
    print("\n3. BaseGrid public methods:")
    for name in dir(BaseGrid):
        if not name.startswith('_') and name not in dir(object):
            attr = getattr(BaseGrid, name)
            if callable(attr):
                print(f"   - {name}")

    # Check GreenHeaderView
    print("\n4. GreenHeaderView inspection:")
    print(f"   Module: {GreenHeaderView.__module__}")
    print(f"   Base classes: {[c.__name__ for c in GreenHeaderView.__mro__]}")

    # List methods
    print("\n5. GreenHeaderView public methods:")
    for name in dir(GreenHeaderView):
        if not name.startswith('_') and name not in dir(object):
            attr = getattr(GreenHeaderView, name)
            if callable(attr):
                try:
                    sig = inspect.signature(attr)
                    print(f"   - {name}{sig}")
                except:
                    print(f"   - {name}")

    print("\n" + "=" * 80)
    print("TEST COMPLETE - BaseGrid READY TO USE")
    print("=" * 80)
    print("\nNext step: Refactor invoice_list_widget.py to use BaseGrid")
    print("  python scripts\\04-refactor-invoice-list-widget.py")

if __name__ == "__main__":
    main()