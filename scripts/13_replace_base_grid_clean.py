"""
Replace: Nahradí rozhádzaný base_grid.py čistou verziou
Location: C:\Development\nex-automat\scripts\13_replace_base_grid_clean.py
"""
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).parent
DEV_ROOT = SCRIPT_DIR.parent
BASE_GRID = DEV_ROOT / "packages" / "nex-shared" / "ui" / "base_grid.py"

# Čistá verzia - copy from artifact
CLEAN_CONTENT = '''"""
BaseGrid - univerzálna base trieda pre všetky gridy
Automatická grid persistence (column widths, active column, quick search).
"""
import logging
from typing import List, Tuple, Optional
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableView, QHeaderView, QAbstractItemView
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPalette, QColor, QPainter, QPen

logger = logging.getLogger(__name__)


class GreenHeaderView(QHeaderView):
    """Custom QHeaderView s green highlighting pre active column"""

    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)
        self.active_column = 0

    def paintSection(self, painter, rect, logicalIndex):
        """Custom paint pre každý header section"""
        painter.save()

        # Background color
        if logicalIndex == self.active_column:
            painter.fillRect(rect, QColor(144, 238, 144))  # Light green
        else:
            painter.fillRect(rect, QColor(240, 240, 240))  # Light gray

        # Border
        painter.setPen(QPen(QColor(160, 160, 160)))
        painter.drawLine(rect.topRight(), rect.bottomRight())
        painter.drawLine(rect.bottomLeft(), rect.bottomRight())

        # Text
        text = self.model().headerData(logicalIndex, self.orientation(), Qt.DisplayRole)
        painter.setPen(QPen(QColor(0, 0, 0)))
        painter.drawText(rect, Qt.AlignCenter, str(text) if text else "")

        painter.restore()

    def set_active_column(self, column):
        """Nastav ktorý column je active pre search"""
        self.active_column = column
        self.viewport().update()


class BaseGrid(QWidget):
    """
    Base trieda pre všetky gridy v NEX Automat systéme.

    Automaticky:
    - Vytvorí QTableView s GreenHeaderView
    - Pridá QuickSearchContainer (musí byť importovaný potomkom)
    - Načíta column settings pri inicializácii
    - Uloží column settings pri zmene
    - Persistence active column

    Použitie:
        class MyGrid(BaseGrid):
            def __init__(self, parent=None):
                super().__init__(
                    window_name="my_window",
                    grid_name="my_grid",
                    parent=parent
                )
                # Create model
                self.model = MyModel()
                self.table_view.setModel(self.model)

                # Špecifická logika
                self._setup_custom_stuff()
    """

    def __init__(self,
                 window_name: str,
                 grid_name: str,
                 user_id: str = "Server",
                 auto_load: bool = True,
                 parent=None):
        """
        Inicializácia BaseGrid.

        Args:
            window_name: Identifikátor okna (napr. "sie_main_window")
            grid_name: Identifikátor gridu (napr. "invoice_list")
            user_id: User ID pre multi-user support
            auto_load: Ak True, automaticky načíta settings
            parent: Parent widget
        """
        super().__init__(parent)

        # Store parameters
        self._window_name = window_name
        self._grid_name = grid_name
        self._user_id = user_id

        # Logger
        self.logger = logging.getLogger(__name__)

        # Create UI
        self._setup_base_ui()

        # Auto-load settings (po nastavení modelu potomkom)
        self._auto_load = auto_load

        self.logger.info(f"BaseGrid initialized: {window_name}/{grid_name}")

    def _setup_base_ui(self):
        """Setup základného UI s QTableView a QuickSearch."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Create table view
        self.table_view = QTableView()

        # Replace header with custom green header
        custom_header = GreenHeaderView(Qt.Horizontal, self.table_view)
        self.table_view.setHorizontalHeader(custom_header)

        # Basic table settings
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_view.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table_view.setSortingEnabled(False)  # QuickSearchController enabled sorting

        layout.addWidget(self.table_view)

        # Placeholder pre QuickSearch - bude pridaný potomkom
        self.quick_search_container = None
        self.search_controller = None

        # Connect header signals pre grid settings
        header = self.table_view.horizontalHeader()
        header.sectionResized.connect(self._on_column_resized)
        header.sectionMoved.connect(self._on_column_moved)

    def setup_quick_search(self, QuickSearchContainer, QuickSearchController):
        """
        Setup quick search functionality.

        MUSÍ byť zavolaný potomkom ABY fungoval quick search.

        Args:
            QuickSearchContainer: Trieda QuickSearchContainer z widgets
            QuickSearchController: Trieda QuickSearchController z widgets
        """
        # Add quick search container
        self.quick_search_container = QuickSearchContainer(self.table_view, self)
        self.layout().addWidget(self.quick_search_container)

        # Create quick search controller
        self.search_controller = QuickSearchController(
            self.table_view, 
            self.quick_search_container
        )

        self.logger.info(f"Quick search setup complete for {self._grid_name}")

    def _load_grid_settings(self):
        """Načíta a aplikuje uložené nastavenia gridu."""
        print(f"[LOAD] _load_grid_settings called: {self._window_name}/{self._grid_name}")

        header = self.table_view.horizontalHeader()

        try:
            # Disconnect signals during load to prevent recursive save
            header.sectionResized.disconnect(self._on_column_resized)
            header.sectionMoved.disconnect(self._on_column_moved)

            # Import grid_settings functions
            from ..utils.grid_settings import load_column_settings, load_grid_settings

            model = self.table_view.model()
            if not model:
                self.logger.warning("No model set, skipping grid settings load")
                return

            # Load column settings
            column_settings = load_column_settings(
                self._window_name, 
                self._grid_name, 
                self._user_id
            )

            print(f"[LOAD] column_settings loaded: {column_settings is not None}")
            if column_settings:
                print(f"[LOAD] Found {len(column_settings)} column settings")

                # Aplikuj nastavenia pre každý stĺpec
                for col_idx in range(model.columnCount()):
                    # Get column name from model
                    col_name = model.headerData(col_idx, Qt.Horizontal, Qt.DisplayRole)

                    # Nájdi nastavenia pre tento stĺpec
                    col_settings = next(
                        (s for s in column_settings if s.get('column_name') == col_name), 
                        None
                    )

                    if col_settings:
                        print(f"[LOAD] Applying settings for column {col_idx}: {col_name} - width={col_settings.get('width')}")
                        # Šírka stĺpca
                        if 'width' in col_settings:
                            header.resizeSection(col_idx, col_settings['width'])

                        # Vizuálny index (poradie)
                        if 'visual_index' in col_settings:
                            header.moveSection(
                                header.visualIndex(col_idx), 
                                col_settings['visual_index']
                            )

                        # Viditeľnosť
                        if 'visible' in col_settings:
                            self.table_view.setColumnHidden(
                                col_idx, 
                                not col_settings['visible']
                            )

                self.logger.info(
                    f"Loaded column settings for {self._window_name}/{self._grid_name}"
                )

            # Load grid settings (active column pre quick search)
            grid_settings = load_grid_settings(
                self._window_name, 
                self._grid_name, 
                self._user_id
            )

            if grid_settings and 'active_column_index' in grid_settings:
                print(f"[LOAD] Found grid settings, active_column={grid_settings['active_column_index']}")
                active_col = grid_settings['active_column_index']

                # Nastav aktívny stĺpec v quick search
                if self.search_controller:
                    self.search_controller.set_active_column(active_col)
                    self.logger.info(
                        f"Loaded active column: {active_col} for {self._grid_name}"
                    )

        except Exception as e:
            self.logger.error(f"Error loading grid settings: {e}")

        finally:
            # Reconnect signals after load
            header.sectionResized.connect(self._on_column_resized)
            header.sectionMoved.connect(self._on_column_moved)

    def _save_grid_settings(self):
        """Uloží aktuálne nastavenia gridu."""
        print(f"[DEBUG] _save_grid_settings called: {self._window_name}/{self._grid_name}")
        try:
            # Import grid_settings functions
            from ..utils.grid_settings import save_column_settings, save_grid_settings

            model = self.table_view.model()
            if not model:
                print(f"[DEBUG] No model for {self._window_name}/{self._grid_name}")
                self.logger.warning("No model set, skipping grid settings save")
                return
            print(f"[DEBUG] Model OK, columns: {model.columnCount()}")

            header = self.table_view.horizontalHeader()

            # Zozbieraj column settings
            column_settings = []
            for col_idx in range(model.columnCount()):
                col_name = model.headerData(col_idx, Qt.Horizontal, Qt.DisplayRole)
                column_settings.append({
                    'column_name': col_name,
                    'width': header.sectionSize(col_idx),
                    'visual_index': header.visualIndex(col_idx),
                    'visible': not self.table_view.isColumnHidden(col_idx)
                })

            # Uloží column settings
            print(f"[DEBUG] Saving {len(column_settings)} columns for {self._grid_name}")
            save_column_settings(
                self._window_name, 
                self._grid_name, 
                column_settings, 
                self._user_id
            )
            print(f"[DEBUG] Column settings saved")

            # Zozbieraj grid settings (active column)
            active_column = None
            if self.search_controller:
                active_column = self.search_controller.get_active_column()

            # Uloží grid settings
            if active_column is not None:
                print(f"[DEBUG] Saving active column: {active_column}")
                save_grid_settings(
                    self._window_name, 
                    self._grid_name, 
                    active_column, 
                    self._user_id
                )
                print(f"[DEBUG] Grid settings saved")
            else:
                print(f"[DEBUG] No active column to save (search_controller={self.search_controller})")

            self.logger.debug(
                f"Saved grid settings for {self._window_name}/{self._grid_name}"
            )

        except Exception as e:
            self.logger.error(f"Error saving grid settings: {e}")

    def _on_column_resized(self, logical_index, old_size, new_size):
        """Handler pre zmenu šírky stĺpca."""
        self._save_grid_settings()

    def _on_column_moved(self, logical_index, old_visual_index, new_visual_index):
        """Handler pre presunutie stĺpca."""
        self._save_grid_settings()

    # Public API

    def apply_model_and_load_settings(self):
        """
        Aplikuje settings PO nastavení modelu.

        MUSÍ byť zavolaný potomkom PO self.table_view.setModel()!
        """
        if self._auto_load:
            # Delayed load (aby bol model fully ready)
            QTimer.singleShot(0, self._load_grid_settings)

    def save_grid_settings_now(self):
        """Manuálne uloženie grid settings (napr. pri Apply button)."""
        self._save_grid_settings()

    def reload_grid_settings(self):
        """Manuálne reload grid settings."""
        self._load_grid_settings()

    @property
    def window_name(self) -> str:
        """Vráti window name."""
        return self._window_name

    @property
    def grid_name(self) -> str:
        """Vráti grid name."""
        return self._grid_name
'''


def replace():
    """Nahradí base_grid.py čistou verziou"""

    print("=" * 80)
    print("REPLACE: base_grid.py s čistou verziou")
    print("=" * 80)

    # Write clean content
    with open(BASE_GRID, 'w', encoding='utf-8') as f:
        f.write(CLEAN_CONTENT)

    print(f"\n✓ File replaced: {BASE_GRID.relative_to(DEV_ROOT)}")
    print("\nTeraz:")
    print("  1. Spusti aplikáciu - syntax error by mal byť vyriešený")
    print("  2. Testuj active column persistence")


if __name__ == "__main__":
    replace()