r"""
Script 25: Skontroluje či sú signály sectionResized a sectionMoved pripojené.
"""

from pathlib import Path

# Cesta k projektu
PROJECT_ROOT = Path("C:/Development/nex-automat")
TARGET_FILE = PROJECT_ROOT / "apps/supplier-invoice-editor/src/ui/widgets/invoice_list_widget.py"


def main():
    """Skontroluje pripojenie signálov."""
    print(f"Analyzujem: {TARGET_FILE}")
    print("=" * 70)

    if not TARGET_FILE.exists():
        print(f"❌ Súbor neexistuje: {TARGET_FILE}")
        return

    content = TARGET_FILE.read_text(encoding='utf-8')
    lines = content.splitlines()

    # 1. Hľadaj _setup_ui metódu
    print("\n1. _setup_ui METÓDA:")
    print("-" * 70)

    in_setup_ui = False
    setup_ui_start = 0

    for i, line in enumerate(lines, 1):
        if 'def _setup_ui(self):' in line:
            in_setup_ui = True
            setup_ui_start = i
            print(f"✅ Nájdená na riadku {i}")
            break

    if not in_setup_ui:
        print("❌ _setup_ui() nenájdená!")
        return

    # 2. Hľadaj pripojenie signálov v _setup_ui
    print("\n2. PRIPOJENIE SIGNÁLOV v _setup_ui:")
    print("-" * 70)

    found_resized = False
    found_moved = False

    for i in range(setup_ui_start, len(lines)):
        line = lines[i]

        # Koniec _setup_ui = ďalšia metóda
        if i > setup_ui_start and line.strip().startswith('def '):
            break

        if 'sectionResized.connect' in line:
            print(f"  ✅ {i + 1:4d}: {line.strip()}")
            found_resized = True

        if 'sectionMoved.connect' in line:
            print(f"  ✅ {i + 1:4d}: {line.strip()}")
            found_moved = True

    if not found_resized:
        print("  ❌ sectionResized.connect CHÝBA!")
    if not found_moved:
        print("  ❌ sectionMoved.connect CHÝBA!")

    # 3. Hľadaj handlery
    print("\n3. HANDLERY:")
    print("-" * 70)

    has_on_resized = False
    has_on_moved = False

    for i, line in enumerate(lines, 1):
        if 'def _on_column_resized' in line:
            print(f"  ✅ {i:4d}: {line.strip()}")
            has_on_resized = True

        if 'def _on_column_moved' in line:
            print(f"  ✅ {i:4d}: {line.strip()}")
            has_on_moved = True

    if not has_on_resized:
        print("  ❌ _on_column_resized() CHÝBA!")
    if not has_on_moved:
        print("  ❌ _on_column_moved() CHÝBA!")

    # 4. Hľadaj _save_grid_settings
    print("\n4. _save_grid_settings METÓDA:")
    print("-" * 70)

    has_save = False
    for i, line in enumerate(lines, 1):
        if 'def _save_grid_settings' in line:
            print(f"  ✅ {i:4d}: {line.strip()}")
            has_save = True
            break

    if not has_save:
        print("  ❌ _save_grid_settings() CHÝBA!")

    # 5. Hľadaj _load_grid_settings
    print("\n5. _load_grid_settings METÓDA:")
    print("-" * 70)

    has_load = False
    for i, line in enumerate(lines, 1):
        if 'def _load_grid_settings' in line:
            print(f"  ✅ {i:4d}: {line.strip()}")
            has_load = True
            break

    if not has_load:
        print("  ❌ _load_grid_settings() CHÝBA!")

    # 6. Hľadaj volanie _load_grid_settings v __init__
    print("\n6. VOLANIE _load_grid_settings v __init__:")
    print("-" * 70)

    has_call = False
    for i, line in enumerate(lines, 1):
        if 'self._load_grid_settings()' in line and i < 200:  # V __init__ cca do riadku 200
            print(f"  ✅ {i:4d}: {line.strip()}")
            has_call = True

    if not has_call:
        print("  ❌ self._load_grid_settings() sa NEVOLÁ v __init__!")

    # Záver
    print("\n" + "=" * 70)
    print("ZÁVER:")
    print("=" * 70)

    if found_resized and found_moved and has_on_resized and has_on_moved and has_save:
        print("✅ Signály a handlery sú OK")
        print("⚠️  Problém je pravdepodobne inde - možno sa handlery nevolajú")
    else:
        print("❌ PROBLÉM NÁJDENÝ:")
        if not found_resized:
            print("  - sectionResized.connect nie je pripojené")
        if not found_moved:
            print("  - sectionMoved.connect nie je pripojené")
        if not has_on_resized:
            print("  - Handler _on_column_resized() chýba")
        if not has_on_moved:
            print("  - Handler _on_column_moved() chýba")
        if not has_save:
            print("  - Metóda _save_grid_settings() chýba")


if __name__ == "__main__":
    main()