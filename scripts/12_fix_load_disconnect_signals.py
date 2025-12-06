"""
Fix: _load_grid_settings() - disconnect signals počas load aby sa neukladalo
Location: C:\Development\nex-automat\scripts\12_fix_load_disconnect_signals.py
"""
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).parent
DEV_ROOT = SCRIPT_DIR.parent
BASE_GRID = DEV_ROOT / "packages" / "nex-shared" / "ui" / "base_grid.py"

def fix_load():
    """Pridaj disconnect/connect signals v _load_grid_settings"""

    print("=" * 80)
    print("FIX: base_grid.py - disconnect signals počas load")
    print("=" * 80)

    with open(BASE_GRID, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Find _load_grid_settings start
    load_start = None
    for i, line in enumerate(lines):
        if 'def _load_grid_settings(self):' in line:
            load_start = i
            print(f"✓ Found _load_grid_settings at line {i+1}")
            break

    if load_start is None:
        print("❌ Nenašiel som _load_grid_settings")
        return False

    # Find try: after load_start
    try_line = None
    for i in range(load_start, min(load_start+10, len(lines))):
        if lines[i].strip() == 'try:':
            try_line = i
            print(f"✓ Found try: at line {i+1}")
            break

    if try_line is None:
        print("❌ Nenašiel som try: block")
        return False

    # Find except Exception at end
    except_line = None
    for i in range(try_line, min(try_line+100, len(lines))):
        if 'except Exception as e:' in lines[i]:
            # Check next line contains "loading grid settings"
            if i+1 < len(lines) and 'loading grid settings' in lines[i+1]:
                except_line = i
                print(f"✓ Found except at line {i+1}")
                break

    if except_line is None:
        print("❌ Nenašiel som except block")
        return False

    # Now do insertions
    insertions = []

    # Add disconnect AFTER try: (as first thing in try block)
    disconnect_code = [
        '            # Disconnect signals during load to prevent recursive save\n',
        '            header = self.table_view.horizontalHeader()\n',
        '            header.sectionResized.disconnect(self._on_column_resized)\n',
        '            header.sectionMoved.disconnect(self._on_column_moved)\n',
        '\n'
    ]

    for offset, code_line in enumerate(disconnect_code):
        insertions.append((try_line + 1 + offset, code_line))

    # Add reconnect with finally: before except
    reconnect_code = [
        '\n',
        '        finally:\n',
        '            # Reconnect signals after load\n',
        '            header = self.table_view.horizontalHeader()\n',
        '            header.sectionResized.connect(self._on_column_resized)\n',
        '            header.sectionMoved.connect(self._on_column_moved)\n'
    ]

    # Adjust except_line by the number of disconnect lines we'll insert
    except_adjusted = except_line + len(disconnect_code)

    for offset, code_line in enumerate(reconnect_code):
        insertions.append((except_adjusted + offset, code_line))

    print(f"\n✓ Total insertions: {len(insertions)}")

    # Sort insertions (reverse) to insert from bottom
    insertions.sort(reverse=True)

    # Insert all lines
    for line_num, new_line in insertions:
        lines.insert(line_num, new_line)

    # Write back
    with open(BASE_GRID, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    print(f"\n✓ File updated: {BASE_GRID.relative_to(DEV_ROOT)}")
    print("\nTeraz:")
    print("  1. Spusti aplikáciu - syntax error by mal byť opravený")
    print("  2. Vymaž DB a testuj active column persistence")
    return True

if __name__ == "__main__":
    fix_load()