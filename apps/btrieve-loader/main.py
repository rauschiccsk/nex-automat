"""
Btrieve-Loader - Entry Point
============================

Re-exports the FastAPI application from src.main for backward compatibility.
"""

from src.main import app

# Re-export for uvicorn and other tools
__all__ = ["app"]

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True, log_level="info")
