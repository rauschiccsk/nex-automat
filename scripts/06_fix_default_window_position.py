#!/usr/bin/env python3
"""
Fix Default Window Position
============================
Session: 2025-12-05
Location: scripts/06_fix_default_window_position.py

Pridá explicitnú default pozíciu ak databáza neobsahuje záznam.
Qt používa OS cache, takže musíme explicitne nastaviť validnú pozíciu.
"""

from pathlib import Path

# Cesty
PROJECT_ROOT = Path(__file__).parent.parent
TARGET_FILE = PROJECT_ROOT / "apps/supplier-invoice-editor/src/ui/main_window.py"


def fix_default_position():
    """Pridá default pozíciu do _load_geometry"""

    print("=" * 80)
    print("FIX DEFAULT WINDOW POSITION")
    print("=" * 80)

    # 1. Načítaj súbor
    print(f"\n1. Načítavam: {TARGET_FILE.name}")
    if not TARGET_FILE.exists():
        print(f"   ❌ Súbor neexistuje")
        return False

    with open(TARGET_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # 2. Oprava _load_geometry - pridať else vetvu
    print("\n2. Pridávam default pozíciu do _load_geometry()...")

    old_load_geometry = (
        "    def _load_geometry(self):\n"
        "        \"\"\"Načíta a aplikuje uloženú pozíciu a veľkosť okna.\"\"\"\n"
        "        settings = load_window_settings(window_name=WINDOW_MAIN)\n"
        "        if settings:\n"
        "            self.setGeometry(\n"
        "                settings['x'],\n"
        "                settings['y'],\n"
        "                settings['width'],\n"
        "                settings['height']\n"
        "            )"
    )

    new_load_geometry = (
        "    def _load_geometry(self):\n"
        "        \"\"\"Načíta a aplikuje uloženú pozíciu a veľkosť okna.\"\"\"\n"
        "        settings = load_window_settings(window_name=WINDOW_MAIN)\n"
        "        if settings:\n"
        "            self.setGeometry(\n"
        "                settings['x'],\n"
        "                settings['y'],\n"
        "                settings['width'],\n"
        "                settings['height']\n"
        "            )\n"
        "            self.logger.info(f\"Loaded window position: ({settings['x']}, {settings['y']}) [{settings['width']}x{settings['height']}]\")\n"
        "        else:\n"
        "            # Žiadny uložený záznam - použiť bezpečnú default pozíciu\n"
        "            default_x, default_y = 100, 100\n"
        "            default_width, default_height = 1400, 900\n"
        "            self.setGeometry(default_x, default_y, default_width, default_height)\n"
        "            self.logger.info(f\"Using default position: ({default_x}, {default_y}) [{default_width}x{default_height}]\")"
    )

    if old_load_geometry in content:
        content = content.replace(old_load_geometry, new_load_geometry)
        print("   ✅ Pridaná default pozícia")
    else:
        print("   ⚠️  Pattern nenájdený")
        return False

    # 3. Kontrola zmien
    if content == original_content:
        print("\n   ❌ Žiadne zmeny")
        return False

    # 4. Ulož súbor
    print("\n3. Ukladám súbor...")
    with open(TARGET_FILE, 'w', encoding='utf-8') as f:
        f.write(content)

    print("   ✅ Uložené")

    # 5. Zhrnutie
    print("\n" + "=" * 80)
    print("✅ HOTOVO - Default Position Added")
    print("=" * 80)
    print("\nZmeny:")
    print("  • Pridaná default pozícia (100, 100)")
    print("  • Ak DB prázdna → použije safe default")
    print("  • Loguje odkiaľ prišla pozícia")

    print("\n" + "=" * 80)
    print("FINÁLNY TEST:")
    print("=" * 80)
    print("1. Spusti aplikáciu - malo by sa otvoriť na (100, 100)")
    print("2. Zatvor (ESC) - nevalidná pozícia sa neuloží")
    print("3. Spusti znovu - malo by byť opäť na (100, 100)")
    print("4. Presuň okno na validnú pozíciu (napr. stred obrazovky)")
    print("5. Zatvor (ESC) - validná pozícia sa uloží")
    print("6. Spusti znovu - malo by zapamätať validnú pozíciu")
    print("=" * 80)

    return True


if __name__ == "__main__":
    success = fix_default_position()
    exit(0 if success else 1)