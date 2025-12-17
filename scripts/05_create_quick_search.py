#!/usr/bin/env python
"""
Create QuickSearch for shared-pyside6 package.
Phase 5 of PySide6 migration.
"""
from pathlib import Path

BASE_DIR = Path(r"C:\Development\nex-automat")
PACKAGE_DIR = BASE_DIR / "packages" / "shared-pyside6" / "shared_pyside6"
TESTS_DIR = BASE_DIR / "packages" / "shared-pyside6" / "tests"


def create_file(path: Path, content: str) -> None:
    """Create file with content."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"✅ Created: {path.relative_to(BASE_DIR)}")


def main():
    print("=" * 60)
    print("Phase 5: Creating QuickSearch for PySide6")
    print("=" * 60)

    # === Text Utils ===
    create_file(PACKAGE_DIR / "utils" / "text_utils.py", '''"""
Text utilities for normalization and comparison.
Used by QuickSearch for diacritic-insensitive search.
"""
import unicodedata


def remove_diacritics(text: str) -> str:
    """
    Remove diacritical marks from text.

    Converts: "Žeľazničný" -> "Zelaznicny"

    Args:
        text: Input text with diacritics

    Returns:
        Text without diacritical marks
    """
    if not text:
        return text

    # Normalize to NFD (decomposed form), remove combining marks
    normalized = unicodedata.normalize('NFD', text)
    return ''.join(
        char for char in normalized 
        if unicodedata.category(char) != 'Mn'
    )


def normalize_for_search(text: str) -> str:
    """
    Normalize text for search comparison.
    - Remove diacritics
    - Convert to lowercase
    - Strip whitespace

    Args:
        text: Input text

    Returns:
        Normalized text suitable for comparison
    """
    if not text:
        return ""
    return remove_diacritics(str(text)).lower().strip()


def is_numeric(text: str) -> bool:
    """
    Check if text represents a number.

    Args:
        text: Input text

    Returns:
        True if text is numeric
    """
    if not text:
        return False
    try:
        float(str(text).replace(',', '.'))
        return True
    except ValueError:
        return False


def normalize_numeric(text: str) -> str:
    """
    Normalize numeric text for comparison.
    - Convert comma to dot
    - Strip whitespace

    Args:
        text: Numeric text

    Returns:
        Normalized numeric string
    """
    if not text:
        return ""
    return str(text).replace(',', '.').strip()
''')

    # === QuickSearch ===
    create_file(PACKAGE_DIR / "ui" / "quick_search.py", '''"""
