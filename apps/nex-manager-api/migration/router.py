"""Migration API endpoints — categories, batches, stats, mappings, run, reset."""

import json
import math
import os
import sys
import time
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status

from auth.dependencies import require_permission
from database import get_db
from nex_config.limits import DEFAULT_PAGE_SIZE

from .schemas import (
    BatchListResponse,
    BatchResponse,
    CategoriesListResponse,
    CategoryResponse,
    DependencyInfo,
    IdMappingListResponse,
    IdMappingResponse,
    MigrationRunRequest,
    MigrationRunResponse,
    MigrationStatsResponse,
)

# ---------------------------------------------------------------------------
# Import nex-migration config (categories, dependency graph)
# ---------------------------------------------------------------------------
_migration_path = Path(__file__).resolve().parents[2] / "nex-migration"
if str(_migration_path) not in sys.path:
    sys.path.insert(0, str(_migration_path))

from config.categories import CATEGORIES  # noqa: E402

router = APIRouter(prefix="/api/migration", tags=["migration"])


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _compute_levels() -> dict[str, int]:
    """Compute dependency level for each category via topological sort."""
    levels: dict[str, int] = {}
    remaining = set(CATEGORIES.keys())
    completed: set[str] = set()
    current_level = 0

    while remaining:
        ready = [
            code
            for code in remaining
            if all(dep in completed for dep in CATEGORIES[code].dependencies)
        ]
        if not ready:
            break
        for code in sorted(ready):
            levels[code] = current_level
        completed.update(ready)
        remaining -= set(ready)
        current_level += 1

    return levels


_CATEGORY_LEVELS = _compute_levels()


def _get_category_status(cur, category_code: str) -> dict:
    """Fetch status row for a single category from migration_category_status."""
    cur.execute(
        "SELECT status, record_count, first_migrated_at, last_migrated_at, last_batch_id "
        "FROM migration_category_status WHERE category = %s",
        (category_code,),
    )
    row = cur.fetchone()
    if row:
        return {
            "status": row[0],
            "record_count": row[1] or 0,
            "first_migrated_at": row[2],
            "last_migrated_at": row[3],
            "last_batch_id": row[4],
        }
    return {
        "status": "pending",
        "record_count": 0,
        "first_migrated_at": None,
        "last_migrated_at": None,
        "last_batch_id": None,
    }


def _build_category_response(cur, code: str) -> CategoryResponse:
    """Build a full CategoryResponse for a given category code."""
    cat = CATEGORIES[code]
    cat_status = _get_category_status(cur, code)

    # Build dependency info
    dependencies: list[DependencyInfo] = []
    blocked_by: list[str] = []
    for dep_code in cat.dependencies:
        dep_cat = CATEGORIES[dep_code]
        dep_status = _get_category_status(cur, dep_code)
        is_satisfied = dep_status["status"] == "completed"
        dependencies.append(
            DependencyInfo(
                code=dep_code,
                name=dep_cat.name,
                status=dep_status["status"],
                is_satisfied=is_satisfied,
            )
        )
        if not is_satisfied:
            blocked_by.append(dep_code)

    can_run = len(blocked_by) == 0

    return CategoryResponse(
        code=cat.code,
        name=cat.name,
        description=cat.description,
        source_tables=cat.source_tables,
        target_tables=cat.target_tables,
        dependency_codes=cat.dependencies,
        dependencies=dependencies,
        level=_CATEGORY_LEVELS.get(code, 0),
        status=cat_status["status"],
        record_count=cat_status["record_count"],
        first_migrated_at=cat_status["first_migrated_at"],
        last_migrated_at=cat_status["last_migrated_at"],
        last_batch_id=cat_status["last_batch_id"],
        can_run=can_run,
        blocked_by=blocked_by,
    )


def _write_audit_log(
    cur,
    user_id: int,
    action: str,
    entity_type: str,
    entity_id: str | None = None,
    details: dict | None = None,
) -> None:
    """Insert an audit log entry."""
    cur.execute(
        "INSERT INTO audit_log (user_id, action, entity_type, entity_id, details) "
        "VALUES (%s, %s, %s, %s, %s)",
        (
            user_id,
            action,
            entity_type,
            None,  # entity_id is INTEGER — pass category info in details
            json.dumps({**(details or {}), "category": entity_id})
            if entity_id
            else json.dumps(details)
            if details
            else None,
        ),
    )


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.get("/categories", response_model=CategoriesListResponse)
def list_categories(
    _current_user=Depends(require_permission("MIG", "can_view")),
    db=Depends(get_db),
):
    """List all migration categories with status and dependency info."""
    cur = db.cursor()

    categories: list[CategoryResponse] = []
    for code in CATEGORIES:
        categories.append(_build_category_response(cur, code))

    # Sort by level ASC, then code ASC
    categories.sort(key=lambda c: (c.level, c.code))

    completed = sum(1 for c in categories if c.status == "completed")
    pending = sum(1 for c in categories if c.status == "pending")
    failed = sum(1 for c in categories if c.status == "failed")

    return CategoriesListResponse(
        categories=categories,
        total=len(categories),
        completed=completed,
        pending=pending,
        failed=failed,
    )


