"""
Script 06: Cleanup quick_search.py - remove GreenHeaderView

Odstráni GreenHeaderView z quick_search.py lebo je už v BaseGrid.

Spustenie:
    python scripts\06-cleanup-quick-search.py
"""

import sys
from pathlib import Path
import shutil
from datetime import datetime

# Project root
project_root = Path(__file__).parent.parent


def cleanup_quick_search():
    """Vyčistí quick_search.py"""

    target_file = project_root / "apps" / "supplier-invoice-editor" / "src" / "ui" / "widgets" / "quick_search.py"

    print("=" * 80)
    print("CLEANING UP quick_search.py")
    print("=" * 80)

    print(f"\n1. Target file: {target_file}")

    if not target_file.exists():
        print("   ERROR: File not found!")
        return

    # Create backup
    backup_file = target_file.with_suffix(f'.py.backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
    shutil.copy2(target_file, backup_file)
    print(f"   ✓ Backup created: {backup_file.name}")

    # New cleaned content (removed GreenHeaderView, kept only QuickSearch components)
    cleaned_content = '''"""
Quick Search Widget - NEX Genesis style incremental search
Rýchlo-vyhľadávač v štýle NEX Genesis

Note: GreenHeaderView is now in nex-shared/ui/base_grid.py
"""

import logging
from PyQt5.QtWidgets import QLineEdit, QApplication, QWidget
from PyQt5.QtCore import Qt, pyqtSignal, QTimer, QEvent, QObject
from PyQt5.QtGui import QPalette, QColor

from ...utils.text_utils import normalize_for_search, is_numeric, normalize_numeric


class QuickSearchEdit(QLineEdit):
    """
    Quick search editor with NEX Genesis behavior

    Features:
    - Incremental prefix search
    - Case-insensitive, diacritic-insensitive
    - Numeric values compared as numbers
    - Arrow keys: ← → change column, ↑ ↓ move in list + clear
    - Beep on no match
    """

    # Signals
    search_text_changed = pyqtSignal(str)  # Search text changed
    column_change_requested = pyqtSignal(int)  # +1 or -1
    row_change_requested = pyqtSignal(int)  # +1 or -1

    def __init__(self, parent=None):
        super().__init__(parent)

        self.logger = logging.getLogger(__name__)

        # Setup appearance
        self._setup_appearance()

        # Connect signals
        self.textChanged.connect(self._on_text_changed)

    def _setup_appearance(self):
        """Setup green background and styling"""
        palette = self.palette()
        palette.setColor(QPalette.Base, QColor(144, 238, 144))  # Light green
        self.setPalette(palette)

        # Set fixed height
        self.setFixedHeight(25)

        # Set placeholder
        self.setPlaceholderText("Rýchlo-vyhľadávač...")

    def _on_text_changed(self, text):
        """Handle text change"""
        self.search_text_changed.emit(text)

    def keyPressEvent(self, event):
        """Handle key press events"""
        key = event.key()

        if key == Qt.Key_Left:
            # Move to previous column
            self.column_change_requested.emit(-1)
            event.accept()
            return

        elif key == Qt.Key_Right:
            # Move to next column
            self.column_change_requested.emit(1)
            event.accept()
            return

        elif key == Qt.Key_Up:
            # Move to previous row and clear search
            self.clear()
            self.row_change_requested.emit(-1)
            event.accept()
            return

        elif key == Qt.Key_Down:
            # Move to next row and clear search
            self.clear()
            self.row_change_requested.emit(1)
            event.accept()
            return

        # Default handling for other keys
        super().keyPressEvent(event)

    def trigger_beep(self):
        """Trigger system beep"""
        QApplication.beep()
        self.logger.debug("Search beep triggered (no match)")


class QuickSearchContainer(QWidget):
    """
    Container for quick search that positions editor under active column
    """

    def __init__(self, table_view, parent=None):
        super().__init__(parent)

        self.table_view = table_view
        self.logger = logging.getLogger(__name__)

        # Create search edit
        self.search_edit = QuickSearchEdit(self)

        # Set container height
        self.setFixedHeight(25)

        # Current column
        self.current_column = 0
        self._active_search_column = 0

        # Update position when table layout changes
        self.table_view.horizontalHeader().sectionResized.connect(self._update_position)

        # Initial position
        QTimer.singleShot(0, self._update_position)

    def _update_position(self):
        """Update editor position to match current column"""
        header = self.table_view.horizontalHeader()

        # Account for vertical header (row numbers)
        vertical_header_width = self.table_view.verticalHeader().width()

        # Get column position and width
        col_x = header.sectionViewportPosition(self.current_column) + vertical_header_width
        col_width = header.sectionSize(self.current_column)

        # Position editor under column
        self.search_edit.setGeometry(col_x, 0, col_width, 25)

        self.logger.debug(f"Search editor positioned: x={col_x}, width={col_width}, column={self.current_column}")

    def set_column(self, column):
        """Set active search column"""
        self.current_column = column
        self._update_position()
        self._highlight_header(column)

    def _highlight_header(self, column):
        """Highlight active column header with green background"""
        header = self.table_view.horizontalHeader()

        # Store active column
        self._active_search_column = column

        # Update custom header view if it has set_active_column method
        if hasattr(header, 'set_active_column'):
            header.set_active_column(column)
            self.logger.info(f"Header updated to column {column}")

        header.viewport().update()
        self.logger.info(f"Header highlighted for column {column}")


class QuickSearchController(QObject):
    """
    Controller for quick search functionality
    Handles search logic and table interaction
    """

    def __init__(self, table_view, search_container):
        """
        Initialize quick search controller

        Args:
            table_view: QTableView instance
            search_container: QuickSearchContainer instance
        """
        super().__init__()

        self.table_view = table_view
        self.search_container = search_container
        self.search_edit = search_container.search_edit
        self.logger = logging.getLogger(__name__)

        self.current_column = 0  # Current search column

        # Disable any existing sorting first
        self.table_view.setSortingEnabled(False)

        # Install event filter on table to intercept arrow keys
        self.table_view.installEventFilter(self)

        # Connect signals
        self._connect_signals()

        # Initial sort - explicitly sort by first column
        self._sort_by_column(self.current_column)

        # Update header highlight for initial column
        if hasattr(self.search_container, '_highlight_header'):
            self.search_container._highlight_header(self.current_column)

        # Give focus to search edit
        QTimer.singleShot(100, self.search_edit.setFocus)

    def eventFilter(self, obj, event):
        """Filter events from table view to redirect to search edit"""
        if obj == self.table_view and event.type() == QEvent.KeyPress:
            key = event.key()

            # Redirect arrow keys to search edit when it has content or for column navigation
            if key in (Qt.Key_Left, Qt.Key_Right):
                # Always handle left/right for column change
                self.search_edit.keyPressEvent(event)
                return True

            # Redirect printable characters to search edit
            if event.text() and event.text().isprintable():
                self.search_edit.setFocus()
                self.search_edit.keyPressEvent(event)
                return True

        return super(QuickSearchController, self).eventFilter(obj, event)

    def _connect_signals(self):
        """Connect widget signals"""
        self.search_edit.search_text_changed.connect(self._on_search)
        self.search_edit.column_change_requested.connect(self._change_column)
        self.search_edit.row_change_requested.connect(self._change_row)

    def _sort_by_column(self, column):
        """Sort table by column - force visual reordering"""
        model = self.table_view.model()
        if not model:
            self.logger.warning("No model available for sorting")
            return

        self.logger.info(f"Attempting to sort by column {column}")

        # Method 1: Use QSortFilterProxyModel if available
        # Check if we're already using a proxy
        if hasattr(model, 'sourceModel'):
            self.logger.info("Using proxy model for sorting")
            proxy = model
            proxy.sort(column, Qt.AscendingOrder)
        else:
            # Method 2: Direct model sorting
            self.logger.info("Using direct model sorting")

            # Disable sorting temporarily
            self.table_view.setSortingEnabled(False)

            # Enable sorting
            self.table_view.setSortingEnabled(True)

            # Sort by column
            self.table_view.sortByColumn(column, Qt.AscendingOrder)

            # If model has sort method, call it directly
            if hasattr(model, 'sort'):
                self.logger.info("Calling model.sort() directly")
                model.sort(column, Qt.AscendingOrder)

            # Force layout change signal
            model.layoutAboutToBeChanged.emit()
            model.layoutChanged.emit()

        # Update viewport
        self.table_view.viewport().update()
        self.table_view.update()

        # Scroll to top to see sort effect
        self.table_view.scrollToTop()

        self.logger.info(f"Table sorted by column {column} (ascending) - check visually")

    def _change_column(self, direction):
        """Change search column"""
        model = self.table_view.model()
        if not model:
            return

        column_count = model.columnCount()

        # Calculate new column
        new_column = self.current_column + direction

        # Wrap around
        if new_column < 0:
            new_column = column_count - 1
        elif new_column >= column_count:
            new_column = 0

        self.current_column = new_column

        # Clear search text BEFORE sorting to avoid search during sort
        self.search_edit.blockSignals(True)
        self.search_edit.clear()
        self.search_edit.blockSignals(False)

        # Sort by new column FIRST
        self._sort_by_column(self.current_column)

        # Then update container position and header highlight
        self.search_container.set_column(self.current_column)

        # Keep focus on search edit
        self.search_edit.setFocus()

        self.logger.info(f"Changed to column {self.current_column}, sorted and repositioned")

    def _change_row(self, direction):
        """Move to next/previous row"""
        selection_model = self.table_view.selectionModel()
        if not selection_model:
            return

        current = selection_model.currentIndex()
        if not current.isValid():
            # Select first row
            model = self.table_view.model()
            if model and model.rowCount() > 0:
                first_index = model.index(0, self.current_column)
                selection_model.setCurrentIndex(
                    first_index,
                    selection_model.ClearAndSelect | selection_model.Rows
                )
            return

        # Calculate new row
        model = self.table_view.model()
        row_count = model.rowCount()
        new_row = current.row() + direction

        # Clamp to valid range
        if new_row < 0:
            new_row = 0
        elif new_row >= row_count:
            new_row = row_count - 1

        # Select new row
        new_index = model.index(new_row, self.current_column)
        selection_model.setCurrentIndex(
            new_index,
            selection_model.ClearAndSelect | selection_model.Rows
        )

        # Ensure visible
        self.table_view.scrollTo(new_index)

        # Keep focus on search edit
        self.search_edit.setFocus()

        self.logger.debug(f"Moved to row {new_row}")

    def _on_search(self, search_text):
        """Handle search text change"""
        if not search_text:
            return

        model = self.table_view.model()
        if not model:
            return

        # Find matching row
        match_row = self._find_match(search_text, self.current_column)

        if match_row is not None:
            # Select matching row
            match_index = model.index(match_row, self.current_column)
            selection_model = self.table_view.selectionModel()
            selection_model.setCurrentIndex(
                match_index,
                selection_model.ClearAndSelect | selection_model.Rows
            )

            # Ensure visible
            self.table_view.scrollTo(match_index)

            self.logger.debug(f"Match found at row {match_row}")
        else:
            # No match - trigger beep and don't update display
            self.search_edit.trigger_beep()

            # Remove last character from search text
            current_text = self.search_edit.text()
            if current_text:
                self.search_edit.blockSignals(True)
                self.search_edit.setText(current_text[:-1])
                self.search_edit.blockSignals(False)

            self.logger.debug(f"No match for '{search_text}'")

    def _find_match(self, search_text, column):
        """
        Find first row matching search text (prefix)

        Args:
            search_text: Text to search for
            column: Column index to search in

        Returns:
            Row index or None if no match
        """
        model = self.table_view.model()
        row_count = model.rowCount()

        # Determine if searching numeric or text
        search_is_numeric = is_numeric(search_text)

        if search_is_numeric:
            # Numeric search
            search_normalized = normalize_numeric(search_text)

            for row in range(row_count):
                index = model.index(row, column)
                cell_value = model.data(index, Qt.DisplayRole)

                if cell_value and is_numeric(str(cell_value)):
                    cell_normalized = normalize_numeric(str(cell_value))

                    # Prefix match
                    if cell_normalized.startswith(search_normalized):
                        return row
        else:
            # Text search (case-insensitive, diacritic-insensitive)
            search_normalized = normalize_for_search(search_text)

            for row in range(row_count):
                index = model.index(row, column)
                cell_value = model.data(index, Qt.DisplayRole)

                if cell_value:
                    cell_normalized = normalize_for_search(str(cell_value))

                    # Prefix match
                    if cell_normalized.startswith(search_normalized):
                        return row

        return None

    def get_active_column(self):
        """
        Vráti index aktuálne aktívneho stĺpca.

        Returns:
            int: Index aktívneho stĺpca
        """
        return self.current_column

    def set_active_column(self, column):
        """
        Nastaví aktívny stĺpec a aktualizuje UI.

        Args:
            column: Index stĺpca
        """
        if 0 <= column < self.table_view.model().columnCount():
            self.current_column = column
            self._sort_by_column(column)
            self.search_container.set_column(column)
            self.logger.info(f"Active column set to {column}")

    def set_column(self, column):
        """Set active search column programmatically"""
        self.current_column = column
        self.search_container.set_column(column)
        self.search_edit.clear()
        self._sort_by_column(column)
'''

    # Write cleaned file
    target_file.write_text(cleaned_content, encoding='utf-8')
    print(f"\n2. ✓ Cleaned file saved")

    # Summary
    print("\n3. Changes made:")
    print("   ✓ Removed GreenHeaderView class (now in BaseGrid)")
    print("   ✓ Removed HighlightHeaderView class (unused)")
    print("   ✓ Kept QuickSearchEdit")
    print("   ✓ Kept QuickSearchContainer")
    print("   ✓ Kept QuickSearchController")
    print("   ✓ Updated header highlight logic to use external GreenHeaderView")

    print("\n" + "=" * 80)
    print("CLEANUP COMPLETE")
    print("=" * 80)
    print("\nNext step: Test the application")
    print("  cd apps/supplier-invoice-editor")
    print("  python main.py")


if __name__ == "__main__":
    cleanup_quick_search()