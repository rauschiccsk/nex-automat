"""API Schemas for Btrieve-Loader REST API."""

from .barcodes import Barcode, BarcodeCreate, BarcodeList
from .common import PaginatedResponse, PaginationParams, ResponseStatus
from .documents import DocumentHeader, DocumentHeaderList, DocumentItem, DocumentItemList
from .partners import Partner, PartnerCreate, PartnerList
from .products import Product, ProductCreate, ProductList
from .stores import ProductGroup, ProductGroupList

__all__ = [
    # Common
    "PaginationParams",
    "PaginatedResponse",
    "ResponseStatus",
    # Products
    "Product",
    "ProductCreate",
    "ProductList",
    # Partners
    "Partner",
    "PartnerCreate",
    "PartnerList",
    # Documents
    "DocumentHeader",
    "DocumentHeaderList",
    "DocumentItem",
    "DocumentItemList",
    # Barcodes
    "Barcode",
    "BarcodeCreate",
    "BarcodeList",
    # Stores
    "ProductGroup",
    "ProductGroupList",
]
