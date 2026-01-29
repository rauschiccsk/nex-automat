"""Tests for MARSO SOAP adapter."""

from datetime import date

import pytest
from adapters.base_adapter import AuthType, SupplierConfig
from adapters.marso_adapter import MARSOAdapter


class TestMARSOAdapter:
    """Test cases for MARSOAdapter."""

    @pytest.fixture
    def config(self):
        """Create test config."""
        return SupplierConfig(
            supplier_id="marso",
            supplier_name="MARSO Hungary Kft.",
            auth_type=AuthType.API_KEY_BODY,
            base_url="",
            endpoint_list_invoices="",
            endpoint_get_invoice="",
            endpoint_acknowledge="",
            product_code_field="ItemId",
            product_code_type="ean",
            protocol="soap",
            wsdl_url="http://test.wsdl",
            soap_method="CallComax",
            message_types={"invoice_list": "CustInvoiceList", "invoice_detail": "CustInvoiceLines"},
            request_params={"sender": "WebCatHU", "receiver": "Ax", "test_mode": "0"},
            response_format="json",
            api_key="test_api_key",
        )

    @pytest.fixture
    def adapter(self, config):
        """Create adapter instance."""
        return MARSOAdapter(config)

    def test_init(self, adapter):
        """Test adapter initialization."""
        assert adapter.config.supplier_id == "marso"
        assert adapter.config.protocol == "soap"
        assert adapter._client is None

    def test_get_wsdl_url_test_mode(self, adapter):
        """Test WSDL URL in test mode."""
        adapter._use_test = True
        url = adapter._get_wsdl_url()
        assert "8082" in url

    def test_get_wsdl_url_live_mode(self, adapter):
        """Test WSDL URL in live mode."""
        adapter._use_test = False
        url = adapter._get_wsdl_url()
        assert "8081" in url

    def test_build_request_xml_with_dates(self, adapter):
        """Test SOAP request XML generation with date range."""
        xml = adapter._build_request_xml(
            message_type="CustInvoiceList",
            date_from=date(2026, 1, 1),
            date_to=date(2026, 1, 31),
        )

        assert "<MessageType>CustInvoiceList</MessageType>" in xml
        assert "<DatumTol>2026-01-01</DatumTol>" in xml
        assert "<DatumIg>2026-01-31</DatumIg>" in xml
        assert "<Sender>WebCatHU</Sender>" in xml
        assert "<Receiver>Ax</Receiver>" in xml

    def test_build_request_xml_with_invoice_id(self, adapter):
        """Test SOAP request XML generation with invoice ID."""
        xml = adapter._build_request_xml(
            message_type="CustInvoiceLines",
            invoice_id="12345",
        )

        assert "<MessageType>CustInvoiceLines</MessageType>" in xml
        assert "<SzlSzamResz>12345</SzlSzamResz>" in xml

    def test_parse_response_json_list(self, adapter):
        """Test JSON response parsing - list."""
        response = '[{"InvoiceId": "123"}, {"InvoiceId": "456"}]'
        result = adapter._parse_response(response)
        assert len(result) == 2
        assert result[0]["InvoiceId"] == "123"
        assert result[1]["InvoiceId"] == "456"

    def test_parse_response_json_single(self, adapter):
        """Test JSON response parsing - single object."""
        response = '{"InvoiceId": "456"}'
        result = adapter._parse_response(response)
        assert len(result) == 1
        assert result[0]["InvoiceId"] == "456"

    def test_parse_response_empty(self, adapter):
        """Test empty response handling."""
        result = adapter._parse_response("")
        assert result == []

    def test_parse_response_invalid_json(self, adapter):
        """Test invalid JSON response handling."""
        result = adapter._parse_response("not valid json")
        assert result == []

    def test_map_unit(self, adapter):
        """Test unit code mapping."""
        assert adapter._map_unit("Db") == "PCE"
        assert adapter._map_unit("Pr") == "PR"
        assert adapter._map_unit("Kg") == "KGM"
        assert adapter._map_unit("M") == "MTR"
        assert adapter._map_unit("Unknown") == "PCE"

    def test_calculate_vat_rate(self, adapter):
        """Test VAT rate calculation."""
        line = {"Netto": 100, "Afa": 20}
        rate = adapter._calculate_vat_rate(line)
        assert rate == 20.0

    def test_calculate_vat_rate_hungarian(self, adapter):
        """Test VAT rate calculation for Hungarian 27%."""
        line = {"Netto": 100, "Afa": 27}
        rate = adapter._calculate_vat_rate(line)
        assert rate == 27.0

    def test_calculate_vat_rate_zero_netto(self, adapter):
        """Test VAT rate with zero netto."""
        line = {"Netto": 0, "Afa": 0}
        rate = adapter._calculate_vat_rate(line)
        assert rate == 27.0  # Default HU VAT

    def test_to_unified_invoice(self, adapter, marso_invoice_json):
        """Test conversion to UnifiedInvoice."""
        unified = adapter.to_unified_invoice(marso_invoice_json)

        assert unified.invoice_number == "11926-00447"
        assert unified.supplier_id == "marso"
        assert unified.source_type == "api"
        assert unified.invoice_date.strftime("%Y-%m-%d") == "2026-01-15"
        assert unified.currency == "EUR"
        assert unified.total_without_vat == 1000.00
        assert unified.total_vat == 200.00
        assert unified.total_with_vat == 1200.00
        assert unified.external_invoice_id == "VR1234567"

    def test_to_unified_invoice_items(self, adapter, marso_invoice_json):
        """Test conversion of invoice items."""
        unified = adapter.to_unified_invoice(marso_invoice_json)

        assert len(unified.items) == 2

        item1 = unified.items[0]
        assert item1.product_code == "ABC123456"
        assert item1.product_code_type == "ean"
        assert item1.product_name == "Michelin Pilot Sport 4 225/45R17"
        assert item1.quantity == 4
        assert item1.unit == "PCE"
        assert item1.total_price == 250.00

        item2 = unified.items[1]
        assert item2.product_code == "DEF789012"
        assert item2.quantity == 2

    def test_build_address(self, adapter, marso_invoice_json):
        """Test address building."""
        address = adapter._build_address(marso_invoice_json)
        assert "Hradná 123" in address
        assert "Komárno" in address
        assert "94501" in address
        assert "SK" in address

    def test_build_address_partial(self, adapter):
        """Test address building with partial data."""
        data = {"InvCity": "Budapest", "InvCountryRegionId": "HU"}
        address = adapter._build_address(data)
        assert "Budapest" in address
        assert "HU" in address
