"""
Barcode schemas (BARCODE table).

Based on nexdata.models.barcode.BarcodeRecord
"""

from datetime import datetime

from pydantic import BaseModel, Field, field_validator

from .common import PaginatedResponse


class BarcodeBase(BaseModel):
    """Base barcode fields."""

    gs_code: int = Field(..., gt=0, description="Product code (PLU)")
    bar_code: str = Field(..., min_length=1, max_length=15, description="Barcode string")

    @field_validator("bar_code")
    @classmethod
    def validate_barcode(cls, v: str) -> str:
        """Validate barcode format."""
        v = v.strip()
        if not v:
            raise ValueError("Barcode cannot be empty")
        if len(v) < 8:
            raise ValueError("Barcode must be at least 8 characters")
        return v


class BarcodeCreate(BarcodeBase):
    """Schema for creating a barcode."""

    pass


class Barcode(BarcodeBase):
    """Full barcode schema (read)."""

    mod_user: str = Field(default="", description="Last modified by")
    mod_date: datetime | None = Field(default=None, description="Last modified date")
    mod_time: datetime | None = Field(default=None, description="Last modified time")

    class Config:
        from_attributes = True

    @classmethod
    def from_barcode_record(cls, record) -> "Barcode":
        """Create Barcode from BarcodeRecord."""
        return cls(
            gs_code=record.gs_code,
            bar_code=record.bar_code,
            mod_user=record.mod_user,
            mod_date=record.mod_date,
            mod_time=record.mod_time,
        )


class BarcodeList(PaginatedResponse[Barcode]):
    """Paginated list of barcodes."""

    pass


class BarcodeSearch(BaseModel):
    """Barcode search parameters."""

    gs_code: int | None = Field(default=None, description="Filter by product code")
    bar_code: str | None = Field(default=None, description="Search by barcode (partial match)")


class BarcodeWithProduct(Barcode):
    """Barcode with associated product info."""

    product_name: str = Field(default="", description="Product name from GSCAT")
    product_supplier_code: str = Field(default="", description="Supplier code from GSCAT")
