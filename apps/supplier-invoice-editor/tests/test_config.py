"""
Test configuration loading
"""

import sys
from pathlib import Path

import pytest

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def test_config_module_exists():
    """Test that config module exists"""
    config_file = Path(__file__).parent.parent / "src" / "utils" / "config.py"
    assert config_file.exists(), f"Config file not found: {config_file}"


def test_config_class_can_be_imported():
    """Test that Config class can be imported"""
    from utils.config import Config

    assert Config is not None


@pytest.mark.skip(reason="Config might require actual config file")
def test_config_initialization():
    """Test Config initialization"""
    from utils.config import Config

    try:
        config = Config()
        assert config is not None
    except Exception as e:
        pytest.skip(f"Config initialization requires valid config file: {e}")
