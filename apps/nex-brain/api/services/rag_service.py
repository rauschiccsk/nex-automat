"""
RAG Service - Integration with existing RAG API.
"""

from typing import Any

import httpx
from config.settings import settings


class RAGService:
    """Service for RAG queries."""

    def __init__(self):
        self.base_url = settings.RAG_API_URL

    async def search(self, query: str, limit: int = 10, tenant: str | None = None) -> list[dict[str, Any]]:
        """Search RAG knowledge base."""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                params = {"query": query, "limit": limit}
                if tenant:
                    params["tenant"] = tenant
                response = await client.get(f"{self.base_url}/search", params=params)
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

    def _boost_relevant(self, results: list[dict[str, Any]], query: str) -> list[dict[str, Any]]:
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
                raw_content = r.get("content", "")
                # Check if section header is at START (first 200 chars) - this is the RIGHT chunk
                start_content = raw_content[:200]
                if "IMPLEMENTAČNÉ FÁZY" in start_content or "## 5." in start_content:
                    boost += 0.8  # Strong boost - this is THE chunk about phases
                elif "Fáza 1:" in start_content or "Foundation" in start_content[:300]:
                    boost += 0.6  # Also good - starts with phase details
                # No boost if IMPLEMENTAČNÉ is buried deep in chunk

            if "co je" in query_lower or "co to je" in query_lower:
                # Definition question - boost SUMMARY
                if "summary" in content or "je " in content[:100]:
                    boost += 0.2

            r["adjusted_score"] = score + boost

        # Sort by adjusted score
        results.sort(key=lambda x: x.get("adjusted_score", 0), reverse=True)
        return results

    def _extract_keywords(self, query: str) -> list[str]:
        """Extract meaningful keywords from query."""
        # Remove common words
        stopwords = {"ake", "su", "co", "je", "ako", "pre", "na", "do", "sa", "to", "a", "v", "s"}
        words = query.split()
        keywords = [w for w in words if w not in stopwords and len(w) > 2]
        return keywords

    def _deduplicate_best(self, results: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Keep only BEST chunk per unique filename (by adjusted_score)."""
        best = {}
        for r in results:
            filename = r.get("filename", "")
            current_score = r.get("adjusted_score", r.get("score", 0))
            existing = best.get(filename)
            if existing is None:
                best[filename] = r
            else:
                existing_score = existing.get("adjusted_score", existing.get("score", 0))
                if current_score > existing_score:
                    best[filename] = r
        # Sort by adjusted_score descending
        sorted_results = sorted(best.values(), key=lambda x: x.get("adjusted_score", 0), reverse=True)
        return sorted_results

    def _filter_by_tenant(self, results: list[dict[str, Any]], tenant: str) -> list[dict[str, Any]]:
        """Filter results by tenant."""
        filtered = []
        for r in results:
            filename = r.get("filename", "").lower()
            if f"{tenant}/" in filename or "shared/" in filename or "/" not in filename:
                filtered.append(r)
        return filtered

    def format_context(self, results: list[dict[str, Any]]) -> str:
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

        return "\n\n".join(context_parts)

    def _clean_content(self, content: str) -> str:
        """Clean content for LLM."""
        lines = content.split("\n")
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

        return "\n".join(cleaned[:30])  # More lines allowed
