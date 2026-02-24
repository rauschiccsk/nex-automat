#!/usr/bin/env python
"""
NEX Brain CLI - Command line interface for testing.
Multi-tenant support.
"""

import asyncio
import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from api.services.llm_service import LLMService
from api.services.rag_service import RAGService
from config.settings import settings


async def main():
    """Interactive CLI for NEX Brain."""
    print("=" * 60)
    print("  NEX Brain CLI - Interaktívne rozhranie")
    print("=" * 60)

    # Show mode
    if settings.is_multi_tenant:
        print(f"Mode: Multi-tenant ({', '.join(settings.tenant_list)})")
    else:
        print(f"Mode: Single-tenant ({settings.TENANT})")

    print("-" * 60)
    print("Príkazy:")
    print("  'quit' alebo 'q'    - ukončenie")
    print("  'rag <query>'       - priame RAG vyhľadávanie")
    print("  'tenant <name>'     - zmena tenanta (multi-tenant mode)")
    print("-" * 60)

    rag = RAGService()
    llm = LLMService()

    # Current tenant
    if settings.is_multi_tenant:
        current_tenant = settings.tenant_list[0]  # Default to first
        print(f"Aktuálny tenant: {current_tenant}")
    else:
        current_tenant = settings.TENANT or "default"

    # Check Ollama
    if await llm.health_check():
        print(f"✅ Ollama: {llm.model_name}")
    else:
        print("⚠️  Ollama nie je dostupná - odpovede budú len z RAG")

    print()

    while True:
        try:
            prompt = (
                f"[{current_tenant}] Otázka: "
                if settings.is_multi_tenant
                else "Otázka: "
            )
            question = input(prompt).strip()

            if not question:
                continue

            if question.lower() in ("quit", "q", "exit"):
                print("Dovidenia!")
                break

            # Change tenant
            if question.lower().startswith("tenant "):
                new_tenant = question[7:].strip()
                if new_tenant in settings.tenant_list:
                    current_tenant = new_tenant
                    print(f"✅ Tenant zmenený na: {current_tenant}")
                else:
                    print(
                        f"❌ Neznámy tenant. Dostupné: {', '.join(settings.tenant_list)}"
                    )
                print()
                continue

            # Direct RAG search
            if question.lower().startswith("rag "):
                query = question[4:].strip()
                print(f"\nVyhľadávam v RAG: '{query}' (tenant: {current_tenant})...")
                results = await rag.search(query, limit=5, tenant=current_tenant)

                if results:
                    for i, r in enumerate(results, 1):
                        print(
                            f"\n[{i}] {r.get('filename')} (score: {r.get('score', 0):.3f})"
                        )
                        content = r.get("content", "")[:200]
                        print(f"    {content}...")
                else:
                    print("Žiadne výsledky.")
                print()
                continue

            # Full RAG + LLM query
            print("\nHľadám kontext...")
            context = await rag.search(question, limit=5, tenant=current_tenant)

            if context:
                print(f"Našiel som {len(context)} relevantných dokumentov.")

            print("Generujem odpoveď...\n")
            answer, tokens = await llm.generate(
                question, context, tenant=current_tenant
            )

            print("-" * 40)
            print(answer)
            print("-" * 40)

            if tokens:
                print(f"[tenant: {current_tenant}, tokens: {tokens}]")
            print()

        except KeyboardInterrupt:
            print("\nUkončené.")
            break
        except Exception as e:
            print(f"Chyba: {e}")


if __name__ == "__main__":
    asyncio.run(main())
