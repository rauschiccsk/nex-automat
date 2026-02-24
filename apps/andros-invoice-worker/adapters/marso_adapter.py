"""
MARSO SOAP API Adapter for ANDROS.

Implements BaseSupplierAdapter for MARSO Hungary Kft. SOAP API.
Uses zeep for SOAP communication with JSON response parsing.
"""

import json
import logging
import os
import re
from datetime import date, datetime
from typing import Any

from adapters.base_adapter import BaseSupplierAdapter, SupplierConfig
from models.unified_invoice import InvoiceItem, InvoiceStatus, UnifiedInvoice
from zeep import Client
from zeep.exceptions import Fault, TransportError

logger = logging.getLogger(__name__)


class MARSOAdapter(BaseSupplierAdapter):
    """SOAP client for MARSO Comax API."""

    def __init__(self, config: SupplierConfig):
        """Initialize MARSO adapter with configuration."""
        super().__init__(config)
        self._client: Client | None = None
        self._account_num = os.environ.get("MARSO_ACCOUNT_NUM", "339792")
        self._api_key = os.environ.get("MARSO_API_KEY") or self.config.api_key
        self._use_test = os.environ.get("MARSO_USE_TEST", "false").lower() == "true"

    @property
    def client(self) -> Client:
        """Lazy-load SOAP client."""
        if self._client is None:
            wsdl_url = self._get_wsdl_url()
            logger.info(f"Connecting to MARSO WSDL: {wsdl_url}")
            self._client = Client(wsdl_url)
        return self._client

    def _get_wsdl_url(self) -> str:
        """Get WSDL URL based on environment."""
        if self._use_test:
            return "http://195.228.175.10:8082/ComaxWS/Comax.asmx?wsdl"
        return "http://195.228.175.10:8081/ComaxWS/Comax.asmx?wsdl"

    def _build_request_xml(
        self,
        message_type: str,
        date_from: date | None = None,
        date_to: date | None = None,
        invoice_id: str | None = None,
    ) -> str:
        """Build SOAP request XML."""
        params = self.config.request_params

        xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Document>
  <ComaxEnvelope>
    <Sender>{params.get("sender", "WebCatHU")}</Sender>
    <Receiver>{params.get("receiver", "Ax")}</Receiver>
    <MessageType>{message_type}</MessageType>
    <MessageId/>
    <RespMessageId/>
    <test>{params.get("test_mode", "0")}</test>
  </ComaxEnvelope>
  <Message>
    <AccountNum>{self._account_num}</AccountNum>"""

        if date_from and date_to:
            xml += f"""
    <DatumTol>{date_from.isoformat()}</DatumTol>
    <DatumIg>{date_to.isoformat()}</DatumIg>"""

        if invoice_id:
            xml += f"""
    <SzlSzamResz>{invoice_id}</SzlSzamResz>"""
        else:
            xml += """
    <SzlSzamResz></SzlSzamResz>"""

        xml += f"""
    <Key>{self._api_key}</Key>
  </Message>
