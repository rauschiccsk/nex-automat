"""
Migration API schemas.
Pydantic modely pre MIG modul — migrácia dát z NEX Genesis (Btrieve) do PostgreSQL.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# === Category schemas ===


class DependencyInfo(BaseModel):
    """Info o jednej dependency."""

    code: str
    name: str
    status: str  # pending, completed, failed
    is_satisfied: bool  # True ak status == 'completed'


class CategoryResponse(BaseModel):
    """Jedna migračná kategória s kompletným stavom."""

    code: str
    name: str
    description: str
    source_tables: list[str]
    target_tables: list[str]
    dependency_codes: list[str]
    dependencies: list[DependencyInfo]
    level: int  # dependency úroveň (0, 1, 2, 3)

    # Status z DB
    status: str  # pending, completed, failed
    record_count: int
    first_migrated_at: Optional[datetime] = None
    last_migrated_at: Optional[datetime] = None
    last_batch_id: Optional[int] = None

    # Computed
    can_run: bool  # True ak všetky dependencies completed
    blocked_by: list[str]  # kódy nesplnených dependencies


class CategoriesListResponse(BaseModel):
    """Zoznam všetkých kategórií."""

    categories: list[CategoryResponse]
    total: int
    completed: int
    pending: int
    failed: int


# === Batch schemas ===


class BatchResponse(BaseModel):
    """Jeden migration batch."""

    id: int
    category: str
    status: str
    source_count: int
    target_count: int
    error_count: int
    skipped_count: int
    started_at: datetime
    completed_at: Optional[datetime] = None
    error_log: Optional[str] = None
    metadata: Optional[dict] = None
    duration_seconds: Optional[float] = None


class BatchListResponse(BaseModel):
    """Zoznam batchov pre kategóriu."""

    batches: list[BatchResponse]
    total: int


# === Migration run schemas ===


class MigrationRunRequest(BaseModel):
    """Request na spustenie migrácie."""

    category: str
    dry_run: bool = False


class MigrationRunResponse(BaseModel):
    """Response po spustení migrácie."""

    batch_id: Optional[int] = None
    category: str
    status: str
    source_count: int = 0
    target_count: int = 0
    error_count: int = 0
    errors: list[dict] = []
    warnings: list[dict] = []
    duration_seconds: float = 0
    message: str = ""


# === ID Mapping schemas ===


class IdMappingResponse(BaseModel):
    """Jeden ID mapping záznam."""

    source_table: str
    source_key: str
    target_table: str
    target_id: str
    migrated_at: datetime


class IdMappingListResponse(BaseModel):
    """Zoznam ID mappingov."""

    items: list[IdMappingResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


# === Stats schemas ===


class MigrationStatsResponse(BaseModel):
    """Celkové štatistiky migrácie."""

    total_categories: int
    completed_categories: int
    pending_categories: int
    failed_categories: int
    total_records_migrated: int
    total_batches: int
    last_migration_at: Optional[datetime] = None
