#!/usr/bin/env python
"""
Fix rag_service.py - Better relevance filtering.
"""

from pathlib import Path

FILE_PATH = Path("C:/Development/nex-automat/apps/nex-brain/api/services/rag_service.py")

CONTENT = '''"""
RAG Service - Integration with existing RAG API.
"""

import httpx
from typing import List, Dict, Any, Optional
from config.settings import settings


class RAGService:
    """Service for RAG queries."""

    def __init__(self):
        self.base_url = settings.RAG_API_URL

    async def search(
        self, 
        query: str, 
        limit: int = 5,
        tenant: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Search RAG knowledge base."""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                params = {"query": query, "limit": limit}
                response = await client.get(
                    f"{self.base_url}/search",
                    params=params
                )
                response.raise_for_status()
                data = response.json()
                results = data.get("results", [])

                # Filter by relevance
                results = self._filter_relevant(results, query)

                if tenant:
                    results = self._filter_by_tenant(results, tenant)

                # Deduplicate by filename
                results = self._deduplicate(results)

                return results[:2]

        except httpx.RequestError as e:
            print(f"RAG API error: {e}")
            return []

    def _filter_relevant(
        self, 
        results: List[Dict[str, Any]], 
        query: str
    ) -> List[Dict[str, Any]]:
        """Filter results by relevance to query."""
        query_lower = query.lower()
        filtered = []

        # Extract key terms from query
        key_terms = []
        if "nex brain" in query_lower:
            key_terms.append("nex_brain")
        if "automat" in query_lower:
            key_terms.append("automat")
        if "genesis" in query_lower:
            key_terms.append("genesis")
        if "faktur" in query_lower:
            key_terms.append("invoice")
            key_terms.append("faktur")

        for r in results:
            filename = r.get("filename", "").lower()
            score = r.get("score", 0)

            # If we have key terms, prioritize matching filenames
            if key_terms:
                matches_term = any(term in filename for term in key_terms)
                if matches_term:
                    filtered.append(r)
                elif score > 0.5:  # High score = include anyway
                    filtered.append(r)
            else:
                # No specific terms - use score threshold
                if score > 0.35:
                    filtered.append(r)

        # If nothing passed filter, return top result
        if not filtered and results:
            filtered = [results[0]]

        return filtered

    def _deduplicate(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Keep only best chunk per unique filename."""
        seen = {}
        for r in results:
            filename = r.get("filename", "")
            if filename not in seen:
                seen[filename] = r
        return list(seen.values())

    def _filter_by_tenant(
        self, 
        results: List[Dict[str, Any]], 
        tenant: str
    ) -> List[Dict[str, Any]]:
        """Filter results by tenant."""
        filtered = []
        for r in results:
            filename = r.get("filename", "").lower()
            if (
                f"{tenant}/" in filename or
                "shared/" in filename or
                "/" not in filename
            ):
                filtered.append(r)
        return filtered

    def format_context(self, results: List[Dict[str, Any]]) -> str:
        """Format RAG results as concise context for LLM."""
        if not results:
            return ""

        context_parts = []
        for r in results:
            content = r.get("content", "")
            if len(content) > 600:
                content = content[:600] + "..."
            content = self._clean_content(content)
            if content.strip():
                context_parts.append(content)

        return "\\n\\n".join(context_parts)

    def _clean_content(self, content: str) -> str:
        """Clean content for better LLM understanding."""
        lines = content.split("\\n")
        cleaned = []
        in_code_block = False

        for line in lines:
            if line.strip().startswith("```"):
                in_code_block = not in_code_block
                continue
            if in_code_block:
                continue
            if line.strip() and not line.strip().startswith("---"):
                cleaned.append(line)

        return "\\n".join(cleaned[:15])
'''


def main():
    FILE_PATH.write_text(CONTENT, encoding="utf-8")
    print("✅ Fixed: rag_service.py")
    print("   - Added relevance filtering by query terms")
    print("   - 'NEX Brain' query -> prioritize NEX_BRAIN files")


if __name__ == "__main__":
    main()