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
- GET  /health                  — health check
"""

from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from auth.router import router as auth_router
from modules.router import router as modules_router

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
app.include_router(modules_router)


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

    print("=" * 60)
    print("  NEX Manager API v0.1.0")
    print("  Docs: http://localhost:9110/docs")
    print("=" * 60)

    uvicorn.run(app, host="0.0.0.0", port=9110, log_level="info")
