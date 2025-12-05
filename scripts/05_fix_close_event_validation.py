#!/usr/bin/env python3
"""
Fix Close Event Validation
===========================
Session: 2025-12-05
Location: scripts/05_fix_close_event_validation.py

Pridá validáciu pozície okna v closeEvent() pred uložením.
Ak je okno mimo obrazovky, neuloží pozíciu.
"""

from pathlib import Path

# Cesty
PROJECT_ROOT = Path(__file__).parent.parent
TARGET_FILE = PROJECT_ROOT / "apps/supplier-invoice-editor/src/ui/main_window.py"


def fix_close_event():
    """Pridá validáciu do closeEvent"""

    print("=" * 80)
    print("FIX CLOSE EVENT VALIDATION")
    print("=" * 80)

    # 1. Načítaj súbor
    print(f"\n1. Načítavam: {TARGET_FILE.name}")
    if not TARGET_FILE.exists():
        print(f"   ❌ Súbor neexistuje")
        return False

    with open(TARGET_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # 2. Oprava closeEvent - pridať validáciu
    print("\n2. Pridávam validáciu do closeEvent()...")

    # Staré closeEvent (bez validácie)
    old_close_event = (
        "    def closeEvent(self, event):\n"
        "        \"\"\"Handle window close event\"\"\"\n"
        "        self.logger.info(\"Application closing\")\n"
        "        # Ulož pozíciu a veľkosť okna\n"
        "        save_window_settings(\n"
        "            window_name=WINDOW_MAIN,\n"
        "            x=self.x(),\n"
        "            y=self.y(),\n"
        "            width=self.width(),\n"
        "            height=self.height()\n"
        "        )\n"
        "        event.accept()"
    )

    # Nové closeEvent (s validáciou)
    new_close_event = (
        "    def closeEvent(self, event):\n"
        "        \"\"\"Handle window close event\"\"\"\n"
        "        self.logger.info(\"Application closing\")\n"
        "        \n"
        "        # Validuj pozíciu pred uložením\n"
        "        x, y = self.x(), self.y()\n"
        "        width, height = self.width(), self.height()\n"
        "        \n"
        "        # Validačné limity (rovnaké ako v window_settings.py)\n"
        "        MIN_X, MIN_Y = -50, 0\n"
        "        MIN_WIDTH, MIN_HEIGHT = 400, 300\n"
        "        MAX_WIDTH, MAX_HEIGHT = 3840, 2160\n"
        "        \n"
        "        # Kontrola validity\n"
        "        is_valid = (\n"
        "            x >= MIN_X and y >= MIN_Y and\n"
        "            MIN_WIDTH <= width <= MAX_WIDTH and\n"
        "            MIN_HEIGHT <= height <= MAX_HEIGHT\n"
        "        )\n"
        "        \n"
        "        if is_valid:\n"
        "            # Ulož len validné nastavenia\n"
        "            save_window_settings(\n"
        "                window_name=WINDOW_MAIN,\n"
        "                x=x, y=y,\n"
        "                width=width, height=height\n"
        "            )\n"
        "            self.logger.info(f\"Window settings saved: ({x}, {y}) [{width}x{height}]\")\n"
        "        else:\n"
        "            self.logger.warning(f\"Invalid position not saved: ({x}, {y}) [{width}x{height}]\")\n"
        "        \n"
        "        event.accept()"
    )

    if old_close_event in content:
        content = content.replace(old_close_event, new_close_event)
        print("   ✅ Pridaná validácia do closeEvent()")
    else:
        print("   ⚠️  Pattern nenájdený - možno už je upravené")
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
    print("✅ HOTOVO - Close Event Validation Added")
    print("=" * 80)
    print("\nZmeny:")
    print("  • Pridaná validácia pozície pred save")
    print("  • Nevalidné pozície sa už neuložia")
    print("  • Loguje sa či bolo uložené alebo nie")

    print("\n" + "=" * 80)
    print("ĎALŠÍ KROK:")
    print("=" * 80)
    print("1. Vyčisti databázu: python scripts\\clean_invalid_window_positions.py")
    print("2. Test: spusti aplikáciu 2x - nevalidná pozícia by sa už nemala uložiť")
    print("=" * 80)

    return True


if __name__ == "__main__":
    success = fix_close_event()
    exit(0 if success else 1)