#!/usr/bin/env python3
"""
RAG Delete Tool - Delete documents from RAG database.

Usage:
    python tools/rag/rag_delete.py --id 1381                    # Delete by document ID
    python tools/rag/rag_delete.py --filename "config_v1.md"    # Delete by filename (partial match)
    python tools/rag/rag_delete.py --path "deployment/andros"   # Delete by path (partial match)
    python tools/rag/rag_delete.py --list                       # List all documents
    python tools/rag/rag_delete.py --duplicates                 # Find and remove duplicates

Location: tools/rag/rag_delete.py
"""

import argparse
import asyncio
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from tools.rag.database import DatabaseManager


class RAGDeleteManager:
    """Manager for RAG document deletion."""

    def __init__(self):
        self.db = DatabaseManager()

    async def connect(self):
        await self.db.connect()

    async def close(self):
        await self.db.close()

    async def list_documents(self, limit: int = 50):
        """List all documents in RAG database."""
        rows = await self.db.pool.fetch(
            """
            SELECT 
                d.id,
                d.filename,
                d.created_at,
                d.metadata,
                COUNT(c.id) as chunk_count
            FROM documents d
            LEFT JOIN chunks c ON c.document_id = d.id
            GROUP BY d.id
            ORDER BY d.created_at DESC
            LIMIT $1
        """,
            limit,
        )

        print()
        print("=" * 80)
        print(f"{'ID':<6} {'Filename':<50} {'Chunks':<8} {'Created'}")
        print("=" * 80)

        for row in rows:
            created = (
                row["created_at"].strftime("%Y-%m-%d %H:%M")
                if row["created_at"]
                else "N/A"
            )
            print(
                f"{row['id']:<6} {row['filename'][:49]:<50} {row['chunk_count']:<8} {created}"
            )

        print("=" * 80)
        print(f"Total: {len(rows)} documents (showing max {limit})")
        print()

    async def find_duplicates(self) -> list[dict]:
        """Find duplicate documents (same filename, different IDs)."""
        rows = await self.db.pool.fetch("""
            SELECT 
                filename,
                COUNT(*) as count,
                ARRAY_AGG(id ORDER BY created_at DESC) as ids,
                ARRAY_AGG(created_at ORDER BY created_at DESC) as dates
            FROM documents
            GROUP BY filename
            HAVING COUNT(*) > 1
            ORDER BY filename
        """)

        duplicates = []
        for row in rows:
            duplicates.append(
                {
                    "filename": row["filename"],
                    "count": row["count"],
                    "ids": row["ids"],
                    "dates": row["dates"],
                }
            )

        return duplicates

    async def show_duplicates(self):
        """Show duplicate documents."""
        duplicates = await self.find_duplicates()

        if not duplicates:
            print("\n✓ No duplicate documents found.\n")
            return

        print()
        print("=" * 80)
        print("DUPLICATE DOCUMENTS")
        print("=" * 80)

        for dup in duplicates:
            print(f"\n📄 {dup['filename']} ({dup['count']} copies)")
            print("-" * 60)
            for i, (doc_id, date) in enumerate(zip(dup["ids"], dup["dates"])):
                marker = "✓ KEEP (newest)" if i == 0 else "✗ DELETE"
                date_str = date.strftime("%Y-%m-%d %H:%M") if date else "N/A"
                print(f"  ID {doc_id}: {date_str} - {marker}")

        print()
        print("=" * 80)
        print(f"Found {len(duplicates)} files with duplicates")
        print()

    async def remove_duplicates(self, dry_run: bool = True) -> int:
        """Remove duplicate documents, keeping the newest."""
        duplicates = await self.find_duplicates()

        if not duplicates:
            print("\n✓ No duplicate documents to remove.\n")
            return 0

        ids_to_delete = []
        for dup in duplicates:
            # Keep first (newest), delete rest
            ids_to_delete.extend(dup["ids"][1:])

        if dry_run:
            print(f"\n[DRY RUN] Would delete {len(ids_to_delete)} duplicate documents:")
            for doc_id in ids_to_delete:
                print(f"  • Document ID: {doc_id}")
            print("\nRun with --duplicates --confirm to actually delete.\n")
            return 0

        # Actually delete
        deleted = 0
        for doc_id in ids_to_delete:
            count = await self.delete_by_id(doc_id, confirm=True)
            deleted += count

        print(f"\n✓ Deleted {deleted} duplicate documents.\n")
        return deleted

    async def delete_by_id(self, document_id: int, confirm: bool = False) -> int:
        """Delete document by ID."""
        # First check if exists
        doc = await self.db.pool.fetchrow(
            "SELECT id, filename FROM documents WHERE id = $1", document_id
        )

        if not doc:
            print(f"\n✗ Document with ID {document_id} not found.\n")
            return 0

        if not confirm:
            print("\nDocument found:")
            print(f"  ID: {doc['id']}")
            print(f"  Filename: {doc['filename']}")
            print("\nRun with --confirm to delete.\n")
            return 0

        # Delete chunks first (foreign key)
        chunks_deleted = await self.db.pool.execute(
            "DELETE FROM chunks WHERE document_id = $1", document_id
        )
        chunks_count = int(chunks_deleted.split()[-1])

        # Delete document
        await self.db.pool.execute("DELETE FROM documents WHERE id = $1", document_id)

        print(
            f"✓ Deleted document ID {document_id} ({doc['filename']}) with {chunks_count} chunks"
        )
        return 1

    async def delete_by_filename(self, filename: str, confirm: bool = False) -> int:
        """Delete documents by filename (partial match)."""
        docs = await self.db.pool.fetch(
            "SELECT id, filename FROM documents WHERE filename ILIKE $1",
            f"%{filename}%",
        )

        if not docs:
            print(f"\n✗ No documents matching '{filename}' found.\n")
            return 0

        print(f"\nFound {len(docs)} documents matching '{filename}':")
        for doc in docs:
            print(f"  ID {doc['id']}: {doc['filename']}")

        if not confirm:
            print("\nRun with --confirm to delete these documents.\n")
            return 0

        deleted = 0
        for doc in docs:
            await self.db.pool.execute(
                "DELETE FROM chunks WHERE document_id = $1", doc["id"]
            )
            await self.db.pool.execute("DELETE FROM documents WHERE id = $1", doc["id"])
            print(f"✓ Deleted: {doc['filename']} (ID: {doc['id']})")
            deleted += 1

        print(f"\n✓ Deleted {deleted} documents.\n")
        return deleted

    async def delete_by_path(self, path: str, confirm: bool = False) -> int:
        """Delete documents by metadata filepath (partial match)."""
        docs = await self.db.pool.fetch(
            "SELECT id, filename, metadata FROM documents WHERE metadata->>'filepath' ILIKE $1",
            f"%{path}%",
        )

        if not docs:
            print(f"\n✗ No documents with path containing '{path}' found.\n")
            return 0

        print(f"\nFound {len(docs)} documents with path containing '{path}':")
        for doc in docs:
            filepath = (
                doc["metadata"].get("filepath", "N/A") if doc["metadata"] else "N/A"
            )
            print(f"  ID {doc['id']}: {filepath}")

        if not confirm:
            print("\nRun with --confirm to delete these documents.\n")
            return 0

        deleted = 0
        for doc in docs:
            await self.db.pool.execute(
                "DELETE FROM chunks WHERE document_id = $1", doc["id"]
            )
            await self.db.pool.execute("DELETE FROM documents WHERE id = $1", doc["id"])
            print(f"✓ Deleted: {doc['filename']} (ID: {doc['id']})")
            deleted += 1

        print(f"\n✓ Deleted {deleted} documents.\n")
        return deleted


