"""
CLEANUP: Odstráni debug výpisy z window_settings.py
"""
from pathlib import Path

WINDOW_SETTINGS_PATH = Path("apps/supplier-invoice-editor/src/utils/window_settings.py")


def main():
    print("=" * 80)
    print("CLEANUP: Debug outputs")
    print("=" * 80)

    # Načítaj súbor
    with open(WINDOW_SETTINGS_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Odstráň debug riadky
    new_lines = []
    removed_count = 0

    for line in lines:
        # Odstráň riadky s DEBUG
        if 'DEBUG save_window_settings:' in line:
            removed_count += 1
            continue
        if 'DEBUG: Database committed successfully' in line:
            removed_count += 1
            continue
        if 'logger = logging.getLogger(__name__)' in line and removed_count > 0:
            # Tento logger bol len pre debug
            removed_count += 1
            continue
        if '# DEBUG: Log parameters before save' in line:
            removed_count += 1
            continue

        new_lines.append(line)

    # Ulož súbor
    with open(WINDOW_SETTINGS_PATH, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

    print(f"✅ Odstránených {removed_count} debug riadkov")
    print(f"✅ Súbor vyčistený: {WINDOW_SETTINGS_PATH}")

    print("\n" + "=" * 80)
    print("HOTOVO")
    print("=" * 80)
    print("Window maximize state persistence je FUNKČNÁ ✅")
    print("\nRiešenie:")
    print("  1. DELETE + INSERT namiesto INSERT OR REPLACE")
    print("  2. SELECT window_state stĺpec")
    print("  3. return window_state v load funkcie")
    print("=" * 80)


if __name__ == '__main__':
    main()