"""Test that all imports work correctly."""


def test_pyside6_available():
    """Test that PySide6 is installed."""
    import PySide6

    assert PySide6 is not None


def test_package_import():
    """Test that package can be imported."""
    import shared_pyside6

    assert shared_pyside6.__version__ == "1.0.0"


def test_ui_imports():
    """Test UI component imports."""
    from shared_pyside6.ui import BaseGrid, BaseWindow

    assert BaseWindow is not None
    assert BaseGrid is not None
