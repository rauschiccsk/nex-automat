"""Tests for QuickSearch."""

import pytest
from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtWidgets import QTableView
from shared_pyside6.ui import GreenHeaderView, QuickSearchContainer, QuickSearchController, QuickSearchEdit
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