async def main_async(args):
    manager = RAGDeleteManager()
    await manager.connect()

    try:
        if args.list:
            await manager.list_documents(limit=args.limit or 50)

        elif args.duplicates:
            if args.confirm:
                await manager.remove_duplicates(dry_run=False)
            else:
                await manager.show_duplicates()
                print("Run with --duplicates --confirm to remove duplicates.\n")

        elif args.id:
            await manager.delete_by_id(args.id, confirm=args.confirm)

        elif args.filename:
            await manager.delete_by_filename(args.filename, confirm=args.confirm)

        elif args.path:
            await manager.delete_by_path(args.path, confirm=args.confirm)

    finally:
        await manager.close()


def main():
    parser = argparse.ArgumentParser(
        description="RAG Delete Tool - Delete documents from RAG database",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tools/rag/rag_delete.py --list                         # List all documents
  python tools/rag/rag_delete.py --list --limit 100             # List 100 documents
  python tools/rag/rag_delete.py --id 1381                      # Show document (dry run)
  python tools/rag/rag_delete.py --id 1381 --confirm            # Delete document
  python tools/rag/rag_delete.py --filename "config_v1.md"      # Find by filename
  python tools/rag/rag_delete.py --filename "config_v1" --confirm   # Delete by filename
  python tools/rag/rag_delete.py --path "deployment/old"        # Find by path
  python tools/rag/rag_delete.py --duplicates                   # Show duplicates
  python tools/rag/rag_delete.py --duplicates --confirm         # Remove duplicates
        """,
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--list", action="store_true", help="List all documents in RAG database"
    )
    group.add_argument("--id", type=int, metavar="ID", help="Delete document by ID")
    group.add_argument(
        "--filename",
        type=str,
        metavar="NAME",
        help="Delete documents by filename (partial match)",
    )
    group.add_argument(
        "--path",
        type=str,
        metavar="PATH",
        help="Delete documents by filepath (partial match)",
    )
    group.add_argument(
        "--duplicates",
        action="store_true",
        help="Find and optionally remove duplicate documents",
    )

    parser.add_argument(
        "--confirm",
        action="store_true",
        help="Actually perform deletion (without this, dry run only)",
    )
    parser.add_argument(
        "--limit", type=int, default=50, help="Limit for --list (default: 50)"
    )

    args = parser.parse_args()
    asyncio.run(main_async(args))


if __name__ == "__main__":
    main()
