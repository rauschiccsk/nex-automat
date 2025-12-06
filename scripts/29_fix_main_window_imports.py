"""
Odstráni staré window_settings imports z main_window.py
"""
from pathlib import Path

MAIN_WINDOW_PATH = Path("apps/supplier-invoice-editor/src/ui/main_window.py")


def main():
    print("=" * 80)
    print("FIX: main_window.py imports")
    print("=" * 80)

    # Načítaj súbor
    with open(MAIN_WINDOW_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Odstráň import window_settings funkcií
    new_lines = []

    for i, line in enumerate(lines):
        # Ak je to import load_window_settings, save_window_settings
        if 'from utils.window_settings import' in line and (
                'load_window_settings' in line or 'save_window_settings' in line):
            print(f"✅ Odstránený riadok {i + 1}: {line.strip()}")
            continue

        new_lines.append(line)

    # Ulož súbor
    with open(MAIN_WINDOW_PATH, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

    print(f"\n✅ Súbor opravený: {MAIN_WINDOW_PATH}")

    print("\n" + "=" * 80)
    print("TEST:")
    print("=" * 80)
    print("python main.py")
    print("  → Ak ModuleNotFoundError 'nex_shared', pridám sys.path fix")
    print("=" * 80)


if __name__ == '__main__':
    main()