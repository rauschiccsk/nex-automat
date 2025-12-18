"""
Fix BaseGrid to accept settings_db_path parameter and pass it to SettingsRepository.
Also update supplier-invoice-staging app to use local settings.db.
"""

from pathlib import Path

# === FILE 1: base_grid.py ===
BASE_GRID_FILE = Path("packages/shared-pyside6/shared_pyside6/ui/base_grid.py")

# Update __init__ signature
OLD_INIT_SIG = '''    def __init__(
        self,
        window_name: str,
        grid_name: str,
        user_id: str = "default",
        auto_load: bool = True,
        parent: QWidget | None = None
    ):
        """
        Initialize BaseGrid.

        Args:
            window_name: Window identifier (e.g., "staging_main")
            grid_name: Grid identifier (e.g., "invoice_list")
            user_id: User ID for multi-user support
            auto_load: If True, automatically load settings after model set
            parent: Parent widget
        """
        super().__init__(parent)

        self._window_name = window_name
        self._grid_name = grid_name
        self._user_id = user_id
        self._auto_load = auto_load
        self._repository = SettingsRepository()'''

NEW_INIT_SIG = '''    def __init__(
        self,
        window_name: str,
        grid_name: str,
        user_id: str = "default",
        auto_load: bool = True,
        settings_db_path: str | Path | None = None,
        parent: QWidget | None = None
    ):
        """
        Initialize BaseGrid.

        Args:
            window_name: Window identifier (e.g., "staging_main")
            grid_name: Grid identifier (e.g., "invoice_list")
            user_id: User ID for multi-user support
            auto_load: If True, automatically load settings after model set
            settings_db_path: Path to settings.db (default: ~/.nex-automat/settings.db)
            parent: Parent widget
        """
        super().__init__(parent)

        self._window_name = window_name
        self._grid_name = grid_name
        self._user_id = user_id
        self._auto_load = auto_load
        self._repository = SettingsRepository(settings_db_path)'''

# === FILE 2: main_window.py ===
MAIN_WINDOW_FILE = Path("apps/supplier-invoice-staging/ui/main_window.py")

OLD_GRID_INIT = '''        # Grid
        self.grid = BaseGrid(
            window_name=self.WINDOW_ID,
            grid_name=self.GRID_NAME,
            parent=self
        )'''

NEW_GRID_INIT = '''        # Grid
        self.grid = BaseGrid(
            window_name=self.WINDOW_ID,
            grid_name=self.GRID_NAME,
            settings_db_path=self.settings.get_settings_db_path(),
            parent=self
        )'''

# === FILE 3: invoice_items_window.py ===
ITEMS_WINDOW_FILE = Path("apps/supplier-invoice-staging/ui/invoice_items_window.py")

OLD_ITEMS_GRID_INIT = '''        # Grid
        self.grid = BaseGrid(
            window_name=self.WINDOW_ID,
            grid_name=self.GRID_NAME,
            parent=self
        )'''

NEW_ITEMS_GRID_INIT = '''        # Grid
        self.grid = BaseGrid(
            window_name=self.WINDOW_ID,
            grid_name=self.GRID_NAME,
            settings_db_path=self.settings.get_settings_db_path(),
            parent=self
        )'''


def update_file(filepath: Path, replacements: list) -> bool:
    if not filepath.exists():
        print(f"ERROR: {filepath} not found!")
        return False

    content = filepath.read_text(encoding="utf-8")
    changed = False

    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
            print(f"  Updated in {filepath.name}")
            changed = True

    if changed:
        filepath.write_text(content, encoding="utf-8")
        print(f"Saved: {filepath}")
    else:
        print(f"No changes needed: {filepath}")

    return changed


def main():
    print("=== Updating base_grid.py ===")
    update_file(BASE_GRID_FILE, [(OLD_INIT_SIG, NEW_INIT_SIG)])

    print("\n=== Updating main_window.py ===")
    update_file(MAIN_WINDOW_FILE, [(OLD_GRID_INIT, NEW_GRID_INIT)])

    print("\n=== Updating invoice_items_window.py ===")
    update_file(ITEMS_WINDOW_FILE, [(OLD_ITEMS_GRID_INIT, NEW_ITEMS_GRID_INIT)])

    print("\nDone!")


if __name__ == "__main__":
    main()