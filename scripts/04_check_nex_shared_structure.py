"""
Check: Zobrazí štruktúru nex-shared package
Location: C:\Development\nex-automat\scripts\04_check_nex_shared_structure.py
"""
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).parent
DEV_ROOT = SCRIPT_DIR.parent
NEX_SHARED = DEV_ROOT / "packages" / "nex-shared"


def show_structure():
    """Zobraz štruktúru nex-shared package"""

    print("=" * 80)
    print("NEX-SHARED PACKAGE ŠTRUKTÚRA")
    print("=" * 80)

    if not NEX_SHARED.exists():
        print(f"\n❌ Adresár neexistuje: {NEX_SHARED}")
        return

    print(f"\nRoot: {NEX_SHARED.relative_to(DEV_ROOT)}\n")

    # Zobraz štruktúru
    def print_tree(directory, prefix="", is_last=True):
        """Rekurzívne vypíše stromovú štruktúru"""
        items = sorted(directory.iterdir(), key=lambda x: (not x.is_dir(), x.name))

        # Filter out __pycache__
        items = [item for item in items if item.name != "__pycache__"]

        for i, item in enumerate(items):
            is_last_item = i == len(items) - 1

            # Prefix pre aktuálnu položku
            current_prefix = "└── " if is_last_item else "├── "
            print(f"{prefix}{current_prefix}{item.name}")

            # Ak je to adresár, rekurzívne zobraz obsah
            if item.is_dir():
                # Prefix pre children
                extension = "    " if is_last_item else "│   "
                print_tree(item, prefix + extension, is_last_item)

    print_tree(NEX_SHARED)

    print("\n" + "=" * 80)
    print("KONTROLA __init__.py SÚBOROV")
    print("=" * 80)

    # Find all __init__.py files
    init_files = list(NEX_SHARED.rglob("__init__.py"))

    if not init_files:
        print("\n❌ ŽIADNE __init__.py súbory!")
        return

    for init_file in sorted(init_files):
        rel_path = init_file.relative_to(NEX_SHARED)
        print(f"\n✓ {rel_path}")

        # Show content
        with open(init_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()

        if content:
            lines = content.split('\n')
            if len(lines) > 10:
                print(f"  ({len(lines)} lines)")
            else:
                for line in lines[:5]:
                    print(f"  {line}")
                if len(lines) > 5:
                    print(f"  ... ({len(lines) - 5} more lines)")
        else:
            print("  (prázdny)")

    print("\n" + "=" * 80)
    print("HOTOVO")
    print("=" * 80)


if __name__ == "__main__":
    show_structure()