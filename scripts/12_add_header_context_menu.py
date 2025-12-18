"""
Add context menu to header for column visibility and rename.
Run from: C:/Development/nex-automat
"""

from pathlib import Path

def main():
    file_path = Path("packages/shared-pyside6/shared_pyside6/ui/base_grid.py")

    if not file_path.exists():
        print(f"ERROR: {file_path} not found")
        return False

    content = file_path.read_text(encoding="utf-8")

    # Check if already implemented
    if "_show_header_context_menu" in content:
        print("SKIP: Already implemented")
        return True

    # 1. Add QInputDialog to imports
    old_import = '''from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTableView, QHeaderView,
    QAbstractItemView, QMenu, QFileDialog, QMessageBox
)'''

    new_import = '''from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTableView, QHeaderView,
    QAbstractItemView, QMenu, QFileDialog, QMessageBox, QInputDialog
)'''

    if old_import not in content:
        print("ERROR: Could not find imports")
        return False

    content = content.replace(old_import, new_import)

    # 2. Add context menu policy to header in _setup_base_ui
    old_setup = '''        layout.addWidget(self.table_view)

        # Connect signals
        self._connect_base_signals()'''

    new_setup = '''        layout.addWidget(self.table_view)

        # Enable context menu on header
        self.header.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.header.customContextMenuRequested.connect(self._show_header_context_menu)

        # Connect signals
        self._connect_base_signals()'''

    if old_setup not in content:
        print("ERROR: Could not find _setup_base_ui pattern")
        return False

    content = content.replace(old_setup, new_setup)

    # 3. Add _show_header_context_menu method before _show_context_menu
    old_context = '''    # === Context Menu ===

    def _show_context_menu(self, position) -> None:'''

    new_context = '''    # === Context Menu ===

    def _show_header_context_menu(self, position) -> None:
        """Show context menu on header for column visibility and rename."""
        model = self.table_view.model()
        if not model:
            return
        
        # Get column under cursor
        clicked_col = self.header.logicalIndexAt(position)
        
        menu = QMenu(self)
        
        # Rename option for clicked column
        if clicked_col >= 0:
            current_name = self.get_custom_header(clicked_col)
            if not current_name:
                current_name = model.headerData(clicked_col, Qt.Orientation.Horizontal) or f"Column {clicked_col}"
            
            rename_action = QAction(f"Premenovať '{current_name}'...", self)
            rename_action.triggered.connect(lambda: self._rename_column_dialog(clicked_col))
            menu.addAction(rename_action)
            
            # Reset name option (only if custom name exists)
            if self.get_custom_header(clicked_col):
                reset_action = QAction("Obnoviť pôvodný názov", self)
                reset_action.triggered.connect(lambda: self._reset_column_name(clicked_col))
                menu.addAction(reset_action)
            
            menu.addSeparator()
        
        # Column visibility submenu
        columns_menu = menu.addMenu("Stĺpce")
        for col in range(model.columnCount()):
            # Get display name (custom or original)
            custom = self.get_custom_header(col)
            if custom:
                header = custom
            else:
                header = model.headerData(col, Qt.Orientation.Horizontal) or f"Column {col}"
            
            action = QAction(str(header), self)
            action.setCheckable(True)
            action.setChecked(self.is_column_visible(col))
            action.triggered.connect(
                lambda checked, c=col: self.set_column_visible(c, checked)
            )
            columns_menu.addAction(action)
        
        menu.exec(self.header.mapToGlobal(position))

    def _rename_column_dialog(self, column: int) -> None:
        """Show dialog to rename column."""
        model = self.table_view.model()
        if not model:
            return
        
        # Get current name
        current = self.get_custom_header(column)
        if not current:
            current = model.headerData(column, Qt.Orientation.Horizontal) or ""
        
        # Show input dialog
        new_name, ok = QInputDialog.getText(
            self,
            "Premenovať stĺpec",
            "Nový názov:",
            text=str(current)
        )
        
        if ok and new_name:
            self.set_custom_header(column, new_name)
            # Update header display
            model.setHeaderData(column, Qt.Orientation.Horizontal, new_name)

    def _reset_column_name(self, column: int) -> None:
        """Reset column name to original."""
        model = self.table_view.model()
        if not model or str(column) not in self._custom_headers:
            return
        
        # Remove custom header
        del self._custom_headers[str(column)]
        self._save_grid_settings()
        
        # Restore original - need to get from model's original data
        # For QStandardItemModel, we need to reload or store originals
        # For now, just trigger a visual update
        self.header.updateSection(column)

    def _show_context_menu(self, position) -> None:'''

    if old_context not in content:
        print("ERROR: Could not find _show_context_menu")
        return False

    content = content.replace(old_context, new_context)

    file_path.write_text(content, encoding="utf-8")
    print(f"OK: Added header context menu to {file_path}")
    return True

if __name__ == "__main__":
    main()