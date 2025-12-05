r"""
Script 34: Zobraz celú _setup_ui metódu bez obmedzenia riadkov.
"""

from pathlib import Path

# Cesta k projektu
PROJECT_ROOT = Path("C:/Development/nex-automat")
TARGET_FILE = PROJECT_ROOT / "apps/supplier-invoice-editor/src/ui/widgets/invoice_list_widget.py"


def main():
    """Zobraz celú _setup_ui metódu."""
    print(f"Analyzujem: {TARGET_FILE}")
    print("=" * 70)

    if not TARGET_FILE.exists():
        print(f"❌ Súbor neexistuje: {TARGET_FILE}")
        return

    content = TARGET_FILE.read_text(encoding='utf-8')
    lines = content.splitlines()

    # Nájdi _setup_ui metódu
    in_setup_ui = False
    setup_ui_start = 0

    for i, line in enumerate(lines, 1):
        if 'def _setup_ui(self):' in line and i > 140:
            in_setup_ui = True
            setup_ui_start = i
            break

    if not in_setup_ui:
        print("❌ _setup_ui metóda nenájdená!")
        return

    print(f"_setup_ui začína na riadku {setup_ui_start}")
    print("-" * 70)

    # Zobraz až do ďalšej metódy (bez obmedzenia)
    line_count = 0
    for i in range(setup_ui_start - 1, len(lines)):
        line = lines[i]

        # Koniec metódy = ďalšia metóda na úrovni triedy
        if i > setup_ui_start and line.strip().startswith('def '):
            print(f"\n... koniec _setup_ui na riadku {i}")
            break

        print(f"  {i + 1:4d}: {line}")
        line_count += 1

        # Safety limit
        if line_count > 100:
            print("\n... (zobrazených prvých 100 riadkov)")
            break

    print("\n" + "=" * 70)
    print("Hľadám kľúčové časti ktoré MUSIA byť:")
    print("-" * 70)

    # Hľadaj v celom súbore
    found_quick_search = False
    found_add_widget = False

    for i, line in enumerate(lines, 1):
        if i >= setup_ui_start and 'QuickSearchContainer' in line:
            print(f"  ✅ {i:4d}: QuickSearchContainer nájdené")
            found_quick_search = True

        if i >= setup_ui_start and 'layout.addWidget' in line and i < setup_ui_start + 100:
            print(f"  ✅ {i:4d}: {line.strip()}")
            found_add_widget = True

    if not found_quick_search:
        print("  ❌ QuickSearchContainer nie je v _setup_ui!")

    if not found_add_widget:
        print("  ❌ layout.addWidget nie je v _setup_ui!")


if __name__ == "__main__":
    main()