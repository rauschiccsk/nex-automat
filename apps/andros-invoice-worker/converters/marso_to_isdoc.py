"""
MARSO JSON to ISDOC XML Converter.

Converts MARSO API JSON response to ISDOC 6.0.1 XML format.
"""

import hashlib
import logging
from decimal import ROUND_HALF_UP, Decimal
from typing import Any
from xml.etree import ElementTree as ET

logger = logging.getLogger(__name__)

# ISDOC namespace
ISDOC_NS = "http://isdoc.cz/namespace/2013"


class MARSOToISDOCConverter:
    """Converts MARSO JSON invoice data to ISDOC XML format."""

    # MARSO supplier info (hardcoded)
    SUPPLIER = {
        "id": "MARSO",
        "name": "MARSO Hungary Kft.",
        "ico": "10428342215",  # IČO from NEX Genesis ANDROS
        "vat": "HU10428342",
        "country": "HU",
        "city": "Budapest",
        "street": "Maglódi út 6.",
        "zip": "1106",
    }

    def __init__(self):
        """Initialize converter."""
        self._register_namespaces()

    def _register_namespaces(self):
        """Register ISDOC namespace."""
        ET.register_namespace("", ISDOC_NS)

    def convert(self, marso_json: dict[str, Any]) -> str:
        """
        Convert MARSO JSON to ISDOC XML string.

        Args:
            marso_json: MARSO invoice data as dictionary

        Returns:
            ISDOC XML as string
        """
        root = ET.Element("Invoice", xmlns=ISDOC_NS)
        root.set("version", "6.0.1")

        # Document header
        self._add_element(root, "DocumentType", "1")  # 1 = Invoice
        self._add_element(root, "ID", marso_json.get("InvoiceId", ""))
        self._add_element(root, "UUID", self._generate_uuid(marso_json))
        self._add_element(root, "IssueDate", marso_json.get("Kelt", ""))
        self._add_element(root, "TaxPointDate", marso_json.get("Teljesites", ""))
        self._add_element(root, "VATApplicable", "true")
        self._add_element(root, "ElectronicPossibilityAgreementReference", "")

        # Note with SalesId reference
        if marso_json.get("SalesId"):
            self._add_element(root, "Note", f"SalesId: {marso_json['SalesId']}")

        # Currency
        self._add_element(root, "LocalCurrencyCode", marso_json.get("Penznem", "EUR"))
        self._add_element(root, "CurrRate", "1")
        self._add_element(root, "RefCurrRate", "1")

        # Supplier party
        self._build_supplier_party(root)

        # Customer party
        self._build_customer_party(root, marso_json)

        # Payment terms
        self._build_payment_means(root, marso_json)

        # Tax summary
        self._build_tax_total(root, marso_json)

        # Totals
        self._build_legal_monetary_total(root, marso_json)

        # Invoice lines
        self._build_invoice_lines(root, marso_json.get("Lines", []))

        # Generate XML string
        return ET.tostring(root, encoding="unicode", xml_declaration=True)

    def _add_element(
        self, parent: ET.Element, tag: str, text: str | None = None
    ) -> ET.Element:
        """Add child element with optional text."""
        elem = ET.SubElement(parent, tag)
        if text is not None:
            elem.text = str(text)
        return elem

    def _generate_uuid(self, data: dict[str, Any]) -> str:
        """Generate deterministic UUID from invoice data."""
        content = f"MARSO-{data.get('InvoiceId', '')}-{data.get('Kelt', '')}"
        hash_hex = hashlib.md5(content.encode()).hexdigest()
        return f"{hash_hex[:8]}-{hash_hex[8:12]}-{hash_hex[12:16]}-{hash_hex[16:20]}-{hash_hex[20:32]}"

    def _build_supplier_party(self, root: ET.Element):
        """Build AccountingSupplierParty element (hardcoded MARSO)."""
        supplier = self._add_element(root, "AccountingSupplierParty")
        party = self._add_element(supplier, "Party")

        # Identification
        party_id = self._add_element(party, "PartyIdentification")
        self._add_element(party_id, "UserID", self.SUPPLIER["id"])
        self._add_element(party_id, "CatalogFirmIdentification", self.SUPPLIER["ico"])
        self._add_element(party_id, "ID", self.SUPPLIER["ico"])

        # Name
        party_name = self._add_element(party, "PartyName")
        self._add_element(party_name, "Name", self.SUPPLIER["name"])

        # Address
        address = self._add_element(party, "PostalAddress")
        self._add_element(address, "StreetName", self.SUPPLIER["street"])
        self._add_element(address, "CityName", self.SUPPLIER["city"])
        self._add_element(address, "PostalZone", self.SUPPLIER["zip"])
        country = self._add_element(address, "Country")
        self._add_element(country, "IdentificationCode", self.SUPPLIER["country"])
        self._add_element(country, "Name", "Hungary")

        # VAT registration
        tax_scheme = self._add_element(party, "PartyTaxScheme")
        self._add_element(tax_scheme, "CompanyID", self.SUPPLIER["vat"])
        scheme = self._add_element(tax_scheme, "TaxScheme")
        self._add_element(scheme, "Name", "VAT")

    def _build_customer_party(self, root: ET.Element, data: dict[str, Any]):
        """Build AccountingCustomerParty element."""
        customer = self._add_element(root, "AccountingCustomerParty")
        party = self._add_element(customer, "Party")

        # Name
        party_name = self._add_element(party, "PartyName")
        self._add_element(party_name, "Name", data.get("InvName", ""))

        # Address
        address = self._add_element(party, "PostalAddress")
        self._add_element(address, "StreetName", data.get("InvStreet", ""))
        self._add_element(address, "CityName", data.get("InvCity", ""))
        self._add_element(address, "PostalZone", data.get("InvZipCode", ""))
        country = self._add_element(address, "Country")
        self._add_element(
            country, "IdentificationCode", data.get("InvCountryRegionId", "SK")
        )

    def _build_payment_means(self, root: ET.Element, data: dict[str, Any]):
        """Build PaymentMeans element."""
        payment = self._add_element(root, "PaymentMeans")
        self._add_element(payment, "Payment")
        self._add_element(payment, "PaymentMeansCode", "42")  # Bank transfer
        self._add_element(payment, "PaymentDueDate", data.get("Hatarido", ""))

    def _build_tax_total(self, root: ET.Element, data: dict[str, Any]):
        """Build TaxTotal element."""
        tax_total = self._add_element(root, "TaxTotal")

        tax_amount = self._format_amount(data.get("Afa", 0))
        self._add_element(tax_total, "TaxAmount", tax_amount)

        # Tax subtotal (assuming single VAT rate)
        subtotal = self._add_element(tax_total, "TaxSubTotal")
        self._add_element(
            subtotal, "TaxableAmount", self._format_amount(data.get("Netto", 0))
        )
        self._add_element(subtotal, "TaxAmount", tax_amount)

        # Calculate VAT percent
        netto = float(data.get("Netto", 0))
        afa = float(data.get("Afa", 0))
        vat_percent = round((afa / netto * 100) if netto > 0 else 27, 2)

        tax_category = self._add_element(subtotal, "TaxCategory")
        self._add_element(tax_category, "Percent", str(vat_percent))
        scheme = self._add_element(tax_category, "TaxScheme")
        self._add_element(scheme, "Name", "VAT")

    def _build_legal_monetary_total(self, root: ET.Element, data: dict[str, Any]):
        """Build LegalMonetaryTotal element."""
        total = self._add_element(root, "LegalMonetaryTotal")
        self._add_element(
            total, "TaxExclusiveAmount", self._format_amount(data.get("Netto", 0))
        )
        self._add_element(
            total, "TaxInclusiveAmount", self._format_amount(data.get("Brutto", 0))
        )
        self._add_element(total, "AlreadyClaimedTaxExclusiveAmount", "0.00")
        self._add_element(total, "AlreadyClaimedTaxInclusiveAmount", "0.00")
        self._add_element(
            total,
            "DifferenceTaxExclusiveAmount",
            self._format_amount(data.get("Netto", 0)),
        )
        self._add_element(
            total,
            "DifferenceTaxInclusiveAmount",
            self._format_amount(data.get("Brutto", 0)),
        )
        self._add_element(total, "PayableRoundingAmount", "0.00")
        self._add_element(total, "PaidDepositsAmount", "0.00")
        self._add_element(
            total, "PayableAmount", self._format_amount(data.get("Brutto", 0))
        )

    def _build_invoice_lines(self, root: ET.Element, lines: list[dict[str, Any]]):
        """Build InvoiceLines element."""
        lines_elem = self._add_element(root, "InvoiceLines")

        for idx, line in enumerate(lines, start=1):
            self._build_invoice_line(lines_elem, line, idx)

    def _build_invoice_line(
        self, parent: ET.Element, line: dict[str, Any], line_number: int
    ):
        """Build single InvoiceLine element."""
        line_elem = self._add_element(parent, "InvoiceLine")

        self._add_element(line_elem, "ID", str(line_number))

        # Quantity and unit
        qty = float(line.get("Qty", 0))
        unit = self._map_unit(line.get("SalesUnit", "Db"))
        qty_elem = self._add_element(
            line_elem, "InvoicedQuantity", self._format_amount(qty)
        )
        qty_elem.set("unitCode", unit)

        # Line extension (net amount)
        self._add_element(
            line_elem, "LineExtensionAmount", self._format_amount(line.get("Netto", 0))
        )
        self._add_element(
            line_elem,
            "LineExtensionAmountTaxInclusive",
            self._format_amount(line.get("Brutto", 0)),
        )
        self._add_element(
            line_elem, "LineExtensionTaxAmount", self._format_amount(line.get("Afa", 0))
        )

        # Unit price
        netto = float(line.get("Netto", 0))
        unit_price = netto / qty if qty > 0 else 0
        self._add_element(line_elem, "UnitPrice", self._format_amount(unit_price))
        self._add_element(
            line_elem,
            "UnitPriceTaxInclusive",
            self._format_amount(float(line.get("Brutto", 0)) / qty if qty > 0 else 0),
        )

        # Tax category for line
        class_tax = self._add_element(line_elem, "ClassifiedTaxCategory")
        vat_percent = round(
            (float(line.get("Afa", 0)) / netto * 100) if netto > 0 else 27, 2
        )
        self._add_element(class_tax, "Percent", str(vat_percent))
        self._add_element(class_tax, "VATCalculationMethod", "0")  # 0 = from base
        scheme = self._add_element(class_tax, "TaxScheme")
        self._add_element(scheme, "Name", "VAT")

        # Item description
        item = self._add_element(line_elem, "Item")
        self._add_element(item, "Description", line.get("ItemName", ""))

        # Seller identification
        seller_id = self._add_element(item, "SellersItemIdentification")
        self._add_element(seller_id, "ID", line.get("ItemId", ""))

    def _map_unit(self, marso_unit: str) -> str:
        """Map MARSO unit to UN/ECE unit code."""
        unit_map = {
            "Db": "PCE",
            "Pr": "PR",
            "Kg": "KGM",
            "M": "MTR",
            "L": "LTR",
        }
        return unit_map.get(marso_unit, "PCE")

    def _format_amount(self, value: Any) -> str:
        """Format numeric value to 2 decimal places."""
        decimal_val = Decimal(str(value)).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        return str(decimal_val)

    def validate(self, isdoc_xml: str) -> bool:
        """
        Basic validation of generated ISDOC XML.

        Args:
            isdoc_xml: ISDOC XML string

        Returns:
            True if valid, False otherwise
        """
        try:
            root = ET.fromstring(isdoc_xml)

            # Check required elements (with namespace)
            required = [
                "ID",
                "IssueDate",
                "AccountingSupplierParty",
                "AccountingCustomerParty",
                "LegalMonetaryTotal",
            ]
            for elem_name in required:
                # Try both with and without namespace
                found = root.find(f".//{{{ISDOC_NS}}}{elem_name}")
                if found is None:
                    found = root.find(f".//{elem_name}")
                if found is None:
                    logger.error(f"Missing required element: {elem_name}")
                    return False

            return True
        except ET.ParseError as e:
            logger.error(f"Invalid XML: {e}")
            return False
