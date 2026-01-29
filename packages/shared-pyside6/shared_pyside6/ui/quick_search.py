"""
QuickSearch - NEX Genesis style incremental search.
PySide6 version for NEX Automat.
"""

import winsound
from typing import TYPE_CHECKING

from PySide6.QtCore import QEvent, QObject, Qt, Signal
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QLineEdit, QTableView, QWidget

from shared_pyside6.utils.text_utils import is_numeric, normalize_for_search

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
    row_change_requested = Signal(int)  # -1 = up, +1 = down

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self._setup_appearance()
        self.textChanged.connect(self._on_text_changed)

    def _setup_appearance(self) -> None:
        """Setup green background and styling."""
        self.setStyleSheet("""
            QLineEdit {
                background-color: #90EE90;
                color: #000000;
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

    def __init__(self, table_view: QTableView, parent: QWidget | None = None):
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
        self, table_view: QTableView, search_container: QuickSearchContainer, header: "GreenHeaderView | None" = None
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
        """Change search column using visual order."""
        model = self._table_view.model()
        if not model:
            return

        header = self._table_view.horizontalHeader()
        col_count = model.columnCount()

        # Get current visual index from logical index
        current_visual = header.visualIndex(self._active_column)

        # Move in visual order
        new_visual = current_visual + direction

        # Wrap around
        if new_visual < 0:
            new_visual = col_count - 1
        elif new_visual >= col_count:
            new_visual = 0

        # Convert visual to logical index
        new_logical = header.logicalIndex(new_visual)

        # Skip hidden columns (in visual order)
        attempts = 0
        while self._table_view.isColumnHidden(new_logical) and attempts < col_count:
            new_visual += direction
            if new_visual < 0:
                new_visual = col_count - 1
            elif new_visual >= col_count:
                new_visual = 0
            new_logical = header.logicalIndex(new_visual)
            attempts += 1

        # Clear search text when changing column
        self._search_container.search_edit.clear()

        self.set_active_column(new_logical)

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
                    search_num = float(search_text.replace(",", "."))
                    cell_num = float(cell_str.replace(",", "."))
                    if str(cell_num).startswith(str(search_num).rstrip("0").rstrip(".")):
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

        # Auto-sort by new active column (ascending)
        self._sort_by_column(column)

        self.active_column_changed.emit(column)

    def _sort_by_column(self, column: int) -> None:
        """Sort table by column ascending."""
        model = self._table_view.model()
        if model and hasattr(model, "sort"):
            model.sort(column, Qt.SortOrder.AscendingOrder)

    def set_column(self, column: int) -> None:
        """Alias for set_active_column."""
        self.set_active_column(column)
