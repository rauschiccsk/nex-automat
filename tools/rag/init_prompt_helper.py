"""
Init Prompt Helper
Generates RAG context for Claude chat initialization.

Usage:
  python -m tools.rag.init_prompt_helper "topic or task"
  python -m tools.rag.init_prompt_helper --interactive
"""

import argparse
import asyncio
import sys
from datetime import datetime
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from tools.rag.api import RAGSearchAPI

CONTEXT_TEMPLATE = """## [DOCS] RAG Context - Auto-generated

**Query:** {query}
**Generated:** {timestamp}
**Sources:** {source_count} chunks from {doc_count} documents

---

{context}

---

**Note:** Tento kontext bol automaticky vygenerovaný z projektovej knowledge base.
"""


async def generate_context(
    query: str, max_chunks: int = 5, max_tokens: int = 6000, include_scores: bool = True
) -> str:
    """
    Generate context section for init prompt.

    Args:
        query: Topic or task description
        max_chunks: Maximum chunks to include
        max_tokens: Approximate token limit

    Returns:
        Formatted context string
    """
    async with RAGSearchAPI() as api:
        response = await api.search(query, limit=max_chunks, mode="hybrid")

        if not response.results:
            return f"No relevant context found for: {query}"

        # Build context sections
        sections = []
        total_chars = 0
        char_limit = max_tokens * 4
        unique_docs = set()

        for r in response.results:
            if total_chars + len(r["content"]) > char_limit:
                break

            unique_docs.add(r["filename"])

            if include_scores:
                header = f"### [DOC] {r['filename']} (relevance: {r['score']:.2f})"
            else:
                header = f"### [DOC] {r['filename']}"

            sections.append(f"{header}\n\n{r['content']}")
            total_chars += len(r["content"])

        context = "\n\n---\n\n".join(sections)

        return CONTEXT_TEMPLATE.format(
            query=query,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M"),
            source_count=len(sections),
            doc_count=len(unique_docs),
            context=context,
        )


async def generate_multi_context(queries: list, max_chunks_per_query: int = 3) -> str:
    """Generate context for multiple queries/topics."""

    all_sections = []

    async with RAGSearchAPI() as api:
        for query in queries:
            response = await api.search(
                query, limit=max_chunks_per_query, mode="hybrid"
            )

            if response.results:
                section = f"## Topic: {query}\n\n"
                for r in response.results:
                    section += f"**{r['filename']}** (score: {r['score']:.2f})\n"
                    section += f"{r['content'][:500]}...\n\n"
                all_sections.append(section)

    header = f"""## [DOCS] Multi-Topic RAG Context

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M")}
**Topics:** {len(queries)}

---

"""
    return header + "\n---\n\n".join(all_sections)


async def interactive_mode():
    """Interactive context generation."""
    print("\n[BOT] RAG Init Prompt Helper - Interactive Mode")
    print("=" * 50)
    print("Type queries to generate context. Commands:")
    print("  /quit    - Exit")
    print("  /copy    - Copy last context to clipboard")
    print("  /save    - Save last context to file")
    print("  /multi   - Enter multi-topic mode")
    print()

    last_context = None

    async with RAGSearchAPI() as api:
        stats = await api.get_stats()
        print(
            f"[STATS] Database: {stats['documents']} docs, {stats['chunks']} chunks\n"
        )

    while True:
        try:
            query = input("[SEARCH] Query: ").strip()
        except EOFError:
            break

        if not query:
            continue

        if query == "/quit":
            break

        if query == "/copy" and last_context:
            try:
                import pyperclip

                pyperclip.copy(last_context)
                print("[OK] Copied to clipboard!\n")
            except ImportError:
                print("[WARN] pyperclip not installed. Use /save instead.\n")
            continue

        if query == "/save" and last_context:
            filename = f"rag_context_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            Path(filename).write_text(last_context, encoding="utf-8")
            print(f"[OK] Saved to {filename}\n")
            continue

        if query == "/multi":
            print("Enter topics (one per line, empty line to finish):")
            topics = []
            while True:
                topic = input("  > ").strip()
                if not topic:
                    break
                topics.append(topic)

            if topics:
                print("\nGenerating multi-topic context...")
                last_context = await generate_multi_context(topics)
                print("\n" + last_context)
            continue

        # Regular query
        print("\nGenerating context...\n")
        last_context = await generate_context(query)
        print(last_context)
        print()

    print("\nGoodbye! ")


def main():
    parser = argparse.ArgumentParser(
        description="Generate RAG context for Claude init prompts"
    )

    parser.add_argument(
        "query", nargs="?", help="Topic or task to generate context for"
    )

    parser.add_argument(
        "-i", "--interactive", action="store_true", help="Interactive mode"
    )

    parser.add_argument(
        "-c", "--chunks", type=int, default=5, help="Max chunks to include (default: 5)"
    )

    parser.add_argument("-o", "--output", help="Save to file")

    args = parser.parse_args()

    if args.interactive:
        asyncio.run(interactive_mode())
    elif args.query:
        context = asyncio.run(generate_context(args.query, max_chunks=args.chunks))

        if args.output:
            Path(args.output).write_text(context, encoding="utf-8")
            print(f"[OK] Saved to {args.output}")
        else:
            print(context)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
