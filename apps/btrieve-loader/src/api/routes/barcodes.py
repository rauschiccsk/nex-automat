"""
Barcode endpoints (BARCODE table).
"""

from fastapi import APIRouter, HTTPException
from nexdata.btrieve.btrieve_client import BtrieveClient
from nexdata.repositories.barcode_repository import BARCODERepository
from nexdata.repositories.gscat_repository import GSCATRepository

from src.api.schemas.barcodes import Barcode, BarcodeList, BarcodeWithProduct
from src.api.schemas.common import PaginatedResponse
from src.core.config import settings

from .dependencies import ApiKey

router = APIRouter()


def get_barcode_repository() -> BARCODERepository:
    """Get BARCODE repository instance."""
    btrieve_config = settings.btrieve_config
    client = BtrieveClient(config_or_path=btrieve_config)
    return BARCODERepository(client)


def get_gscat_repository() -> GSCATRepository:
    """Get GSCAT repository instance."""
    btrieve_config = settings.btrieve_config
    client = BtrieveClient(config_or_path=btrieve_config)
    return GSCATRepository(client)


@router.get("/{ean}", response_model=BarcodeWithProduct)
async def lookup_barcode(
    ean: str,
    _api_key: ApiKey,
):
    """
    Lookup product by EAN barcode.

    Searches both GSCAT (primary barcode) and BARCODE (secondary barcodes).
    Returns barcode with associated product info.

    Args:
        ean: EAN/barcode string
    """
    # Normalize EAN
    ean_normalized = ean.replace(" ", "").replace("-", "").strip()

    if not ean_normalized:
        raise HTTPException(status_code=400, detail="Invalid barcode")

    gscat_repo = get_gscat_repository()
    barcode_repo = get_barcode_repository()

    try:
        # First, try GSCAT (primary barcode) - 95% hit rate
        product = gscat_repo.find_by_barcode(ean_normalized)

        if product:
            return BarcodeWithProduct(
                gs_code=product.GsCode,
                bar_code=product.BarCode,
                product_name=product.GsName,
                product_supplier_code=product.SupplierCode,
            )

        # Then, try BARCODE table (secondary barcodes)
        barcode_record = barcode_repo.find_by_barcode(ean_normalized)

        if barcode_record:
            # Get product from GSCAT
            product = gscat_repo.find_one(lambda r: r.GsCode == barcode_record.gs_code)

            if product:
                return BarcodeWithProduct(
                    gs_code=barcode_record.gs_code,
                    bar_code=barcode_record.bar_code,
                    mod_user=barcode_record.mod_user,
                    mod_date=barcode_record.mod_date,
                    mod_time=barcode_record.mod_time,
                    product_name=product.GsName,
                    product_supplier_code=product.SupplierCode,
                )

        raise HTTPException(status_code=404, detail=f"Barcode {ean} not found")

    finally:
        gscat_repo.close()
        barcode_repo.close()


@router.get("/product/{product_code}", response_model=BarcodeList)
async def get_product_barcodes(
    product_code: int,
    _api_key: ApiKey,
):
    """
    Get all barcodes for a product.

    Returns primary barcode from GSCAT and all secondary barcodes from BARCODE.

    Args:
        product_code: Product code (GsCode/PLU)
    """
    gscat_repo = get_gscat_repository()
    barcode_repo = get_barcode_repository()

    try:
        barcodes = []

        # Get primary barcode from GSCAT
        product = gscat_repo.find_one(lambda r: r.GsCode == product_code)

        if product and product.BarCode:
            barcodes.append(
                Barcode(
                    gs_code=product.GsCode,
                    bar_code=product.BarCode,
                )
            )

        # Get secondary barcodes from BARCODE table
        secondary_records = barcode_repo.find(lambda r: r.gs_code == product_code, max_results=100)

        for record in secondary_records:
            # Avoid duplicates
            if not any(b.bar_code == record.bar_code for b in barcodes):
                barcodes.append(Barcode.from_barcode_record(record))

        if not barcodes:
            raise HTTPException(status_code=404, detail=f"No barcodes found for product {product_code}")

        return PaginatedResponse.create(
            data=barcodes,
            page=1,
            page_size=len(barcodes),
            total_items=len(barcodes),
        )

    finally:
        gscat_repo.close()
        barcode_repo.close()
