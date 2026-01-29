"""
RAG Search Module
Semantic and hybrid search capabilities
"""

import asyncio
from typing import Any

from .config import SearchConfig, get_config
from .database import DatabaseManager
from .embeddings import EmbeddingModel


class SearchEngine:
    """
    Handles semantic and hybrid search operations

    Provides vector similarity search and keyword-based search.
    """

    def __init__(
        self,
        db: DatabaseManager | None = None,
        embedding_model: EmbeddingModel | None = None,
        config: SearchConfig | None = None,
    ):
        """
        Initialize search engine

        Args:
            db: Database manager, creates new if None
            embedding_model: Embedding model, creates new if None
            config: Search configuration, uses global config if None
        """
        self.db = db or DatabaseManager()
        self.embedding_model = embedding_model or EmbeddingModel()

        if config is None:
            config = get_config().search
        self.config = config

        # Load embedding model
        if self.embedding_model.model is None:
            self.embedding_model.load()

    async def search(
        self,
        query: str,
        limit: int | None = None,
        similarity_threshold: float | None = None,
        document_ids: list[int] | None = None,
    ) -> list[dict[str, Any]]:
        """
        Perform semantic vector search

        Args:
            query: Search query
            limit: Maximum number of results, uses config default if None
            similarity_threshold: Minimum similarity score, uses config default if None
            document_ids: Optional list of document IDs to filter

        Returns:
            List of search results with relevance scores
        """
        if limit is None:
            limit = self.config.default_limit

        if similarity_threshold is None:
            similarity_threshold = self.config.similarity_threshold

        # Generate query embedding
        query_embedding = self.embedding_model.encode(query)

        # Search similar chunks
        results = await self.db.search_similar(
            query_embedding=query_embedding,
            limit=limit,
            similarity_threshold=similarity_threshold,
            document_ids=document_ids,
        )

        return results

    async def search_with_context(
        self, query: str, limit: int | None = None, context_size: int = 1, **kwargs
    ) -> list[dict[str, Any]]:
        """
        Search with surrounding context chunks

        Retrieves matching chunks plus N chunks before and after for context.

        Args:
            query: Search query
            limit: Maximum number of results
            context_size: Number of chunks before/after to include (0-3)
            **kwargs: Additional arguments passed to search()

        Returns:
            List of results with context chunks
        """
        # Get initial results
        results = await self.search(query, limit=limit, **kwargs)

        # For each result, get surrounding chunks
        enriched_results = []
        for result in results:
            doc_id = result["document_id"]
            chunk_idx = result["chunk_index"]

            # Get all chunks for this document
            all_chunks = await self.db.get_chunks(doc_id)

            # Find context chunks
            context_before = []
            context_after = []

            for i in range(1, context_size + 1):
                # Before
                before_idx = chunk_idx - i
                if before_idx >= 0 and before_idx < len(all_chunks):
                    context_before.insert(0, all_chunks[before_idx])

                # After
                after_idx = chunk_idx + i
                if after_idx < len(all_chunks):
                    context_after.append(all_chunks[after_idx])

            # Add context to result
            result["context_before"] = context_before
            result["context_after"] = context_after

            enriched_results.append(result)

        return enriched_results

    async def search_documents(self, query: str, limit: int | None = None, **kwargs) -> list[dict[str, Any]]:
        """
        Search and group results by document

        Args:
            query: Search query
            limit: Maximum number of documents
            **kwargs: Additional arguments passed to search()

        Returns:
            List of documents with their matching chunks
        """
        # Search chunks
        chunk_results = await self.search(query, limit=limit * 3 if limit else None, **kwargs)

        # Group by document
        docs_dict = {}
        for result in chunk_results:
            doc_id = result["document_id"]

            if doc_id not in docs_dict:
                docs_dict[doc_id] = {
                    "document_id": doc_id,
                    "filename": result["filename"],
                    "chunks": [],
                    "max_similarity": result["similarity"],
                }

            docs_dict[doc_id]["chunks"].append(result)
            docs_dict[doc_id]["max_similarity"] = max(docs_dict[doc_id]["max_similarity"], result["similarity"])

        # Convert to list and sort by max similarity
        documents = list(docs_dict.values())
        documents.sort(key=lambda x: x["max_similarity"], reverse=True)

        # Limit to requested number of documents
        if limit:
            documents = documents[:limit]

        return documents

    async def explain_search(self, query: str, limit: int = 3) -> dict[str, Any]:
        """
        Search with explanation of results

        Provides detailed information about why results were returned.

        Args:
            query: Search query
            limit: Number of results to explain

        Returns:
            Dict with query info and explained results
        """
        # Generate query embedding
        query_embedding = self.embedding_model.encode(query)

        # Search
        results = await self.search(query, limit=limit)

        # Prepare explanation
        explanation = {
            "query": query,
            "query_tokens": len(query.split()),
            "embedding_dimension": len(query_embedding),
            "num_results": len(results),
            "results": [],
        }

        for result in results:
            explained_result = {
                "rank": len(explanation["results"]) + 1,
                "document": result["filename"],
                "chunk_index": result["chunk_index"],
                "similarity": result["similarity"],
                "similarity_explanation": self._explain_similarity(result["similarity"]),
                "content_preview": result["content"][:200] + "..."
                if len(result["content"]) > 200
                else result["content"],
                "full_content": result["content"],
            }

            explanation["results"].append(explained_result)

        return explanation

    def _explain_similarity(self, similarity: float) -> str:
        """Generate human-readable similarity explanation"""
        if similarity >= 0.9:
            return "Very high similarity - nearly identical meaning"
        elif similarity >= 0.8:
            return "High similarity - very similar content"
        elif similarity >= 0.7:
            return "Good similarity - related content"
        elif similarity >= 0.6:
            return "Moderate similarity - somewhat related"
        elif similarity >= 0.5:
            return "Low similarity - loosely related"
        else:
            return "Very low similarity - barely related"

    async def __aenter__(self):
        """Async context manager entry"""
        await self.db.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.db.close()


async def search(query: str, limit: int = 10) -> list[dict[str, Any]]:
    """
    Quick helper for semantic search

    Args:
        query: Search query
        limit: Maximum results

    Returns:
        List of search results
    """
    async with SearchEngine() as engine:
        return await engine.search(query, limit=limit)


if __name__ == "__main__":

    async def test():
        """Test search engine"""
        print("Testing search engine...")

        # Test search
        query = "document indexing"

        async with SearchEngine() as engine:
            print(f"\nSearching for: '{query}'")
            results = await engine.search(query, limit=5)

            print(f"\n✓ Found {len(results)} results")
            for i, result in enumerate(results, 1):
                print(f"\n{i}. {result['filename']} (chunk {result['chunk_index']})")
                print(f"   Similarity: {result['similarity']:.4f}")
                print(f"   Preview: {result['content'][:100]}...")

            # Test explanation
            print("\n" + "=" * 60)
            print("Search Explanation")
            print("=" * 60)

            explanation = await engine.explain_search(query, limit=2)
            print(f"\nQuery: {explanation['query']}")
            print(f"Results: {explanation['num_results']}")

            for result in explanation["results"]:
                print(f"\n{result['rank']}. {result['document']}")
                print(f"   Similarity: {result['similarity']:.4f}")
                print(f"   {result['similarity_explanation']}")

    asyncio.run(test())
