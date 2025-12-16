#!/usr/bin/env python
"""
Script 18: Index All Project Documents
Indexes all markdown documents from docs/ directory.
"""

import asyncio
import sys
import json
from pathlib import Path
from datetime import datetime
import numpy as np

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tools.rag.config import get_config
from tools.rag.database import DatabaseManager
from tools.rag.embeddings import EmbeddingModel
from tools.rag.chunker import DocumentChunker


def find_markdown_files(base_path: Path) -> list:
    """Find all markdown files in docs/ directory."""
    docs_path = base_path / "docs"

    if not docs_path.exists():
        print(f"⚠ docs/ directory not found")
        return []

    md_files = []
    for md_file in docs_path.rglob("*.md"):
        # Get relative path from project root
        rel_path = md_file.relative_to(base_path)
        md_files.append(rel_path)

    return sorted(md_files)


async def index_all_documents():
    """Index all markdown documents."""
    print("=" * 60)
    print("RAG FULL INDEXER - Phase 5.1")
    print("=" * 60)
    print()

    # Find all markdown files
    md_files = find_markdown_files(project_root)
    print(f"Found {len(md_files)} markdown files\n")

    if not md_files:
        print("No files to index!")
        return False

    # Initialize
    config = get_config()
    db = DatabaseManager(config.database)
    embedder = EmbeddingModel(config.embedding)
    chunker = DocumentChunker(config.chunking)

    await db.connect()
    embedder.load()

    # Check existing documents
    existing = await db.pool.fetch("SELECT filename FROM documents")
    existing_files = {r['filename'] for r in existing}
    print(f"Already indexed: {len(existing_files)} documents\n")

    # Stats
    new_docs = 0
    skipped_docs = 0
    total_chunks = 0
    total_tokens = 0
    errors = []
    start_time = datetime.now()

    for doc_path in md_files:
        filepath = project_root / doc_path
        str_path = str(doc_path)

        # Skip if already indexed
        if str_path in existing_files:
            skipped_docs += 1
            continue

        try:
            # Read document
            content = filepath.read_text(encoding='utf-8')

            # Skip very small files
            if len(content) < 100:
                print(f"⏭ Skipping (too small): {doc_path}")
                skipped_docs += 1
                continue

            print(f"📄 {doc_path}")

            # Chunk document
            chunks = chunker.chunk_text(content)

            if not chunks:
                print(f"   ⚠ No chunks created, skipping")
                skipped_docs += 1
                continue

            # Generate embeddings
            embeddings = embedder.encode(chunks)
            if isinstance(embeddings, np.ndarray) and embeddings.ndim == 1:
                embeddings = np.array([embeddings])

            # Store document
            doc_id = await db.insert_document(
                filename=str_path,
                content=content,
                metadata=json.dumps({
                    "indexed_at": datetime.now().isoformat(),
                    "chunks": len(chunks),
                    "size": len(content)
                })
            )

            # Store chunks
            for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                token_count = chunker.count_tokens(chunk)
                await db.insert_chunk(
                    document_id=doc_id,
                    chunk_index=i,
                    content=chunk,
                    embedding=embedding,
                    metadata=json.dumps({"token_count": token_count})
                )
                total_tokens += token_count

            new_docs += 1
            total_chunks += len(chunks)
            print(f"   ✓ {len(chunks)} chunks ({len(content)} chars)")

        except Exception as e:
            errors.append((str_path, str(e)))
            print(f"   ❌ Error: {e}")

    # Summary
    elapsed = (datetime.now() - start_time).total_seconds()

    print()
    print("=" * 60)
    print("INDEXING COMPLETE")
    print("=" * 60)
    print(f"  New documents: {new_docs}")
    print(f"  Skipped: {skipped_docs}")
    print(f"  Total chunks: {total_chunks}")
    print(f"  Total tokens: {total_tokens:,}")
    print(f"  Time: {elapsed:.2f}s")
    if total_chunks > 0:
        print(f"  Speed: {total_chunks / elapsed:.1f} chunks/sec")

    if errors:
        print(f"\n  Errors: {len(errors)}")
        for path, err in errors[:5]:
            print(f"    - {path}: {err}")

    # Database status
    doc_count = await db.pool.fetchval("SELECT COUNT(*) FROM documents")
    chunk_count = await db.pool.fetchval("SELECT COUNT(*) FROM chunks")
    print()
    print(f"Database total:")
    print(f"  Documents: {doc_count}")
    print(f"  Chunks: {chunk_count}")

    await db.close()
    return True


if __name__ == "__main__":
    try:
        asyncio.run(index_all_documents())
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)