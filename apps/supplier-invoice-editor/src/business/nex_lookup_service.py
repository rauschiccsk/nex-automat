# src/business/nex_lookup_service.py
"""
NEX Genesis Lookup Service
Vyhladavanie produktov v NEX Genesis GSCAT.BTR podla EAN
"""

import sys
from pathlib import Path
from typing import Dict, Optional

# Add src to path for standalone usage
sys.path.insert(0, str(Path(__file__).parent.parent))

from btrieve.btrieve_client import BtrieveClient

from ..models.barcode import BarcodeRecord
from ..models.gscat import GSCATRecord


class NexLookupService:
    """Service pre vyhladavanie produktov v NEX Genesis"""

    def __init__(self, nex_path: str = r"C:\NEX\YEARACT"):
        """
        Args:
            nex_path: Cesta k NEX Genesis YEARACT adresaru
        """
        self.nex_path = Path(nex_path)
        self.gscat_path = self.nex_path / "STORES" / "GSCAT.BTR"
        self.barcode_path = self.nex_path / "STORES" / "BARCODE.BTR"

        # Validate paths
        if not self.gscat_path.exists():
            raise FileNotFoundError(f"GSCAT.BTR not found: {self.gscat_path}")

    def lookup_by_ean(self, ean: str) -> dict | None:
        """
        Vyhlada produkt podla EAN

        Logika:
        1. Najprv hlada v GSCAT.BarCode (primarny EAN)
        2. Ak nenajde, hlada v BARCODE.BTR (druhotne EAN)

        Args:
            ean: EAN kod

        Returns:
            Dict s produktovymi udajmi alebo None
            {
                'plu': int,
                'name': str,
                'category': int,
                'price_buy': float,
                'price_sell': float,
                'unit': str,
                'in_nex': bool,
                'source': 'GSCAT' | 'BARCODE'
            }
        """
        # 1. Hladaj v GSCAT.BarCode
        gscat_record = self._find_in_gscat(ean)
        if gscat_record:
            return {
                "plu": gscat_record.gs_code,
                "name": gscat_record.gs_name,
                "category": gscat_record.mglst_code,
                "price_buy": float(gscat_record.price_buy),
                "price_sell": float(gscat_record.price_sell),
                "unit": gscat_record.unit,
                "in_nex": True,
                "source": "GSCAT",
            }

        # 2. Hladaj v BARCODE.BTR
        barcode_record = self._find_in_barcode(ean)
        if barcode_record:
            # Nacitaj produkt podla PLU
            gscat_record = self._find_in_gscat_by_plu(barcode_record.gs_code)
            if gscat_record:
                return {
                    "plu": gscat_record.gs_code,
                    "name": gscat_record.gs_name,
                    "category": gscat_record.mglst_code,
                    "price_buy": float(gscat_record.price_buy),
                    "price_sell": float(gscat_record.price_sell),
                    "unit": gscat_record.unit,
                    "in_nex": True,
                    "source": "BARCODE",
                }

        return None

    def _find_in_gscat(self, ean: str) -> GSCATRecord | None:
        """Najde produkt v GSCAT.BTR podla BarCode"""
        client = BtrieveClient()

        try:
            status, pos_block = client.open_file(str(self.gscat_path))
            if status != BtrieveClient.STATUS_SUCCESS:
                return None

            try:
                status, data = client.get_first(pos_block, key_num=0)

                while status == BtrieveClient.STATUS_SUCCESS:
                    try:
                        if len(data) >= 72:
                            # Read BarCode: [00 00][length][data...]
                            barcode_length = data[59] if len(data) > 59 else 0
                            barcode_data = (
                                data[60 : 60 + barcode_length]
                                if len(data) >= 60 + barcode_length
                                else b""
                            )
                            barcode_str = barcode_data.decode("cp852", errors="ignore")

                            if barcode_str.strip() == ean.strip():
                                return GSCATRecord.from_bytes(data)
                    except:
                        pass

                    status, data = client.get_next(pos_block)

                return None
            finally:
                client.close_file(pos_block)
        except:
            return None

    def _find_in_gscat_by_plu(self, plu: int) -> GSCATRecord | None:
        """Najde produkt v GSCAT.BTR podla PLU"""
        client = BtrieveClient()

        try:
            status, pos_block = client.open_file(str(self.gscat_path))
            if status != BtrieveClient.STATUS_SUCCESS:
                return None

            try:
                status, data = client.get_first(pos_block, key_num=0)

                while status == BtrieveClient.STATUS_SUCCESS:
                    try:
                        record = GSCATRecord.from_bytes(data)
                        if record.gs_code == plu:
                            return record
                    except:
                        pass

                    status, data = client.get_next(pos_block)

                return None
            finally:
                client.close_file(pos_block)
        except:
            return None

    def _find_in_barcode(self, ean: str) -> BarcodeRecord | None:
        """Najde zaznam v BARCODE.BTR"""
        if not self.barcode_path.exists():
            return None

        client = BtrieveClient()

        try:
            status, pos_block = client.open_file(str(self.barcode_path))
            if status != BtrieveClient.STATUS_SUCCESS:
                return None

            try:
                status, data = client.get_first(pos_block, key_num=0)

                while status == BtrieveClient.STATUS_SUCCESS:
                    try:
                        record = BarcodeRecord.from_bytes(data)
                        if record.bar_code.strip() == ean.strip():
                            return record
                    except:
                        pass

                    status, data = client.get_next(pos_block)

                return None
            finally:
                client.close_file(pos_block)
        except:
            return None
