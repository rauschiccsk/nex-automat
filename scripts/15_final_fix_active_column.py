"""
Final Fix: Pridá active_column_changed signal a handler (safe check ak už existuje)
Location: C:\Development\nex-automat\scripts\15_final_fix_active_column.py
"""
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
DEV_ROOT = SCRIPT_DIR.parent
QUICK_SEARCH = DEV_ROOT / "apps" / "supplier-invoice-editor" / "src" / "ui" / "widgets" / "quick_search.py"
BASE_GRID = DEV_ROOT / "packages" / "nex-shared" / "ui" / "base_grid.py"


def fix_quick_search():
    print("=" * 80)
    print("FIX: quick_search.py")
    print("=" * 80)

    with open(QUICK_SEARCH, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Check if signal already exists
    has_signal = any('active_column_changed' in line and 'pyqtSignal' in line for line in lines)
    has_emit = any('active_column_changed.emit' in line for line in lines)

    if has_signal and has_emit:
        print("✓ Quick search už má signal a emit - OK")
        return True

    # Find class QuickSearchController and add signal
    if not has_signal:
        for i, line in enumerate(lines):
            if 'class QuickSearchController(QObject):' in line:
                # Find def __init__ after this
                for j in range(i, min(i + 15, len(lines))):
                    if 'def __init__' in lines[j]:
                        # Insert signal before __init__
                        lines.insert(j, '\n')
                        lines.insert(j + 1, '    # Signal emitted when active column changes\n')
                        lines.insert(j + 2, '    active_column_changed = pyqtSignal(int)\n')
                        print(f"✓ Pridaný signal na riadok {j + 1}")
                        break
                break

    # Find _change_column and add emit
    if not has_emit:
        for i, line in enumerate(lines):
            if 'self.current_column = new_column' in line and '_change_column' in ''.join(lines[max(0, i - 20):i]):
                # Insert emit after current_column assignment
                indent = len(line) - len(line.lstrip())
                lines.insert(i + 1, '\n')
                lines.insert(i + 2, ' ' * indent + '# Emit signal for BaseGrid to save\n')
                lines.insert(i + 3, ' ' * indent + 'self.active_column_changed.emit(new_column)\n')
                print(f"✓ Pridaný emit na riadok {i + 2}")
                break

    with open(QUICK_SEARCH, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    print(f"✓ Updated: {QUICK_SEARCH.relative_to(DEV_ROOT)}")
    return True


def fix_base_grid():
    print("\n" + "=" * 80)
    print("FIX: base_grid.py")
    print("=" * 80)

    with open(BASE_GRID, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Check if connection and handler exist
    has_connection = any('active_column_changed.connect' in line for line in lines)
    has_handler = any('def _on_active_column_changed' in line for line in lines)

    if has_connection and has_handler:
        print("✓ Base grid už má connection a handler - OK")
        return True

    # Add connection in setup_quick_search
    if not has_connection:
        for i, line in enumerate(lines):
            if 'self.logger.info(f"Quick search setup complete for {self._grid_name}")' in line:
                # Insert before this line
                indent = len(line) - len(line.lstrip())
                lines.insert(i, '\n')
                lines.insert(i + 1, ' ' * indent + '# Connect active column changed signal to save\n')
                lines.insert(i + 2,
                             ' ' * indent + 'self.search_controller.active_column_changed.connect(self._on_active_column_changed)\n')
                print(f"✓ Pridaný connect na riadok {i + 1}")
                break

    # Add handler before _on_column_resized
    if not has_handler:
        for i, line in enumerate(lines):
            if 'def _on_column_resized(self, logical_index, old_size, new_size):' in line:
                # Insert handler before this
                indent = len(line) - len(line.lstrip())
                lines.insert(i, ' ' * indent + 'def _on_active_column_changed(self, column):\n')
                lines.insert(i + 1, ' ' * (indent + 4) + '"""Handler pre zmenu active column."""\n')
                lines.insert(i + 2, ' ' * (
                            indent + 4) + 'print(f"[ACTIVE] Active column changed to {column} for {self._grid_name}")\n')
                lines.insert(i + 3, ' ' * (indent + 4) + 'self._save_grid_settings()\n')
                lines.insert(i + 4, '\n')
                print(f"✓ Pridaný handler na riadok {i}")
                break

    with open(BASE_GRID, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    print(f"✓ Updated: {BASE_GRID.relative_to(DEV_ROOT)}")
    return True


def main():
    if not fix_quick_search():
        return
    if not fix_base_grid():
        return

    print("\n" + "=" * 80)
    print("HOTOVO")
    print("=" * 80)
    print("\nTeraz:")
    print("  1. del C:\\NEX\\YEARACT\\SYSTEM\\SQLITE\\grid_settings.db")
    print("  2. python main.py")
    print("  3. Šípkami → zmeň active column")
    print("  4. Sleduj [ACTIVE] a [DEBUG] v console")


if __name__ == "__main__":
    main()