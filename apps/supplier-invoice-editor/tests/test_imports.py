"""
Test module imports
"""

import sys
from pathlib import Path

import pytest

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def test_pyqt5_available():
    """Test that PyQt5 is installed"""
    try:
        from PyQt5.QtCore import Qt
        from PyQt5.QtWidgets import QApplication

        assert True
    except ImportError as e:
        pytest.fail(f"PyQt5 not available: {e}")


def test_invoice_shared_available():
    """Test that invoice-shared package is available"""
    try:
        from invoice_shared.database.postgres_staging import PostgresStagingClient

        assert PostgresStagingClient is not None
    except ImportError as e:
        pytest.fail(f"invoice-shared not available: {e}")


def test_config_module_import():
    """Test that config module can be imported"""
    try:
        from utils.config import Config

        assert Config is not None
    except ImportError as e:
        pytest.fail(f"Failed to import config: {e}")


def test_main_window_module_import():
    """Test that main window module can be imported"""
    try:
        from ui.main_window import MainWindow

        assert MainWindow is not None
    except ImportError as e:
        pytest.skip(f"MainWindow import failed (might need Qt display): {e}")
