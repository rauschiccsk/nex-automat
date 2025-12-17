#!/usr/bin/env python3
"""
RAG Update Tool - Unified workflow for code documentation and indexing.

Combines:
  1. Generate Markdown docs from Python source code
  2. Index to RAG database
  3. Cleanup generated .md files

Usage:
    python tools/rag/rag_update.py --new      # Incremental: new/changed files only
    python tools/rag/rag_update.py --all      # Full: regenerate and reindex everything
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

from tools.rag.generate_code_docs import CodeDocGenerator
from tools.rag.indexer import DocumentIndexer
from tools.rag.database import DatabaseManager


class RAGUpdateManager:
    """Unified manager for RAG update workflow."""

    def __init__(self):
        self.project_root = PROJECT_ROOT
        self.docs_path = PROJECT_ROOT / "docs"
        self.code_docs_path = PROJECT_ROOT / "docs" / "code"
        self.generated_files: list[Path] = []

    async def get_indexed_files(self) -> set:
        """Get set of already indexed filenames."""
        db = DatabaseManager()
        await db.connect()
        try:
            rows = await db.pool.fetch("SELECT filename FROM documents")
            return {row['filename'] for row in rows}
        finally:
            await db.close()

    def get_today_modified_files(self, directory: Path) -> list[Path]:
        """Get .py files modified today."""
        today = datetime.now().date()
        modified_today = []

        exclude_dirs = {'venv', '__pycache__', '.git', 'node_modules', '.pytest_cache'}

        for py_file in directory.rglob("*.py"):
            if any(d in py_file.parts for d in exclude_dirs):
                continue

            mtime = datetime.fromtimestamp(py_file.stat().st_mtime).date()
            if mtime == today:
                modified_today.append(py_file)

        return modified_today

    def generate_code_docs(self, incremental: bool = True) -> list[Path]:
        """Generate Markdown documentation from Python source code."""
        print("=" * 60)
        print("STEP 1: Generate Code Documentation")
        print("=" * 60)
        print()

        generator = CodeDocGenerator(self.project_root)
        self.code_docs_path.mkdir(parents=True, exist_ok=True)

        dirs_to_process = [
            self.project_root / "tools",
            self.project_root / "apps",
            self.project_root / "packages",
        ]

        generated = []

        if incremental:
            # Only files modified today
            print(f"Mode: INCREMENTAL (files modified today)")
            print()

            all_today_files = []
            for directory in dirs_to_process:
                if directory.exists():
                    all_today_files.extend(self.get_today_modified_files(directory))

            if not all_today_files:
                print("No Python files modified today")
                print()
                self.generated_files = []
                return []

            print(f"Found {len(all_today_files)} files modified today:")
            for f in all_today_files:
                print(f"  • {f.relative_to(self.project_root)}")
            print()

            for filepath in all_today_files:
                if filepath.name == '__init__.py':
                    content = filepath.read_text(encoding='utf-8')
                    if len(content.strip()) < 100:
                        continue

                doc = generator.extract_from_file(filepath)

                if not doc.get('classes') and not doc.get('functions') and not doc.get('module_docstring'):
                    continue

                if 'error' in doc:
                    print(f"  ⚠ Skipping {filepath.name}: {doc['error']}")
                    continue

                markdown = generator.generate_markdown(doc)

                rel_path = filepath.relative_to(self.project_root)
                output_name = str(rel_path).replace('/', '_').replace('\\', '_').replace('.py', '.md')
                output_path = self.code_docs_path / output_name

                output_path.write_text(markdown, encoding='utf-8')
                generated.append(output_path)
                print(f"  ✓ {output_name}")
        else:
            # Full - all files
            print(f"Mode: FULL (all Python files)")
            print()

            for directory in dirs_to_process:
                if directory.exists():
                    print(f"Processing: {directory.name}/")
                    files = generator.process_directory(directory)
                    generated.extend(files)
                    print()

        self.generated_files = generated
        print(f"Generated {len(generated)} documentation files")
        print()

        return generated

    async def index_to_rag(self, full_reindex: bool = False):
        """Index generated docs to RAG database."""
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

            # Index all docs
            async with DocumentIndexer() as indexer:
                results = await indexer.index_directory(
                    directory=self.docs_path,
                    pattern="*.md",
                    recursive=True,
                    show_progress=True
                )
            print(f"\n✓ Indexed {len(results)} documents")

        else:
            # Incremental - index only generated files
            if not self.generated_files:
                print("No new files to index")
                return

            async with DocumentIndexer() as indexer:
                for i, filepath in enumerate(self.generated_files, 1):
                    print(f"[{i}/{len(self.generated_files)}] {filepath.name}")
                    try:
                        await indexer.index_file(filepath, show_progress=True)
                    except Exception as e:
                        print(f"  ✗ Error: {e}")

            print(f"\n✓ Indexed {len(self.generated_files)} documents")

        print()

    def cleanup_generated_docs(self):
        """Remove generated .md files from docs/code/."""
        print("=" * 60)
        print("STEP 3: Cleanup Generated Files")
        print("=" * 60)
        print()

        if not self.code_docs_path.exists():
            print("No docs/code/ directory found")
            return

        # Remove all .md files in docs/code/
        removed = 0
        for md_file in self.code_docs_path.glob("*.md"):
            md_file.unlink()
            removed += 1

        # Remove directory if empty
        if self.code_docs_path.exists() and not any(self.code_docs_path.iterdir()):
            self.code_docs_path.rmdir()
            print(f"✓ Removed empty directory: docs/code/")

        print(f"✓ Removed {removed} generated .md files")
        print()

    async def run_full_update(self):
        """Full update: regenerate all and reindex."""
        print()
        print("╔" + "═" * 58 + "╗")
        print("║" + " RAG FULL UPDATE ".center(58) + "║")
        print("╚" + "═" * 58 + "╝")
        print()

        start_time = datetime.now()

        # Step 1: Generate
        self.generate_code_docs(incremental=False)

        # Step 2: Index (full)
        await self.index_to_rag(full_reindex=True)

        # Step 3: Cleanup
        self.cleanup_generated_docs()

        elapsed = (datetime.now() - start_time).total_seconds()

        print("=" * 60)
        print(f"COMPLETE - Full update finished in {elapsed:.1f}s")
        print("=" * 60)

    async def run_incremental_update(self):
        """Incremental update: new/changed files only."""
        print()
        print("╔" + "═" * 58 + "╗")
        print("║" + " RAG INCREMENTAL UPDATE ".center(58) + "║")
        print("╚" + "═" * 58 + "╝")
        print()

        start_time = datetime.now()

        # Step 1: Generate
        self.generate_code_docs(incremental=True)

        # Step 2: Index (incremental)
        await self.index_to_rag(full_reindex=False)

        # Step 3: Cleanup
        self.cleanup_generated_docs()

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

            print()
            print("╔" + "═" * 40 + "╗")
            print("║" + " RAG Database Statistics ".center(40) + "║")
            print("╠" + "═" * 40 + "╣")
            print(f"║  Documents: {docs:<26} ║")
            print(f"║  Chunks:    {chunks:<26} ║")
            print(f"║  Tokens:    {tokens:,<26} ║")
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
  python tools/rag/rag_update.py --new      # Incremental update
  python tools/rag/rag_update.py --all      # Full regenerate and reindex
  python tools/rag/rag_update.py --stats    # Show statistics
        """
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--new', action='store_true',
                       help='Incremental: generate, index, cleanup new files')
    group.add_argument('--all', action='store_true',
                       help='Full: regenerate all docs and reindex')
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