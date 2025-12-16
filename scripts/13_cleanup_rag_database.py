#!/usr/bin/env python
"""
Script 13: Cleanup RAG Database
Removes all test data and resets sequences.
"""

import asyncio
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tools.rag.config import get_config
from tools.rag.database import DatabaseManager


async def cleanup_database():
    """Clean all data from RAG tables."""
    print("=" * 50)
    print("RAG DATABASE CLEANUP")
    print("=" * 50)
    print()

    config = get_config()
    db = DatabaseManager(config.database)
    await db.connect()

    # Get counts before
    doc_count = await db.pool.fetchval("SELECT COUNT(*) FROM documents")
    chunk_count = await db.pool.fetchval("SELECT COUNT(*) FROM chunks")

    print(f"Before cleanup:")
    print(f"  Documents: {doc_count}")
    print(f"  Chunks: {chunk_count}")
    print()

    # Delete all data (chunks first due to FK)
    print("Cleaning tables...")
    await db.pool.execute("DELETE FROM chunks")
    print("  ✓ Chunks deleted")

    await db.pool.execute("DELETE FROM documents")
    print("  ✓ Documents deleted")

    # Reset sequences
    await db.pool.execute("ALTER SEQUENCE documents_id_seq RESTART WITH 1")
    await db.pool.execute("ALTER SEQUENCE chunks_id_seq RESTART WITH 1")
    print("  ✓ Sequences reset")

    # Verify
    doc_count = await db.pool.fetchval("SELECT COUNT(*) FROM documents")
    chunk_count = await db.pool.fetchval("SELECT COUNT(*) FROM chunks")

    print()
    print(f"After cleanup:")
    print(f"  Documents: {doc_count}")
    print(f"  Chunks: {chunk_count}")

    await db.close()

    print()
    print("✅ Database cleaned and ready for indexing!")
    return True


if __name__ == "__main__":
    asyncio.run(cleanup_database())