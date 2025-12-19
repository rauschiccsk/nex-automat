"""
Add tenant filtering to RAG system.

Changes:
1. hybrid_search.py - add tenant filter to SQL query
2. server_app.py - add ?tenant= parameter to /search endpoint
3. api.py - pass tenant through search chain
"""
from pathlib import Path

RAG_DIR = Path(r"C:\Development\nex-automat\tools\rag")

# =============================================================================
# 1. UPDATE hybrid_search.py - Add tenant parameter to search
# =============================================================================

HYBRID_SEARCH_UPDATES = {
    # Update search method signature
    "old": '''    async def search(
            self,
            query: str,
            limit: int = 10,
            min_similarity: float = 0.0,
            rerank: bool = True
    ) -> List[SearchResult]:''',
    "new": '''    async def search(
            self,
            query: str,
            limit: int = 10,
            min_similarity: float = 0.0,
            rerank: bool = True,
            tenant: Optional[str] = None
    ) -> List[SearchResult]:'''
}

HYBRID_SEARCH_SQL_UPDATE = {
    # Update SQL query to filter by tenant
    "old": '''        # Vector search
        results = await self.db.pool.fetch("""
            SELECT 
                c.id as chunk_id,
                c.document_id,
                d.filename,
                c.chunk_index,
                c.content,
                1 - (c.embedding <=> $1::vector) as similarity
            FROM chunks c
            JOIN documents d ON c.document_id = d.id
            WHERE 1 - (c.embedding <=> $1::vector) >= $2
            ORDER BY c.embedding <=> $1::vector
            LIMIT $3
        """, query_str, min_similarity, fetch_limit)''',
    "new": '''        # Vector search with optional tenant filter
        if tenant:
            results = await self.db.pool.fetch("""
                SELECT 
                    c.id as chunk_id,
                    c.document_id,
                    d.filename,
                    c.chunk_index,
                    c.content,
                    1 - (c.embedding <=> $1::vector) as similarity
                FROM chunks c
                JOIN documents d ON c.document_id = d.id
                WHERE 1 - (c.embedding <=> $1::vector) >= $2
                  AND (d.metadata->>'tenant' = $4 OR d.metadata->>'tenant' IS NULL)
                ORDER BY c.embedding <=> $1::vector
                LIMIT $3
            """, query_str, min_similarity, fetch_limit, tenant)
        else:
            results = await self.db.pool.fetch("""
                SELECT 
                    c.id as chunk_id,
                    c.document_id,
                    d.filename,
                    c.chunk_index,
                    c.content,
                    1 - (c.embedding <=> $1::vector) as similarity
                FROM chunks c
                JOIN documents d ON c.document_id = d.id
                WHERE 1 - (c.embedding <=> $1::vector) >= $2
                ORDER BY c.embedding <=> $1::vector
                LIMIT $3
            """, query_str, min_similarity, fetch_limit)'''
}

HYBRID_SEARCH_CONVENIENCE_UPDATE = {
    # Update convenience function
    "old": '''# Convenience function
async def search(query: str, limit: int = 10, **kwargs) -> List[SearchResult]:
    """Quick search function."""
    async with HybridSearch() as searcher:
        return await searcher.search(query, limit=limit, **kwargs)''',
    "new": '''# Convenience function
async def search(query: str, limit: int = 10, tenant: Optional[str] = None, **kwargs) -> List[SearchResult]:
    """Quick search function."""
    async with HybridSearch() as searcher:
        return await searcher.search(query, limit=limit, tenant=tenant, **kwargs)'''
}

# =============================================================================
# 2. UPDATE api.py - Pass tenant through
# =============================================================================

API_SEARCH_UPDATE = {
    "old": '''    async def search(
        self,
        query: str,
        limit: int = 5,
        mode: str = 'hybrid'
    ) -> RAGResponse:''',
    "new": '''    async def search(
        self,
        query: str,
        limit: int = 5,
        mode: str = 'hybrid',
        tenant: Optional[str] = None
    ) -> RAGResponse:'''
}

API_SEARCH_CALL_UPDATE = {
    "old": '''        # hybrid_search returns list of its own SearchResult objects
        results = await hybrid_search_func(query, limit=limit)''',
    "new": '''        # hybrid_search returns list of its own SearchResult objects
        results = await hybrid_search_func(query, limit=limit, tenant=tenant)'''
}

API_CONTEXT_UPDATE = {
    "old": '''    async def get_context_for_llm(
        self,
        query: str,
        max_chunks: int = 3,
        max_tokens: int = 4000
    ) -> str:''',
    "new": '''    async def get_context_for_llm(
        self,
        query: str,
        max_chunks: int = 3,
        max_tokens: int = 4000,
        tenant: Optional[str] = None
    ) -> str:'''
}

API_CONTEXT_CALL_UPDATE = {
    "old": '''        response = await self.search(query, limit=max_chunks, mode='hybrid')''',
    "new": '''        response = await self.search(query, limit=max_chunks, mode='hybrid', tenant=tenant)'''
}