@router.get("/categories/{code}", response_model=CategoryResponse)
def get_category_detail(
    code: str,
    _current_user=Depends(require_permission("MIG", "can_view")),
    db=Depends(get_db),
):
    """Get a single migration category by code."""
    if code not in CATEGORIES:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Migračná kategória '{code}' neexistuje",
        )

    cur = db.cursor()
    return _build_category_response(cur, code)


@router.get("/categories/{code}/batches", response_model=BatchListResponse)
def list_category_batches(
    code: str,
    _current_user=Depends(require_permission("MIG", "can_view")),
    db=Depends(get_db),
):
    """List migration batches for a specific category."""
    if code not in CATEGORIES:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Migračná kategória '{code}' neexistuje",
        )

    cur = db.cursor()

    cur.execute(
        "SELECT id, category, status, source_count, target_count, error_count, "
        "skipped_count, started_at, completed_at, error_log, metadata "
        "FROM migration_batches WHERE category = %s ORDER BY started_at DESC",
        (code,),
    )
    rows = cur.fetchall()

    batches: list[BatchResponse] = []
    for row in rows:
        started_at = row[7]
        completed_at = row[8]
        duration = None
        if completed_at and started_at:
            duration = (completed_at - started_at).total_seconds()

        batches.append(
            BatchResponse(
                id=row[0],
                category=row[1],
                status=row[2],
                source_count=row[3] or 0,
                target_count=row[4] or 0,
                error_count=row[5] or 0,
                skipped_count=row[6] or 0,
                started_at=started_at,
                completed_at=completed_at,
                error_log=row[9],
                metadata=row[10],
                duration_seconds=duration,
            )
        )

    return BatchListResponse(batches=batches, total=len(batches))


@router.post("/run", response_model=MigrationRunResponse)
def run_migration(
    body: MigrationRunRequest,
    current_user=Depends(require_permission("MIG", "can_create")),
    db=Depends(get_db),
):
    """Start a migration run for a specific category.

    Currently supports: PAB.
    Other categories return 501 until their transformer/loader are implemented.
    """
    # Validate category exists
    if body.category not in CATEGORIES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Neznáma migračná kategória: '{body.category}'",
        )

    cur = db.cursor()

    # Check dependencies
    cat = CATEGORIES[body.category]
    blocked_by: list[str] = []
    for dep_code in cat.dependencies:
        dep_status = _get_category_status(cur, dep_code)
        if dep_status["status"] != "completed":
            blocked_by.append(dep_code)

    if blocked_by:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Nesplnené závislosti pre '{body.category}': {blocked_by}",
        )

    # Check for running batch
    cur.execute(
        "SELECT id FROM migration_batches WHERE category = %s AND status = 'running'",
        (body.category,),
    )
    if cur.fetchone():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Pre kategóriu '{body.category}' už beží migrácia",
        )

    # Audit log
    _write_audit_log(
        cur,
        user_id=current_user["user_id"],
        action="migration_run_attempt",
        entity_type="MIG",
        entity_id=body.category,
        details={
            "dry_run": body.dry_run,
            "message": f"Migration run attempt for {body.category}",
        },
    )
    db.commit()

    # --- Dispatch to category-specific transformer + loader ---
    if body.category == "PAB":
        return _run_pab_migration(body, db)

    # Other categories — 501 until implemented
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail=(
            f"Transformer/Loader for {body.category} not yet implemented. "
            "Will be available in future milestones."
        ),
    )


def _run_pab_migration(body: MigrationRunRequest, db) -> MigrationRunResponse:
    """Execute PAB migration: transform JSON → INSERT into partner_catalog* tables."""
    from transform.pab_transformer import PABTransformer
    from load.pab_loader import PABLoader

    # Determine data directory (relative to nex-migration)
    data_dir = str(_migration_path / "data")

    # Check that PAB extract data exists
    pab_json = Path(data_dir) / "PAB" / "PAB.json"
    if not pab_json.exists():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="PAB extract data not found. Run extract on Windows CC first.",
        )

    start_time = time.time()

    # --- Transform ---
    transformer = PABTransformer(data_dir=data_dir)
    records, transform_stats = transformer.run()

    if not records:
        duration = time.time() - start_time
        return MigrationRunResponse(
            category="PAB",
            status="completed",
            source_count=transform_stats["total"],
            target_count=0,
            error_count=transform_stats["errors"],
            errors=transformer.errors[:50],
            warnings=transformer.warnings[:50],
            duration_seconds=round(duration, 2),
            message="No valid records to load after transform.",
        )

    if body.dry_run:
        duration = time.time() - start_time
        return MigrationRunResponse(
            category="PAB",
            status="dry_run",
            source_count=transform_stats["total"],
            target_count=transform_stats["valid"],
            error_count=transform_stats["errors"],
            errors=transformer.errors[:50],
            warnings=transformer.warnings[:50],
            duration_seconds=round(duration, 2),
            message=f"Dry run: {transform_stats['valid']} records would be loaded.",
        )

    # --- Load ---
    db_config = {
        "host": os.getenv("POSTGRES_HOST", "localhost"),
        "port": int(os.getenv("POSTGRES_PORT", "5432")),
        "database": os.getenv("POSTGRES_DB", "nex_automat"),
        "user": os.getenv("POSTGRES_USER", "nex_admin"),
        "password": os.getenv("POSTGRES_PASSWORD", ""),
    }

    loader = PABLoader(db_config=db_config)
    load_stats = loader.run(records)

    duration = time.time() - start_time

    return MigrationRunResponse(
        batch_id=loader.batch_id,
        category="PAB",
        status="completed" if load_stats["errors"] == 0 else "completed_with_errors",
        source_count=transform_stats["total"],
        target_count=load_stats["inserted"] + load_stats["updated"],
        error_count=load_stats["errors"],
        errors=transformer.errors[:50],
        warnings=transformer.warnings[:50],
        duration_seconds=round(duration, 2),
        message=(
            f"PAB migration completed: {load_stats['inserted']} inserted, "
            f"{load_stats['updated']} updated, {load_stats['errors']} errors."
        ),
    )


