"""
Product schemas (GSCAT table).

Based on nexdata.models.gscat.GSCATRecord
"""

from pydantic import BaseModel, Field

from .common import PaginatedResponse


class ProductBase(BaseModel):
    """Base product fields."""

    gs_name: str = Field(..., max_length=60, description="Product name")
    bar_code: str = Field(default="", max_length=15, description="EAN barcode")
    supplier_code: str = Field(default="", max_length=6, description="Supplier code")
    mg_code: str = Field(default="", max_length=2, description="Unit of measure code")


class ProductCreate(ProductBase):
    """Schema for creating a product."""

    gs_code: int | None = Field(
        default=None, description="Product code (auto-generated if not provided)"
    )


class Product(ProductBase):
    """Full product schema (read)."""

    gs_code: int = Field(..., description="Product code (PLU)")

    class Config:
        from_attributes = True

    @classmethod
    def from_gscat_record(cls, record) -> "Product":
        """Create Product from GSCATRecord."""
        return cls(
            gs_code=record.GsCode,
            gs_name=record.GsName,
            bar_code=record.BarCode,
            supplier_code=record.SupplierCode,
            mg_code=record.MgCode,
        )


class ProductList(PaginatedResponse[Product]):
    """Paginated list of products."""

    pass


class ProductSearch(BaseModel):
    """Product search parameters."""

    query: str | None = Field(
        default=None, description="Search query (name or barcode)"
    )
    bar_code: str | None = Field(default=None, description="Filter by barcode")
    supplier_code: str | None = Field(
        default=None, description="Filter by supplier code"
    )
    mg_code: str | None = Field(default=None, description="Filter by unit code")
