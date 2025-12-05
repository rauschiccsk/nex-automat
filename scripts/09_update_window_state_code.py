#!/usr/bin/env python3
"""
Update Window State Code
=========================
Session: 2025-12-05
Location: scripts/09_update_window_state_code.py

Upravuje window_settings.py a main_window.py aby ukladali windowState.
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent


def update_window_settings_py():
    """Upraví window_settings.py"""

    target = PROJECT_ROOT / "apps/supplier-invoice-editor/src/utils/window_settings.py"

    print("=" * 80)
    print("WINDOW_SETTINGS.PY")
    print("=" * 80)

    with open(target, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # 1. Upraviť load_window_settings - pridať window_state do SELECT a return
    print("\n1. Upravujem load_window_settings()...")

    old_select = "        cursor.execute(\"\"\"\n            SELECT x, y, width, height\n            FROM window_settings\n            WHERE user_id = ? AND window_name = ?\n        \"\"\", (user_id, window_name))"

    new_select = "        cursor.execute(\"\"\"\n            SELECT x, y, width, height, window_state\n            FROM window_settings\n            WHERE user_id = ? AND window_name = ?\n        \"\"\", (user_id, window_name))"

    if old_select in content:
        content = content.replace(old_select, new_select)
        print("   ✅ SELECT rozšírený o window_state")
    else:
        print("   ⚠️  SELECT pattern nenájdený")
        return False

    # 2. Upraviť spracovanie výsledku
    old_row_parse = "        if row:\n            x, y, width, height = row[0], row[1], row[2], row[3]"
    new_row_parse = "        if row:\n            x, y, width, height = row[0], row[1], row[2], row[3]\n            window_state = row[4] if len(row) > 4 else 0"

    if old_row_parse in content:
        content = content.replace(old_row_parse, new_row_parse)
        print("   ✅ Row parsing rozšírený")
    else:
        print("   ⚠️  Row parsing nenájdený")
        return False

    # 3. Upraviť return dictionary
    old_return = "            return {\n                'x': x,\n                'y': y,\n                'width': width,\n                'height': height\n            }"

    new_return = "            return {\n                'x': x,\n                'y': y,\n                'width': width,\n                'height': height,\n                'window_state': window_state\n            }"

    if old_return in content:
        content = content.replace(old_return, new_return)
        print("   ✅ Return dictionary rozšírený")
    else:
        print("   ⚠️  Return dictionary nenájdený")
        return False

    # 4. Upraviť save_window_settings - pridať window_state parameter
    old_save_sig = "def save_window_settings(window_name: str, x: int, y: int, width: int, height: int,\n                        user_id: Optional[str] = None) -> bool:"

    new_save_sig = "def save_window_settings(window_name: str, x: int, y: int, width: int, height: int,\n                        window_state: int = 0, user_id: Optional[str] = None) -> bool:"

    if old_save_sig in content:
        content = content.replace(old_save_sig, new_save_sig)
        print("   ✅ save_window_settings() signature rozšírená")
    else:
        print("   ⚠️  Signature nenájdená")
        return False

    # 5. Upraviť INSERT statement
    old_insert = "        cursor.execute(\"\"\"\n            INSERT OR REPLACE INTO window_settings\n            (user_id, window_name, x, y, width, height, updated_at)\n            VALUES (?, ?, ?, ?, ?, ?, ?)\n        \"\"\", (user_id, window_name, x, y, width, height, datetime.now()))"

    new_insert = "        cursor.execute(\"\"\"\n            INSERT OR REPLACE INTO window_settings\n            (user_id, window_name, x, y, width, height, window_state, updated_at)\n            VALUES (?, ?, ?, ?, ?, ?, ?, ?)\n        \"\"\", (user_id, window_name, x, y, width, height, window_state, datetime.now()))"

    if old_insert in content:
        content = content.replace(old_insert, new_insert)
        print("   ✅ INSERT statement rozšírený")
    else:
        print("   ⚠️  INSERT nenájdený")
        return False

    # Ulož
    if content != original:
        with open(target, 'w', encoding='utf-8') as f:
            f.write(content)
        print("\n✅ window_settings.py uložený")
        return True

    return False


def update_main_window_py():
    """Upraví main_window.py"""

    target = PROJECT_ROOT / "apps/supplier-invoice-editor/src/ui/main_window.py"

    print("\n" + "=" * 80)
    print("MAIN_WINDOW.PY")
    print("=" * 80)

    with open(target, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # 1. Upraviť _load_geometry - načítať a aplikovať windowState
    print("\n1. Upravujem _load_geometry()...")

    old_load = "        if settings:\n            self.setGeometry(\n                settings['x'],\n                settings['y'],\n                settings['width'],\n                settings['height']\n            )\n            self.logger.info(f\"Loaded window position: ({settings['x']}, {settings['y']}) [{settings['width']}x{settings['height']}]\")"

    new_load = "        if settings:\n            self.setGeometry(\n                settings['x'],\n                settings['y'],\n                settings['width'],\n                settings['height']\n            )\n            # Načítaj a aplikuj window state (maximalizované/normálne)\n            if settings.get('window_state', 0) == 2:  # Qt.WindowMaximized = 2\n                self.setWindowState(Qt.WindowMaximized)\n                self.logger.info(f\"Loaded maximized window at ({settings['x']}, {settings['y']})\")\n            else:\n                self.logger.info(f\"Loaded window position: ({settings['x']}, {settings['y']}) [{settings['width']}x{settings['height']}]\")"

    if old_load in content:
        content = content.replace(old_load, new_load)
        print("   ✅ _load_geometry() rozšírený o windowState")
    else:
        print("   ⚠️  Load pattern nenájdený")
        return False

    # 2. Pridať Qt import pre WindowMaximized
    print("\n2. Kontrolujem Qt importy...")

    if "from PyQt5.QtCore import Qt" in content:
        print("   ✅ Qt už importovaný")
    else:
        print("   ⚠️  Qt import chýba - pridaj manuálne")

    # 3. Upraviť closeEvent - uložiť windowState
    print("\n3. Upravujem closeEvent()...")

    old_close = "        if is_valid:\n            # Ulož len validné nastavenia\n            save_window_settings(\n                window_name=WINDOW_MAIN,\n                x=x, y=y,\n                width=width, height=height\n            )\n            self.logger.info(f\"Window settings saved: ({x}, {y}) [{width}x{height}]\")"

    new_close = "        if is_valid:\n            # Ulož len validné nastavenia vrátane windowState\n            window_state = 2 if self.isMaximized() else 0  # Qt.WindowMaximized = 2\n            save_window_settings(\n                window_name=WINDOW_MAIN,\n                x=x, y=y,\n                width=width, height=height,\n                window_state=window_state\n            )\n            state_str = \"maximized\" if window_state == 2 else \"normal\"\n            self.logger.info(f\"Window settings saved: ({x}, {y}) [{width}x{height}] {state_str}\")"

    if old_close in content:
        content = content.replace(old_close, new_close)
        print("   ✅ closeEvent() rozšírený o windowState")
    else:
        print("   ⚠️  Close pattern nenájdený")
        return False

    # Ulož
    if content != original:
        with open(target, 'w', encoding='utf-8') as f:
            f.write(content)
        print("\n✅ main_window.py uložený")
        return True

    return False


def main():
    print("=" * 80)
    print("UPDATE WINDOW STATE CODE")
    print("=" * 80)

    success1 = update_window_settings_py()
    success2 = update_main_window_py()

    print("\n" + "=" * 80)
    if success1 and success2:
        print("✅ HOTOVO - Window State Code Updated")
    else:
        print("⚠️  ČIASTOČNE HOTOVO")
    print("=" * 80)

    print("\nZmeny:")
    print("  • window_settings.py - pridaný window_state do load/save")
    print("  • main_window.py - ukladá/načítava maximalized state")

    print("\n" + "=" * 80)
    print("TEST:")
    print("=" * 80)
    print("1. Spusti aplikáciu")
    print("2. Maximalizuj okno (Windows key + Up)")
    print("3. Zatvor (ESC)")
    print("4. Spusti znovu - malo by sa otvoriť maximalizované")
    print("=" * 80)

    return success1 and success2


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)