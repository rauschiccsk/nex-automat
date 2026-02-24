"""
RAG CLI Tool
Usage: python -m tools.rag "your search query"
       python -m tools.rag --help
"""

import argparse
import asyncio
import sys
from pathlib import Path

# Ensure project root is in path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from tools.rag.api import RAGSearchAPI


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser."""
    parser = argparse.ArgumentParser(
        prog="python -m tools.rag",
        description="RAG Search Tool - Search project knowledge base",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m tools.rag "Btrieve database migration"
  python -m tools.rag "supplier invoice" --limit 5
  python -m tools.rag "stock cards" --mode vector
  python -m tools.rag --stats
  python -m tools.rag "deployment guide" --context
""",
    )

    parser.add_argument("query", nargs="?", help="Search query (Slovak or English)")

    parser.add_argument(
        "-l", "--limit", type=int, default=5, help="Number of results (default: 5)"
    )

    parser.add_argument(
        "-m",
        "--mode",
        choices=["hybrid", "vector"],
        default="hybrid",
        help="Search mode (default: hybrid)",
    )

    parser.add_argument(
        "-c", "--context", action="store_true", help="Output LLM-ready context format"
    )

    parser.add_argument(
        "-f", "--full", action="store_true", help="Show full chunk content"
    )

    parser.add_argument("--stats", action="store_true", help="Show database statistics")

    parser.add_argument(
        "-q", "--quiet", action="store_true", help="Minimal output (no headers)"
    )

    return parser


async def show_stats(quiet: bool = False):
    """Show database statistics."""
    async with RAGSearchAPI() as api:
        stats = await api.get_stats()

    if quiet:
        print(f"{stats['documents']} docs, {stats['chunks']} chunks")
    else:
        print("\n[STATS] RAG Database Statistics")
        print("=" * 40)
        print(f"  Documents:  {stats['documents']}")
        print(f"  Chunks:     {stats['chunks']}")
        print(f"  Model:      {stats['embedding_model']}")
        print(f"  Dimension:  {stats['embedding_dimension']}")
        print()


async def do_search(
    query: str, limit: int, mode: str, context: bool, full: bool, quiet: bool
):
    """Perform search and display results."""
    async with RAGSearchAPI() as api:
        if context:
            # LLM context format
            ctx = await api.get_context_for_llm(query, max_chunks=limit)
            print(ctx)
            return

        # Regular search
        response = await api.search(query, limit=limit, mode=mode)

    if not quiet:
        print(f'\n[SEARCH] Query: "{query}"')
        print(f"   Mode: {mode} | Results: {response.total_found}")
        print("=" * 60)

    for i, r in enumerate(response.results, 1):
        score = r["score"]
        filename = r["filename"]

        # Score indicator
        indicator = "[HIGH]" if score > 0.5 else "[MED]" if score > 0.3 else "[LOW]"

        if quiet:
            print(f"{score:.3f} {filename}")
        else:
            print(f"\n{i}. {indicator} [{score:.3f}] {filename}")

            if r.get("keyword_score", 0) > 0:
                print(
                    f"   (vector: {r['vector_score']:.3f}, keyword: {r['keyword_score']:.3f})"
                )

            # Content preview
            content = r["content"]
            if full:
                print(f"\n{content}\n")
                print("-" * 60)
            else:
                preview = content[:200].replace("\n", " ")
                if len(content) > 200:
                    preview += "..."
                print(f"   {preview}")

    if not quiet:
        print()


def main():
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()

    # Suppress connection messages for cleaner output
    import logging

    logging.getLogger("asyncpg").setLevel(logging.WARNING)

    try:
        if args.stats:
            asyncio.run(show_stats(args.quiet))
        elif args.query:
            asyncio.run(
                do_search(
                    query=args.query,
                    limit=args.limit,
                    mode=args.mode,
                    context=args.context,
                    full=args.full,
                    quiet=args.quiet,
                )
            )
        else:
            parser.print_help()
            sys.exit(1)
    except KeyboardInterrupt:
        print("\nCancelled.")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
