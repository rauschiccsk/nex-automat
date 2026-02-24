"""Unit tests for MARSO adapter."""

import sys
from datetime import date, datetime
from pathlib import Path
from unittest.mock import patch

import pytest

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from adapters.base_adapter import AuthType, SupplierConfig
from adapters.marso_adapter import MARSOAdapter


@pytest.fixture
def marso_config():
    """Create test MARSO configuration."""
    return SupplierConfig(
        supplier_id="marso",
        supplier_name="MARSO Hungary Kft.",
        auth_type=AuthType.API_KEY_BODY,
        base_url="",
        endpoint_list_invoices="CustInvoiceList",
        endpoint_get_invoice="CustInvoiceLines",
        endpoint_acknowledge="",
        product_code_field="ItemId",
        product_code_type="ean",
        api_key="test_key",
        protocol="soap",
        wsdl_url="http://test:8081/ComaxWS/Comax.asmx?wsdl",
        soap_method="CallComax",
        message_types={
            "invoice_list": "CustInvoiceList",
            "invoice_detail": "CustInvoiceLines",
        },
        request_params={
            "sender": "WebCatHU",
            "receiver": "Ax",
            "test_mode": "0",
        },
    )


@pytest.fixture
def sample_marso_invoice():
    """Sample MARSO invoice data."""
    return {
        "InvoiceId": "M-2024-001",
        "SalesId": "SO-12345",
        "Kelt": "2024.01.15",
        "Hatarido": "2024.02.15",
        "Teljesites": "2024.01.15",
        "Netto": 1000.00,
        "Afa": 270.00,
        "Brutto": 1270.00,
        "Penznem": "EUR",
        "InvName": "Test Customer",
        "InvStreet": "Test Street 1",
        "InvCity": "Budapest",
        "InvZipCode": "1000",
        "InvCountryRegionId": "HU",
        "Lines": [
            {
                "ItemId": "8590000000001",
                "ItemName": "Test Tire 205/55R16",
                "Qty": 4,
                "SalesUnit": "Db",
                "Netto": 500.00,
                "Afa": 135.00,
                "Brutto": 635.00,
            },
            {
                "ItemId": "8590000000002",
                "ItemName": "Wheel Nut Set",
                "Qty": 2,
                "SalesUnit": "Pr",
                "Netto": 500.00,
                "Afa": 135.00,
                "Brutto": 635.00,
            },
        ],
    }


