"""
NEX Manager API — FastAPI Backend
==================================

REST API backend for the NEX Manager Electron desktop application.
Provides JWT authentication, user management, and module permissions.

Endpoints:
- POST /api/auth/login          — authenticate, return JWT tokens
- POST /api/auth/refresh        — refresh access token
- GET  /api/auth/me             — current user info + permissions
- GET  /api/modules             — list all active modules
- GET  /api/modules/by-category — modules grouped by category
- GET  /api/modules/{code}      — single module detail
- PUT  /api/auth/change-password — change own password
- GET  /api/migration/categories — list migration categories (RBAC: MIG.can_view)
- GET  /api/migration/categories/{code} — category detail
- GET  /api/migration/categories/{code}/batches — category batches
- POST /api/migration/run        — run migration (RBAC: MIG.can_create)
- GET  /api/migration/stats      — migration statistics
- GET  /api/migration/mappings/{category} — ID mappings
- POST /api/migration/categories/{code}/reset — reset category (RBAC: MIG.can_delete)
- GET  /api/partners            — list partners (RBAC: PAB.can_view)
- GET  /api/partners/{id}       — partner detail
- POST /api/partners            — create partner (RBAC: PAB.can_create)
- PUT  /api/partners/{id}       — update partner (RBAC: PAB.can_edit)
- GET  /api/users               — list users (RBAC: USR.can_view)
- GET  /api/users/{id}          — user detail
- POST /api/users               — create user (RBAC: USR.can_create)
- PUT  /api/users/{id}          — update user (RBAC: USR.can_edit)
- PUT  /api/users/{id}/password — admin password change
- GET  /health                  — health check
"""

from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from auth.router import router as auth_router
from migration.router import router as migration_router
from modules.router import router as modules_router
from partners.router import router as partners_router
from users.router import router as users_router

app = FastAPI(
    title="NEX Manager API",
    description="Backend API for NEX Manager — authentication, users, permissions",
    version="0.1.0",
)

# ---------------------------------------------------------------------------
# CORS — allow all origins for Electron desktop client
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# ROUTERS
# ---------------------------------------------------------------------------
app.include_router(auth_router)
app.include_router(migration_router)
app.include_router(modules_router)
app.include_router(partners_router)
app.include_router(users_router)


# ---------------------------------------------------------------------------
# HEALTH / ROOT
# ---------------------------------------------------------------------------
@app.get("/")
def root():
    """Service information."""
    return {
        "service": "NEX Manager API",
        "version": "0.1.0",
        "status": "running",
        "endpoints": {
            "auth_login": "/api/auth/login",
            "auth_refresh": "/api/auth/refresh",
            "auth_me": "/api/auth/me",
            "auth_change_password": "/api/auth/change-password",
            "users_list": "/api/users",
            "users_detail": "/api/users/{id}",
            "users_create": "/api/users",
            "users_update": "/api/users/{id}",
            "users_password": "/api/users/{id}/password",
            "partners_list": "/api/partners",
            "partners_detail": "/api/partners/{id}",
            "partners_create": "/api/partners",
            "partners_update": "/api/partners/{id}",
            "migration_categories": "/api/migration/categories",
            "migration_run": "/api/migration/run",
            "migration_stats": "/api/migration/stats",
            "modules_list": "/api/modules",
            "modules_by_category": "/api/modules/by-category",
            "modules_detail": "/api/modules/{code}",
            "docs": "/docs",
            "health": "/health",
        },
    }


@app.get("/health")
def health():
    """Health check for monitoring systems."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
    }


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    from nex_config.services import NEX_MANAGER_API_PORT

    print("=" * 60)
    print("  NEX Manager API v0.1.0")
    print(f"  Docs: http://localhost:{NEX_MANAGER_API_PORT}/docs")
    print("=" * 60)

    uvicorn.run(app, host="0.0.0.0", port=NEX_MANAGER_API_PORT, log_level="info")
