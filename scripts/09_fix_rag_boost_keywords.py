#!/usr/bin/env python
"""
Fix rag_service.py - Better keyword boosting for implementation phases.
"""

from pathlib import Path

FILE_PATH = Path("C:/Development/nex-automat/apps/nex-brain/api/services/rag_service.py")

CONTENT = '''"""
RAG Service - Integration with existing RAG API.
"""

import httpx
import re
from typing import List, Dict, Any, Optional
from config.settings import settings


class RAGService:
    """Service for RAG queries."""

    def __init__(self):
        self.base_url = settings.RAG_API_URL

    async def search(
        self, 
        query: str, 
        limit: int = 10,
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

                # Boost by query relevance
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
        """Boost score for chunks that match query intent."""
        query_lower = query.lower()

        # Extract important keywords from query
        keywords = self._extract_keywords(query_lower)

        for r in results:
            content = r.get("content", "").lower()
            score = r.get("score", 0)
            boost = 0

            # Boost for each keyword match in content
            for kw in keywords:
                if kw in content:
                    boost += 0.15

            # Extra boost for structural matches
            if "faz" in query_lower or "implementa" in query_lower:
                # Looking for phases - boost chunks with numbered phases
                if re.search(r"faz[ae]\s*[123456]", content) or "## 5. IMPLEMENT" in r.get("content", ""):
                    boost += 0.3

            if "co je" in query_lower or "co to je" in query_lower:
                # Definition question - boost SUMMARY
                if "summary" in content or "je " in content[:100]:
                    boost += 0.2

            r["adjusted_score"] = score + boost

        # Sort by adjusted score
        results.sort(key=lambda x: x.get("adjusted_score", 0), reverse=True)
        return results

    def _extract_keywords(self, query: str) -> List[str]:
        """Extract meaningful keywords from query."""
        # Remove common words
        stopwords = {"ake", "su", "co", "je", "ako", "pre", "na", "do", "sa", "to", "a", "v", "s"}
        words = query.split()
        keywords = [w for w in words if w not in stopwords and len(w) > 2]
        return keywords

    def _deduplicate_best(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Keep only BEST chunk per unique filename."""
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
        """Format RAG results as context for LLM."""
        if not results:
            return ""

        context_parts = []
        for r in results:
            content = r.get("content", "")
            # Allow longer content for better context
            if len(content) > 1200:
                content = content[:1200]
            content = self._clean_content(content)
            if content.strip():
                context_parts.append(content)

        return "\\n\\n".join(context_parts)

    def _clean_content(self, content: str) -> str:
        """Clean content for LLM."""
        lines = content.split("\\n")
        cleaned = []
        in_code_block = False

        for line in lines:
            if line.strip().startswith("```"):
                in_code_block = not in_code_block
                continue
            if in_code_block:
                continue
            if line.strip() and line.strip() != "---":
                cleaned.append(line)

        return "\\n".join(cleaned[:30])  # More lines allowed
'''


def main():
    FILE_PATH.write_text(CONTENT, encoding="utf-8")
    print("✅ Fixed: rag_service.py")
    print("   - Better keyword extraction")
    print("   - Boost for 'faz' + numbered phases")
    print("   - Boost for definition questions")
    print("   - Longer content allowed (1200 chars)")


if __name__ == "__main__":
    main()