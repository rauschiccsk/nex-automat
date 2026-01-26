"""
MARSO SOAP API Adapter.

Implements BaseSupplierAdapter for MARSO Hungary Kft. SOAP API.
Uses zeep for SOAP communication with JSON response parsing.
"""

import json
import logging
import os
from datetime import date
from typing import Any, Dict, List, Optional

from zeep import Client
from zeep.exceptions import Fault, TransportError

from adapters.base_adapter import BaseSupplierAdapter, SupplierConfig
from models.unified_invoice import InvoiceItem, InvoiceStatus, UnifiedInvoice

logger = logging.getLogger(__name__)


class MARSOAdapter(BaseSupplierAdapter):
    """SOAP client for MARSO Comax API."""

    def __init__(self, config: SupplierConfig):
        """Initialize MARSO adapter with configuration."""
        super().__init__(config)
        self._client: Optional[Client] = None
        self._account_num = os.environ.get("MARSO_ACCOUNT_NUM", "339792")
        self._use_test = os.environ.get("MARSO_USE_TEST", "true").lower() == "true"

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
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        invoice_id: Optional[str] = None,
    ) -> str:
        """Build SOAP request XML."""
        params = self.config.request_params

        xml = f'''<?xml version="1.0" encoding="UTF-8"?>
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
    <AccountNum>{self._account_num}</AccountNum>'''

        if date_from and date_to:
            xml += f'''
    <DatumTol>{date_from.isoformat()}</DatumTol>
    <DatumIg>{date_to.isoformat()}</DatumIg>'''

        if invoice_id:
            xml += f'''
    <SzlSzamResz>{invoice_id}</SzlSzamResz>'''
        else:
            xml += '''
    <SzlSzamResz></SzlSzamResz>'''

        xml += f'''
    <Key>{self.config.api_key}</Key>
  </Message>
</Document>'''
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
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
    ) -> List[Dict[str, Any]]:
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

    async def fetch_invoice_by_id(self, invoice_id: str) -> Dict[str, Any]:
        """Fetch single invoice details by ID."""
        message_type = self.config.message_types.get("invoice_detail", "CustInvoiceLines")
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

    def _parse_response(self, response: str) -> List[Dict[str, Any]]:
        """Parse SOAP response (JSON format)."""
        if not response:
            return []

        try:
            # MARSO returns JSON in response
            data = json.loads(response)
            if isinstance(data, list):
                return data
            elif isinstance(data, dict):
                return [data]
            return []
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse MARSO JSON response: {e}")
            logger.debug(f"Response: {response[:500]}")
            return []

    async def acknowledge_invoice(self, invoice_id: str) -> bool:
        """MARSO does not support invoice acknowledgment."""
        logger.warning(f"MARSO does not support acknowledge_invoice for {invoice_id}")
        return True  # Always return success

    def parse_invoice(self, json_content: str) -> UnifiedInvoice:
        """Parse JSON content into UnifiedInvoice."""
        raw_data = json.loads(json_content)
        return self.to_unified_invoice(raw_data)

    def to_unified_invoice(self, raw_data: Dict[str, Any]) -> UnifiedInvoice:
        """Convert MARSO JSON to UnifiedInvoice."""
        lines = raw_data.get("Lines", [])
        items = [
            InvoiceItem(
                line_number=idx + 1,
                product_code=line.get("ItemId", ""),
                product_name=line.get("ItemName", ""),
                quantity=float(line.get("Qty", 0)),
                unit=self._map_unit(line.get("SalesUnit", "Db")),
                unit_price=float(line.get("Netto", 0)) / max(float(line.get("Qty", 1)), 1),
                total_without_vat=float(line.get("Netto", 0)),
                vat_rate=self._calculate_vat_rate(line),
                vat_amount=float(line.get("Afa", 0)),
                total_with_vat=float(line.get("Brutto", 0)),
            )
            for idx, line in enumerate(lines)
        ]

        return UnifiedInvoice(
            supplier_id=self.config.supplier_id,
            invoice_number=raw_data.get("InvoiceId", ""),
            issue_date=raw_data.get("Kelt", ""),
            tax_point_date=raw_data.get("Teljesites", ""),
            due_date=raw_data.get("Hatarido", ""),
            currency=raw_data.get("Penznem", "EUR"),
            total_without_vat=float(raw_data.get("Netto", 0)),
            total_vat=float(raw_data.get("Afa", 0)),
            total_with_vat=float(raw_data.get("Brutto", 0)),
            supplier_name=self.config.supplier_name,
            supplier_vat_id="HU10428342",
            customer_name=raw_data.get("InvName", ""),
            customer_address=self._build_address(raw_data),
            items=items,
            status=InvoiceStatus.PENDING,
            raw_data=raw_data,
        )

    def _map_unit(self, marso_unit: str) -> str:
        """Map MARSO unit to ISDOC unit code."""
        unit_map = {
            "Db": "PCE",  # Piece
            "Pr": "PR",   # Pair
            "Kg": "KGM",  # Kilogram
            "M": "MTR",   # Meter
        }
        return unit_map.get(marso_unit, "PCE")

    def _calculate_vat_rate(self, line: Dict[str, Any]) -> float:
        """Calculate VAT rate from line amounts."""
        netto = float(line.get("Netto", 0))
        afa = float(line.get("Afa", 0))
        if netto > 0:
            return round((afa / netto) * 100, 2)
        return 27.0  # Default Hungarian VAT

    def _build_address(self, data: Dict[str, Any]) -> str:
        """Build address string from invoice data."""
        parts = [
            data.get("InvStreet", ""),
            data.get("InvCity", ""),
            data.get("InvZipCode", ""),
            data.get("InvCountryRegionId", ""),
        ]
        return ", ".join(p for p in parts if p)
