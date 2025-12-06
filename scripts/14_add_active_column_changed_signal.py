"""
Fix: Pridať active_column_changed signal do QuickSearchController
Location: C:\Development\nex-automat\scripts\14_add_active_column_changed_signal.py
"""
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).parent
DEV_ROOT = SCRIPT_DIR.parent
QUICK_SEARCH = DEV_ROOT / "apps" / "supplier-invoice-editor" / "src" / "ui" / "widgets" / "quick_search.py"
BASE_GRID = DEV_ROOT / "packages" / "nex-shared" / "ui" / "base_grid.py"


def fix_quick_search():
    """Pridaj signal active_column_changed"""

    print("=" * 80)
    print("FIX: quick_search.py - active_column_changed signal")
    print("=" * 80)

    with open(QUICK_SEARCH, 'r', encoding='utf-8') as f:
        content = f.read()

    # Add signal to QuickSearchController class
    old_class_start = '''class QuickSearchController(QObject):
    """
    Controller for quick search functionality
    Handles search logic and table interaction
    """

    def __init__(self, table_view, search_container):'''

    new_class_start = '''class QuickSearchController(QObject):
    """
    Controller for quick search functionality
    Handles search logic and table interaction
    """

    # Signal emitted when active column changes
    active_column_changed = pyqtSignal(int)

    def __init__(self, table_view, search_container):'''

    if old_class_start in content:
        content = content.replace(old_class_start, new_class_start)
        print("✓ Pridaný signal active_column_changed")
    else:
        print("❌ Nenašiel som QuickSearchController class start")
        return False

    # Emit signal in _change_column after setting current_column
    old_change = '''        self.current_column = new_column

        # Clear search text BEFORE sorting to avoid search during sort'''

    new_change = '''        self.current_column = new_column

        # Emit signal for BaseGrid to save
        self.active_column_changed.emit(new_column)

        # Clear search text BEFORE sorting to avoid search during sort'''

    if old_change in content:
        content = content.replace(old_change, new_change)
        print("✓ Pridaný emit() v _change_column()")
    else:
        print("❌ Nenašiel som _change_column() pattern")
        return False

    # Write back
    with open(QUICK_SEARCH, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"\n✓ Updated: {QUICK_SEARCH.relative_to(DEV_ROOT)}")
    return True


def fix_base_grid():
    """Pripoj signal v BaseGrid"""

    print("\n" + "=" * 80)
    print("FIX: base_grid.py - connect active_column_changed signal")
    print("=" * 80)

    with open(BASE_GRID, 'r', encoding='utf-8') as f:
        content = f.read()

    # Add connection in setup_quick_search
    old_setup = '''        self.search_controller = QuickSearchController(
            self.table_view, 
            self.quick_search_container
        )

        self.logger.info(f"Quick search setup complete for {self._grid_name}")'''

    new_setup = '''        self.search_controller = QuickSearchController(
            self.table_view, 
            self.quick_search_container
        )

        # Connect active column changed signal to save
        self.search_controller.active_column_changed.connect(self._on_active_column_changed)

        self.logger.info(f"Quick search setup complete for {self._grid_name}")'''

    if old_setup in content:
        content = content.replace(old_setup, new_setup)
        print("✓ Pripojený signal v setup_quick_search()")
    else:
        print("❌ Nenašiel som setup_quick_search() pattern")
        return False

    # Add handler method before _on_column_resized
    old_handler = '''    def _on_column_resized(self, logical_index, old_size, new_size):'''

    new_handler = '''    def _on_active_column_changed(self, column):
        """Handler pre zmenu active column."""
        print(f"[ACTIVE] Active column changed to {column} for {self._grid_name}")
        self._save_grid_settings()

    def _on_column_resized(self, logical_index, old_size, new_size):'''

    if old_handler in content:
        content = content.replace(old_handler, new_handler)
        print("✓ Pridaný handler _on_active_column_changed()")
    else:
        print("❌ Nenašiel som _on_column_resized()")
        return False

    # Write back
    with open(BASE_GRID, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"\n✓ Updated: {BASE_GRID.relative_to(DEV_ROOT)}")
    return True


def main():
    if not fix_quick_search():
        return

    if not fix_base_grid():
        return

    print("\n" + "=" * 80)
    print("HOTOVO - Active column change signal pridaný")
    print("=" * 80)
    print("\nTeraz:")
    print("  1. Vymaž DB: del C:\\NEX\\YEARACT\\SYSTEM\\SQLITE\\grid_settings.db")
    print("  2. Spusti aplikáciu")
    print("  3. Zmeň active column šípkami (→)")
    print("  4. Sleduj console - mali by sa objaviť [ACTIVE] a [DEBUG] výpisy")
    print("  5. Zatvor a znova spusti - active column by mal byť uložený")


if __name__ == "__main__":
    main()