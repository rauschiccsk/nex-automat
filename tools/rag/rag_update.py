#!/usr/bin/env python3
"""
RAG Update Tool - Unified workflow for documentation indexing.

Usage:
    python tools/rag/rag_update.py --new      # Incremental: new/changed .md files today
    python tools/rag/rag_update.py --all      # Full: reindex everything
    python tools/rag/rag_update.py --stats    # Show RAG statistics only

Location: tools/rag/rag_update.py
"""

import argparse
import asyncio
import sys
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from tools.rag.indexer import DocumentIndexer
from tools.rag.database import DatabaseManager


class RAGUpdateManager:
    """Unified manager for RAG update workflow."""

    def __init__(self):
        self.project_root = PROJECT_ROOT
        self.docs_path = PROJECT_ROOT / "docs"
        self.knowledge_path = PROJECT_ROOT / "docs" / "knowledge"
        self.files_to_index: list[Path] = []

    def get_today_modified_md_files(self) -> list[Path]:
        """Get .md files modified today in docs/knowledge/."""
        today = datetime.now().date()
        modified_today = []

        if not self.knowledge_path.exists():
            return []

        for md_file in self.knowledge_path.rglob("*.md"):
            mtime = datetime.fromtimestamp(md_file.stat().st_mtime).date()
            if mtime == today:
                modified_today.append(md_file)

        return modified_today

    def find_new_files(self) -> list[Path]:
        """Find .md files modified today in docs/knowledge/."""
        print("=" * 60)
        print("STEP 1: Find New/Modified Knowledge Files")
        print("=" * 60)
        print()
        print(f"Scanning: docs/knowledge/")
        print(f"Mode: Files modified today ({datetime.now().date()})")
        print()

        files = self.get_today_modified_md_files()

        if not files:
            print("No .md files modified today in docs/knowledge/")
            print()
            self.files_to_index = []
            return []

        print(f"Found {len(files)} files modified today:")
        for f in files:
            rel_path = f.relative_to(self.project_root)
            print(f"  • {rel_path}")
        print()

        self.files_to_index = files
        return files

    async def index_to_rag(self, full_reindex: bool = False):
        """Index files to RAG database."""
        print("=" * 60)
        print("STEP 2: Index to RAG Database")
        print("=" * 60)
        print()

        if full_reindex:
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

            # Index all docs (entire docs/ folder)
            async with DocumentIndexer() as indexer:
                results = await indexer.index_directory(
                    directory=self.docs_path,
                    pattern="*.md",
                    recursive=True,
                    show_progress=True
                )
            print(f"\n✓ Indexed {len(results)} documents")

        else:
            # Incremental - index only today's modified files
            if not self.files_to_index:
                print("No new files to index")
                return

            async with DocumentIndexer() as indexer:
                for i, filepath in enumerate(self.files_to_index, 1):
                    rel_path = filepath.relative_to(self.project_root)
                    print(f"[{i}/{len(self.files_to_index)}] {rel_path}")
                    try:
                        await indexer.index_file(filepath, show_progress=False)
                        print(f"  ✓ Indexed")
                    except Exception as e:
                        print(f"  ✗ Error: {e}")

            print(f"\n✓ Indexed {len(self.files_to_index)} documents")

        print()

    async def run_full_update(self):
        """Full update: reindex all docs."""
        print()
        print("╔" + "═" * 58 + "╗")
        print("║" + " RAG FULL UPDATE ".center(58) + "║")
        print("╚" + "═" * 58 + "╝")
        print()

        start_time = datetime.now()

        # Index all (full)
        await self.index_to_rag(full_reindex=True)

        elapsed = (datetime.now() - start_time).total_seconds()

        print("=" * 60)
        print(f"COMPLETE - Full update finished in {elapsed:.1f}s")
        print("=" * 60)

    async def run_incremental_update(self):
        """Incremental update: new/changed files in docs/knowledge/ only."""
        print()
        print("╔" + "═" * 58 + "╗")
        print("║" + " RAG INCREMENTAL UPDATE ".center(58) + "║")
        print("╚" + "═" * 58 + "╝")
        print()

        start_time = datetime.now()

        # Step 1: Find new files
        self.find_new_files()

        # Step 2: Index (incremental)
        await self.index_to_rag(full_reindex=False)

        elapsed = (datetime.now() - start_time).total_seconds()

        print("=" * 60)
        print(f"COMPLETE - Incremental update finished in {elapsed:.1f}s")
        print("=" * 60)

    async def show_stats(self):
        """Show RAG database statistics."""
        db = DatabaseManager()
        await db.connect()
        try:
            docs = await db.pool.fetchval("SELECT COUNT(*) FROM documents")
            chunks = await db.pool.fetchval("SELECT COUNT(*) FROM chunks")
            tokens = await db.pool.fetchval(
                "SELECT SUM((metadata->>'token_count')::int) FROM chunks"
            ) or 0

            # Get knowledge docs count
            knowledge_docs = await db.pool.fetchval(
                "SELECT COUNT(*) FROM documents WHERE filename LIKE '%knowledge%'"
            ) or 0

            print()
            print("╔" + "═" * 40 + "╗")
            print("║" + " RAG Database Statistics ".center(40) + "║")
            print("╠" + "═" * 40 + "╣")
            print(f"║  Documents:      {docs:<21} ║")
            print(f"║  Knowledge docs: {knowledge_docs:<21} ║")
            print(f"║  Chunks:         {chunks:<21} ║")
            print(f"║  Tokens:         {tokens:,<21} ║")
            print("╚" + "═" * 40 + "╝")
            print()
        finally:
            await db.close()


def main():
    parser = argparse.ArgumentParser(
        description="RAG Update Tool - Unified workflow",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tools/rag/rag_update.py --new      # Index today's docs/knowledge/ files
  python tools/rag/rag_update.py --all      # Full reindex all docs/
  python tools/rag/rag_update.py --stats    # Show statistics
        """
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--new', action='store_true',
                       help='Incremental: index new/modified docs/knowledge/ files')
    group.add_argument('--all', action='store_true',
                       help='Full: clear and reindex all docs/')
    group.add_argument('--stats', action='store_true',
                       help='Show RAG statistics only')

    args = parser.parse_args()

    manager = RAGUpdateManager()

    if args.all:
        asyncio.run(manager.run_full_update())
    elif args.new:
        asyncio.run(manager.run_incremental_update())
    elif args.stats:
        asyncio.run(manager.show_stats())


if __name__ == "__main__":
    main()