QuickSearch - NEX Genesis style incremental search.
PySide6 version for NEX Automat.
"""
import winsound
from typing import TYPE_CHECKING

from PySide6.QtWidgets import QLineEdit, QWidget, QTableView
from PySide6.QtCore import Qt, QObject, Signal, QEvent
from PySide6.QtGui import QKeyEvent

from shared_pyside6.utils.text_utils import normalize_for_search, is_numeric

if TYPE_CHECKING:
    from shared_pyside6.ui.base_grid import GreenHeaderView


class QuickSearchEdit(QLineEdit):
    """
    Quick search editor with NEX Genesis behavior.

    Features:
    - Incremental prefix search
    - Case-insensitive, diacritic-insensitive
    - Numeric values compared as numbers
    - Arrow keys: ← → change column, ↑ ↓ move in list + clear
    - Beep on no match

    Signals:
        search_text_changed: Emitted when search text changes
        column_change_requested: Emitted when arrow left/right pressed
        row_change_requested: Emitted when arrow up/down pressed
    """

    search_text_changed = Signal(str)
    column_change_requested = Signal(int)  # -1 = left, +1 = right
    row_change_requested = Signal(int)     # -1 = up, +1 = down

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self._setup_appearance()
        self.textChanged.connect(self._on_text_changed)

    def _setup_appearance(self) -> None:
        """Setup green background and styling."""
        self.setStyleSheet("""
            QLineEdit {
                background-color: #90EE90;
                border: 1px solid #228B22;
                padding: 2px 4px;
                font-size: 12px;
            }
        """)
        self.setFixedHeight(22)
        self.setPlaceholderText("Search...")

    def _on_text_changed(self, text: str) -> None:
        """Handle text change."""
        self.search_text_changed.emit(text)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """Handle key press events."""
        key = event.key()

        if key == Qt.Key.Key_Left:
            if self.cursorPosition() == 0 or not self.text():
                self.column_change_requested.emit(-1)
                return

        elif key == Qt.Key.Key_Right:
            if self.cursorPosition() == len(self.text()) or not self.text():
                self.column_change_requested.emit(1)
                return

        elif key == Qt.Key.Key_Up:
            self.clear()
            self.row_change_requested.emit(-1)
            return

        elif key == Qt.Key.Key_Down:
            self.clear()
            self.row_change_requested.emit(1)
            return

        elif key == Qt.Key.Key_Escape:
            self.clear()
            return

        elif key == Qt.Key.Key_Return or key == Qt.Key.Key_Enter:
            # Enter confirms selection, clear search
            self.clear()
            return

        super().keyPressEvent(event)

    def trigger_beep(self) -> None:
        """Trigger system beep on no match."""
        try:
            winsound.MessageBeep(winsound.MB_OK)
        except:
            pass  # Ignore if winsound not available


class QuickSearchContainer(QWidget):
    """
    Container for quick search that positions editor under active column.
    """

    def __init__(
        self, 
        table_view: QTableView,
        parent: QWidget | None = None
    ):
        super().__init__(parent)
        self._table_view = table_view
        self._current_column = 0

        # Create search edit
        self.search_edit = QuickSearchEdit(self)

        # Position initially
        self._update_position()

    def _update_position(self) -> None:
        """Update editor position to match current column."""
        header = self._table_view.horizontalHeader()
        if not header:
            return

        # Get column position and width
        x = header.sectionPosition(self._current_column)
        width = header.sectionSize(self._current_column)

        # Account for horizontal scroll
        x -= self._table_view.horizontalScrollBar().value()

        # Position search edit
        self.search_edit.setGeometry(x, 0, min(width, 200), 22)
        self.setFixedHeight(24)

    def set_column(self, column: int) -> None:
        """Set active search column."""
        model = self._table_view.model()
        if model and 0 <= column < model.columnCount():
            self._current_column = column
            self._update_position()

    def get_column(self) -> int:
        """Get current search column."""
        return self._current_column

    def resizeEvent(self, event) -> None:
        """Handle resize to update position."""
        super().resizeEvent(event)
        self._update_position()


class QuickSearchController(QObject):
    """
    Controller for quick search functionality.
    Handles search logic and table interaction.

    Signals:
        active_column_changed: Emitted when active column changes
    """

    active_column_changed = Signal(int)

    def __init__(
        self,
        table_view: QTableView,
        search_container: QuickSearchContainer,
        header: "GreenHeaderView | None" = None
    ):
        """
        Initialize quick search controller.

        Args:
            table_view: QTableView instance
            search_container: QuickSearchContainer instance
            header: Optional GreenHeaderView for highlighting
        """
        super().__init__()
        self._table_view = table_view
        self._search_container = search_container
        self._header = header
        self._active_column = 0

        self._connect_signals()

        # Install event filter on table view
        table_view.installEventFilter(self)

    def _connect_signals(self) -> None:
        """Connect widget signals."""
        edit = self._search_container.search_edit

        edit.search_text_changed.connect(self._on_search)
        edit.column_change_requested.connect(self._change_column)
        edit.row_change_requested.connect(self._change_row)

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        """Filter events from table view to redirect typing to search edit."""
        if obj == self._table_view and event.type() == QEvent.Type.KeyPress:
            key_event = event
            key = key_event.key()

            # Redirect alphanumeric keys to search edit
            if key_event.text() and key_event.text().isprintable():
                edit = self._search_container.search_edit
                edit.setFocus()
                edit.setText(edit.text() + key_event.text())
                return True

            # Arrow keys for navigation
            if key == Qt.Key.Key_Left:
                self._change_column(-1)
                return True
            elif key == Qt.Key.Key_Right:
                self._change_column(1)
                return True

        return super().eventFilter(obj, event)

    def _change_column(self, direction: int) -> None:
        """Change search column."""
        model = self._table_view.model()
        if not model:
            return

        new_column = self._active_column + direction

        # Wrap around
        if new_column < 0:
            new_column = model.columnCount() - 1
        elif new_column >= model.columnCount():
            new_column = 0

        # Skip hidden columns
        while self._table_view.isColumnHidden(new_column):
            new_column += direction
            if new_column < 0:
                new_column = model.columnCount() - 1
            elif new_column >= model.columnCount():
                new_column = 0

        self.set_active_column(new_column)

    def _change_row(self, direction: int) -> None:
        """Move to next/previous row."""
        model = self._table_view.model()
        if not model:
            return

        current = self._table_view.currentIndex()
        new_row = current.row() + direction

        if 0 <= new_row < model.rowCount():
            self._table_view.selectRow(new_row)

    def _on_search(self, search_text: str) -> None:
        """Handle search text change."""
        if not search_text:
            return

        match_row = self._find_match(search_text, self._active_column)

        if match_row is not None:
            self._table_view.selectRow(match_row)
        else:
            self._search_container.search_edit.trigger_beep()

    def _find_match(self, search_text: str, column: int) -> int | None:
        """
        Find first row matching search text (prefix).

        Args:
            search_text: Text to search for
            column: Column index to search in

        Returns:
            Row index or None if no match
        """
        model = self._table_view.model()
        if not model:
            return None

        normalized_search = normalize_for_search(search_text)
        search_is_numeric = is_numeric(search_text)

        for row in range(model.rowCount()):
            index = model.index(row, column)
            cell_value = model.data(index, Qt.ItemDataRole.DisplayRole)

            if cell_value is None:
                continue

            cell_str = str(cell_value)

            # Numeric comparison
            if search_is_numeric and is_numeric(cell_str):
                try:
                    search_num = float(search_text.replace(',', '.'))
                    cell_num = float(cell_str.replace(',', '.'))
                    if str(cell_num).startswith(str(search_num).rstrip('0').rstrip('.')):
                        return row
                except ValueError:
                    pass

            # Text prefix comparison (diacritic-insensitive)
            normalized_cell = normalize_for_search(cell_str)
            if normalized_cell.startswith(normalized_search):
                return row

        return None

    def get_active_column(self) -> int:
        """Get active column index."""
        return self._active_column

    def set_active_column(self, column: int) -> None:
        """Set active column and update UI."""
        self._active_column = column
        self._search_container.set_column(column)

        if self._header:
            self._header.set_active_column(column)

        self.active_column_changed.emit(column)

    def set_column(self, column: int) -> None:
        """Alias for set_active_column."""
        self.set_active_column(column)
''')

    # === Update utils/__init__.py ===
    create_file(PACKAGE_DIR / "utils" / "__init__.py", '''"""
