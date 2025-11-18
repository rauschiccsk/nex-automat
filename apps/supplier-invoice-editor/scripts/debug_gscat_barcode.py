#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""
Debug script - zobrazí prvých 10 produktov z GSCAT s ich BarCode poľom
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from btrieve.btrieve_client import BtrieveClient
from models.gscat import GSCATRecord


def debug_gscat_barcodes(nex_path: str = r"C:\NEX\YEARACT", limit: int = 10):
    """Zobrazí prvých N produktov z GSCAT s BarCode"""

    gscat_path = Path(nex_path) / "STORES" / "GSCAT.BTR"

    if not gscat_path.exists():
        print(f"ERROR GSCAT.BTR not found: {gscat_path}")
        return

    print("=" * 100)
    print("GSCAT.BTR - BarCode Debug")
    print("=" * 100)
    print(f"Súbor: {gscat_path}")
    print(f"Zobrazujem prvých {limit} záznamov\n")

    client = BtrieveClient()

    try:
        # Open GSCAT.BTR
        status, pos_block = client.open_file(str(gscat_path))
        if status != BtrieveClient.STATUS_SUCCESS:
            print(f"ERROR Failed to open GSCAT.BTR: {client.get_status_message(status)}")
            return

        try:
            print(f"{'#':<4} {'PLU':<8} {'BarCode':<18} {'Názov':<40} {'Veľkosť':<10}")
            print("-" * 100)

            # Get first record
            status, data = client.get_first(pos_block, key_num=0)
            count = 0

            while status == BtrieveClient.STATUS_SUCCESS and count < limit:
                count += 1

                try:
                    # Parse full record
                    record = GSCATRecord.from_bytes(data)

                    # Extract BarCode directly from raw data
                    # Structure: [00 00][length][data...] at offset 57
                    barcode_raw = data[57:72] if len(data) >= 72 else b''
                    barcode_length = data[59] if len(data) > 59 else 0
                    barcode_data = data[60:60 + barcode_length] if len(data) >= 60 + barcode_length else b''

                    # Decode
                    barcode_str = barcode_data.decode('cp852', errors='ignore')

                    # Show hex dump of BarCode bytes
                    barcode_hex = ' '.join(f'{b:02x}' for b in barcode_raw[:15])

                    print(f"{count:<4} {record.gs_code:<8} {barcode_str:<18} {record.gs_name[:40]:<40} {len(data)} B")

                    # Ak BarCode nie je prázdny, zobraz detaily
                    if barcode_str.strip():
                        print(f"     ├─ Length:     {barcode_length}")
                        print(f"     ├─ BarCode:    '{barcode_str}'")
                        print(f"     └─ HEX:        {barcode_hex}")
                    else:
                        print(f"     └─ (prázdne BarCode)")

                except Exception as e:
                    print(f"{count:<4} ERROR: {e}")

                # Next record
                status, data = client.get_next(pos_block)

            print("-" * 100)
            print(f"\nCelkom zobrazených: {count} záznamov")

        finally:
            client.close_file(pos_block)

    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()


def search_by_ean(ean: str, nex_path: str = r"C:\NEX\YEARACT"):
    """Vyhľadá konkrétny EAN v GSCAT"""

    gscat_path = Path(nex_path) / "STORES" / "GSCAT.BTR"

    print("\n" + "=" * 100)
    print(f"Hľadám EAN: {ean}")
    print("=" * 100)

    client = BtrieveClient()

    try:
        status, pos_block = client.open_file(str(gscat_path))
        if status != BtrieveClient.STATUS_SUCCESS:
            print(f"ERROR Failed to open GSCAT.BTR")
            return

        try:
            status, data = client.get_first(pos_block, key_num=0)
            count = 0
            found = False

            while status == BtrieveClient.STATUS_SUCCESS:
                count += 1

                try:
                    if len(data) >= 72:
                        # Read length and data
                        barcode_length = data[59] if len(data) > 59 else 0
                        barcode_data = data[60:60 + barcode_length] if len(data) >= 60 + barcode_length else b''
                        barcode_str = barcode_data.decode('cp852', errors='ignore')

                        # Porovnaj
                        if barcode_str.strip() == ean.strip():
                            found = True
                            record = GSCATRecord.from_bytes(data)

                            print(f"\nOK NÁJDENÉ!")
                            print(f"  PLU:      {record.gs_code}")
                            print(f"  Názov:    {record.gs_name}")
                            print(f"  BarCode:  '{barcode_str}'")
                            print(f"  Length:   {barcode_length}")
                            print(f"  Záznam #: {count}")
                            break

                except Exception as e:
                    pass

                status, data = client.get_next(pos_block)

            if not found:
                print(f"\nMISSING EAN '{ean}' nebol nájdený v GSCAT.BTR")
                print(f"Prehľadaných záznamov: {count}")

        finally:
            client.close_file(pos_block)

    except Exception as e:
        print(f"ERROR: {e}")


def main():
    """Hlavná funkcia"""

    if len(sys.argv) > 1:
        # Hľadaj konkrétny EAN
        ean = sys.argv[1]
        search_by_ean(ean)
    else:
        # Zobraz prvých 10 záznamov
        debug_gscat_barcodes(limit=20)


if __name__ == '__main__':
    main()