#!/usr/bin/env python3
"""
Script 03: Add detailed DEBUG logging to base_window.py
Pridá detailné logovanie pre diagnostiku problému s rozmermi okna
"""

from pathlib import Path
import re


def add_debug_logging():
    """Pridá DEBUG logovanie do _save_settings a _load_settings"""

    base_window_path = Path("packages/nex-shared/ui/base_window.py")

    if not base_window_path.exists():
        print(f"❌ File not found: {base_window_path}")
        return False

    content = base_window_path.read_text(encoding='utf-8')

    # 1. Pridaj DEBUG log na začiatok _save_settings (po try:)
    pattern1 = r'(def _save_settings\(self\):.*?try:)'
    replacement1 = r'\1\n            logger.debug(f"🔍 _save_settings called for {self._window_name}")'
    content = re.sub(pattern1, replacement1, content, flags=re.DOTALL)

    # 2. Pridaj DEBUG log pred získaním rozmerov (riadok 135)
    pattern2 = r'(# Normal window - get actual size\n\s+x, y = self\.x\(\), self\.y\(\))'
    replacement2 = r'\1\n                logger.debug(f"🔍 Getting window dimensions for {self._window_name}")'
    content = re.sub(pattern2, replacement2, content)

    # 3. Pridaj DEBUG log po získaní rozmerov s AKTUÁLNYMI hodnotami
    pattern3 = r'(width, height = self\.width\(\), self\.height\(\))'
    replacement3 = r'\1\n                logger.debug(f"🔍 ACTUAL dimensions: x={x}, y={y}, w={width}, h={height}")'
    content = re.sub(pattern3, replacement3, content)

    # 4. Pridaj DEBUG log pred uložením do DB
    pattern4 = r'(# ALWAYS save \(with corrected position if needed\)\n\s+self\._db\.save\()'
    replacement4 = r'logger.debug(f"🔍 SAVING to DB: x={x}, y={y}, w={width}, h={height}, state=0")\n                \1'
    content = re.sub(pattern4, replacement4, content)

    # 5. Pridaj DEBUG log do _load_settings pri načítaní z DB
    pattern5 = r'(def _load_settings\(self\):.*?settings = self\._db\.load\()'
    replacement5 = r'\1'

    # Najprv nájdeme _load_settings a pridáme logovanie
    lines = content.split('\n')
    new_lines = []
    in_load_settings = False

    for i, line in enumerate(lines):
        new_lines.append(line)

        if 'def _load_settings(self):' in line:
            in_load_settings = True

        if in_load_settings and 'settings = self._db.load(' in line:
            # Pridaj DEBUG log hneď po načítaní z DB
            indent = ' ' * (len(line) - len(line.lstrip()))
            new_lines.append(f'{indent}logger.debug(f"🔍 LOADED from DB for {{self._window_name}}: {{settings}}")')
            in_load_settings = False

    content = '\n'.join(new_lines)

    # Ulož upravený súbor
    base_window_path.write_text(content, encoding='utf-8')

    print("✅ DEBUG logging added to base_window.py")
    print("\nAdded logs:")
    print("  1. _save_settings() entry point")
    print("  2. Getting window dimensions")
    print("  3. ACTUAL dimensions values")
    print("  4. SAVING to DB values")
    print("  5. LOADED from DB values")
    print("\n⚠️  Spustiť aplikáciu, zmeniť veľkosť, zavrieť a otvoriť - skontroluj log!")

    return True


if __name__ == "__main__":
    success = add_debug_logging()
    if success:
        print("\n" + "=" * 80)
        print("NEXT STEP: Test application")
        print("=" * 80)
        print("1. cd apps/supplier-invoice-editor")
        print("2. python main.py")
        print("3. Zmeň veľkosť okna (napr. na 800x600)")
        print("4. Zavri aplikáciu")
        print("5. Otvor aplikáciu znova")
        print("6. Skontroluj console output - hľadaj 🔍 DEBUG logy")