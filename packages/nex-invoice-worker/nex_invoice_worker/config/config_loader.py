"""Supplier configuration loader.

Loads supplier API configuration from YAML files and environment variables.
"""

import os
from pathlib import Path

import yaml
from nex_invoice_worker.adapters.base_adapter import AuthType, SupplierConfig


class SupplierConfigError(Exception):
    pass


def get_suppliers_config_dir() -> Path:
    return Path(__file__).parent / "suppliers"


def load_supplier_config(supplier_id: str) -> SupplierConfig:
    config_dir = get_suppliers_config_dir()
    config_file = config_dir / f"{supplier_id}.yaml"

    if not config_file.exists():
        raise SupplierConfigError(
            f"Configuration file not found: {config_file}. Create it from _template.yaml"
        )

    try:
        with open(config_file, encoding="utf-8") as f:
            yaml_config = yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise SupplierConfigError(f"Invalid YAML in {config_file}: {e}")

    required_fields = ["supplier_id", "supplier_name", "auth_type"]
    for field in required_fields:
        if field not in yaml_config:
            raise SupplierConfigError(
                f"Missing required field '{field}' in {config_file}"
            )

    connection = yaml_config.get("connection", {})
    protocol = yaml_config.get("protocol", connection.get("protocol", "rest"))
    if protocol == "rest" and "base_url" not in yaml_config:
        raise SupplierConfigError(
            f"Missing 'base_url' for REST protocol in {config_file}"
        )
    if protocol == "soap" and not (
        connection.get("wsdl_url") or connection.get("wsdl_test")
    ):
        raise SupplierConfigError(
            f"Missing 'connection.wsdl_url' for SOAP protocol in {config_file}"
        )

    try:
        auth_type = AuthType(yaml_config["auth_type"])
    except ValueError:
        valid_types = [t.value for t in AuthType]
        raise SupplierConfigError(
            f"Invalid auth_type '{yaml_config['auth_type']}'. Valid types: {valid_types}"
        )

    env_prefix = supplier_id.upper()
    api_key = os.environ.get(f"{env_prefix}_API_KEY")
    username = os.environ.get(f"{env_prefix}_USERNAME")
    password = os.environ.get(f"{env_prefix}_PASSWORD")

    api_key_types = [
        AuthType.API_KEY,
        AuthType.API_KEY_HEADER,
        AuthType.API_KEY_QUERY,
        AuthType.API_KEY_BODY,
    ]
    if auth_type in api_key_types and not api_key:
        raise SupplierConfigError(
            f"Missing environment variable {env_prefix}_API_KEY for auth_type '{auth_type.value}'"
        )
    elif auth_type in [AuthType.BASIC, AuthType.BEARER] and (
        not username or not password
    ):
        raise SupplierConfigError(
            f"Missing environment variables {env_prefix}_USERNAME and/or "
            f"{env_prefix}_PASSWORD for auth_type '{auth_type.value}'"
        )

    endpoints = yaml_config.get("endpoints", {})
    product_code = yaml_config.get("product_code", {})
    request_config = yaml_config.get("request", {})
    response_config = yaml_config.get("response", {})
    wsdl_url = connection.get("wsdl_url") or connection.get("wsdl_test")

    return SupplierConfig(
        supplier_id=yaml_config["supplier_id"],
        supplier_name=yaml_config["supplier_name"],
        auth_type=auth_type,
        base_url=yaml_config.get("base_url", ""),
        endpoint_list_invoices=endpoints.get(
            "list_invoices", endpoints.get("invoice_list", "")
        ),
        endpoint_get_invoice=endpoints.get(
            "get_invoice", endpoints.get("invoice_detail", "")
        ),
        endpoint_acknowledge=endpoints.get(
            "acknowledge", endpoints.get("invoice_ack", "")
        ),
        product_code_field=product_code.get("xml_field", ""),
        product_code_type=product_code.get("type", ""),
        api_key=api_key,
        username=username,
        password=password,
        timeout_seconds=yaml_config.get("timeout_seconds", 30),
        max_retries=yaml_config.get("max_retries", 3),
        rate_limit_per_minute=yaml_config.get("rate_limit_per_minute", 60),
        protocol=protocol,
        wsdl_url=wsdl_url,
        soap_method=connection.get("method"),
        message_types=endpoints,
        request_params=request_config,
        response_format=response_config.get("format", "xml"),
    )


def list_available_suppliers() -> list[str]:
    config_dir = get_suppliers_config_dir()
    suppliers = []
    for yaml_file in config_dir.glob("*.yaml"):
        if yaml_file.name.startswith("_"):
            continue
        suppliers.append(yaml_file.stem)
    return sorted(suppliers)
