"""
Btrieve-Loader - Main Application Entry Point
==============================================

Universal REST API for Btrieve data access + Legacy invoice processing.

Routes:
- /api/v1/* - New Btrieve REST API (products, partners, barcodes, stores, documents)
- /api/legacy/* - Legacy invoice processing endpoints
- /staging/* - Staging web UI endpoints
- /app/* - Frontend SPA
"""

import time
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from src.api.routes import api_router
from src.api.routes.legacy import invoice_router
from src.api.staging_routes import router as staging_router
from src.core.btrieve import get_btrieve_manager
from src.core.config import settings
from src.utils import config, monitoring

# Start time for uptime calculation
START_TIME = time.time()


# ============================================================================
# LIFESPAN (Startup/Shutdown)
# ============================================================================


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan - startup and shutdown events."""
    # Startup
    print("=" * 60)
    print("[ROCKET] Btrieve-Loader v2.0 Starting...")
    print("=" * 60)
    print(f"Customer: {config.CUSTOMER_NAME}")
    print(f"Btrieve Path: {settings.btrieve_path}")
    print(f"API Key: {'configured' if settings.api_key else 'not set'}")
    print(
        f"PostgreSQL Staging: {'Enabled' if config.POSTGRES_STAGING_ENABLED else 'Disabled'}"
    )
    if config.POSTGRES_STAGING_ENABLED:
        print(
            f"PostgreSQL: {config.POSTGRES_HOST}:{config.POSTGRES_PORT}/{config.POSTGRES_DATABASE}"
        )
    print("=" * 60)

    # Initialize BtrieveClientManager
    try:
        get_btrieve_manager()  # Initialize singleton
        print("[OK] BtrieveClientManager initialized")
    except Exception as e:
        print(f"[WARNING] BtrieveClientManager not available: {e}")

    # Initialize legacy ProductMatcher
    from src.api.routes.legacy.invoice import init_product_matcher

    init_product_matcher()

    yield  # Application is running

    # Shutdown
    print("=" * 60)
    print("[STOP] Btrieve-Loader Shutting Down...")
    print("=" * 60)


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

app = FastAPI(
    title=settings.api_title,
    description="Universal REST API for Btrieve data access + Invoice processing",
    version=settings.api_version,
    lifespan=lifespan,
)


# ============================================================================
# CORS MIDDLEWARE
# ============================================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",  # React dev server
        "http://localhost:8001",  # Self
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# REQUEST TRACKING MIDDLEWARE
# ============================================================================


@app.middleware("http")
async def track_requests(request: Request, call_next):
    """Middleware to track API requests in metrics."""
    monitoring.get_metrics().increment_request()
    response = await call_next(request)
    return response


# ============================================================================
# EXCEPTION HANDLERS
# ============================================================================


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled errors."""
    print(f"[ERROR] Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "path": str(request.url.path),
            "timestamp": datetime.now().isoformat(),
        },
    )


# ============================================================================
# ROUTERS
# ============================================================================

# New Btrieve REST API routes under /api/v1
app.include_router(api_router, prefix="/api/v1")

# Legacy invoice processing routes under /api/legacy
app.include_router(invoice_router, prefix="/api/legacy", tags=["Legacy Invoice"])

# Staging web UI routes (already has /staging prefix)
app.include_router(staging_router)


# ============================================================================
# ROOT ENDPOINTS (backward compatibility)
# ============================================================================


@app.get("/")
async def root():
    """Root endpoint - service information."""
    return {
        "service": settings.api_title,
        "version": settings.api_version,
        "status": "running",
        "endpoints": {
            "api_v1": "/api/v1",
            "legacy": "/api/legacy",
            "staging": "/staging",
            "docs": "/docs",
        },
    }


@app.get("/health")
async def health():
    """Health check endpoint - for monitoring systems."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "uptime_seconds": int(time.time() - START_TIME),
    }


@app.get("/metrics")
async def metrics():
    """Metrics endpoint - basic metrics in JSON format."""
    uptime = int(time.time() - START_TIME)

    try:
        from src.database import database

        stats = database.get_stats()
        total_processed = stats.get("total", 0)
    except Exception:
        total_processed = 0

    return {
        "uptime_seconds": uptime,
        "app_invoices_processed_total": total_processed,
        "app_info": {
            "version": settings.api_version,
            "customer": config.CUSTOMER_NAME,
        },
    }


# ============================================================================
# FRONTEND STATIC FILES
# ============================================================================

FRONTEND_DIR = (
    Path(__file__).parent.parent.parent / "supplier-invoice-staging-web" / "dist"
)

if FRONTEND_DIR.exists():
    app.mount(
        "/app/assets",
        StaticFiles(directory=FRONTEND_DIR / "assets"),
        name="static_assets",
    )

    @app.get("/app")
    async def serve_frontend_root():
        """Serve frontend index.html at /app."""
        return FileResponse(FRONTEND_DIR / "index.html")

    @app.get("/app/{path:path}")
    async def serve_frontend_spa(path: str):
        """Serve frontend SPA for all /app/* routes."""
        if "." in path:
            file_path = FRONTEND_DIR / path
            if file_path.exists():
                return FileResponse(file_path)
        return FileResponse(FRONTEND_DIR / "index.html")


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    print("=" * 60)
    print("[ROCKET] Starting Btrieve-Loader v2.0")
    print("=" * 60)
    print(" API Documentation: http://localhost:8001/docs")
    print(" API v1: http://localhost:8001/api/v1")
    print(" Legacy API: http://localhost:8001/api/legacy")
    print(" Health Check: http://localhost:8001/health")
    print("=" * 60)

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")
