"""Tests for config/config_loader.py"""

import os
import tempfile
from pathlib import Path
from unittest import mock

import pytest
import yaml

from adapters.base_adapter import AuthType
from config.config_loader import (
    SupplierConfigError,
    get_suppliers_config_dir,
    list_available_suppliers,
    load_supplier_config,
)


class TestLoadSupplierConfig:
    """Tests for load_supplier_config function."""

    def test_load_marso_yaml_success(self):
        """Test loading marso.yaml with valid credentials."""
        # Set required env variable for api_key auth
        with mock.patch.dict(os.environ, {"MARSO_API_KEY": "test-api-key-123"}):
            config = load_supplier_config("marso")

            assert config.supplier_id == "marso"
            assert config.supplier_name == "MARSO Slovakia s.r.o."
            assert config.auth_type == AuthType.API_KEY
            assert config.base_url == "https://api.marso.sk"
            assert config.endpoint_list_invoices == "/invoices?status=pending"
            assert config.endpoint_get_invoice == "/invoices/{invoice_id}"
            assert config.endpoint_acknowledge == "/invoices/{invoice_id}/ack"
            assert config.product_code_field == "MarsoCode"
            assert config.product_code_type == "marso_code"
            assert config.api_key == "test-api-key-123"
            assert config.timeout_seconds == 30
            assert config.max_retries == 3

    def test_load_missing_file_raises_error(self):
        """Test that loading non-existent supplier raises SupplierConfigError."""
        with pytest.raises(SupplierConfigError) as exc_info:
            load_supplier_config("nonexistent_supplier")

        assert "Configuration file not found" in str(exc_info.value)
        assert "nonexistent_supplier.yaml" in str(exc_info.value)

    def test_load_missing_api_key_raises_error(self):
        """Test that missing API key env variable raises SupplierConfigError."""
        # Ensure MARSO_API_KEY is not set
        env_without_key = {k: v for k, v in os.environ.items() if k != "MARSO_API_KEY"}

        with mock.patch.dict(os.environ, env_without_key, clear=True):
            with pytest.raises(SupplierConfigError) as exc_info:
                load_supplier_config("marso")

            assert "MARSO_API_KEY" in str(exc_info.value)

    def test_credentials_loaded_from_env_variables(self):
        """Test that credentials are correctly loaded from environment variables."""
        test_env = {
            "MARSO_API_KEY": "my-secret-api-key",
            "MARSO_USERNAME": "test-user",
            "MARSO_PASSWORD": "test-pass",
        }

        with mock.patch.dict(os.environ, test_env):
            config = load_supplier_config("marso")

            assert config.api_key == "my-secret-api-key"
            assert config.username == "test-user"
            assert config.password == "test-pass"


