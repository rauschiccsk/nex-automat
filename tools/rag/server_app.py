"""
FastAPI server application for RAG system.
Provides HTTP endpoints for document search and stats.
"""

from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
from typing import List, Dict, Any, Optional
from contextlib import asynccontextmanager
from datetime import datetime

from .api import search, get_context  # Use existing API functions
from .database import DatabaseManager
from .config import get_config


# Global database manager
db_manager: Optional[DatabaseManager] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    global db_manager

    # Startup
    config = get_config()
    db_manager = DatabaseManager(config.database)
    await db_manager.connect()
    print(f"[OK] RAG API server started")
    print(f"[OK] Database: {config.database.host}:{config.database.port}/{config.database.database}")

    yield

    # Shutdown
    if db_manager:
        await db_manager.close()
        print("[OK] Database connection closed")


app = FastAPI(
    title="NEX Automat RAG API",
    description="Retrieval-Augmented Generation system for NEX Automat project documentation",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "service": "NEX Automat RAG API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "search": "/search?query=<query>&max_results=<n>&format=<json|context>",
            "stats": "/stats",
            "health": "/health"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    global db_manager

    if not db_manager:
        raise HTTPException(status_code=503, detail="Database not initialized")

    try:
        # Simple query to check database connectivity
        query = "SELECT COUNT(*) FROM documents"
        result = await db_manager.pool.fetchval(query)

        return {
            "status": "healthy",
            "database": "connected",
            "documents": result,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Database health check failed: {str(e)}"
        )


@app.get("/search")
async def search_endpoint(
    query: str = Query(..., description="Search query"),
    max_results: int = Query(5, ge=1, le=20, description="Maximum number of results (1-20)"),
    format: str = Query("json", pattern="^(json|context)$", description="Response format: json or context")
):
    """
    Search RAG database for relevant documents.

    Args:
        query: Search query string
        max_results: Number of results to return (1-20)
        format: Response format - 'json' for raw data, 'context' for LLM-formatted text

    Returns:
        JSON response with search results or formatted context
    """
    try:
        # Use existing API search function
        response = await search(query, limit=max_results)

        if format == "context":
            # Use existing get_context function
            context = await get_context(query, max_chunks=max_results)
            return JSONResponse(content={"context": context})
        else:
            # Return raw JSON - convert SearchResult objects to dicts
            results_dict = [
                {
                    "filename": r.filename,
                    "content": r.content,
                    "score": r.score,
                    "chunk_id": r.chunk_id,
                    "section": r.section,
                    "metadata": r.metadata
                }
                for r in response.results
            ]

            return JSONResponse(content={
                "query": query,
                "results": results_dict,
                "count": len(results_dict),
                "timestamp": datetime.utcnow().isoformat()
            })

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Search failed: {str(e)}"
        )


@app.get("/stats")
async def stats_endpoint():
    """
    Get RAG database statistics.

    Returns:
        Statistics about indexed documents and chunks
    """
    global db_manager

    if not db_manager:
        raise HTTPException(status_code=503, detail="Database not initialized")

    try:
        # Get document count
        doc_count = await db_manager.pool.fetchval(
            "SELECT COUNT(*) FROM documents"
        )

        # Get chunk count
        chunk_count = await db_manager.pool.fetchval(
            "SELECT COUNT(*) FROM chunks"
        )

        # Get last indexed document
        last_indexed = await db_manager.pool.fetchrow(
            "SELECT filename, updated_at FROM documents ORDER BY updated_at DESC LIMIT 1"
        )

        return {
            "documents": doc_count,
            "chunks": chunk_count,
            "last_indexed": {
                "filename": last_indexed["filename"] if last_indexed else None,
                "timestamp": last_indexed["updated_at"].isoformat() if last_indexed else None
            },
            "timestamp": datetime.utcnow().isoformat()
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Stats retrieval failed: {str(e)}"
        )