API_CONVENIENCE_UPDATE = {
    "old": '''# Convenience functions for quick usage
async def search(query: str, limit: int = 5, mode: str = 'hybrid') -> RAGResponse:
    """Quick search function."""
    async with RAGSearchAPI() as api:
        return await api.search(query, limit=limit, mode=mode)


async def get_context(query: str, max_chunks: int = 3) -> str:
    """Quick context retrieval for LLM."""
    async with RAGSearchAPI() as api:
        return await api.get_context_for_llm(query, max_chunks=max_chunks)''',
    "new": '''# Convenience functions for quick usage
async def search(query: str, limit: int = 5, mode: str = 'hybrid', tenant: Optional[str] = None) -> RAGResponse:
    """Quick search function."""
    async with RAGSearchAPI() as api:
        return await api.search(query, limit=limit, mode=mode, tenant=tenant)


async def get_context(query: str, max_chunks: int = 3, tenant: Optional[str] = None) -> str:
    """Quick context retrieval for LLM."""
    async with RAGSearchAPI() as api:
        return await api.get_context_for_llm(query, max_chunks=max_chunks, tenant=tenant)'''
}

# =============================================================================
# 3. UPDATE server_app.py - Add tenant parameter to endpoint
# =============================================================================

SERVER_SEARCH_UPDATE = {
    "old": '''@app.get("/search")
async def search_endpoint(
    query: str = Query(..., description="Search query"),
    max_results: int = Query(5, ge=1, le=20, description="Maximum number of results (1-20)"),
    format: str = Query("json", pattern="^(json|context)$", description="Response format: json or context")
):''',
    "new": '''@app.get("/search")
async def search_endpoint(
    query: str = Query(..., description="Search query"),
    max_results: int = Query(5, ge=1, le=20, description="Maximum number of results (1-20)"),
    format: str = Query("json", pattern="^(json|context)$", description="Response format: json or context"),
    tenant: Optional[str] = Query(None, description="Tenant filter (e.g., 'icc', 'andros')")
):'''
}

SERVER_SEARCH_CALL_UPDATE = {
    "old": '''        # Use existing API search function
        response = await search(query, limit=max_results)''',
    "new": '''        # Use existing API search function
        response = await search(query, limit=max_results, tenant=tenant)'''
}

SERVER_CONTEXT_CALL_UPDATE = {
    "old": '''            # Use existing get_context function
            context = await get_context(query, max_chunks=max_results)''',
    "new": '''            # Use existing get_context function
            context = await get_context(query, max_chunks=max_results, tenant=tenant)'''
}

SERVER_IMPORT_UPDATE = {
    "old": '''from typing import List, Dict, Any, Optional''',
    "new": '''from typing import List, Dict, Any, Optional'''  # No change needed, Optional already imported
}


def apply_update(filepath: Path, old: str, new: str, description: str) -> bool:
    """Apply a single update to a file."""
    content = filepath.read_text(encoding="utf-8")

    if old not in content:
        print(f"  ⚠️  Pattern not found: {description}")
        return False

    if new in content:
        print(f"  ✓ Already applied: {description}")
        return True

    content = content.replace(old, new)
    filepath.write_text(content, encoding="utf-8")
    print(f"  ✅ Applied: {description}")
    return True


def main():
    print("=" * 60)
    print("Add Tenant Filtering to RAG System")
    print("=" * 60)

    # 1. Update hybrid_search.py
    print("\n1. Updating hybrid_search.py...")
    hs_file = RAG_DIR / "hybrid_search.py"

    apply_update(hs_file, HYBRID_SEARCH_UPDATES["old"], HYBRID_SEARCH_UPDATES["new"],
                 "search() signature")
    apply_update(hs_file, HYBRID_SEARCH_SQL_UPDATE["old"], HYBRID_SEARCH_SQL_UPDATE["new"],
                 "SQL query with tenant filter")
    apply_update(hs_file, HYBRID_SEARCH_CONVENIENCE_UPDATE["old"], HYBRID_SEARCH_CONVENIENCE_UPDATE["new"],
                 "convenience function")

    # 2. Update api.py
    print("\n2. Updating api.py...")
    api_file = RAG_DIR / "api.py"

    apply_update(api_file, API_SEARCH_UPDATE["old"], API_SEARCH_UPDATE["new"],
                 "search() signature")
    apply_update(api_file, API_SEARCH_CALL_UPDATE["old"], API_SEARCH_CALL_UPDATE["new"],
                 "search() call")
    apply_update(api_file, API_CONTEXT_UPDATE["old"], API_CONTEXT_UPDATE["new"],
                 "get_context_for_llm() signature")
    apply_update(api_file, API_CONTEXT_CALL_UPDATE["old"], API_CONTEXT_CALL_UPDATE["new"],
                 "get_context_for_llm() call")
    apply_update(api_file, API_CONVENIENCE_UPDATE["old"], API_CONVENIENCE_UPDATE["new"],
                 "convenience functions")

    # 3. Update server_app.py
    print("\n3. Updating server_app.py...")
    server_file = RAG_DIR / "server_app.py"

    apply_update(server_file, SERVER_SEARCH_UPDATE["old"], SERVER_SEARCH_UPDATE["new"],
                 "/search endpoint signature")
    apply_update(server_file, SERVER_SEARCH_CALL_UPDATE["old"], SERVER_SEARCH_CALL_UPDATE["new"],
                 "search() call")
    apply_update(server_file, SERVER_CONTEXT_CALL_UPDATE["old"], SERVER_CONTEXT_CALL_UPDATE["new"],
                 "get_context() call")

    print("\n" + "=" * 60)
    print("✅ DONE - Tenant filtering added to RAG system")
    print("=" * 60)
    print("\nUsage:")
    print("  /search?query=test&tenant=icc")
    print("  /search?query=test&tenant=andros")
    print("  /search?query=test  (no filter - all documents)")
    print("\nNote: Documents without tenant in metadata are included in all searches.")


if __name__ == "__main__":
    main()