class TestLoadSupplierConfigWithTempFiles:
    """Tests using temporary YAML files."""

    def test_load_basic_auth_requires_username_and_password(self, tmp_path):
        """Test that basic auth type requires username and password."""
        yaml_content = {
            "supplier_id": "test_supplier",
            "supplier_name": "Test Supplier",
            "auth_type": "basic",
            "base_url": "https://api.test.com",
            "endpoints": {
                "list_invoices": "/invoices",
                "get_invoice": "/invoices/{id}",
                "acknowledge": "/invoices/{id}/ack",
            },
            "product_code": {
                "xml_field": "EAN",
                "type": "ean",
            },
        }

        # Create temp config file
        config_dir = tmp_path / "suppliers"
        config_dir.mkdir()
        config_file = config_dir / "test_supplier.yaml"
        config_file.write_text(yaml.dump(yaml_content))

        with mock.patch(
            "config.config_loader.get_suppliers_config_dir", return_value=config_dir
        ):
            # Test without credentials - should fail
            with mock.patch.dict(os.environ, {}, clear=True):
                with pytest.raises(SupplierConfigError) as exc_info:
                    load_supplier_config("test_supplier")

                assert "TEST_SUPPLIER_USERNAME" in str(exc_info.value)

            # Test with credentials - should succeed
            with mock.patch.dict(
                os.environ,
                {"TEST_SUPPLIER_USERNAME": "user", "TEST_SUPPLIER_PASSWORD": "pass"},
            ):
                config = load_supplier_config("test_supplier")
                assert config.auth_type == AuthType.BASIC
                assert config.username == "user"
                assert config.password == "pass"

    def test_invalid_auth_type_raises_error(self, tmp_path):
        """Test that invalid auth_type raises SupplierConfigError."""
        yaml_content = {
            "supplier_id": "bad_auth",
            "supplier_name": "Bad Auth Supplier",
            "auth_type": "invalid_type",
            "base_url": "https://api.test.com",
            "endpoints": {
                "list_invoices": "/invoices",
                "get_invoice": "/invoices/{id}",
                "acknowledge": "/invoices/{id}/ack",
            },
        }

        config_dir = tmp_path / "suppliers"
        config_dir.mkdir()
        config_file = config_dir / "bad_auth.yaml"
        config_file.write_text(yaml.dump(yaml_content))

        with mock.patch(
            "config.config_loader.get_suppliers_config_dir", return_value=config_dir
        ):
            with pytest.raises(SupplierConfigError) as exc_info:
                load_supplier_config("bad_auth")

            assert "Invalid auth_type" in str(exc_info.value)
            assert "invalid_type" in str(exc_info.value)

    def test_missing_required_field_raises_error(self, tmp_path):
        """Test that missing required fields raise SupplierConfigError."""
        yaml_content = {
            "supplier_id": "incomplete",
            # Missing: supplier_name, auth_type, base_url, endpoints
        }

        config_dir = tmp_path / "suppliers"
        config_dir.mkdir()
        config_file = config_dir / "incomplete.yaml"
        config_file.write_text(yaml.dump(yaml_content))

        with mock.patch(
            "config.config_loader.get_suppliers_config_dir", return_value=config_dir
        ):
            with pytest.raises(SupplierConfigError) as exc_info:
                load_supplier_config("incomplete")

            assert "Missing required field" in str(exc_info.value)


class TestListAvailableSuppliers:
    """Tests for list_available_suppliers function."""

    def test_list_available_suppliers_returns_marso(self):
        """Test that marso is in the list of available suppliers."""
        suppliers = list_available_suppliers()

        assert "marso" in suppliers

    def test_list_excludes_template_file(self):
        """Test that _template.yaml is not included in the list."""
        suppliers = list_available_suppliers()

        assert "_template" not in suppliers
        for supplier in suppliers:
            assert not supplier.startswith("_")

    def test_list_returns_sorted(self):
        """Test that the list is sorted alphabetically."""
        suppliers = list_available_suppliers()

        assert suppliers == sorted(suppliers)

    def test_list_with_multiple_suppliers(self, tmp_path):
        """Test listing multiple supplier configs."""
        config_dir = tmp_path / "suppliers"
        config_dir.mkdir()

        # Create multiple config files
        (config_dir / "aaa_supplier.yaml").write_text("supplier_id: aaa")
        (config_dir / "zzz_supplier.yaml").write_text("supplier_id: zzz")
        (config_dir / "middle_supplier.yaml").write_text("supplier_id: middle")
        (config_dir / "_template.yaml").write_text("# template")

        with mock.patch(
            "config.config_loader.get_suppliers_config_dir", return_value=config_dir
        ):
            suppliers = list_available_suppliers()

            assert suppliers == ["aaa_supplier", "middle_supplier", "zzz_supplier"]
            assert "_template" not in suppliers


class TestGetSuppliersConfigDir:
    """Tests for get_suppliers_config_dir function."""

    def test_returns_path_object(self):
        """Test that function returns a Path object."""
        result = get_suppliers_config_dir()

        assert isinstance(result, Path)

    def test_path_ends_with_suppliers(self):
        """Test that path ends with 'suppliers' directory."""
        result = get_suppliers_config_dir()

        assert result.name == "suppliers"

    def test_path_exists(self):
        """Test that the suppliers config directory exists."""
        result = get_suppliers_config_dir()

        assert result.exists()
        assert result.is_dir()
