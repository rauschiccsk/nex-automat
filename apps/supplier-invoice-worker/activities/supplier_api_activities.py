"""
Temporal Activities for Supplier Invoice API integration.

Activities for fetching invoices from supplier APIs and converting to ISDOC format.
"""

import logging
import os
from dataclasses import asdict
from datetime import date
from typing import Any

from adapters import MARSOAdapter, SupplierConfig
from config.config_loader import SupplierConfigError
from config.config_loader import load_supplier_config as _load_config
from converters import MARSOToISDOCConverter
from temporalio import activity

logger = logging.getLogger(__name__)


@activity.defn
async def fetch_supplier_config_activity(supplier_id: str) -> dict[str, Any]:
    """
    Load supplier configuration from YAML.

    Args:
        supplier_id: Supplier identifier (e.g., "marso")

    Returns:
        Supplier configuration as dictionary
    """
    activity.logger.info(f"Loading config for supplier: {supplier_id}")

    try:
        config = _load_config(supplier_id)
        # Convert to dict for Temporal serialization
        config_dict = asdict(config)
        config_dict["auth_type"] = config.auth_type.value
        activity.logger.info(f"Config loaded for {config.supplier_name}")
        return config_dict
    except SupplierConfigError as e:
        activity.logger.error(f"Failed to load config: {e}")
        raise


@activity.defn
async def authenticate_supplier_activity(supplier_id: str) -> bool:
    """
    Authenticate with supplier API.

    Args:
        supplier_id: Supplier identifier

    Returns:
        True if authentication successful
    """
    activity.logger.info(f"Authenticating with supplier: {supplier_id}")

    config = _load_config(supplier_id)
    adapter = _get_adapter(supplier_id, config)

    result = await adapter.authenticate()
    if result:
        activity.logger.info(f"Authentication successful for {supplier_id}")
    else:
        activity.logger.error(f"Authentication failed for {supplier_id}")

    return result


@activity.defn
async def fetch_invoice_list_activity(
    supplier_id: str,
    date_from: str,
    date_to: str,
) -> list[dict[str, Any]]:
    """
    Fetch list of invoices from supplier API.

    Args:
        supplier_id: Supplier identifier
        date_from: Start date (ISO format)
        date_to: End date (ISO format)

    Returns:
        List of raw invoice data
    """
    activity.logger.info(f"Fetching invoices from {supplier_id}: {date_from} to {date_to}")

    config = _load_config(supplier_id)
    adapter = _get_adapter(supplier_id, config)

    invoices = await adapter.fetch_invoice_list(
        date_from=date.fromisoformat(date_from),
        date_to=date.fromisoformat(date_to),
    )

    activity.logger.info(f"Retrieved {len(invoices)} invoices from {supplier_id}")
    return invoices


@activity.defn
async def fetch_invoice_detail_activity(
    supplier_id: str,
    invoice_id: str,
) -> dict[str, Any]:
    """
    Fetch single invoice details.

    Args:
        supplier_id: Supplier identifier
        invoice_id: Invoice ID from supplier

    Returns:
        Raw invoice data with lines
    """
    activity.logger.info(f"Fetching invoice {invoice_id} from {supplier_id}")

    config = _load_config(supplier_id)
    adapter = _get_adapter(supplier_id, config)

    invoice_data = await adapter.fetch_invoice_by_id(invoice_id)
    activity.logger.info(f"Invoice {invoice_id} fetched successfully")

    return invoice_data


@activity.defn
async def convert_to_unified_activity(
    supplier_id: str,
    raw_invoice: dict[str, Any],
) -> dict[str, Any]:
    """
    Convert raw invoice to UnifiedInvoice format.

    Args:
        supplier_id: Supplier identifier
        raw_invoice: Raw invoice data from API

    Returns:
        UnifiedInvoice as dictionary
    """
    invoice_id = raw_invoice.get("InvoiceId", "unknown")
    activity.logger.info(f"Converting invoice {invoice_id} to unified format")

    config = _load_config(supplier_id)
    adapter = _get_adapter(supplier_id, config)

    unified = adapter.to_unified_invoice(raw_invoice)

    activity.logger.info(f"Invoice {invoice_id} converted to unified format")
    return asdict(unified)


