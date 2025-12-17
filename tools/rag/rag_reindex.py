#!/usr/bin/env python3
"""
RAG Reindex Tool
Reindex documents in the RAG database.

Usage:
    python tools/rag/rag_reindex.py --all              # Reindex all docs
    python tools/rag/rag_reindex.py --file <path>      # Index single file
    python tools/rag/rag_reindex.py --dir <path>       # Index directory
    python tools/rag/rag_reindex.py --new              # Index only new files
    python tools/rag/rag_reindex.py --stats            # Show stats only

Location: tools/rag/rag_reindex.py
"""

import argparse
import asyncio
from pathlib import Path
import sys

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from tools.rag.indexer import DocumentIndexer
from tools.rag.database import DatabaseManager


async def get_indexed_files(db: DatabaseManager) -> set:
    """Get set of already indexed filenames."""
    await db.connect()
    try:
        rows = await db.pool.fetch("SELECT filename FROM documents")
        return {row['filename'] for row in rows}
    finally:
        await db.close()


async def reindex_all(docs_path: Path):
    """Reindex all documents (drop and recreate)."""
    print("=" * 60)
    print("FULL REINDEX - All Documents")
    print("=" * 60)
    print()

    # Clear database first
    db = DatabaseManager()
    await db.connect()
    try:
        await db.pool.execute("DELETE FROM chunks")
        await db.pool.execute("DELETE FROM documents")
        print("✓ Database cleared")
        print()
    finally:
        await db.close()

    # Reindex all
    async with DocumentIndexer() as indexer:
        results = await indexer.index_directory(
            directory=docs_path,
            pattern="*.md",
            recursive=True,
            show_progress=True
        )

    print()
    print("=" * 60)
    print(f"DONE: {len(results)} documents indexed")
    print("=" * 60)


async def index_new_files(docs_path: Path):
    """Index only new files (incremental)."""
    print("=" * 60)
    print("INCREMENTAL INDEX - New Files Only")
    print("=" * 60)
    print()

    # Get already indexed files
    db = DatabaseManager()
    indexed = await get_indexed_files(db)
    print(f"Already indexed: {len(indexed)} files")

    # Find all markdown files
    all_files = list(docs_path.rglob("*.md"))
    print(f"Total files on disk: {len(all_files)}")

    # Filter new files
    new_files = []
    for f in all_files:
        # Use relative path as filename for comparison
        rel_path = str(f.relative_to(PROJECT_ROOT))
        if rel_path not in indexed and f.name not in indexed:
            new_files.append(f)

    if not new_files:
        print()
        print("✓ No new files to index")
        return

    print(f"New files to index: {len(new_files)}")
    print()

    # Index new files
    async with DocumentIndexer() as indexer:
        for i, filepath in enumerate(new_files, 1):
            print(f"[{i}/{len(new_files)}] {filepath.name}")
            try:
                await indexer.index_file(filepath, show_progress=True)
            except Exception as e:
                print(f"  ✗ Error: {e}")
            print()

    print("=" * 60)
    print(f"DONE: {len(new_files)} new documents indexed")
    print("=" * 60)


async def index_single_file(filepath: Path):
    """Index a single file."""
    print(f"Indexing: {filepath}")
    print()

    async with DocumentIndexer() as indexer:
        result = await indexer.index_file(filepath, show_progress=True)

    print()
    print(f"✓ Document indexed: {result['chunk_count']} chunks, {result['total_tokens']} tokens")


async def index_directory(dir_path: Path):
    """Index all files in a directory."""
    print(f"Indexing directory: {dir_path}")
    print()

    async with DocumentIndexer() as indexer:
        results = await indexer.index_directory(
            directory=dir_path,
            pattern="*.md",
            recursive=True,
            show_progress=True
        )

    print()
    print(f"✓ Indexed {len(results)} documents")


async def show_stats():
    """Show database statistics."""
    db = DatabaseManager()
    await db.connect()
    try:
        docs = await db.pool.fetchval("SELECT COUNT(*) FROM documents")
        chunks = await db.pool.fetchval("SELECT COUNT(*) FROM chunks")
        tokens = await db.pool.fetchval(
            "SELECT SUM((metadata->>'token_count')::int) FROM chunks"
        ) or 0

        print("=" * 40)
        print("RAG Database Statistics")
        print("=" * 40)
        print(f"Documents: {docs}")
        print(f"Chunks:    {chunks}")
        print(f"Tokens:    {tokens:,}")
        print("=" * 40)
    finally:
        await db.close()


def main():
    parser = argparse.ArgumentParser(
        description="RAG Reindex Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tools/rag/rag_reindex.py --all         # Full reindex
  python tools/rag/rag_reindex.py --new         # Index new files only
  python tools/rag/rag_reindex.py --file docs/infrastructure/RAG_EXTERNAL_ACCESS.md
  python tools/rag/rag_reindex.py --dir docs/infrastructure/
  python tools/rag/rag_reindex.py --stats       # Show statistics
        """
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--all', action='store_true', help='Full reindex (drop and recreate)')
    group.add_argument('--new', action='store_true', help='Index only new files (incremental)')
    group.add_argument('--file', type=Path, help='Index single file')
    group.add_argument('--dir', type=Path, help='Index directory')
    group.add_argument('--stats', action='store_true', help='Show statistics only')

    args = parser.parse_args()

    docs_path = PROJECT_ROOT / "docs"

    if args.all:
        asyncio.run(reindex_all(docs_path))
    elif args.new:
        asyncio.run(index_new_files(docs_path))
    elif args.file:
        if not args.file.exists():
            print(f"Error: File not found: {args.file}")
            sys.exit(1)
        asyncio.run(index_single_file(args.file))
    elif args.dir:
        if not args.dir.exists():
            print(f"Error: Directory not found: {args.dir}")
            sys.exit(1)
        asyncio.run(index_directory(args.dir))
    elif args.stats:
        asyncio.run(show_stats())


if __name__ == "__main__":
    main()