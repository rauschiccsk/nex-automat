r"""
Script 09: Diagnostika main_window.py - zobrazí importy a closeEvent.
"""

from pathlib import Path

# Cesta k projektu
PROJECT_ROOT = Path("C:/Development/nex-automat")
TARGET_FILE = PROJECT_ROOT / "apps/supplier-invoice-editor/src/ui/main_window.py"


def main():
    """Zobrazí relevantné časti main_window.py."""
    print(f"Analyzujem: {TARGET_FILE}")

    if not TARGET_FILE.exists():
        print(f"❌ Súbor neexistuje: {TARGET_FILE}")
        return

    content = TARGET_FILE.read_text(encoding='utf-8')
    lines = content.splitlines()

    print("\n" + "=" * 60)
    print("IMPORTY (prvých 20 riadkov):")
    print("=" * 60)
    for i, line in enumerate(lines[:20], 1):
        marker = "👉" if "window_settings" in line or "WINDOW_MAIN" in line else "  "
        print(f"{marker} {i:3d}: {line}")

    print("\n" + "=" * 60)
    print("CLOSE EVENT metóda:")
    print("=" * 60)

    in_close_event = False
    for i, line in enumerate(lines, 1):
        if 'def closeEvent(self, event):' in line:
            in_close_event = True
            start = i

        if in_close_event:
            print(f"  {i:3d}: {line}")

            if line.strip() == 'event.accept()' or (line.strip().startswith('def ') and i > start):
                break

    print("\n" + "=" * 60)
    print("HĽADÁM save_window_settings v súbore:")
    print("=" * 60)

    found_import = False
    found_usage = False

    for i, line in enumerate(lines, 1):
        if 'save_window_settings' in line:
            if 'import' in line:
                print(f"✅ IMPORT na riadku {i}: {line.strip()}")
                found_import = True
            else:
                print(f"📍 POUŽITIE na riadku {i}: {line.strip()}")
                found_usage = True

    print("\n" + "=" * 60)
    print("VÝSLEDOK:")
    print("=" * 60)
    if found_import and found_usage:
        print("✅ Import aj použitie nájdené - mala by fungovať")
    elif not found_import:
        print("❌ IMPORT CHÝBA - to je problém!")
    elif not found_usage:
        print("⚠️  Import je ale použitie chýba")
    else:
        print("❓ Neznáma situácia")


if __name__ == "__main__":
    main()