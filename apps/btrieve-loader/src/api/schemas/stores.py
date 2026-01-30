"""
Product group schemas (MGLST table).

Based on nexdata.models.mglst.MGLSTRecord
"""

from datetime import datetime

from pydantic import BaseModel, Field

from .common import PaginatedResponse


class ProductGroupBase(BaseModel):
    """Base product group fields."""

    mglst_name: str = Field(..., max_length=80, description="Group name")
    short_name: str = Field(default="", max_length=30, description="Short name")

    parent_code: int = Field(default=0, ge=0, description="Parent group code (0 = root)")
    level: int = Field(default=1, ge=1, description="Hierarchy level")
    sort_order: int = Field(default=0, ge=0, description="Sort order")
    color_code: str = Field(default="", max_length=10, description="Color code (hex)")

    default_vat_rate: float = Field(default=20.0, ge=0, le=100, description="Default VAT rate %")
    default_unit: str = Field(default="ks", max_length=10, description="Default unit of measure")

    active: bool = Field(default=True, description="Is active")
    show_in_catalog: bool = Field(default=True, description="Show in catalog")

    note: str = Field(default="", max_length=100, description="Note")
    description: str = Field(default="", max_length=200, description="Description")


class ProductGroupCreate(ProductGroupBase):
    """Schema for creating a product group."""

    mglst_code: int | None = Field(default=None, description="Group code (auto-generated if not provided)")


class ProductGroup(ProductGroupBase):
    """Full product group schema (read)."""

    mglst_code: int = Field(..., description="Group code")
    mod_user: str = Field(default="", description="Last modified by")
    mod_date: datetime | None = Field(default=None, description="Last modified date")

    class Config:
        from_attributes = True

    @classmethod
    def from_mglst_record(cls, record) -> "ProductGroup":
        """Create ProductGroup from MGLSTRecord."""
        return cls(
            mglst_code=record.mglst_code,
            mglst_name=record.mglst_name,
            short_name=record.short_name,
            parent_code=record.parent_code,
            level=record.level,
            sort_order=record.sort_order,
            color_code=record.color_code,
            default_vat_rate=record.default_vat_rate,
            default_unit=record.default_unit,
            active=record.active,
            show_in_catalog=record.show_in_catalog,
            note=record.note,
            description=record.description,
            mod_user=record.mod_user,
            mod_date=record.mod_date,
        )

    @property
    def is_root(self) -> bool:
        """Check if this is a root-level category."""
        return self.parent_code == 0


class ProductGroupList(PaginatedResponse[ProductGroup]):
    """Paginated list of product groups."""

    pass


class ProductGroupTree(ProductGroup):
    """Product group with children for tree view."""

    children: list["ProductGroupTree"] = Field(default_factory=list, description="Child groups")

    @classmethod
    def build_tree(cls, groups: list[ProductGroup]) -> list["ProductGroupTree"]:
        """Build hierarchical tree from flat list of groups."""
        # Create lookup dict
        lookup: dict[int, ProductGroupTree] = {}
        for group in groups:
            tree_node = cls(
                mglst_code=group.mglst_code,
                mglst_name=group.mglst_name,
                short_name=group.short_name,
                parent_code=group.parent_code,
                level=group.level,
                sort_order=group.sort_order,
                color_code=group.color_code,
                default_vat_rate=group.default_vat_rate,
                default_unit=group.default_unit,
                active=group.active,
                show_in_catalog=group.show_in_catalog,
                note=group.note,
                description=group.description,
                mod_user=group.mod_user,
                mod_date=group.mod_date,
            )
            lookup[group.mglst_code] = tree_node

        # Build tree
        roots: list[ProductGroupTree] = []
        for node in lookup.values():
            if node.parent_code == 0:
                roots.append(node)
            elif node.parent_code in lookup:
                lookup[node.parent_code].children.append(node)

        # Sort children by sort_order
        def sort_children(node: ProductGroupTree) -> None:
            node.children.sort(key=lambda x: x.sort_order)
            for child in node.children:
                sort_children(child)

        for root in roots:
            sort_children(root)

        roots.sort(key=lambda x: x.sort_order)
        return roots


class ProductGroupSearch(BaseModel):
    """Product group search parameters."""

    query: str | None = Field(default=None, description="Search query (name)")
    parent_code: int | None = Field(default=None, description="Filter by parent code")
    active: bool | None = Field(default=None, description="Filter by active status")
    level: int | None = Field(default=None, description="Filter by level")
