"""Supplier configuration loader.

Loads supplier API configuration from YAML files and environment variables.
"""

import os
from pathlib import Path

import yaml

from adapters.base_adapter import AuthType, SupplierConfig


class SupplierConfigError(Exception):
    """Raised when supplier configuration cannot be loaded."""

    pass


def get_suppliers_config_dir() -> Path:
    """Get the path to suppliers configuration directory."""
    return Path(__file__).parent / "suppliers"


def load_supplier_config(supplier_id: str) -> SupplierConfig:
    """
    Load supplier configuration from YAML file and environment variables.

    Args:
        supplier_id: Supplier identifier (e.g., "marso", "continental").

    Returns:
        SupplierConfig instance with all configuration loaded.

    Raises:
        SupplierConfigError: If configuration file not found or invalid.
    """
    config_dir = get_suppliers_config_dir()
    config_file = config_dir / f"{supplier_id}.yaml"

    if not config_file.exists():
        raise SupplierConfigError(
            f"Configuration file not found: {config_file}. "
            f"Create it from _template.yaml"
        )

    # Load YAML file
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            yaml_config = yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise SupplierConfigError(f"Invalid YAML in {config_file}: {e}")

    # Validate required fields
    required_fields = ["supplier_id", "supplier_name", "auth_type", "base_url", "endpoints"]
    for field in required_fields:
        if field not in yaml_config:
            raise SupplierConfigError(f"Missing required field '{field}' in {config_file}")

    # Parse auth_type
    try:
        auth_type = AuthType(yaml_config["auth_type"])
    except ValueError:
        valid_types = [t.value for t in AuthType]
        raise SupplierConfigError(
            f"Invalid auth_type '{yaml_config['auth_type']}'. "
            f"Valid types: {valid_types}"
        )

    # Load credentials from environment variables
    # Format: {SUPPLIER_ID}_API_KEY, {SUPPLIER_ID}_USERNAME, etc.
    env_prefix = supplier_id.upper()

    api_key = os.environ.get(f"{env_prefix}_API_KEY")
    username = os.environ.get(f"{env_prefix}_USERNAME")
    password = os.environ.get(f"{env_prefix}_PASSWORD")

    # Validate credentials based on auth_type
    if auth_type == AuthType.API_KEY and not api_key:
        raise SupplierConfigError(
            f"Missing environment variable {env_prefix}_API_KEY for auth_type 'api_key'"
        )
    elif auth_type == AuthType.BASIC and (not username or not password):
        raise SupplierConfigError(
            f"Missing environment variables {env_prefix}_USERNAME and/or "
            f"{env_prefix}_PASSWORD for auth_type 'basic'"
        )

    # Extract endpoints
    endpoints = yaml_config.get("endpoints", {})

    # Extract product_code configuration
    product_code = yaml_config.get("product_code", {})

    # Build SupplierConfig
    return SupplierConfig(
        supplier_id=yaml_config["supplier_id"],
        supplier_name=yaml_config["supplier_name"],
        auth_type=auth_type,
        base_url=yaml_config["base_url"],
        endpoint_list_invoices=endpoints.get("list_invoices", ""),
        endpoint_get_invoice=endpoints.get("get_invoice", ""),
        endpoint_acknowledge=endpoints.get("acknowledge", ""),
        product_code_field=product_code.get("xml_field", ""),
        product_code_type=product_code.get("type", ""),
        api_key=api_key,
        username=username,
        password=password,
        timeout_seconds=yaml_config.get("timeout_seconds", 30),
        max_retries=yaml_config.get("max_retries", 3),
        rate_limit_per_minute=yaml_config.get("rate_limit_per_minute", 60),
    )


def list_available_suppliers() -> list[str]:
    """
    List all available supplier configurations.

    Returns:
        List of supplier IDs (filenames without .yaml extension).
    """
    config_dir = get_suppliers_config_dir()
    suppliers = []

    for yaml_file in config_dir.glob("*.yaml"):
        # Skip template file
        if yaml_file.name.startswith("_"):
            continue
        suppliers.append(yaml_file.stem)

    return sorted(suppliers)
