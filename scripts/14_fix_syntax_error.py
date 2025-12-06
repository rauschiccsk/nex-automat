#!/usr/bin/env python3
"""
Script 14: Fix syntax error in base_window.py
Opraví syntax chybu spôsobenú Script 13
"""

from pathlib import Path


def fix_syntax_error():
    """Opraví syntax error v _load_and_apply_settings()"""

    base_window_path = Path("packages/nex-shared/ui/base_window.py")

    if not base_window_path.exists():
        print(f"❌ File not found: {base_window_path}")
        return False

    content = base_window_path.read_text(encoding='utf-8')

    # Odstráň všetky DEBUG printy ktoré Script 13 pridal zle
    lines = content.split('\n')

    # Zobraz problematickú oblasť
    print("=" * 80)
    print("PROBLEMATIC AREA (lines 70-85):")
    print("=" * 80)
    for i in range(69, min(85, len(lines))):
        print(f"{i + 1:4d}: {lines[i]}")

    # Odstráň všetky DEBUG printy z _load_and_apply_settings
    # a znovu ich pridaj správne

    new_lines = []
    skip_next = False

    for i, line in enumerate(lines):
        # Preskočiť DEBUG printy ktoré Script 13 pridal
        if skip_next:
            skip_next = False
            continue

        if '🔍 DEBUG:' in line and '_load_and_apply_settings' in line:
            continue
        if '🔍 DEBUG: LOADED from DB:' in line:
            continue
        if '🔍 DEBUG: SAFE settings returned:' in line:
            continue
        if '🔍 DEBUG: setGeometry called' in line:
            continue

        new_lines.append(line)

    content = '\n'.join(new_lines)
    base_window_path.write_text(content, encoding='utf-8')

    print("\n✅ Removed broken DEBUG prints")
    print("\nNow adding them correctly...")

    # Načítaj znovu
    content = base_window_path.read_text(encoding='utf-8')

    # Pridaj DEBUG printy SPRÁVNE - na samostatné riadky
    # 1. Po def _load_and_apply_settings(self):
    content = content.replace(
        '    def _load_and_apply_settings(self):\n        """Načíta a aplikuje window settings z DB."""\n        try:',
        '    def _load_and_apply_settings(self):\n        """Načíta a aplikuje window settings z DB."""\n        print(f"🔍 DEBUG: _load_and_apply_settings called for {self._window_name}")\n        try:'
    )

    # 2. Po načítaní z DB (po zavretí zátvorky load())
    content = content.replace(
        '            settings = self._db.load(\n                window_name=self._window_name,\n                user_id=self._user_id\n            )\n',
        '            settings = self._db.load(\n                window_name=self._window_name,\n                user_id=self._user_id\n            )\n            print(f"🔍 DEBUG: LOADED from DB: {settings}")\n'
    )

    # 3. Po get_safe_position (po zavretí zátvorky)
    content = content.replace(
        '            safe_settings = self._persistence.get_safe_position(\n                settings=settings,\n                default_size=self._default_size,\n                default_pos=self._default_pos\n            )\n',
        '            safe_settings = self._persistence.get_safe_position(\n                settings=settings,\n                default_size=self._default_size,\n                default_pos=self._default_pos\n            )\n            print(f"🔍 DEBUG: SAFE settings: {safe_settings}")\n'
    )

    # 4. Po setGeometry
    content = content.replace(
        '            self.setGeometry(\n                safe_settings[\'x\'],\n                safe_settings[\'y\'],\n                safe_settings[\'width\'],\n                safe_settings[\'height\']\n            )\n',
        '            self.setGeometry(\n                safe_settings[\'x\'],\n                safe_settings[\'y\'],\n                safe_settings[\'width\'],\n                safe_settings[\'height\']\n            )\n            print(f"🔍 DEBUG: setGeometry({safe_settings[\'x\']}, {safe_settings[\'y\']}, {safe_settings[\'width\']}, {safe_settings[\'height\']})")\n'
    )

    base_window_path.write_text(content, encoding='utf-8')

    print("✅ DEBUG prints added correctly")
    return True


if __name__ == "__main__":
    success = fix_syntax_error()
    if success:
        print("\n" + "=" * 80)
        print("NEXT: Test again")
        print("=" * 80)
        print("cd apps/supplier-invoice-editor")
        print("python main.py")