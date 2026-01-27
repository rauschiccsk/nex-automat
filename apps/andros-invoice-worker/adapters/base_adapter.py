"""Base adapter for supplier API integrations.

Provides abstract base class and configuration models for multi-supplier support.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional

from models import UnifiedInvoice


class AuthType(Enum):
    """Authentication method for supplier API."""

    NONE = "none"
    API_KEY = "api_key"
    API_KEY_HEADER = "api_key_header"
    API_KEY_QUERY = "api_key_query"
    API_KEY_BODY = "api_key_body"
    BASIC = "basic"
    BEARER = "bearer"
    OAUTH2 = "oauth2"
    CERTIFICATE = "certificate"


@dataclass
class SupplierConfig:
    """Configuration for a supplier API connection."""

    # Identifikácia dodávateľa
    supplier_id: str
    supplier_name: str

    # Autentifikácia
    auth_type: AuthType
    base_url: str

    # Endpointy
    endpoint_list_invoices: str
    endpoint_get_invoice: str
    endpoint_acknowledge: str

    # Product code mapovanie
    product_code_field: str  # Názov poľa v XML
    product_code_type: str  # Typ: ean, marso_code, ...

    # Credentials (zo secure storage / .env)
    api_key: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None

    # Settings
    timeout_seconds: int = 30
    max_retries: int = 3
    rate_limit_per_minute: int = 60

    # SOAP support
    protocol: str = "rest"  # "rest" | "soap"
    wsdl_url: Optional[str] = None  # WSDL endpoint URL
    soap_method: Optional[str] = None  # SOAP method name (e.g. "CallComax")
    message_types: Dict[str, str] = field(default_factory=dict)  # {"invoice_list": "CustInvoiceList", ...}
    request_params: Dict[str, Any] = field(default_factory=dict)  # Sender, Receiver, test, etc.
    response_format: str = "xml"  # "xml" | "json"


class BaseSupplierAdapter(ABC):
    """Abstract base class for supplier API adapters.

    Each supplier (MARSO, CONTINENTAL, etc.) implements this interface
    with their specific API logic.
    """

    def __init__(self, config: SupplierConfig):
        self.config = config

    @abstractmethod
    async def authenticate(self) -> bool:
        """Authenticate with the supplier API.

        Returns:
            True if authentication was successful.
        """
        pass

    @abstractmethod
    async def fetch_invoice_list(self) -> list[str]:
        """Fetch list of unprocessed invoice IDs.

        Returns:
            List of invoice IDs available for download.
        """
        pass

    @abstractmethod
    async def fetch_invoice(self, invoice_id: str) -> str:
        """Download invoice XML by ID.

        Args:
            invoice_id: The supplier's invoice identifier.

        Returns:
            Raw XML content of the invoice.
        """
        pass

    @abstractmethod
    async def acknowledge_invoice(self, invoice_id: str) -> bool:
        """Mark invoice as processed at the supplier.

        Args:
            invoice_id: The supplier's invoice identifier.

        Returns:
            True if acknowledgment was successful.
        """
        pass

    @abstractmethod
    def parse_invoice(self, xml_content: str) -> UnifiedInvoice:
        """Parse XML content into UnifiedInvoice.

        Args:
            xml_content: Raw XML string from the supplier.

        Returns:
            Normalized UnifiedInvoice instance.
        """
        pass
