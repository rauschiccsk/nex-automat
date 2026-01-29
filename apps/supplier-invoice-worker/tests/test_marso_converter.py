"""Tests for MARSO to ISDOC converter."""

from xml.etree import ElementTree as ET

import pytest
from converters.marso_to_isdoc import MARSOToISDOCConverter

# ISDOC namespace for XPath queries
ISDOC_NS = "http://isdoc.cz/namespace/2013"


class TestMARSOToISDOCConverter:
    """Test cases for MARSOToISDOCConverter."""

    @pytest.fixture
    def converter(self):
        """Create converter instance."""
        return MARSOToISDOCConverter()

    def test_convert_basic(self, converter, marso_invoice_json):
        """Test basic conversion produces valid XML."""
        isdoc_xml = converter.convert(marso_invoice_json)

        assert isdoc_xml.startswith("<?xml")
        assert "<Invoice" in isdoc_xml
        assert 'version="6.0.1"' in isdoc_xml

    def test_convert_invoice_id(self, converter, marso_invoice_json):
        """Test invoice ID in output."""
        isdoc_xml = converter.convert(marso_invoice_json)
        root = ET.fromstring(isdoc_xml)

        id_elem = root.find(f".//{{{ISDOC_NS}}}ID")
        assert id_elem is not None
        assert id_elem.text == "11926-00447"

    def test_convert_uuid(self, converter, marso_invoice_json):
        """Test UUID generation."""
        isdoc_xml = converter.convert(marso_invoice_json)
        root = ET.fromstring(isdoc_xml)

        uuid_elem = root.find(f".//{{{ISDOC_NS}}}UUID")
        assert uuid_elem is not None
        assert len(uuid_elem.text) == 36  # UUID format with dashes

    def test_convert_dates(self, converter, marso_invoice_json):
        """Test date elements."""
        isdoc_xml = converter.convert(marso_invoice_json)
        root = ET.fromstring(isdoc_xml)

        issue_date = root.find(f".//{{{ISDOC_NS}}}IssueDate")
        assert issue_date is not None
        assert issue_date.text == "2026-01-15"

        tax_point = root.find(f".//{{{ISDOC_NS}}}TaxPointDate")
        assert tax_point is not None
        assert tax_point.text == "2026-01-15"

    def test_convert_currency(self, converter, marso_invoice_json):
        """Test currency element."""
        isdoc_xml = converter.convert(marso_invoice_json)
        root = ET.fromstring(isdoc_xml)

        currency = root.find(f".//{{{ISDOC_NS}}}LocalCurrencyCode")
        assert currency is not None
        assert currency.text == "EUR"

    def test_convert_amounts(self, converter, marso_invoice_json):
        """Test monetary amounts."""
        isdoc_xml = converter.convert(marso_invoice_json)
        root = ET.fromstring(isdoc_xml)

        tax_exclusive = root.find(f".//{{{ISDOC_NS}}}TaxExclusiveAmount")
        assert tax_exclusive is not None
        assert tax_exclusive.text == "1000.00"

        tax_inclusive = root.find(f".//{{{ISDOC_NS}}}TaxInclusiveAmount")
        assert tax_inclusive is not None
        assert tax_inclusive.text == "1200.00"

        payable = root.find(f".//{{{ISDOC_NS}}}PayableAmount")
        assert payable is not None
        assert payable.text == "1200.00"

    def test_convert_tax_amount(self, converter, marso_invoice_json):
        """Test tax amount element."""
        isdoc_xml = converter.convert(marso_invoice_json)
        root = ET.fromstring(isdoc_xml)

        tax_amount = root.find(f".//{{{ISDOC_NS}}}TaxAmount")
        assert tax_amount is not None
        assert tax_amount.text == "200.00"

    def test_convert_supplier_party(self, converter, marso_invoice_json):
        """Test supplier party (hardcoded MARSO)."""
        isdoc_xml = converter.convert(marso_invoice_json)

        assert "MARSO Hungary Kft." in isdoc_xml
        assert "HU10428342" in isdoc_xml
        assert "10428342" in isdoc_xml
        assert "Budapest" in isdoc_xml

    def test_convert_customer_party(self, converter, marso_invoice_json):
        """Test customer party from invoice data."""
        isdoc_xml = converter.convert(marso_invoice_json)

        assert "ANDROS s.r.o." in isdoc_xml
        assert "Komárno" in isdoc_xml
        assert "94501" in isdoc_xml
        assert "Hradná 123" in isdoc_xml

    def test_convert_invoice_lines_count(self, converter, marso_invoice_json):
        """Test invoice lines conversion."""
        isdoc_xml = converter.convert(marso_invoice_json)
        root = ET.fromstring(isdoc_xml)

        lines = root.findall(f".//{{{ISDOC_NS}}}InvoiceLine")
        assert len(lines) == 2

    def test_convert_line_item_id(self, converter, marso_invoice_json):
        """Test line item identification."""
        isdoc_xml = converter.convert(marso_invoice_json)

        assert "ABC123456" in isdoc_xml
        assert "DEF789012" in isdoc_xml

    def test_convert_line_item_description(self, converter, marso_invoice_json):
        """Test line item descriptions."""
        isdoc_xml = converter.convert(marso_invoice_json)

        assert "Michelin Pilot Sport 4 225/45R17" in isdoc_xml
        assert "Continental PremiumContact 6 205/55R16" in isdoc_xml

    def test_convert_line_quantity(self, converter, marso_invoice_json):
        """Test line quantity with unit code."""
        isdoc_xml = converter.convert(marso_invoice_json)
        root = ET.fromstring(isdoc_xml)

        quantities = root.findall(f".//{{{ISDOC_NS}}}InvoicedQuantity")
        assert len(quantities) == 2
        assert quantities[0].get("unitCode") == "PCE"
        assert quantities[0].text == "4.00"

    def test_validate_valid_xml(self, converter, marso_invoice_json):
        """Test validation of valid XML."""
        isdoc_xml = converter.convert(marso_invoice_json)
        assert converter.validate(isdoc_xml) is True

    def test_validate_invalid_xml(self, converter):
        """Test validation of invalid XML."""
        assert converter.validate("<invalid>") is False

    def test_validate_missing_required(self, converter):
        """Test validation with missing required elements."""
        # Minimal XML without required elements
        xml = '<?xml version="1.0"?><Invoice xmlns="http://isdoc.cz/namespace/2013"></Invoice>'
        assert converter.validate(xml) is False

    def test_format_amount(self, converter):
        """Test amount formatting."""
        assert converter._format_amount(100) == "100.00"
        assert converter._format_amount(99.999) == "100.00"
        assert converter._format_amount(99.994) == "99.99"
        assert converter._format_amount(0) == "0.00"
        assert converter._format_amount(1234.567) == "1234.57"

    def test_map_unit(self, converter):
        """Test unit mapping."""
        assert converter._map_unit("Db") == "PCE"
        assert converter._map_unit("Pr") == "PR"
        assert converter._map_unit("Kg") == "KGM"
        assert converter._map_unit("M") == "MTR"
        assert converter._map_unit("L") == "LTR"
        assert converter._map_unit("Unknown") == "PCE"

    def test_generate_uuid_deterministic(self, converter, marso_invoice_json):
        """Test UUID is deterministic for same invoice."""
        uuid1 = converter._generate_uuid(marso_invoice_json)
        uuid2 = converter._generate_uuid(marso_invoice_json)
        assert uuid1 == uuid2

    def test_generate_uuid_different_invoices(self, converter, marso_invoice_json):
        """Test UUID is different for different invoices."""
        uuid1 = converter._generate_uuid(marso_invoice_json)

        different_invoice = marso_invoice_json.copy()
        different_invoice["InvoiceId"] = "DIFFERENT-123"
        uuid2 = converter._generate_uuid(different_invoice)

        assert uuid1 != uuid2

    def test_convert_empty_lines(self, converter, marso_invoice_json):
        """Test conversion with no invoice lines."""
        data = marso_invoice_json.copy()
        data["Lines"] = []

        isdoc_xml = converter.convert(data)
        root = ET.fromstring(isdoc_xml)

        lines = root.findall(f".//{{{ISDOC_NS}}}InvoiceLine")
        assert len(lines) == 0
