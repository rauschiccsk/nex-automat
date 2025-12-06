"""
Diagnostika BaseWindow importu
"""
import sys
from pathlib import Path

# Add nex-shared to path
nex_shared_path = Path(__file__).parent.parent / 'packages' / 'nex-shared'
sys.path.insert(0, str(nex_shared_path))


def main():
    print("=" * 80)
    print("DIAGNOSTIKA BASEWINDOW IMPORT")
    print("=" * 80)

    print(f"\n1. nex-shared path: {nex_shared_path}")
    print(f"   Existuje: {nex_shared_path.exists()}")

    print(f"\n2. sys.path (prvých 5):")
    for i, p in enumerate(sys.path[:5]):
        print(f"   {i}: {p}")

    print(f"\n3. ui/base_window.py:")
    base_window_path = nex_shared_path / 'ui' / 'base_window.py'
    print(f"   Path: {base_window_path}")
    print(f"   Existuje: {base_window_path.exists()}")

    if base_window_path.exists():
        with open(base_window_path, 'r') as f:
            lines = f.readlines()
        print(f"   Riadkov: {len(lines)}")

        # Nájdi class BaseWindow
        for i, line in enumerate(lines):
            if 'class BaseWindow' in line:
                print(f"   class BaseWindow nájdená na riadku {i + 1}: {line.strip()}")
                break

    print(f"\n4. Test importu:")
    try:
        from ui.base_window import BaseWindow
        print(f"   ✅ Import úspešný")
        print(f"   BaseWindow: {BaseWindow}")
        print(f"   __init__ signature: {BaseWindow.__init__.__code__.co_varnames[:10]}")
    except Exception as e:
        print(f"   ❌ Import zlyhal: {e}")
        import traceback
        traceback.print_exc()

    print(f"\n5. main_window.py class definition:")
    main_window_path = Path('apps/supplier-invoice-editor/src/ui/main_window.py')
    if main_window_path.exists():
        with open(main_window_path, 'r') as f:
            lines = f.readlines()

        for i, line in enumerate(lines):
            if 'class MainWindow' in line:
                print(f"   Riadok {i + 1}: {line.strip()}")
                # Zobraz aj import
                for j in range(max(0, i - 20), i):
                    if 'BaseWindow' in lines[j]:
                        print(f"   Import {j + 1}: {lines[j].strip()}")
                break

    print("\n" + "=" * 80)


if __name__ == '__main__':
    main()