Utility functions for NEX Automat.
"""
from shared_pyside6.utils.text_utils import (
    remove_diacritics,
    normalize_for_search,
    is_numeric,
    normalize_numeric
)

__all__ = [
    "remove_diacritics",
    "normalize_for_search",
    "is_numeric",
    "normalize_numeric"
]
''')

    # === Update ui/__init__.py ===
    create_file(PACKAGE_DIR / "ui" / "__init__.py", '''"""
UI components for NEX Automat.

Classes:
    BaseWindow: Base class for all windows with persistence
    BaseGrid: Base class for all grids with advanced features
    GreenHeaderView: Custom header with green highlighting
    QuickSearchEdit: Quick search input widget
    QuickSearchContainer: Container for quick search
    QuickSearchController: Controller for quick search logic
"""
from shared_pyside6.ui.base_window import BaseWindow
from shared_pyside6.ui.base_grid import BaseGrid, GreenHeaderView
from shared_pyside6.ui.quick_search import (
    QuickSearchEdit,
    QuickSearchContainer,
    QuickSearchController
)

__all__ = [
    "BaseWindow",
    "BaseGrid",
    "GreenHeaderView",
    "QuickSearchEdit",
    "QuickSearchContainer",
    "QuickSearchController",
]
''')

    # === Test for QuickSearch ===
    create_file(TESTS_DIR / "test_quick_search.py", '''"""Tests for QuickSearch."""
import pytest

from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QTableView

from shared_pyside6.ui import (
    QuickSearchEdit,
    QuickSearchContainer,
    QuickSearchController,
    GreenHeaderView
)
from shared_pyside6.utils import normalize_for_search, remove_diacritics


class TestTextUtils:
    """Tests for text utilities."""

    def test_remove_diacritics(self):
        """Test diacritic removal."""
        assert remove_diacritics("Žltý") == "Zlty"
        assert remove_diacritics("čučoriedka") == "cucoriedka"
        assert remove_diacritics("ŇUŇUŇ") == "NUNUN"
        assert remove_diacritics("ABC") == "ABC"

    def test_normalize_for_search(self):
        """Test search normalization."""
        assert normalize_for_search("  ŽLTÝ Čaj  ") == "zlty caj"
        assert normalize_for_search("Košice") == "kosice"
        assert normalize_for_search("") == ""


class TestQuickSearchEdit:
    """Tests for QuickSearchEdit."""

    def test_create_edit(self, qtbot):
        """Test creating QuickSearchEdit."""
        edit = QuickSearchEdit()
        qtbot.addWidget(edit)

        assert edit.text() == ""
        assert edit.height() == 22

    def test_text_changed_signal(self, qtbot):
        """Test search_text_changed signal."""
        edit = QuickSearchEdit()
        qtbot.addWidget(edit)

        with qtbot.waitSignal(edit.search_text_changed, timeout=1000):
            edit.setText("test")


class TestQuickSearchContainer:
    """Tests for QuickSearchContainer."""

    def test_create_container(self, qtbot):
        """Test creating QuickSearchContainer."""
        table = QTableView()
        qtbot.addWidget(table)

        container = QuickSearchContainer(table)
        qtbot.addWidget(container)

        assert container.search_edit is not None
        assert container.get_column() == 0

    def test_set_column(self, qtbot):
        """Test setting column."""
        table = QTableView()
        model = QStandardItemModel(3, 3)
        table.setModel(model)
        qtbot.addWidget(table)

        container = QuickSearchContainer(table)
        qtbot.addWidget(container)

        container.set_column(2)
        assert container.get_column() == 2


class TestQuickSearchController:
    """Tests for QuickSearchController."""

    @pytest.fixture
    def setup_controller(self, qtbot):
        """Setup table with controller."""
        table = QTableView()
        header = GreenHeaderView(Qt.Orientation.Horizontal)
        table.setHorizontalHeader(header)

        model = QStandardItemModel(5, 3)
        model.setHorizontalHeaderLabels(["ID", "Name", "City"])

        # Add test data
        data = [
            ("1", "Adam", "Košice"),
            ("2", "Béla", "Bratislava"),
            ("3", "Cyril", "České Budějovice"),
            ("4", "Dávid", "Debrecín"),
            ("5", "Emil", "Eger"),
        ]
        for row, (id_, name, city) in enumerate(data):
            model.setItem(row, 0, QStandardItem(id_))
            model.setItem(row, 1, QStandardItem(name))
            model.setItem(row, 2, QStandardItem(city))

        table.setModel(model)
        qtbot.addWidget(table)

        container = QuickSearchContainer(table)
        qtbot.addWidget(container)

        controller = QuickSearchController(table, container, header)

        return table, container, controller

    def test_create_controller(self, setup_controller):
        """Test creating controller."""
        table, container, controller = setup_controller

        assert controller.get_active_column() == 0

    def test_set_active_column(self, setup_controller):
        """Test setting active column."""
        table, container, controller = setup_controller

        controller.set_active_column(2)

        assert controller.get_active_column() == 2
        assert container.get_column() == 2

    def test_find_match_text(self, setup_controller):
        """Test finding text match."""
        table, container, controller = setup_controller

        # Search for "Cy" in Name column
        controller.set_active_column(1)
        row = controller._find_match("Cy", 1)

        assert row == 2  # Cyril

    def test_find_match_diacritic_insensitive(self, setup_controller):
        """Test diacritic-insensitive search."""
        table, container, controller = setup_controller

        # Search for "Kosice" (without diacritics) in City column
        controller.set_active_column(2)
        row = controller._find_match("Kosice", 2)

        assert row == 0  # Košice

    def test_find_match_no_match(self, setup_controller):
        """Test no match found."""
        table, container, controller = setup_controller

        row = controller._find_match("XYZ", 1)

        assert row is None
''')

    print()
    print("=" * 60)
    print("✅ Phase 5 complete!")
    print("=" * 60)
    print()
    print("Created files:")
    print("  - shared_pyside6/utils/text_utils.py")
    print("  - shared_pyside6/ui/quick_search.py")
    print("  - shared_pyside6/utils/__init__.py")
    print("  - shared_pyside6/ui/__init__.py (updated)")
    print("  - tests/test_quick_search.py")
    print()
    print("Run tests:")
    print("  cd packages/shared-pyside6")
    print("  python -m pytest tests/test_quick_search.py -v")
    print()


if __name__ == "__main__":
    main()