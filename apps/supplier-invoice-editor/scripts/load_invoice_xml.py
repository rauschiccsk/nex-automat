#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""
Script na nacitanie a zobrazenie ISDOC XML faktury
Pouzitie: python scripts/load_invoice_xml.py [path_to_xml]

Ak nie je zadana cesta, hlada XML subory v C:\NEX\
"""

import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Optional
from decimal import Decimal
from datetime import datetime


class ISDOCParser:
    """Parser pre ISDOC XML format"""

    # ISDOC namespace
    NAMESPACE = {
        'isdoc': 'http://isdoc.cz/namespace/2013'
    }

    def __init__(self, xml_path: str):
        self.xml_path = Path(xml_path)
        self.tree = None
        self.root = None

    def load(self) -> bool:
        """Nacita XML subor"""
        try:
            self.tree = ET.parse(self.xml_path)
            self.root = self.tree.getroot()
            print(f"OK XML nacitane: {self.xml_path.name}")
            return True
        except Exception as e:
            print(f"ERROR Chyba pri nacitani XML: {e}")
            return False

    def get_text(self, element, path: str, default: str = "") -> str:
        """Ziska text z elementu"""
        if element is None:
            return default
        found = element.find(path, self.NAMESPACE)
        return found.text if found is not None and found.text else default

    def parse_header(self) -> Dict:
        """Parsuje hlavicku faktury"""
        header = {}

        # Cislo faktury
        header['invoice_number'] = self.get_text(self.root, './/isdoc:ID')

        # UUID
        header['uuid'] = self.get_text(self.root, './/isdoc:UUID')

        # Datum vystavenia
        header['issue_date'] = self.get_text(self.root, './/isdoc:IssueDate')

        # Datum dodania
        header['delivery_date'] = self.get_text(self.root, './/isdoc:TaxPointDate')

        # Datum splatnosti
        payment = self.root.find('.//isdoc:PaymentMeans/isdoc:Payment', self.NAMESPACE)
        if payment is not None:
            header['due_date'] = self.get_text(payment, './/isdoc:PaymentDueDate')
        else:
            header['due_date'] = 'N/A'

        # Celkova suma
        header['total_amount'] = self.get_text(self.root, './/isdoc:LegalMonetaryTotal/isdoc:TaxInclusiveAmount')

        # Mena
        header['currency'] = 'EUR'

        return header

    def parse_supplier(self) -> Dict:
        """Parsuje udaje dodavatela"""
        supplier = {}
        supplier_elem = self.root.find('.//isdoc:AccountingSupplierParty', self.NAMESPACE)

        if supplier_elem is not None:
            party = supplier_elem.find('.//isdoc:Party', self.NAMESPACE)
            if party is not None:
                # Nazov
                supplier['name'] = self.get_text(party, './/isdoc:PartyName/isdoc:Name')

                # ICO
                supplier['ico'] = self.get_text(party, './/isdoc:PartyIdentification/isdoc:ID')

                # DIC
                vat_elem = party.find('.//isdoc:PartyTaxScheme[isdoc:TaxScheme="VAT"]', self.NAMESPACE)
                if vat_elem is not None:
                    supplier['dic'] = self.get_text(vat_elem, './/isdoc:CompanyID')

        return supplier

    def parse_customer(self) -> Dict:
        """Parsuje udaje odberatela"""
        customer = {}
        customer_elem = self.root.find('.//isdoc:AccountingCustomerParty', self.NAMESPACE)

        if customer_elem is not None:
            party = customer_elem.find('.//isdoc:Party', self.NAMESPACE)
            if party is not None:
                customer['name'] = self.get_text(party, './/isdoc:PartyName/isdoc:Name')
                customer['ico'] = self.get_text(party, './/isdoc:PartyIdentification/isdoc:ID')

        return customer

    def parse_items(self) -> List[Dict]:
        """Parsuje polozky faktury"""
        items = []

        lines = self.root.findall('.//isdoc:InvoiceLine', self.NAMESPACE)
        for line in lines:
            item = {}

            # ID riadku
            item['line_id'] = self.get_text(line, './/isdoc:ID')

            # Nazov
            item['name'] = self.get_text(line, './/isdoc:Item/isdoc:Description')

            # EAN kod - moze byt v SellersItemIdentification alebo StandardItemIdentification
            item['seller_code'] = self.get_text(line, './/isdoc:Item/isdoc:SellersItemIdentification/isdoc:ID')
            item['ean'] = self.get_text(line, './/isdoc:Item/isdoc:StandardItemIdentification/isdoc:ID')

            # Mnozstvo
            quantity_elem = line.find('.//isdoc:InvoicedQuantity', self.NAMESPACE)
            if quantity_elem is not None:
                item['quantity'] = quantity_elem.text
                item['unit'] = quantity_elem.get('unitCode', 'ks')

            # Jednotkova cena
            item['unit_price'] = self.get_text(line, './/isdoc:UnitPrice')

            # Celkova cena
            item['line_total'] = self.get_text(line, './/isdoc:LineExtensionAmount')

            # DPH sadzba
            item['vat_rate'] = self.get_text(line, './/isdoc:ClassifiedTaxCategory/isdoc:Percent', '20')

            items.append(item)

        return items

    def print_summary(self):
        """Vypise prehlad faktury"""
        if not self.root:
            print("ERROR XML nie je nacitane")
            return

        header = self.parse_header()
        supplier = self.parse_supplier()
        customer = self.parse_customer()
        items = self.parse_items()

        print("\n" + "=" * 100)
        print("FAKTURA - PREHLAD")
        print("=" * 100)

        # Hlavicka
        print(f"\nZAKLADNE UDAJE")
        print(f"  Cislo faktury:    {header.get('invoice_number', 'N/A')}")
        print(f"  UUID:             {header.get('uuid', 'N/A')}")
        print(f"  Datum vystavenia: {header.get('issue_date', 'N/A')}")
        print(f"  Datum dodania:    {header.get('delivery_date', 'N/A')}")
        print(f"  Splatnost:        {header.get('due_date', 'N/A')}")
        print(f"  Celkova suma:     {header.get('total_amount', 'N/A')} {header.get('currency', 'EUR')}")

        # Dodavatel
        print(f"\nDODAVATEL")
        print(f"  Nazov:   {supplier.get('name', 'N/A')}")
        print(f"  ICO:     {supplier.get('ico', 'N/A')}")
        print(f"  DIC:     {supplier.get('dic', 'N/A')}")

        # Odberatel
        print(f"\nODBERATEL")
        print(f"  Nazov: {customer.get('name', 'N/A')}")
        print(f"  ICO:   {customer.get('ico', 'N/A')}")

        # Polozky
        print(f"\nPOLOZKY ({len(items)} ks)")
        print("-" * 100)
        print(f"{'#':<3} {'EAN':<15} {'Nazov':<40} {'Mn.':<6} {'Cena':<10} {'Spolu':<10}")
        print("-" * 100)

        for idx, item in enumerate(items, 1):
            ean = item.get('ean', 'N/A')[:15]
            name = item.get('name', 'N/A')[:40]
            qty = item.get('quantity', '0')
            unit_price = item.get('unit_price', '0')
            total = item.get('line_total', '0')

            print(f"{idx:<3} {ean:<15} {name:<40} {qty:<6} {unit_price:<10} {total:<10}")

        print("-" * 100)
        print("=" * 100)

        return {
            'header': header,
            'supplier': supplier,
            'customer': customer,
            'items': items
        }


def find_xml_files(base_path: str = r"C:\NEX") -> List[Path]:
    """Najde XML subory v zadanej ceste"""
    path = Path(base_path)
    if not path.exists():
        return []

    xml_files = []
    # Hladaj v korenovom adresari
    xml_files.extend(path.glob("*.xml"))
    # Hladaj v podadresaroch (max 2 urovne)
    xml_files.extend(path.glob("*/*.xml"))
    xml_files.extend(path.glob("*/*/*.xml"))

    return sorted(xml_files)


def main():
    """Hlavna funkcia"""
    print("=" * 100)
    print("ISDOC XML Invoice Loader")
    print("=" * 100)

    # Ziskaj cestu k XML
    if len(sys.argv) > 1:
        xml_path = sys.argv[1]
    else:
        # Hladaj XML subory v C:\NEX
        print(f"\nHladam XML subory v C:\\NEX...")
        xml_files = find_xml_files()

        if not xml_files:
            print("ERROR Nenasiel som ziadne XML subory v C:\\NEX")
            print("\nPouzitie: python scripts/load_invoice_xml.py <cesta_k_xml>")
            return 1

        print(f"\nOK Najdene XML subory ({len(xml_files)} ks):")
        for idx, file in enumerate(xml_files[:10], 1):  # Max 10 suborov
            size = file.stat().st_size / 1024  # KB
            print(f"  {idx}. {file.name} ({size:.1f} KB)")

        if len(xml_files) > 10:
            print(f"  ... a dalsich {len(xml_files) - 10} suborov")

        # Pouzi prvy najdeny subor
        xml_path = str(xml_files[0])
        print(f"\nPouzijem: {xml_path}")

    # Nacitaj a parsuj XML
    parser = ISDOCParser(xml_path)
    if not parser.load():
        return 1

    # Zobraz prehlad
    data = parser.print_summary()

    # Info o datach
    print(f"\nData mozete pouzit v dalsich scriptoch")
    print(f"   - Pocet poloziek: {len(data['items'])}")
    print(f"   - Dodavatel: {data['supplier'].get('name', 'N/A')}")

    return 0


if __name__ == '__main__':
    sys.exit(main())