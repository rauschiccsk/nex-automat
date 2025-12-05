#!/usr/bin/env python3
"""
Script to create quick_search.py - universal quick search widget
Vytvára apps/supplier-invoice-editor/src/ui/widgets/quick_search.py
Location: C:\\Development\\nex-automat\\scripts\\02_create_quick_search.py
"""

import sys
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).parent.parent

# Target file
TARGET_FILE = PROJECT_ROOT / "apps" / "supplier-invoice-editor" / "src" / "ui" / "widgets" / "quick_search.py"

# File content
CONTENT = '''"""
Quick Search Widget - NEX Genesis style incremental search
Rýchlo-vyhľadávač v štýle NEX Genesis
"""

import logging
from PyQt5.QtWidgets import QLineEdit, QApplication
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPalette, QColor

from utils.text_utils import normalize_for_search, is_numeric, normalize_numeric


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


class QuickSearchController:
    """
    Controller for quick search functionality
    Handles search logic and table interaction
    """

    def __init__(self, table_view, search_edit):
        """
        Initialize quick search controller

        Args:
            table_view: QTableView instance
            search_edit: QuickSearchEdit instance
        """
        self.table_view = table_view
        self.search_edit = search_edit
        self.logger = logging.getLogger(__name__)

        self.current_column = 0  # Current search column

        # Connect signals
        self._connect_signals()

        # Initial sort
        self._sort_by_column(self.current_column)

    def _connect_signals(self):
        """Connect widget signals"""
        self.search_edit.search_text_changed.connect(self._on_search)
        self.search_edit.column_change_requested.connect(self._change_column)
        self.search_edit.row_change_requested.connect(self._change_row)

    def _sort_by_column(self, column):
        """Sort table by column"""
        self.table_view.sortByColumn(column, Qt.AscendingOrder)
        self.logger.debug(f"Sorted by column {column}")

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

        # Clear search text
        self.search_edit.clear()

        # Sort by new column
        self._sort_by_column(self.current_column)

        self.logger.debug(f"Changed to column {self.current_column}")

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

    def set_column(self, column):
        """Set active search column programmatically"""
        self.current_column = column
        self.search_edit.clear()
        self._sort_by_column(column)
'''


def main():
    """Create quick_search.py file"""
    try:
        # Create parent directory if needed
        TARGET_FILE.parent.mkdir(parents=True, exist_ok=True)

        # Check if file exists
        if TARGET_FILE.exists():
            print(f"⚠️  File already exists: {TARGET_FILE}")
            print("File will be overwritten.")

        # Write file
        TARGET_FILE.write_text(CONTENT, encoding='utf-8')

        print(f"✅ Created: {TARGET_FILE}")
        print(f"📊 Size: {TARGET_FILE.stat().st_size} bytes")
        print(f"📝 Lines: {len(CONTENT.splitlines())}")

        return 0

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())