"""
RAG Service - Local Qdrant + Ollama embeddings.
"""

import httpx
from typing import Any
from qdrant_client import QdrantClient
from qdrant_client.http import models
from config.settings import settings


class RAGService:
    """Service for RAG queries using local Qdrant."""

    def __init__(self):
        self.qdrant = QdrantClient(url=settings.QDRANT_URL)
        self.ollama_url = settings.OLLAMA_URL
        self.embedding_model = settings.EMBEDDING_MODEL
        self.embedding_dims = settings.EMBEDDING_DIMENSIONS

    async def get_embedding(self, text: str) -> list[float]:
        """Get embedding from Ollama."""
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{self.ollama_url}/api/embeddings",
                json={"model": self.embedding_model, "prompt": text}
            )
            response.raise_for_status()
            data = response.json()
            return data.get("embedding", [])

    async def search(self, query: str, limit: int = 5, tenant: str | None = None) -> list[dict[str, Any]]:
        """Search Qdrant knowledge base."""
        try:
            # Get query embedding
            query_embedding = await self.get_embedding(query)
            if not query_embedding:
                print("Failed to get query embedding")
                return []

            # Determine collection name (tenant = collection)
            collection_name = tenant or "default"

            # Check if collection exists
            collections = self.qdrant.get_collections()
            collection_names = [c.name for c in collections.collections]
            if collection_name not in collection_names:
                print(f"Collection '{collection_name}' not found")
                return []

            # Search in Qdrant using query_points
            search_response = self.qdrant.query_points(
                collection_name=collection_name,
                query=query_embedding,
                limit=limit,
                with_payload=True
            )

            # Convert to standard format
            results = []
            for point in search_response.points:
                results.append({
                    "id": str(point.id),
                    "content": point.payload.get("content", ""),
                    "filename": point.payload.get("filename", ""),
                    "score": point.score,
                    "metadata": point.payload.get("metadata", {})
                })

            # Apply boosting and deduplication
            results = self._boost_relevant(results, query)
            results = self._deduplicate_best(results)

            return results[:5]

        except Exception as e:
            print(f"RAG search error: {e}")
            return []

    async def add_document(self, content: str, filename: str, tenant: str, metadata: dict | None = None) -> bool:
        """Add document to Qdrant."""
        try:
            collection_name = tenant

            # Ensure collection exists
            await self._ensure_collection(collection_name)

            # Get embedding
            embedding = await self.get_embedding(content)
            if not embedding:
                return False

            # Generate point ID
            import hashlib
            point_id = hashlib.md5(f"{tenant}:{filename}:{content[:100]}".encode()).hexdigest()

            # Upsert to Qdrant
            self.qdrant.upsert(
                collection_name=collection_name,
                points=[
                    models.PointStruct(
                        id=point_id,
                        vector=embedding,
                        payload={
                            "content": content,
                            "filename": filename,
                            "tenant": tenant,
                            "metadata": metadata or {}
                        }
                    )
                ]
            )
            return True

        except Exception as e:
            print(f"Add document error: {e}")
            return False

    async def _ensure_collection(self, collection_name: str) -> None:
        """Ensure collection exists in Qdrant."""
        collections = self.qdrant.get_collections()
        collection_names = [c.name for c in collections.collections]

        if collection_name not in collection_names:
            self.qdrant.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                    size=self.embedding_dims,
                    distance=models.Distance.COSINE
                )
            )
            print(f"Created collection: {collection_name}")

    def _boost_relevant(self, results: list[dict[str, Any]], query: str) -> list[dict[str, Any]]:
        """Boost score for chunks that match query intent."""
        query_lower = query.lower()
        keywords = self._extract_keywords(query_lower)

        for r in results:
            content = r.get("content", "").lower()
            score = r.get("score", 0)
            boost = 0

            for kw in keywords:
                if kw in content:
                    boost += 0.1

            r["adjusted_score"] = score + boost

        results.sort(key=lambda x: x.get("adjusted_score", 0), reverse=True)
        return results

    def _extract_keywords(self, query: str) -> list[str]:
        """Extract meaningful keywords from query."""
        stopwords = {"ake", "su", "co", "je", "ako", "pre", "na", "do", "sa", "to", "a", "v", "s"}
        words = query.split()
        return [w for w in words if w not in stopwords and len(w) > 2]

    def _deduplicate_best(self, results: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Keep only best chunk per unique filename."""
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

        return sorted(best.values(), key=lambda x: x.get("adjusted_score", 0), reverse=True)

    def format_context(self, results: list[dict[str, Any]]) -> str:
        """Format RAG results as context for LLM."""
        if not results:
            return ""

        context_parts = []
        for r in results:
            content = r.get("content", "")
            if len(content) > 3000:
                content = content[:3000]
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

        return "\n".join(cleaned[:60])
