#!/usr/bin/env python3
"""
Script 13: Add DEBUG prints to _load_and_apply_settings()
Pridá DEBUG logy do správnej metódy načítavania
"""

from pathlib import Path


def add_debug_logs():
    """Pridá DEBUG printy do _load_and_apply_settings()"""

    base_window_path = Path("packages/nex-shared/ui/base_window.py")

    if not base_window_path.exists():
        print(f"❌ File not found: {base_window_path}")
        return False

    content = base_window_path.read_text(encoding='utf-8')
    lines = content.split('\n')

    # Nájdi _load_and_apply_settings a pridaj DEBUG logy
    new_lines = []
    in_method = False

    for i, line in enumerate(lines):
        new_lines.append(line)

        # Začiatok metódy
        if 'def _load_and_apply_settings(self):' in line:
            in_method = True
            # Pridaj DEBUG hneď na začiatku
            indent = ' ' * 8
            new_lines.append(f'{indent}print(f"🔍 DEBUG: _load_and_apply_settings called for {{self._window_name}}")')
            continue

        # Po načítaní z DB
        if in_method and 'settings = self._db.load(' in line:
            indent = ' ' * (len(line) - len(line.lstrip()))
            new_lines.append(f'{indent}print(f"🔍 DEBUG: LOADED from DB: {{settings}}")')
            continue

        # Po get_safe_position
        if in_method and 'safe_settings = self._persistence.get_safe_position(' in line:
            # Hľadaj koniec volania (môže byť multi-line)
            j = i
            while j < len(lines) and ')' not in lines[j]:
                j += 1
            # Pridaj DEBUG po zatváracej zátvorke
            indent = ' ' * (len(line) - len(line.lstrip()))
            new_lines.append(f'{indent}print(f"🔍 DEBUG: SAFE settings returned: {{safe_settings}}")')
            continue

        # Po setGeometry
        if in_method and 'self.setGeometry(' in line:
            # Hľadaj koniec volania
            j = i
            while j < len(lines) and ')' not in lines[j]:
                j += 1
            indent = ' ' * (len(line) - len(line.lstrip()))
            new_lines.append(f'{indent}print(f"🔍 DEBUG: setGeometry called with safe_settings")')
            in_method = False  # Koniec metódy
            continue

    # Ulož
    content = '\n'.join(new_lines)
    base_window_path.write_text(content, encoding='utf-8')

    print("✅ DEBUG logs added to _load_and_apply_settings()")
    print("\nAdded prints:")
    print("  1. Method entry point")
    print("  2. LOADED from DB")
    print("  3. SAFE settings after get_safe_position()")
    print("  4. setGeometry call confirmation")

    return True


if __name__ == "__main__":
    success = add_debug_logs()
    if success:
        print("\n" + "=" * 80)
        print("NEXT: Test again to see FULL flow")
        print("=" * 80)
        print("cd apps/supplier-invoice-editor")
        print("python main.py")
        print("\n→ Teraz uvidíš CELÝ flow: load → get_safe_position → setGeometry")