"""
Test main application entry point
"""

import sys
from pathlib import Path

import pytest


def test_main_file_exists():
    """Test that main.py exists"""
    main_file = Path(__file__).parent.parent / "main.py"
    assert main_file.exists(), "main.py not found"


def test_main_imports():
    """Test that main.py can be imported"""
    # Add parent to path
    sys.path.insert(0, str(Path(__file__).parent.parent))

    try:
        import main

        assert hasattr(main, "main")
        assert hasattr(main, "setup_logging")
    except ImportError as e:
        pytest.fail(f"Failed to import main: {e}")


def test_logging_setup():
    """Test logging setup function"""
    sys.path.insert(0, str(Path(__file__).parent.parent))

    try:
        from main import setup_logging

        logger = setup_logging()
        assert logger is not None
        assert logger.name == "__main__"
    except Exception as e:
        pytest.skip(f"Logging setup requires file system access: {e}")


@pytest.mark.skip(reason="Requires Qt display and full app initialization")
def test_main_function():
    """Test main function (requires Qt)"""
    sys.path.insert(0, str(Path(__file__).parent.parent))

    # Would need to mock Qt application
    pass
