"""
Tests for core config module.
"""

import os
from pathlib import Path
from unittest.mock import patch

import pytest


class TestSettings:
    """Tests for Settings class."""

    def test_default_settings(self):
        """Test default settings values."""
        from src.core.config import Settings

        settings = Settings()

        assert settings.api_title == "Btrieve-Loader API"
        assert settings.api_version == "1.0.0"
        assert settings.api_prefix == "/api/v1"
        assert settings.port == 8001
        assert settings.host == "0.0.0.0"
        assert settings.debug is False
        assert settings.btrieve_encoding == "cp852"
        assert settings.default_page_size == 50
        assert settings.max_page_size == 1000

    def test_settings_from_env(self, monkeypatch):
        """Test settings loaded from environment variables."""
        from src.core.config import Settings

        monkeypatch.setenv("API_KEY", "test-key-123")
        monkeypatch.setenv("PORT", "9000")
        monkeypatch.setenv("DEBUG", "true")

        settings = Settings()

        assert settings.api_key == "test-key-123"
        assert settings.port == 9000
        assert settings.debug is True

    def test_settings_btrieve_path(self, monkeypatch, tmp_path):
        """Test btrieve_path setting."""
        from src.core.config import Settings

        test_path = tmp_path / "btrieve"
        monkeypatch.setenv("BTRIEVE_PATH", str(test_path))

        settings = Settings()

        assert settings.btrieve_path == test_path

    def test_btrieve_config_property(self):
        """Test btrieve_config property generates correct dict."""
        from src.core.config import Settings

        settings = Settings(
            btrieve_path=Path("/test/stores"),
            btrieve_dials_path=Path("/test/dials"),
        )

        config = settings.btrieve_config

        assert config["database_path"] == "/test/stores"
        assert "nex_genesis" in config
        assert "tables" in config["nex_genesis"]
        assert "gscat" in config["nex_genesis"]["tables"]
        assert "pab" in config["nex_genesis"]["tables"]

    def test_get_settings_cached(self):
        """Test get_settings returns cached instance."""
        from src.core.config import get_settings

        settings1 = get_settings()
        settings2 = get_settings()

        assert settings1 is settings2

    def test_settings_case_insensitive(self, monkeypatch):
        """Test settings are case insensitive."""
        from src.core.config import Settings

        monkeypatch.setenv("API_TITLE", "Custom Title")
        settings = Settings()

        assert settings.api_title == "Custom Title"


class TestSettingsValidation:
    """Tests for settings validation."""

    def test_port_validation(self):
        """Test port accepts valid values."""
        from src.core.config import Settings

        settings = Settings(port=8080)
        assert settings.port == 8080

    def test_page_size_defaults(self):
        """Test pagination defaults."""
        from src.core.config import Settings

        settings = Settings()

        assert settings.default_page_size == 50
        assert settings.max_page_size == 1000
