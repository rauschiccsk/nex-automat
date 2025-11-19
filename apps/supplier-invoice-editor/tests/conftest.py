# -*- coding: utf-8 -*-
"""
pytest configuration for supplier-invoice-editor
"""
import pytest
import sys
from pathlib import Path

# Add src to path for all tests
sys.path.insert(0, str(Path(__file__).parent / "src"))


@pytest.fixture
def app_root():
    """Return application root directory"""
    return Path(__file__).parent


@pytest.fixture
def config_dir(app_root):
    """Return config directory"""
    return app_root / "config"


@pytest.fixture
def src_dir(app_root):
    """Return src directory"""
    return app_root / "src"