</Document>"""
        return xml

    async def authenticate(self) -> bool:
        """Test authentication by making a simple request."""
        try:
            # Test with minimal date range
            today = date.today()
            request_xml = self._build_request_xml(
                message_type="CustInvoiceList",
                date_from=today,
                date_to=today,
            )
            response = self.client.service.CallComax(request_xml)
            logger.info("MARSO authentication successful")
            return True
        except (Fault, TransportError) as e:
            logger.error(f"MARSO authentication failed: {e}")
            return False

    async def fetch_invoice_list(
        self,
        date_from: date | None = None,
        date_to: date | None = None,
    ) -> list[dict[str, Any]]:
        """Fetch list of invoices from MARSO API."""
        if date_from is None:
            date_from = date.today()
        if date_to is None:
            date_to = date.today()

        message_type = self.config.message_types.get("invoice_list", "CustInvoiceList")
        request_xml = self._build_request_xml(
            message_type=message_type,
            date_from=date_from,
            date_to=date_to,
        )

        logger.info(f"Fetching MARSO invoices from {date_from} to {date_to}")

        try:
            response = self.client.service.CallComax(request_xml)
            invoices = self._parse_response(response)
            logger.info(f"Retrieved {len(invoices)} invoices from MARSO")
            return invoices
        except (Fault, TransportError) as e:
            logger.error(f"MARSO fetch_invoice_list failed: {e}")
            raise

    async def fetch_invoice(self, invoice_id: str) -> str:
        """Fetch single invoice details by ID (returns raw JSON string)."""
        data = await self.fetch_invoice_by_id(invoice_id)
        return json.dumps(data)

    async def fetch_invoice_by_id(self, invoice_id: str) -> dict[str, Any]:
        """Fetch single invoice details by ID."""
        message_type = self.config.message_types.get(
            "invoice_detail", "CustInvoiceLines"
        )
        request_xml = self._build_request_xml(
            message_type=message_type,
            invoice_id=invoice_id,
        )

        logger.info(f"Fetching MARSO invoice: {invoice_id}")

        try:
            response = self.client.service.CallComax(request_xml)
            invoices = self._parse_response(response)
            if invoices:
                return invoices[0]
            raise ValueError(f"Invoice {invoice_id} not found")
        except (Fault, TransportError) as e:
            logger.error(f"MARSO fetch_invoice_by_id failed: {e}")
            raise

    def _parse_response(self, response: str) -> list[dict[str, Any]]:
        """Parse SOAP response (XML with JSON inside <Invoices> element)."""
        if not response:
            return []

        try:
            # MARSO returns XML with JSON embedded in <Invoices> element
            # Format: <Document><Message><Invoices>[{...}]</Invoices></Message></Document>

            # Extract JSON from <Invoices> element
            invoices_match = re.search(
                r"<Invoices>\s*(\[.*?\])\s*</Invoices>", response, re.DOTALL
            )
            if not invoices_match:
                # Try direct JSON parsing as fallback (for unit tests)
                try:
                    data = json.loads(response)
                    if isinstance(data, list):
                        return data
                    elif isinstance(data, dict):
                        return [data]
                except json.JSONDecodeError:
                    pass
                logger.debug("No <Invoices> element found in response")
                return []

            invoices_json = invoices_match.group(1)
            data = json.loads(invoices_json)

            # MARSO format: [{"invoice_id": {invoice_data}}, ...]
            # Flatten to [{invoice_data}, ...]
            result = []
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        # Each item is {"invoice_id": {actual_data}}
                        for key, value in item.items():
                            if isinstance(value, dict):
                                result.append(value)
                            else:
                                result.append(item)
                            break  # Only first key-value pair
            elif isinstance(data, dict):
                result.append(data)

            return result

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse MARSO JSON response: {e}")
            logger.debug(f"Response: {response[:500]}")
            return []
        except Exception as e:
            logger.error(f"Failed to parse MARSO response: {e}")
            return []

    async def acknowledge_invoice(self, invoice_id: str) -> bool:
        """MARSO does not support invoice acknowledgment."""
        logger.warning(f"MARSO does not support acknowledge_invoice for {invoice_id}")
        return True  # Always return success

    def parse_invoice(self, json_content: str) -> UnifiedInvoice:
        """Parse JSON content into UnifiedInvoice."""
        raw_data = json.loads(json_content)
        return self.to_unified_invoice(raw_data)

    def to_unified_invoice(self, raw_data: dict[str, Any]) -> UnifiedInvoice:
        """Convert MARSO JSON to UnifiedInvoice."""
        lines = raw_data.get("Lines", [])
        items = [
            InvoiceItem(
                line_number=idx + 1,
                product_code=line.get("ItemId", ""),
                product_code_type="ean",
                product_name=line.get("ItemName", ""),
                quantity=float(line.get("Qty", 0)),
                unit=self._map_unit(line.get("SalesUnit", "Db")),
                unit_price=float(line.get("Netto", 0))
                / max(float(line.get("Qty", 1)), 1),
                total_price=float(line.get("Netto", 0)),
                vat_rate=self._calculate_vat_rate(line),
                vat_amount=float(line.get("Afa", 0)),
            )
            for idx, line in enumerate(lines)
        ]

        # Parse date string to datetime
        # MARSO uses format "YYYY.MM.DD" or "YYYY-MM-DD"
        invoice_date_str = raw_data.get("Kelt", "")
        invoice_date = self._parse_marso_date(invoice_date_str) or datetime.now()

        due_date_str = raw_data.get("Hatarido", "")
        due_date = self._parse_marso_date(due_date_str)

        return UnifiedInvoice(
            source_type="api",
            supplier_id=self.config.supplier_id,
            supplier_name=self.config.supplier_name,
            invoice_number=raw_data.get("InvoiceId", ""),
            invoice_date=invoice_date,
            external_invoice_id=raw_data.get("SalesId", raw_data.get("InvoiceId", "")),
            total_without_vat=float(raw_data.get("Netto", 0)),
            total_vat=float(raw_data.get("Afa", 0)),
            total_with_vat=float(raw_data.get("Brutto", 0)),
            items=items,
            fetched_at=datetime.now(),
            status=InvoiceStatus.PENDING,
            due_date=due_date,
            currency=raw_data.get("Penznem", "EUR"),
            supplier_ico="10428342215",  # MARSO IČO from NEX Genesis ANDROS
            supplier_dic="HU10428342",
            supplier_ic_dph="HU10428342",
        )

    def _map_unit(self, marso_unit: str) -> str:
        """Map MARSO unit to ISDOC unit code."""
        unit_map = {
            "Db": "PCE",  # Piece
            "Pr": "PR",  # Pair
            "Kg": "KGM",  # Kilogram
            "M": "MTR",  # Meter
        }
        return unit_map.get(marso_unit, "PCE")

    def _calculate_vat_rate(self, line: dict[str, Any]) -> float:
        """Calculate VAT rate from line amounts."""
        netto = float(line.get("Netto", 0))
        afa = float(line.get("Afa", 0))
        if netto > 0:
            return round((afa / netto) * 100, 2)
        return 27.0  # Default Hungarian VAT

    def _parse_marso_date(self, date_str: str) -> datetime | None:
        """Parse MARSO date string (formats: YYYY.MM.DD or YYYY-MM-DD)."""
        if not date_str:
            return None

        # Try different formats
        formats = ["%Y.%m.%d", "%Y-%m-%d", "%Y.%m.%d.", "%d.%m.%Y"]
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue

        logger.warning(f"Could not parse MARSO date: {date_str}")
        return None

    def _build_address(self, data: dict[str, Any]) -> str:
        """Build address string from invoice data."""
        parts = [
            data.get("InvStreet", ""),
            data.get("InvCity", ""),
            data.get("InvZipCode", ""),
            data.get("InvCountryRegionId", ""),
        ]
        return ", ".join(p for p in parts if p)
