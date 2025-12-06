"""
Add debug logging to base_grid.py _save_grid_settings()
Location: C:\Development\nex-automat\scripts\08_add_debug_logging.py
"""
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).parent
DEV_ROOT = SCRIPT_DIR.parent
BASE_GRID = DEV_ROOT / "packages" / "nex-shared" / "ui" / "base_grid.py"


def add_debug():
    """Pridaj debug výpisy do _save_grid_settings"""

    print("=" * 80)
    print("ADD DEBUG: base_grid.py")
    print("=" * 80)

    with open(BASE_GRID, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Insert debug statements at specific lines
    insertions = []

    # Find _save_grid_settings method (around line 235)
    for i, line in enumerate(lines):
        if 'def _save_grid_settings(self):' in line:
            # Insert after docstring (2 lines down)
            insertions.append((i + 2,
                               '        print(f"[DEBUG] _save_grid_settings called: {self._window_name}/{self._grid_name}")\n'))
            print(f"✓ Found _save_grid_settings at line {i + 1}")
            break

    # Find model check
    for i, line in enumerate(lines):
        if 'if not model:' in line and i > 230:  # After _save_grid_settings
            insertions.append(
                (i + 1, '                print(f"[DEBUG] No model for {self._window_name}/{self._grid_name}")\n'))
            # Find the return after this
            for j in range(i + 1, min(i + 5, len(lines))):
                if 'return' in lines[j]:
                    insertions.append(
                        (j + 1, '            print(f"[DEBUG] Model OK, columns: {model.columnCount()}")\n'))
                    print(f"✓ Found model check at line {i + 1}")
                    break
            break

    # Find save_column_settings call
    for i, line in enumerate(lines):
        if 'save_column_settings(' in line and i > 250:
            insertions.append(
                (i, '            print(f"[DEBUG] Saving {len(column_settings)} columns for {self._grid_name}")\n'))
            # Find closing ) and add after it
            for j in range(i, min(i + 10, len(lines))):
                if ')' in lines[j] and 'save_column_settings' not in lines[j]:
                    insertions.append((j + 1, '            print(f"[DEBUG] Column settings saved")\n'))
                    print(f"✓ Found save_column_settings at line {i + 1}")
                    break
            break

    # Find save_grid_settings call
    for i, line in enumerate(lines):
        if 'save_grid_settings(' in line and i > 270:
            insertions.append((i, '                print(f"[DEBUG] Saving active column: {active_column}")\n'))
            # Find closing ) and add after it
            for j in range(i, min(i + 10, len(lines))):
                if ')' in lines[j] and 'save_grid_settings' not in lines[j]:
                    insertions.append((j + 1, '                print(f"[DEBUG] Grid settings saved")\n'))
                    print(f"✓ Found save_grid_settings at line {i + 1}")
                    break
            break

    # Find else for active_column check
    for i, line in enumerate(lines):
        if 'if active_column is not None:' in line and i > 270:
            # Find the corresponding else or end of if block
            for j in range(i + 1, min(i + 20, len(lines))):
                if 'self.logger.debug(' in lines[j]:
                    # Insert before logger.debug
                    insertions.append((j,
                                       '            else:\n                print(f"[DEBUG] No active column to save (search_controller={self.search_controller})")\n\n'))
                    print(f"✓ Adding else clause for active_column check")
                    break
            break

    if not insertions:
        print("\n❌ Nenašiel som žiadne insertion points!")
        return False

    # Sort insertions by line number (reverse so we insert from bottom to top)
    insertions.sort(reverse=True)

    # Insert all debug statements
    for line_num, debug_line in insertions:
        lines.insert(line_num, debug_line)

    # Write back
    with open(BASE_GRID, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    print(f"\n✓ Debug logging pridaný: {BASE_GRID.relative_to(DEV_ROOT)}")
    print(f"✓ Vložených {len(insertions)} debug riadkov")
    print("\nTeraz spusti aplikáciu a sleduj console výpisy")
    return True


if __name__ == "__main__":
    add_debug()