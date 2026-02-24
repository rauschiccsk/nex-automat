"""Tests for BaseGrid."""

import os
import tempfile
from pathlib import Path

import pytest
from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItem, QStandardItemModel
from shared_pyside6.database import SettingsRepository
from shared_pyside6.ui import BaseGrid, GreenHeaderView


@pytest.fixture
def temp_db():
    """Create temporary database path."""
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    os.unlink(path)
    yield Path(path)
    try:
        if Path(path).exists():
            os.unlink(path)
    except:
        pass


@pytest.fixture
def repository(temp_db):
    """Create repository with temp database."""
    SettingsRepository._instances.clear()
    repo = SettingsRepository(temp_db)
    yield repo
    repo.close()


@pytest.fixture
def sample_model():
    """Create sample model with test data."""
    model = QStandardItemModel(5, 3)
    model.setHorizontalHeaderLabels(["ID", "Name", "Value"])

    for row in range(5):
        model.setItem(row, 0, QStandardItem(f"ID-{row}"))
        model.setItem(row, 1, QStandardItem(f"Name {row}"))
        model.setItem(row, 2, QStandardItem(str(row * 100)))

    return model


class TestGreenHeaderView:
    """Tests for GreenHeaderView."""

    def test_set_active_column(self, qtbot):
        """Test setting active column."""
        header = GreenHeaderView(Qt.Orientation.Horizontal)

        header.set_active_column(2)
        assert header._active_column == 2

        header.set_active_column(0)
        assert header._active_column == 0


class TestBaseGrid:
    """Tests for BaseGrid."""

    def test_create_grid(self, qtbot, repository):
        """Test creating BaseGrid."""
        grid = BaseGrid(
            window_name="test_window", grid_name="test_grid", user_id="test_user"
        )
        qtbot.addWidget(grid)

        assert grid.window_name == "test_window"
        assert grid.grid_name == "test_grid"
        assert grid.table_view is not None
        assert grid.header is not None

    def test_set_model(self, qtbot, repository, sample_model):
        """Test setting model and loading settings."""
        grid = BaseGrid(
            window_name="test_window", grid_name="test_grid", user_id="test_user"
        )
        qtbot.addWidget(grid)

        grid.table_view.setModel(sample_model)
        grid.apply_model_and_load_settings()

        assert grid.table_view.model() == sample_model

    def test_column_visibility(self, qtbot, repository, sample_model):
        """Test column visibility."""
        grid = BaseGrid(
            window_name="test_window", grid_name="test_grid", user_id="test_user"
        )
        qtbot.addWidget(grid)
        grid.table_view.setModel(sample_model)

        # Hide column 1
        grid.set_column_visible(1, False)
        assert not grid.is_column_visible(1)
        assert grid.is_column_visible(0)

        # Show column 1
        grid.set_column_visible(1, True)
        assert grid.is_column_visible(1)

    def test_get_visible_columns(self, qtbot, repository, sample_model):
        """Test getting visible columns."""
        grid = BaseGrid(
            window_name="test_window", grid_name="test_grid", user_id="test_user"
        )
        qtbot.addWidget(grid)
        grid.table_view.setModel(sample_model)

        # All visible by default
        visible = grid.get_visible_columns()
        assert visible == [0, 1, 2]

        # Hide column 1
        grid.set_column_visible(1, False)
        visible = grid.get_visible_columns()
        assert visible == [0, 2]

    def test_active_column(self, qtbot, repository, sample_model):
        """Test active column."""
        grid = BaseGrid(
            window_name="test_window", grid_name="test_grid", user_id="test_user"
        )
        qtbot.addWidget(grid)
        grid.table_view.setModel(sample_model)

        grid.set_active_column(2)
        assert grid.get_active_column() == 2
        assert grid.header._active_column == 2

    def test_custom_headers(self, qtbot, repository, sample_model):
        """Test custom headers."""
        grid = BaseGrid(
            window_name="test_window", grid_name="test_grid", user_id="test_user"
        )
        qtbot.addWidget(grid)
        grid.table_view.setModel(sample_model)

        grid.set_custom_header(1, "Custom Name")
        assert grid.get_custom_header(1) == "Custom Name"
        assert grid.get_custom_header(0) is None

        grid.reset_headers()
        assert grid.get_custom_header(1) is None

    def test_row_id_column(self, qtbot, repository, sample_model):
        """Test row ID column for cursor memory."""
        grid = BaseGrid(
            window_name="test_window", grid_name="test_grid", user_id="test_user"
        )
        qtbot.addWidget(grid)
        grid.table_view.setModel(sample_model)

        grid.set_row_id_column(0)  # ID column
        grid.table_view.selectRow(2)
        grid._save_cursor_position()

        assert grid._last_row_id == "ID-2"

    def test_settings_persistence(self, qtbot, repository, sample_model):
        """Test that settings are saved and loaded."""
        # Create grid and change settings
        grid1 = BaseGrid(
            window_name="test_window", grid_name="test_grid", user_id="test_user"
        )
        qtbot.addWidget(grid1)
        grid1.table_view.setModel(sample_model)
        grid1.apply_model_and_load_settings()

        grid1.set_active_column(2)
        grid1.set_column_visible(1, False)
        grid1.set_custom_header(0, "Identifier")
        grid1.save_grid_settings_now()

        # Create new grid - should load saved settings
        grid2 = BaseGrid(
            window_name="test_window", grid_name="test_grid", user_id="test_user"
        )
        qtbot.addWidget(grid2)
        grid2.table_view.setModel(sample_model)
        grid2.apply_model_and_load_settings()

        assert grid2.get_active_column() == 2
        assert not grid2.is_column_visible(1)
        assert grid2.get_custom_header(0) == "Identifier"
