"""
Script 01: Check BaseWindow implementation in nex-shared

Načíta BaseWindow z nex-shared aby sme videli ako funguje window persistence.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "packages" / "nex-shared"))


def main():
    print("=" * 80)
    print("CHECKING BaseWindow IN NEX-SHARED")
    print("=" * 80)

    # Check if nex-shared exists
    nex_shared_path = project_root / "packages" / "nex-shared"
    print(f"\n1. Checking nex-shared path: {nex_shared_path}")
    print(f"   Exists: {nex_shared_path.exists()}")

    if not nex_shared_path.exists():
        print("   ERROR: nex-shared package not found!")
        return

    # List nex-shared structure
    print("\n2. nex-shared structure:")
    for item in sorted(nex_shared_path.rglob("*.py")):
        rel_path = item.relative_to(nex_shared_path)
        print(f"   {rel_path}")

    # Try to import BaseWindow
    print("\n3. Trying to import BaseWindow...")
    try:
        from nex_shared.ui import BaseWindow
        print("   ✓ BaseWindow imported successfully")

        # Inspect BaseWindow
        print("\n4. BaseWindow inspection:")
        print(f"   Module: {BaseWindow.__module__}")
        print(f"   File: {BaseWindow.__init__.__code__.co_filename}")

        # Get __init__ signature
        import inspect
        sig = inspect.signature(BaseWindow.__init__)
        print(f"   __init__ signature: {sig}")

        # List methods
        print("\n5. BaseWindow methods:")
        for name in dir(BaseWindow):
            if not name.startswith('_'):
                attr = getattr(BaseWindow, name)
                if callable(attr):
                    print(f"   - {name}")

        # Read BaseWindow source
        print("\n6. Reading BaseWindow source code...")
        source_file = Path(BaseWindow.__init__.__code__.co_filename)
        if source_file.exists():
            print(f"   Source file: {source_file}")
            print("\n" + "=" * 80)
            print("SOURCE CODE:")
            print("=" * 80)
            with open(source_file, 'r', encoding='utf-8') as f:
                content = f.read()
                print(content)

    except ImportError as e:
        print(f"   ✗ Failed to import BaseWindow: {e}")

        # Try to locate base_window.py manually
        print("\n   Searching for base_window.py...")
        for item in nex_shared_path.rglob("*base*window*.py"):
            print(f"   Found: {item}")

    print("\n" + "=" * 80)
    print("CHECK COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()