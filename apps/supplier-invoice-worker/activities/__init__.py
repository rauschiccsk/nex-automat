"""Temporal activities for supplier invoice processing."""

from .email_activities import (
    EmailAttachment,
    EmailMessage,
    fetch_unread_emails,
    mark_email_processed,
)
from .invoice_activities import (
    UploadResult,
    upload_invoice_to_api,
    validate_pdf,
)
from .supplier_api_activities import (
    acknowledge_invoice,
    archive_raw_xml,
    fetch_invoice_xml,
    fetch_pending_invoices,
    load_supplier_config,
    parse_invoice_xml,
)

__all__ = [
    # Email activities
    "EmailAttachment",
    "EmailMessage",
    "fetch_unread_emails",
    "mark_email_processed",
    # Invoice activities
    "UploadResult",
    "upload_invoice_to_api",
    "validate_pdf",
    # Supplier API activities
    "acknowledge_invoice",
    "archive_raw_xml",
    "fetch_invoice_xml",
    "fetch_pending_invoices",
    "load_supplier_config",
    "parse_invoice_xml",
]
