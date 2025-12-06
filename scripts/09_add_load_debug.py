"""
Add debug logging to base_grid.py _load_grid_settings()
Location: C:\Development\nex-automat\scripts\09_add_load_debug.py
"""
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).parent
DEV_ROOT = SCRIPT_DIR.parent
BASE_GRID = DEV_ROOT / "packages" / "nex-shared" / "ui" / "base_grid.py"


def add_debug():
    """Pridaj debug výpisy do _load_grid_settings"""

    print("=" * 80)
    print("ADD DEBUG: _load_grid_settings()")
    print("=" * 80)

    with open(BASE_GRID, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Find _load_grid_settings method
    insertions = []

    for i, line in enumerate(lines):
        if 'def _load_grid_settings(self):' in line:
            # Insert after docstring (2 lines down)
            insertions.append(
                (i + 2, '        print(f"[LOAD] _load_grid_settings called: {self._window_name}/{self._grid_name}")\n'))
            print(f"✓ Found _load_grid_settings at line {i + 1}")
            break

    # Find "if column_settings:" block
    for i, line in enumerate(lines):
        if 'if column_settings:' in line and i > 160 and i < 200:
            insertions.append(
                (i + 1, '                print(f"[LOAD] Found {len(column_settings)} column settings")\n'))
            print(f"✓ Found column_settings check at line {i + 1}")
            break

    # Find "if col_settings:" block
    for i, line in enumerate(lines):
        if 'if col_settings:' in line and i > 180:
            insertions.append((i + 1,
                               '                        print(f"[LOAD] Applying settings for column {col_idx}: {col_name} - width={col_settings.get(\'width\')}")\n'))
            print(f"✓ Found col_settings application at line {i + 1}")
            break

    # Find grid settings load
    for i, line in enumerate(lines):
        if 'grid_settings = load_grid_settings(' in line:
            # Find the if block after this
            for j in range(i + 1, min(i + 20, len(lines))):
                if "if grid_settings and 'active_column_index' in grid_settings:" in lines[j]:
                    insertions.append((j + 1,
                                       '                print(f"[LOAD] Found grid settings, active_column={grid_settings[\'active_column_index\']}")\n'))
                    print(f"✓ Found grid_settings load at line {j + 1}")
                    break
            break

    # Find the else case (no settings found)
    for i, line in enumerate(lines):
        if 'column_settings = load_column_settings(' in line and i > 160:
            # Find the if column_settings check after this
            for j in range(i + 1, min(i + 15, len(lines))):
                if 'if column_settings:' in lines[j]:
                    # Insert before the if to show when no settings found
                    insertions.append(
                        (j, '            print(f"[LOAD] column_settings loaded: {column_settings is not None}")\n'))
                    print(f"✓ Adding column_settings loaded check at line {j}")
                    break
            break

    if not insertions:
        print("\n❌ Nenašiel som žiadne insertion points!")
        return False

    # Sort insertions (reverse)
    insertions.sort(reverse=True)

    # Insert all debug statements
    for line_num, debug_line in insertions:
        lines.insert(line_num, debug_line)

    # Write back
    with open(BASE_GRID, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    print(f"\n✓ Load debug pridaný: {BASE_GRID.relative_to(DEV_ROOT)}")
    print(f"✓ Vložených {len(insertions)} debug riadkov")
    print("\nTeraz:")
    print("  1. Vymaž DB: del C:\\NEX\\YEARACT\\SYSTEM\\SQLITE\\grid_settings.db")
    print("  2. Spusti aplikáciu a zmeň šírky")
    print("  3. Zatvor aplikáciu")
    print("  4. Znova spusti - sleduj [LOAD] výpisy")
    return True


if __name__ == "__main__":
    add_debug()