"""
RAG Service - Integration with existing RAG API.
Multi-tenant support with tenant-based filtering.
"""

import httpx
from typing import List, Dict, Any, Optional
from config.settings import settings


class RAGService:
    """Service for RAG (Retrieval-Augmented Generation) queries."""

    def __init__(self):
        self.base_url = settings.RAG_API_URL

    async def search(
        self, 
        query: str, 
        limit: int = 5,
        tenant: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search RAG knowledge base.

        Args:
            query: Search query
            limit: Max results to return
            tenant: Tenant identifier for filtering

        Returns:
            List of relevant documents with scores
        """
        try:
            # Build query with tenant prefix if provided
            # RAG can filter by path: tenant/docs/...
            search_query = query

            async with httpx.AsyncClient(timeout=30.0) as client:
                params = {"query": search_query, "limit": limit}

                response = await client.get(
                    f"{self.base_url}/search",
                    params=params
                )
                response.raise_for_status()
                data = response.json()
                results = data.get("results", [])

                # Filter by tenant if needed (client-side filtering)
                # TODO: Add server-side tenant filtering to RAG API
                if tenant:
                    results = self._filter_by_tenant(results, tenant)

                return results

        except httpx.RequestError as e:
            print(f"RAG API error: {e}")
            return []

    def _filter_by_tenant(
        self, 
        results: List[Dict[str, Any]], 
        tenant: str
    ) -> List[Dict[str, Any]]:
        """
        Filter results by tenant.

        Convention: Files in tenant folder or shared folder.
        - tenant/... = tenant-specific
        - shared/... = available to all tenants
        """
        filtered = []
        for r in results:
            filename = r.get("filename", "").lower()
            # Include if: tenant-specific OR shared OR no tenant prefix
            if (
                f"{tenant}/" in filename or
                "shared/" in filename or
                "/" not in filename  # Root level = shared
            ):
                filtered.append(r)
        return filtered

    def format_context(self, results: List[Dict[str, Any]]) -> str:
        """Format RAG results as context for LLM."""
        if not results:
            return ""

        context_parts = []
        for i, r in enumerate(results, 1):
            context_parts.append(
                f"[Zdroj {i}: {r.get('filename', 'unknown')}]\n"
                f"{r.get('content', '')}"
            )

        return "\n\n---\n\n".join(context_parts)