@activity.defn
async def convert_to_isdoc_activity(
    supplier_id: str,
    raw_invoice: dict[str, Any],
) -> str:
    """
    Convert raw invoice to ISDOC XML format.

    Args:
        supplier_id: Supplier identifier
        raw_invoice: Raw invoice data from API

    Returns:
        ISDOC XML string
    """
    invoice_id = raw_invoice.get("InvoiceId", "unknown")
    activity.logger.info(f"Converting invoice {invoice_id} to ISDOC XML")

    converter = _get_converter(supplier_id)
    isdoc_xml = converter.convert(raw_invoice)

    # Validate generated XML
    if not converter.validate(isdoc_xml):
        raise ValueError(f"Generated ISDOC XML failed validation for invoice {invoice_id}")

    activity.logger.info(f"Invoice {invoice_id} converted to ISDOC XML ({len(isdoc_xml)} bytes)")
    return isdoc_xml


@activity.defn
async def acknowledge_invoice_activity(
    supplier_id: str,
    invoice_id: str,
) -> bool:
    """
    Acknowledge invoice processing to supplier.

    Args:
        supplier_id: Supplier identifier
        invoice_id: Invoice ID

    Returns:
        True if acknowledged successfully
    """
    activity.logger.info(f"Acknowledging invoice {invoice_id} to {supplier_id}")

    config = _load_config(supplier_id)
    adapter = _get_adapter(supplier_id, config)

    result = await adapter.acknowledge_invoice(invoice_id)

    if result:
        activity.logger.info(f"Invoice {invoice_id} acknowledged successfully")
    else:
        activity.logger.warning(f"Invoice {invoice_id} acknowledgment returned False")

    return result


@activity.defn
async def archive_raw_data_activity(
    supplier_id: str,
    invoice_id: str,
    raw_data: dict[str, Any],
    isdoc_xml: str,
) -> str:
    """
    Archive raw data and ISDOC XML to filesystem.

    Args:
        supplier_id: Supplier identifier
        invoice_id: Invoice ID for tracking
        raw_data: Raw invoice data (JSON)
        isdoc_xml: Generated ISDOC XML

    Returns:
        Path to archived directory
    """
    import json
    from datetime import datetime
    from pathlib import Path

    activity.logger.info(f"Archiving invoice {invoice_id} from {supplier_id}")

    # Build archive path
    base_path = Path(os.environ.get("ARCHIVE_PATH", "C:/NEX/YEARACT/ARCHIV"))
    timestamp = datetime.now()
    archive_dir = base_path / "SUPPLIER-INVOICES" / supplier_id.upper() / str(timestamp.year) / f"{timestamp.month:02d}"
    archive_dir.mkdir(parents=True, exist_ok=True)

    # Generate filename
    safe_invoice_id = invoice_id.replace("/", "_").replace("\\", "_")
    filename_base = f"{timestamp.strftime('%Y%m%d_%H%M%S')}_{safe_invoice_id}"

    # Save JSON
    json_path = archive_dir / f"{filename_base}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(raw_data, f, indent=2, ensure_ascii=False)

    # Save ISDOC XML
    xml_path = archive_dir / f"{filename_base}.xml"
    with open(xml_path, "w", encoding="utf-8") as f:
        f.write(isdoc_xml)

    activity.logger.info(f"Invoice {invoice_id} archived to {archive_dir}")
    return str(archive_dir)


@activity.defn
async def post_isdoc_to_pipeline_activity(
    isdoc_xml: str,
    invoice_id: str,
    supplier_id: str,
) -> dict[str, Any]:
    """
    Post ISDOC XML to existing invoice processing pipeline.

    Args:
        isdoc_xml: ISDOC XML string
        invoice_id: Invoice ID for tracking
        supplier_id: Supplier identifier

    Returns:
        Pipeline response
    """
    import httpx

    activity.logger.info(f"Posting ISDOC to pipeline: {invoice_id}")

    pipeline_url = os.environ.get("INVOICE_PIPELINE_URL", "http://localhost:8000/api/v1/invoice")

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            pipeline_url,
            content=isdoc_xml,
            headers={
                "Content-Type": "application/xml",
                "X-Supplier-ID": supplier_id,
                "X-Invoice-ID": invoice_id,
            },
        )
        response.raise_for_status()

    activity.logger.info(f"Invoice {invoice_id} posted to pipeline successfully")
    return {"status": "success", "invoice_id": invoice_id}


# Helper functions


def _get_adapter(supplier_id: str, config: SupplierConfig):
    """Get appropriate adapter for supplier."""
    adapters = {
        "marso": MARSOAdapter,
    }

    adapter_class = adapters.get(supplier_id.lower())
    if not adapter_class:
        raise ValueError(f"No adapter found for supplier: {supplier_id}")

    return adapter_class(config)


def _get_converter(supplier_id: str):
    """Get appropriate converter for supplier."""
    converters = {
        "marso": MARSOToISDOCConverter,
    }

    converter_class = converters.get(supplier_id.lower())
    if not converter_class:
        raise ValueError(f"No converter found for supplier: {supplier_id}")

    return converter_class()
