"""
RAG Indexer Module
Document indexing pipeline for RAG system
"""

from typing import List, Optional, Dict, Any
from pathlib import Path
import asyncio

from .config import get_config
from .database import DatabaseManager
from .embeddings import EmbeddingModel
from .chunker import DocumentChunker


def detect_tenant(filepath: Path) -> str | None:
    """
    Detect tenant from file path.
    
    Rules:
    - docs/knowledge/tenants/icc/... → 'icc'
    - docs/knowledge/tenants/andros/... → 'andros'  
    - Other paths → None (shared/all tenants)
    """
    path_str = str(filepath).replace("\\", "/").lower()
    
    if "/tenants/" in path_str:
        parts = path_str.split("/tenants/")
        if len(parts) > 1:
            tenant = parts[1].split("/")[0]
            if tenant in ["icc", "andros"]:
                return tenant
    
    return None


class DocumentIndexer:
    """
    Handles document indexing pipeline

    Coordinates chunking, embedding, and storage of documents.
    """

    def __init__(
            self,
            db: Optional[DatabaseManager] = None,
            embedding_model: Optional[EmbeddingModel] = None,
            chunker: Optional[DocumentChunker] = None
    ):
        """
        Initialize document indexer

        Args:
            db: Database manager, creates new if None
            embedding_model: Embedding model, creates new if None
            chunker: Document chunker, creates new if None
        """
        self.db = db or DatabaseManager()
        self.embedding_model = embedding_model or EmbeddingModel()
        self.chunker = chunker or DocumentChunker()

        # Load embedding model
        if self.embedding_model.model is None:
            self.embedding_model.load()

    async def index_document(
            self,
            filename: str,
            content: str,
            metadata: Optional[Dict[str, Any]] = None,
            show_progress: bool = True
    ) -> Dict[str, Any]:
        """
        Index a document

        Workflow:
        1. Insert document into database
        2. Chunk document
        3. Generate embeddings for chunks
        4. Store chunks with embeddings

        Args:
            filename: Document filename
            content: Document content
            metadata: Optional document metadata
            show_progress: Show progress output

        Returns:
            Dict with indexing results
        """
        if show_progress:
            print(f"Indexing document: {filename}")

        # Step 1: Insert document
        doc_id = await self.db.insert_document(filename, content, metadata)

        if show_progress:
            print(f"  ✓ Document inserted (ID: {doc_id})")

        # Step 2: Chunk document
        chunks = self.chunker.chunk_text(content)

        if show_progress:
            print(f"  ✓ Document chunked ({len(chunks)} chunks)")

        # Step 3: Generate embeddings
        if show_progress:
            print(f"  → Generating embeddings...")

        embeddings = self.embedding_model.encode_batch(
            chunks,
            show_progress=show_progress
        )

        if show_progress:
            print(f"  ✓ Embeddings generated")

        # Step 4: Store chunks with embeddings
        if show_progress:
            print(f"  → Storing chunks...")

        chunk_ids = []
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            chunk_metadata = {
                'chunk_size': len(chunk),
                'token_count': self.chunker.count_tokens(chunk)
            }

            chunk_id = await self.db.insert_chunk(
                document_id=doc_id,
                chunk_index=i,
                content=chunk,
                embedding=embedding,
                metadata=chunk_metadata
            )

            chunk_ids.append(chunk_id)

        if show_progress:
            print(f"  ✓ Chunks stored ({len(chunk_ids)} chunks)")

        # Return results
        result = {
            'document_id': doc_id,
            'filename': filename,
            'chunk_count': len(chunks),
            'chunk_ids': chunk_ids,
            'total_tokens': sum(self.chunker.count_tokens(c) for c in chunks)
        }

        if show_progress:
            print(f"✓ Document indexed successfully")
            print(f"  Document ID: {doc_id}")
            print(f"  Chunks: {len(chunks)}")
            print(f"  Total tokens: {result['total_tokens']}")

        return result

    async def index_file(
            self,
            filepath: Path,
            metadata: Optional[Dict[str, Any]] = None,
            show_progress: bool = True
    ) -> Dict[str, Any]:
        """
        Index a file from disk

        Args:
            filepath: Path to file
            metadata: Optional document metadata
            show_progress: Show progress output

        Returns:
            Dict with indexing results
        """
        filepath = Path(filepath)

        if not filepath.exists():
            raise FileNotFoundError(f"File not found: {filepath}")

        # Read file content
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Add filepath and tenant to metadata
        if metadata is None:
            metadata = {}
        metadata['filepath'] = str(filepath.absolute())
        metadata['file_size'] = filepath.stat().st_size
        
        # Detect tenant from path
        tenant = detect_tenant(filepath)
        if tenant:
            metadata['tenant'] = tenant

        # Index document
        return await self.index_document(
            filename=filepath.name,
            content=content,
            metadata=metadata,
            show_progress=show_progress
        )

    async def index_directory(
            self,
            directory: Path,
            pattern: str = "*.md",
            recursive: bool = True,
            show_progress: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Index all files in a directory

        Args:
            directory: Directory path
            pattern: File pattern (glob)
            recursive: Search recursively
            show_progress: Show progress output

        Returns:
            List of indexing results
        """
        directory = Path(directory)

        if not directory.exists():
            raise FileNotFoundError(f"Directory not found: {directory}")

        # Find files
        if recursive:
            files = list(directory.rglob(pattern))
        else:
            files = list(directory.glob(pattern))

        if show_progress:
            print(f"Found {len(files)} files in {directory}")
            print()

        # Index files
        results = []
        for i, filepath in enumerate(files, 1):
            if show_progress:
                print(f"[{i}/{len(files)}] {filepath.name}")

            try:
                result = await self.index_file(filepath, show_progress=show_progress)
                results.append(result)
            except Exception as e:
                print(f"  ✗ Error indexing {filepath.name}: {e}")

            if show_progress:
                print()

        if show_progress:
            total_chunks = sum(r['chunk_count'] for r in results)
            total_tokens = sum(r['total_tokens'] for r in results)
            print(f"✓ Indexed {len(results)} documents")
            print(f"  Total chunks: {total_chunks}")
            print(f"  Total tokens: {total_tokens}")

        return results

    async def reindex_document(
            self,
            document_id: int,
            show_progress: bool = True
    ) -> Dict[str, Any]:
        """
        Reindex an existing document

        Deletes old chunks and creates new ones.

        Args:
            document_id: Document ID
            show_progress: Show progress output

        Returns:
            Dict with indexing results
        """
        # Get document
        doc = await self.db.get_document(document_id)
        if doc is None:
            raise ValueError(f"Document not found: {document_id}")

        if show_progress:
            print(f"Reindexing document: {doc['filename']} (ID: {document_id})")

        # Delete old chunks
        await self.db.pool.execute(
            "DELETE FROM chunks WHERE document_id = $1",
            document_id
        )

        if show_progress:
            print("  ✓ Old chunks deleted")

        # Chunk document
        chunks = self.chunker.chunk_text(doc['content'])

        if show_progress:
            print(f"  ✓ Document chunked ({len(chunks)} chunks)")

        # Generate embeddings
        if show_progress:
            print(f"  → Generating embeddings...")

        embeddings = self.embedding_model.encode_batch(
            chunks,
            show_progress=show_progress
        )

        if show_progress:
            print(f"  ✓ Embeddings generated")

        # Store new chunks
        if show_progress:
            print(f"  → Storing chunks...")

        chunk_ids = []
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            chunk_metadata = {
                'chunk_size': len(chunk),
                'token_count': self.chunker.count_tokens(chunk)
            }

            chunk_id = await self.db.insert_chunk(
                document_id=document_id,
                chunk_index=i,
                content=chunk,
                embedding=embedding,
                metadata=chunk_metadata
            )

            chunk_ids.append(chunk_id)

        if show_progress:
            print(f"  ✓ Chunks stored ({len(chunk_ids)} chunks)")
            print(f"✓ Document reindexed successfully")

        return {
            'document_id': document_id,
            'filename': doc['filename'],
            'chunk_count': len(chunks),
            'chunk_ids': chunk_ids,
            'total_tokens': sum(self.chunker.count_tokens(c) for c in chunks)
        }

    async def __aenter__(self):
        """Async context manager entry"""
        await self.db.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.db.close()


if __name__ == "__main__":
    async def test():
        """Test document indexer"""
        print("Testing document indexer...")

        # Test document
        test_content = """
        This is a test document for the RAG indexing system.
        It contains multiple paragraphs to test chunking.

        The second paragraph demonstrates how the system handles
        longer text that needs to be split into manageable chunks.

        Finally, the third paragraph completes our test document.
        The indexer should process all of this correctly.
        """

        async with DocumentIndexer() as indexer:
            result = await indexer.index_document(
                filename="test_document.txt",
                content=test_content,
                metadata={'type': 'test'},
                show_progress=True
            )

            print("\nIndexing result:")
            print(f"  Document ID: {result['document_id']}")
            print(f"  Chunks: {result['chunk_count']}")
            print(f"  Tokens: {result['total_tokens']}")


    asyncio.run(test())