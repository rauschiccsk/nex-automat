r"""
Script 08: Pridanie chýbajúcich importov do main_window.py.

Problém: save_window_settings a WINDOW_MAIN nie sú importované.
"""

from pathlib import Path

# Cesta k projektu
PROJECT_ROOT = Path("C:/Development/nex-automat")
TARGET_FILE = PROJECT_ROOT / "apps/supplier-invoice-editor/src/ui/main_window.py"

def main():
    """Pridá chýbajúce importy do main_window.py."""
    print(f"Upravujem: {TARGET_FILE}")

    if not TARGET_FILE.exists():
        print(f"❌ Súbor neexistuje: {TARGET_FILE}")
        return

    # Načítaj súbor
    content = TARGET_FILE.read_text(encoding='utf-8')
    lines = content.splitlines()

    # Skontroluj či už importy existujú
    has_window_main = 'from utils.constants import WINDOW_MAIN' in content
    has_window_settings = 'from utils.window_settings import' in content

    if has_window_main and has_window_settings:
        print("✅ Importy už existujú")
        return

    # Nájdi kde sú quick_search importy a pridaj za ne
    new_lines = []
    added = False

    for i, line in enumerate(lines):
        new_lines.append(line)

        # Pridaj importy za quick_search import
        if 'from .widgets.quick_search import' in line and not added:
            if not has_window_main:
                new_lines.append('from utils.constants import WINDOW_MAIN')
            if not has_window_settings:
                new_lines.append('from utils.window_settings import load_window_settings, save_window_settings')
            added = True
            print(f"✅ Pridané importy na riadok {i+2}")

    # Zapíš späť
    content = '\n'.join(new_lines)
    TARGET_FILE.write_text(content, encoding='utf-8')

    print(f"✅ Súbor upravený: {TARGET_FILE}")
    print(f"   Celkom riadkov: {len(new_lines)}")
    print("\nPridané importy:")
    if not has_window_main:
        print("  ✅ from utils.constants import WINDOW_MAIN")
    if not has_window_settings:
        print("  ✅ from utils.window_settings import load_window_settings, save_window_settings")
    print("\nSkús spustiť aplikáciu znova")

if __name__ == "__main__":
    main()