#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""
Script na test Btrieve lookup podla EAN kodu
Overi polozky faktury v NEX Genesis katalogu (BARCODE.BTR + GSCAT.BTR)

Pouzitie: python scripts/test_barcode_lookup.py [ean_code1] [ean_code2] ...
          python scripts/test_barcode_lookup.py --from-xml [xml_path]
"""

import sys
import os
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from decimal import Decimal

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from btrieve.btrieve_client import BtrieveClient
from models.barcode import BarcodeRecord
from models.gscat import GSCATRecord


class BarcodeLookupService:
    """Service pre vyhladavanie produktov podla EAN kodu v NEX Genesis"""

    def __init__(self, nex_path: str = r"C:\NEX\YEARACT"):
        """
        Inicializacia sluzby

        Args:
            nex_path: Cesta k NEX Genesis YEARACT adresaru
        """
        self.nex_path = Path(nex_path)
        self.barcode_path = self.nex_path / "STORES" / "BARCODE.BTR"
        self.gscat_path = self.nex_path / "STORES" / "GSCAT.BTR"

        # Validate paths
        if not self.nex_path.exists():
            raise FileNotFoundError(f"NEX path not found: {self.nex_path}")

        if not self.barcode_path.exists():
            raise FileNotFoundError(f"BARCODE.BTR not found: {self.barcode_path}")

        if not self.gscat_path.exists():
            raise FileNotFoundError(f"GSCAT.BTR not found: {self.gscat_path}")

        print(f"OK NEX Genesis path: {self.nex_path}")
        print(f"OK BARCODE.BTR: {self.barcode_path.name}")
        print(f"OK GSCAT.BTR: {self.gscat_path.name}")

    def lookup_by_ean(self, ean: str) -> Optional[Tuple[Optional[BarcodeRecord], GSCATRecord]]:
        """
        Vyhlada produkt podla EAN kodu

        Logika:
        1. Najprv hlada EAN v GSCAT.BarCode (primarny EAN)
        2. Ak nenajde, hlada v BARCODE.BTR (druhotne EAN)

        Args:
            ean: EAN kod (ciarovy kod)

        Returns:
            Tuple (BarcodeRecord|None, GSCATRecord) ak najdene, inak None
        """
        # 1. Najprv hladaj v GSCAT.BarCode (primarny EAN)
        gscat_record = self._find_product_by_barcode(ean)
        if gscat_record:
            # Nasli sme v GSCAT priamo
            return None, gscat_record

        # 2. Ak nenasli, hladaj v BARCODE.BTR (druhotne EAN)
        barcode_record = self._find_barcode(ean)
        if not barcode_record:
            return None

        # 3. Nacitaj produkt z GSCAT.BTR podla PLU (gs_code)
        gscat_record = self._find_product_by_plu(barcode_record.gs_code)
        if not gscat_record:
            return None

        return barcode_record, gscat_record

    def _find_barcode(self, ean: str) -> Optional[BarcodeRecord]:
        """Najde BARCODE zaznam podla EAN"""
        client = BtrieveClient()

        try:
            # Open BARCODE.BTR
            status, pos_block = client.open_file(str(self.barcode_path))
            if status != BtrieveClient.STATUS_SUCCESS:
                print(f"ERROR Failed to open BARCODE.BTR: {client.get_status_message(status)}")
                return None

            try:
                # Prechadzaj vsetky zaznamy a hladaj EAN
                status, data = client.get_first(pos_block, key_num=0)

                while status == BtrieveClient.STATUS_SUCCESS:
                    try:
                        record = BarcodeRecord.from_bytes(data)

                        # Porovnaj EAN (ignoruj whitespace)
                        if record.bar_code.strip() == ean.strip():
                            return record

                    except Exception as e:
                        # Skip invalid records
                        pass

                    # Next record
                    status, data = client.get_next(pos_block)

                return None

            finally:
                client.close_file(pos_block)

        except Exception as e:
            print(f"ERROR Error searching BARCODE: {e}")
            return None

    def _find_product_by_barcode(self, ean: str) -> Optional[GSCATRecord]:
        """Najde GSCAT zaznam podla BarCode (primarny EAN v GSCAT)"""
        client = BtrieveClient()

        try:
            # Open GSCAT.BTR
            status, pos_block = client.open_file(str(self.gscat_path))
            if status != BtrieveClient.STATUS_SUCCESS:
                print(f"ERROR Failed to open GSCAT.BTR: {client.get_status_message(status)}")
                return None

            try:
                # Prechadzaj vsetky zaznamy a hladaj BarCode
                status, data = client.get_first(pos_block, key_num=0)

                while status == BtrieveClient.STATUS_SUCCESS:
                    try:
                        # Extrahuj BarCode priamo z raw dat
                        # Struktura: [00 00][length][data...] - preskocime prve 3 byty
                        if len(data) >= 72:
                            # Length byte na offset 59
                            barcode_length = data[59] if len(data) > 59 else 0

                            # Data zacinaju na offset 60
                            barcode_bytes = data[60:60 + barcode_length]
                            barcode_str = barcode_bytes.decode('cp852', errors='ignore').rstrip('\x00 ')

                            # Porovnaj EAN
                            if barcode_str.strip() == ean.strip():
                                # Nasli sme - parsuj cely zaznam
                                record = GSCATRecord.from_bytes(data)
                                return record

                    except Exception as e:
                        # Skip invalid records
                        pass

                    # Next record
                    status, data = client.get_next(pos_block)

                return None

            finally:
                client.close_file(pos_block)

        except Exception as e:
            print(f"ERROR Error searching GSCAT by BarCode: {e}")
            return None

    def _find_product_by_plu(self, gs_code: int) -> Optional[GSCATRecord]:
        """Najde GSCAT zaznam podla PLU (gs_code)"""
        client = BtrieveClient()

        try:
            # Open GSCAT.BTR
            status, pos_block = client.open_file(str(self.gscat_path))
            if status != BtrieveClient.STATUS_SUCCESS:
                print(f"ERROR Failed to open GSCAT.BTR: {client.get_status_message(status)}")
                return None

            try:
                # Prechadzaj vsetky zaznamy a hladaj gs_code
                status, data = client.get_first(pos_block, key_num=0)

                while status == BtrieveClient.STATUS_SUCCESS:
                    try:
                        record = GSCATRecord.from_bytes(data)

                        if record.gs_code == gs_code:
                            return record

                    except Exception as e:
                        # Skip invalid records
                        pass

                    # Next record
                    status, data = client.get_next(pos_block)

                return None

            finally:
                client.close_file(pos_block)

        except Exception as e:
            print(f"ERROR Error searching GSCAT: {e}")
            return None

    def check_invoice_items(self, items: List[Dict]) -> Dict:
        """
        Skontroluje vsetky polozky faktury v NEX Genesis

        Args:
            items: List slovnikov s klucmi: name, ean, quantity, unit_price

        Returns:
            Dict so statistikami a detailmi
        """
        results = {
            'total': len(items),
            'found': 0,
            'not_found': 0,
            'items': []
        }

        print(f"\nKontrolujem {len(items)} poloziek v NEX Genesis...")
        print("-" * 100)

        for idx, item in enumerate(items, 1):
            ean = item.get('ean', '').strip()
            name = item.get('name', 'N/A')

            if not ean:
                print(f"  {idx}. WARNING  {name[:50]:<50} - EAN chyba")
                results['items'].append({
                    'index': idx,
                    'name': name,
                    'ean': '',
                    'status': 'no_ean',
                    'in_nex': False
                })
                results['not_found'] += 1
                continue

            # Lookup v NEX Genesis
            result = self.lookup_by_ean(ean)

            if result:
                barcode, product = result
                status_icon = "OK"
                status = "found"
                results['found'] += 1

                # Zisti ci nasiel priamo v GSCAT alebo cez BARCODE
                source = "GSCAT" if barcode is None else "BARCODE"

                print(
                    f"  {idx}. {status_icon} {name[:50]:<50} PLU: {product.gs_code:>6} | {product.gs_name[:30]} ({source})")

                results['items'].append({
                    'index': idx,
                    'name': name,
                    'ean': ean,
                    'status': status,
                    'in_nex': True,
                    'plu': product.gs_code,
                    'nex_name': product.gs_name,
                    'nex_price_buy': float(product.price_buy),
                    'nex_price_sell': float(product.price_sell),
                    'nex_unit': product.unit,
                    'nex_category': product.mglst_code,
                    'found_in': source
                })
            else:
                status_icon = "MISSING"
                status = "not_found"
                results['not_found'] += 1

                print(f"  {idx}. {status_icon} {name[:50]:<50} EAN: {ean} (nie je v NEX)")

                results['items'].append({
                    'index': idx,
                    'name': name,
                    'ean': ean,
                    'status': status,
                    'in_nex': False
                })

        print("-" * 100)
        print(f"\nVYSLEDKY:")
        print(f"   Celkom poloziek:   {results['total']}")
        print(f"   OK Najdene v NEX:  {results['found']} ({results['found'] / results['total'] * 100:.1f}%)")
        print(f"   MISSING Nie su v NEX: {results['not_found']} ({results['not_found'] / results['total'] * 100:.1f}%)")

        return results


def load_invoice_xml(xml_path: str) -> List[Dict]:
    """Nacita polozky z ISDOC XML faktury"""
    import xml.etree.ElementTree as ET

    tree = ET.parse(xml_path)
    root = tree.getroot()

    NAMESPACE = {'isdoc': 'http://isdoc.cz/namespace/2013'}

    items = []
    lines = root.findall('.//isdoc:InvoiceLine', NAMESPACE)

    for line in lines:
        item = {}

        # Nazov
        desc = line.find('.//isdoc:Item/isdoc:Description', NAMESPACE)
        item['name'] = desc.text if desc is not None else 'N/A'

        # EAN - StandardItemIdentification
        standard_item = line.find('.//isdoc:Item/isdoc:StandardItemIdentification', NAMESPACE)
        if standard_item is not None:
            ean_elem = standard_item.find('.//isdoc:ID', NAMESPACE)
            item['ean'] = ean_elem.text if ean_elem is not None else ''
        else:
            item['ean'] = ''

        # Mnozstvo
        qty = line.find('.//isdoc:InvoicedQuantity', NAMESPACE)
        if qty is not None:
            item['quantity'] = qty.text
            item['unit'] = qty.get('unitCode', 'ks')

        # Jednotkova cena
        price = line.find('.//isdoc:UnitPrice', NAMESPACE)
        item['unit_price'] = price.text if price is not None else '0'

        items.append(item)

    return items


def main():
    """Hlavna funkcia"""
    print("=" * 100)
    print("NEX Genesis Barcode Lookup Test")
    print("=" * 100)

    # Initialize service
    try:
        service = BarcodeLookupService()
    except FileNotFoundError as e:
        print(f"\nERROR {e}")
        print("\nSkontroluj cestu k NEX Genesis: C:\\NEX\\YEARACT")
        return 1
    except Exception as e:
        print(f"\nERROR Chyba inicializacie: {e}")
        return 1

    # Zisti rezim
    if len(sys.argv) > 1 and sys.argv[1] == '--from-xml':
        # Load from XML
        if len(sys.argv) < 3:
            print("ERROR Chyba cesta k XML suboru")
            print("Pouzitie: python scripts/test_barcode_lookup.py --from-xml <xml_path>")
            return 1

        xml_path = sys.argv[2]
        print(f"\nNacitavam polozky z XML: {xml_path}")

        try:
            items = load_invoice_xml(xml_path)
            print(f"OK Nacitane {len(items)} poloziek")
        except Exception as e:
            print(f"ERROR Chyba nacitania XML: {e}")
            return 1

        # Check items
        results = service.check_invoice_items(items)

    elif len(sys.argv) > 1:
        # Test jednotlive EAN kody z argumentov
        ean_codes = sys.argv[1:]

        print(f"\nTestujem {len(ean_codes)} EAN kodov...")
        print("-" * 100)

        for idx, ean in enumerate(ean_codes, 1):
            print(f"\n{idx}. EAN: {ean}")

            result = service.lookup_by_ean(ean)

            if result:
                barcode, product = result
                source = "GSCAT.BarCode" if barcode is None else "BARCODE.BTR"
                print(f"   OK NAJDENE v NEX Genesis ({source})")
                print(f"   PLU:           {product.gs_code}")
                print(f"   Nazov:         {product.gs_name}")
                print(f"   Kategoria:     {product.mglst_code}")
                print(f"   Jednotka:      {product.unit}")
                print(f"   Nakupna cena:  {product.price_buy} EUR")
                print(f"   Predajna cena: {product.price_sell} EUR")
                print(f"   DPH:           {product.vat_rate}%")
                print(f"   Aktivny:       {'Ano' if product.active else 'Nie'}")
            else:
                print(f"   MISSING NIE JE v NEX Genesis")

        print("-" * 100)

    else:
        # Ziadne argumenty - zobraz help
        print("\nPOUZITIE:")
        print("\n  1. Test jednotlivych EAN kodov:")
        print("     python scripts/test_barcode_lookup.py 8594000123456 8594000654321")
        print("\n  2. Test poloziek z XML faktury:")
        print("     python scripts/test_barcode_lookup.py --from-xml C:\\NEX\\invoice.xml")
        print("\n  3. Kombinacia s load_invoice_xml.py:")
        print("     python scripts/load_invoice_xml.py")
        print("     python scripts/test_barcode_lookup.py --from-xml <xml_path>")

    return 0


if __name__ == '__main__':
    sys.exit(main())