class TestMARSOAdapter:
    """Tests for MARSOAdapter."""

    def test_init(self, marso_config):
        """Test adapter initialization."""
        adapter = MARSOAdapter(marso_config)
        assert adapter.config.supplier_id == "marso"
        assert adapter._client is None

    def test_build_request_xml(self, marso_config):
        """Test SOAP request XML building."""
        adapter = MARSOAdapter(marso_config)

        with patch.dict(
            "os.environ", {"MARSO_API_KEY": "test_key", "MARSO_ACCOUNT_NUM": "123456"}
        ):
            xml = adapter._build_request_xml(
                message_type="CustInvoiceList",
                date_from=date(2024, 1, 1),
                date_to=date(2024, 1, 31),
            )

        assert "CustInvoiceList" in xml
        assert "2024-01-01" in xml
        assert "2024-01-31" in xml
        assert "<Sender>WebCatHU</Sender>" in xml
        assert "<Receiver>Ax</Receiver>" in xml

    def test_parse_response_with_invoices(self, marso_config):
        """Test parsing XML response with embedded JSON."""
        adapter = MARSOAdapter(marso_config)

        # Simulated MARSO response format
        response = """<?xml version="1.0"?>
        <Document>
            <Message>
                <Invoices>[{"M-2024-001": {"InvoiceId": "M-2024-001", "Netto": 1000}}]</Invoices>
            </Message>
        </Document>"""

        result = adapter._parse_response(response)

        assert len(result) == 1
        assert result[0]["InvoiceId"] == "M-2024-001"
        assert result[0]["Netto"] == 1000

    def test_parse_response_empty(self, marso_config):
        """Test parsing empty response."""
        adapter = MARSOAdapter(marso_config)

        result = adapter._parse_response("")
        assert result == []

        result = adapter._parse_response(None)
        assert result == []

    def test_parse_response_no_invoices(self, marso_config):
        """Test parsing response without Invoices element."""
        adapter = MARSOAdapter(marso_config)

        response = """<?xml version="1.0"?>
        <Document>
            <Message>
                <Status>OK</Status>
            </Message>
        </Document>"""

        result = adapter._parse_response(response)
        assert result == []

    def test_parse_response_direct_json(self, marso_config):
        """Test parsing direct JSON (fallback for tests)."""
        adapter = MARSOAdapter(marso_config)

        response = '[{"InvoiceId": "TEST-001", "Netto": 500}]'
        result = adapter._parse_response(response)

        assert len(result) == 1
        assert result[0]["InvoiceId"] == "TEST-001"

    def test_to_unified_invoice(self, marso_config, sample_marso_invoice):
        """Test conversion to UnifiedInvoice."""
        adapter = MARSOAdapter(marso_config)

        unified = adapter.to_unified_invoice(sample_marso_invoice)

        assert unified.invoice_number == "M-2024-001"
        assert unified.supplier_id == "marso"
        assert unified.supplier_name == "MARSO Hungary Kft."
        assert unified.total_without_vat == 1000.00
        assert unified.total_vat == 270.00
        assert unified.total_with_vat == 1270.00
        assert unified.currency == "EUR"
        assert len(unified.items) == 2

    def test_to_unified_invoice_items(self, marso_config, sample_marso_invoice):
        """Test invoice items conversion."""
        adapter = MARSOAdapter(marso_config)

        unified = adapter.to_unified_invoice(sample_marso_invoice)

        assert unified.items[0].product_code == "8590000000001"
        assert unified.items[0].product_name == "Test Tire 205/55R16"
        assert unified.items[0].quantity == 4
        assert unified.items[0].unit == "PCE"

        assert unified.items[1].product_code == "8590000000002"
        assert unified.items[1].unit == "PR"

    def test_parse_marso_date(self, marso_config):
        """Test MARSO date parsing."""
        adapter = MARSOAdapter(marso_config)

        # MARSO format with dots
        result = adapter._parse_marso_date("2024.01.15")
        assert result == datetime(2024, 1, 15)

        # ISO format
        result = adapter._parse_marso_date("2024-01-15")
        assert result == datetime(2024, 1, 15)

        # Empty string
        result = adapter._parse_marso_date("")
        assert result is None

        # None
        result = adapter._parse_marso_date(None)
        assert result is None

    def test_map_unit(self, marso_config):
        """Test unit mapping."""
        adapter = MARSOAdapter(marso_config)

        assert adapter._map_unit("Db") == "PCE"
        assert adapter._map_unit("Pr") == "PR"
        assert adapter._map_unit("Kg") == "KGM"
        assert adapter._map_unit("M") == "MTR"
        assert adapter._map_unit("Unknown") == "PCE"  # Default

    def test_calculate_vat_rate(self, marso_config):
        """Test VAT rate calculation."""
        adapter = MARSOAdapter(marso_config)

        line = {"Netto": 1000, "Afa": 270}
        assert adapter._calculate_vat_rate(line) == 27.0

        line = {"Netto": 0, "Afa": 0}
        assert adapter._calculate_vat_rate(line) == 27.0  # Default


class TestMARSOAdapterIntegration:
    """Integration tests (require network and credentials)."""

    @pytest.mark.skip(reason="Requires live MARSO API")
    @pytest.mark.asyncio
    async def test_authenticate(self, marso_config):
        """Test live authentication."""
        adapter = MARSOAdapter(marso_config)
        result = await adapter.authenticate()
        assert result is True

    @pytest.mark.skip(reason="Requires live MARSO API")
    @pytest.mark.asyncio
    async def test_fetch_invoice_list(self, marso_config):
        """Test fetching invoice list from live API."""
        adapter = MARSOAdapter(marso_config)
        invoices = await adapter.fetch_invoice_list(
            date_from=date(2024, 1, 1),
            date_to=date(2024, 1, 31),
        )
        assert isinstance(invoices, list)