@router.get("/stats", response_model=MigrationStatsResponse)
def get_migration_stats(
    _current_user=Depends(require_permission("MIG", "can_view")),
    db=Depends(get_db),
):
    """Get overall migration statistics."""
    cur = db.cursor()

    # Category counts
    cur.execute(
        "SELECT status, COUNT(*) FROM migration_category_status GROUP BY status"
    )
    status_counts = dict(cur.fetchall())
    completed = status_counts.get("completed", 0)
    pending = status_counts.get("pending", 0)
    failed = status_counts.get("failed", 0)
    total_categories = completed + pending + failed

    # Total records migrated
    cur.execute("SELECT COALESCE(SUM(record_count), 0) FROM migration_category_status")
    total_records = cur.fetchone()[0]

    # Total batches
    cur.execute("SELECT COUNT(*) FROM migration_batches")
    total_batches = cur.fetchone()[0]

    # Last migration
    cur.execute("SELECT MAX(last_migrated_at) FROM migration_category_status")
    last_migration = cur.fetchone()[0]

    return MigrationStatsResponse(
        total_categories=total_categories,
        completed_categories=completed,
        pending_categories=pending,
        failed_categories=failed,
        total_records_migrated=total_records,
        total_batches=total_batches,
        last_migration_at=last_migration,
    )


@router.get("/mappings/{category}", response_model=IdMappingListResponse)
def list_id_mappings(
    category: str,
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(
        DEFAULT_PAGE_SIZE, ge=1, le=10000, description="Items per page"
    ),
    search: Optional[str] = Query(None, description="Search in source_key"),
    _current_user=Depends(require_permission("MIG", "can_view")),
    db=Depends(get_db),
):
    """List ID mappings for a specific category with pagination."""
    if category not in CATEGORIES:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Migračná kategória '{category}' neexistuje",
        )

    cur = db.cursor()

    conditions = ["category = %s"]
    params: list = [category]

    if search:
        search_val = search.strip()
        if search_val:
            conditions.append("source_key ILIKE %s")
            params.append(f"%{search_val}%")

    where_clause = "WHERE " + " AND ".join(conditions)

    # Count total
    cur.execute(f"SELECT COUNT(*) FROM migration_id_map {where_clause}", params)
    total = cur.fetchone()[0]

    total_pages = math.ceil(total / page_size) if total > 0 else 1
    offset = (page - 1) * page_size

    # Fetch page
    cur.execute(
        f"SELECT source_table, source_key, target_table, target_id, migrated_at "
        f"FROM migration_id_map {where_clause} "
        f"ORDER BY migrated_at DESC LIMIT %s OFFSET %s",
        params + [page_size, offset],
    )
    rows = cur.fetchall()

    items = [
        IdMappingResponse(
            source_table=row[0],
            source_key=row[1],
            target_table=row[2],
            target_id=str(row[3]),
            migrated_at=row[4],
        )
        for row in rows
    ]

    return IdMappingListResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@router.post("/categories/{code}/reset")
def reset_category(
    code: str,
    current_user=Depends(require_permission("MIG", "can_delete")),
    db=Depends(get_db),
):
    """Reset a migration category status back to pending."""
    if code not in CATEGORIES:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Migračná kategória '{code}' neexistuje",
        )

    cur = db.cursor()

    cur.execute(
        "UPDATE migration_category_status "
        "SET status = 'pending', record_count = 0 "
        "WHERE category = %s",
        (code,),
    )

    # Audit log
    _write_audit_log(
        cur,
        user_id=current_user["user_id"],
        action="migration_reset",
        entity_type="MIG",
        entity_id=code,
        details={"message": f"Reset category {code} to pending"},
    )

    db.commit()

    return {
        "message": f"Kategória '{code}' bola resetovaná na 'pending'",
        "category": code,
    }
