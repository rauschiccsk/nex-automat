"""
Pridá sys.path fix do ui/__init__.py PRED import main_window
"""
from pathlib import Path

UI_INIT_PATH = Path("apps/supplier-invoice-editor/src/ui/__init__.py")


def main():
    print("=" * 80)
    print("PRIDANIE sys.path FIX DO ui/__init__.py")
    print("=" * 80)

    # Načítaj súbor
    with open(UI_INIT_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Skontroluj či už sys.path fix existuje
    has_fix = any('nex-shared' in line for line in lines)

    if has_fix:
        print("⏭️  sys.path fix už existuje")
        return

    # Nová implementácia s sys.path fix
    new_content = '''"""UI package"""
import sys
from pathlib import Path

# Add nex-shared to path BEFORE any imports
nex_shared_path = Path(__file__).parent.parent.parent.parent / "packages" / "nex-shared"
if str(nex_shared_path) not in sys.path:
    sys.path.insert(0, str(nex_shared_path))

from .main_window import MainWindow

__all__ = ['MainWindow']
'''

    # Zapíš nový súbor
    with open(UI_INIT_PATH, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"✅ Súbor prepísaný: {UI_INIT_PATH}")
    print("\nNový obsah:")
    print(new_content)

    print("\n" + "=" * 80)
    print("FINÁLNY TEST:")
    print("=" * 80)
    print("cd apps\\supplier-invoice-editor")
    print("python main.py")
    print("  → MUSÍ sa spustiť! ✅")
    print("  → Maximize + Close + Run again")
    print("  → MUSÍ byť maximalized! ✅✅✅")
    print("=" * 80)


if __name__ == '__main__':
    main()
