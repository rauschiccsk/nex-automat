"""Supplier API Activities - Temporal activities for supplier API integration.

These activities handle communication with supplier APIs (MARSO, CONTINENTAL, etc.)
for fetching and processing invoices.
"""

from dataclasses import asdict

from temporalio import activity

from config.config_loader import SupplierConfigError
from config.config_loader import load_supplier_config as _load_config


@activity.defn
async def load_supplier_config(supplier_id: str) -> dict:
    """
    Load supplier configuration from YAML file.

    Args:
        supplier_id: Supplier identifier (e.g., "marso", "continental").

    Returns:
        SupplierConfig as dict (serialized for Temporal).

    Raises:
        SupplierConfigError: If configuration cannot be loaded.
    """
    activity.logger.info(f"Loading config for supplier: {supplier_id}")

    try:
        config = _load_config(supplier_id)
        # Convert to dict for Temporal serialization
        # AuthType enum needs to be converted to string
        config_dict = asdict(config)
        config_dict["auth_type"] = config.auth_type.value
        activity.logger.info(f"Config loaded for {config.supplier_name}")
        return config_dict
    except SupplierConfigError as e:
        activity.logger.error(f"Failed to load config: {e}")
        raise


@activity.defn
async def authenticate_supplier(supplier_id: str) -> str:
    """
    Authenticate with supplier API.

    Args:
        supplier_id: Supplier identifier.

    Returns:
        Authentication token or session identifier.

    TODO:
        - Load adapter for supplier
        - Call adapter.authenticate()
        - Return token/session for subsequent calls
    """
    activity.logger.info(f"Authenticating with supplier: {supplier_id}")
    # TODO: Implement authentication
    raise NotImplementedError("authenticate_supplier not yet implemented")


@activity.defn
async def fetch_pending_invoices(supplier_id: str) -> list[str]:
    """
    Fetch list of unprocessed invoice IDs from supplier.

    Args:
        supplier_id: Supplier identifier.

    Returns:
        List of invoice IDs available for download.

    TODO:
        - Load adapter for supplier
        - Call adapter.fetch_invoice_list()
        - Return list of invoice IDs
    """
    activity.logger.info(f"Fetching pending invoices from: {supplier_id}")
    # TODO: Implement invoice list fetching
    raise NotImplementedError("fetch_pending_invoices not yet implemented")


@activity.defn
async def fetch_invoice_xml(supplier_id: str, invoice_id: str) -> str:
    """
    Download invoice XML from supplier API.

    Args:
        supplier_id: Supplier identifier.
        invoice_id: Invoice ID from supplier system.

    Returns:
        Raw XML content of the invoice.

    TODO:
        - Load adapter for supplier
        - Call adapter.fetch_invoice(invoice_id)
        - Return raw XML string
    """
    activity.logger.info(f"Fetching invoice {invoice_id} from {supplier_id}")
    # TODO: Implement XML fetching
    raise NotImplementedError("fetch_invoice_xml not yet implemented")


@activity.defn
async def archive_raw_xml(supplier_id: str, invoice_id: str, xml_content: str) -> str:
    """
    Archive raw XML to filesystem and database.

    Args:
        supplier_id: Supplier identifier.
        invoice_id: Invoice ID from supplier system.
        xml_content: Raw XML string to archive.

    Returns:
        Path to archived file.

    TODO:
        - Create archive directory structure:
          C:\\NEX\\YEARACT\\ARCHIV\\SUPPLIER-INVOICES\\XML\\{SUPPLIER}\\{YEAR}\\{MONTH}\\
        - Save XML file with naming: {timestamp}_{invoice_number}.xml
        - Optionally store in PostgreSQL
        - Return file path
    """
    activity.logger.info(f"Archiving XML for invoice {invoice_id} from {supplier_id}")
    # TODO: Implement archival
    raise NotImplementedError("archive_raw_xml not yet implemented")


@activity.defn
async def parse_invoice_xml(supplier_id: str, xml_content: str) -> dict:
    """
    Parse XML content into UnifiedInvoice using supplier adapter.

    Args:
        supplier_id: Supplier identifier (determines which parser to use).
        xml_content: Raw XML string from supplier.

    Returns:
        UnifiedInvoice as dict (serialized for Temporal).

    TODO:
        - Load adapter for supplier
        - Call adapter.parse_invoice(xml_content)
        - Return UnifiedInvoice (as dict for Temporal serialization)
    """
    activity.logger.info(f"Parsing invoice XML from {supplier_id}")
    # TODO: Implement XML parsing
    raise NotImplementedError("parse_invoice_xml not yet implemented")


@activity.defn
async def acknowledge_invoice(supplier_id: str, invoice_id: str) -> bool:
    """
    Mark invoice as processed at supplier API.

    Args:
        supplier_id: Supplier identifier.
        invoice_id: Invoice ID from supplier system.

    Returns:
        True if acknowledgment was successful.

    TODO:
        - Load adapter for supplier
        - Call adapter.acknowledge_invoice(invoice_id)
        - Return success status
    """
    activity.logger.info(f"Acknowledging invoice {invoice_id} at {supplier_id}")
    # TODO: Implement acknowledgment
    raise NotImplementedError("acknowledge_invoice not yet implemented")
