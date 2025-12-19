#!/usr/bin/env python
"""
Fix rag_service.py - Select best chunk per file, not first.
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
        limit: int = 10,  # Get more, then filter
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

                # Score chunks that contain query terms higher
                results = self._boost_relevant(results, query)

                if tenant:
                    results = self._filter_by_tenant(results, tenant)

                # Deduplicate - keep BEST chunk per file
                results = self._deduplicate_best(results)

                return results[:2]

        except httpx.RequestError as e:
            print(f"RAG API error: {e}")
            return []

    def _boost_relevant(
        self, 
        results: List[Dict[str, Any]], 
        query: str
    ) -> List[Dict[str, Any]]:
        """Boost score for chunks containing query keywords."""
        query_words = set(query.lower().split())

        for r in results:
            content = r.get("content", "").lower()
            score = r.get("score", 0)

            # Boost if content contains key query words
            matches = sum(1 for w in query_words if w in content and len(w) > 3)
            if matches > 0:
                r["adjusted_score"] = score + (matches * 0.1)
            else:
                r["adjusted_score"] = score

            # Extra boost for "SUMMARY" or definition-like content
            if "summary" in content or "je " in content[:200]:
                r["adjusted_score"] += 0.15

        # Sort by adjusted score
        results.sort(key=lambda x: x.get("adjusted_score", 0), reverse=True)
        return results

    def _deduplicate_best(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Keep only BEST chunk per unique filename (by adjusted_score)."""
        best = {}
        for r in results:
            filename = r.get("filename", "")
            score = r.get("adjusted_score", r.get("score", 0))
            if filename not in best or score > best[filename].get("adjusted_score", 0):
                best[filename] = r
        return list(best.values())

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
            if len(content) > 800:
                content = content[:800]
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
            if line.strip() and not line.strip() == "---":
                cleaned.append(line)

        return "\\n".join(cleaned[:20])
'''


def main():
    FILE_PATH.write_text(CONTENT, encoding="utf-8")
    print("✅ Fixed: rag_service.py")
    print("   - Boost chunks containing query words")
    print("   - Boost 'SUMMARY' sections")
    print("   - Keep BEST chunk per file (not first)")


if __name__ == "__main__":
    main()