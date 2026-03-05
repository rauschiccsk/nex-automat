"""Base adapter for supplier API integrations.

Provides abstract base class and configuration models for multi-supplier support.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from nex_invoice_worker.models import UnifiedInvoice
from nex_config.limits import MAX_RETRIES


class AuthType(Enum):
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
    supplier_id: str
    supplier_name: str
    auth_type: AuthType
    base_url: str
    endpoint_list_invoices: str
    endpoint_get_invoice: str
    endpoint_acknowledge: str
    product_code_field: str
    product_code_type: str
    api_key: str | None = None
    username: str | None = None
    password: str | None = None
    timeout_seconds: int = 30
    max_retries: int = MAX_RETRIES
    rate_limit_per_minute: int = 60
    protocol: str = "rest"
    wsdl_url: str | None = None
    soap_method: str | None = None
    message_types: dict[str, str] = field(default_factory=dict)
    request_params: dict[str, Any] = field(default_factory=dict)
    response_format: str = "xml"


class BaseSupplierAdapter(ABC):
    def __init__(self, config: SupplierConfig):
        self.config = config

    @abstractmethod
    async def authenticate(self) -> bool:
        pass

    @abstractmethod
    async def fetch_invoice_list(self) -> list[str]:
        pass

    @abstractmethod
    async def fetch_invoice(self, invoice_id: str) -> str:
        pass

    @abstractmethod
    async def acknowledge_invoice(self, invoice_id: str) -> bool:
        pass

    @abstractmethod
    def parse_invoice(self, xml_content: str) -> UnifiedInvoice:
        pass
