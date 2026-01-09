#!/usr/bin/env python3
"""
Test script for UAE Legal RAG system
Tests queries against indexed legal documents

Usage:
    python test_rag_uae.py
"""

import sys
from pathlib import Path

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.rag.rag_manager import RAGManager


def print_header(text: str):
    """Print formatted header"""
    print("\n" + "=" * 70)
    print(text)
    print("=" * 70)


def print_result(idx: int, result: dict):
    """Print a single search result"""
    print(f"\n{idx}. Relevance Score: {result.get('distance', 0):.4f}")

    # Extract metadata
    metadata = result.get('metadata', {})
    source = metadata.get('source', 'Unknown')
    tenant = metadata.get('tenant', 'Unknown')

    print(f"   Tenant: {tenant}")
    print(f"   Source: {source}")
    print(f"   Content Preview:")

    content = result.get('content', '')
    # Show first 400 characters
    preview = content[:400] + "..." if len(content) > 400 else content

    # Indent content
    for line in preview.split('\n'):
        print(f"   {line}")

    print("-" * 70)


def test_query(rag: RAGManager, query: str, test_name: str, top_k: int = 3):
    """Execute a test query and display results"""
    print_header(f"TEST: {test_name}")
    print(f"Query: {query}")
    print(f"Searching for top {top_k} results...\n")

    try:
        results = rag.search(
            query=query,
            tenant='uae',
            top_k=top_k
        )

        if not results:
            print("❌ No results found!")
            return

        print(f"✓ Found {len(results)} results\n")

        for i, result in enumerate(results, 1):
            print_result(i, result)

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


def main():
    """Main test function"""
    print_header("UAE LEGAL RAG SYSTEM - TEST SUITE")
    print("Initializing RAG Manager...")

    try:
        # Initialize RAG Manager
        rag = RAGManager()
        print("✓ RAG Manager initialized successfully\n")

        # Get collection stats
        try:
            collection = rag.get_collection('uae')
            count = collection.count()
            print(f"✓ UAE Collection: {count} chunks indexed\n")
        except Exception as e:
            print(f"⚠ Warning: Could not get collection stats: {e}\n")

        # Test 1: Money Laundering Definition
        test_query(
            rag=rag,
            query="What is the definition of money laundering under UAE law?",
            test_name="Money Laundering Definition",
            top_k=3
        )

        # Test 2: Detention Periods
        test_query(
            rag=rag,
            query="What are the maximum detention periods without court approval in UAE criminal procedure?",
            test_name="Detention Periods",
            top_k=3
        )

        # Test 3: Burden of Proof
        test_query(
            rag=rag,
            query="What is the burden of proof for money laundering? Is actual knowledge required?",
            test_name="Burden of Proof - Money Laundering",
            top_k=3
        )

        # Test 4: Right to Legal Representation
        test_query(
            rag=rag,
            query="What are the rights of accused persons to legal representation and defense attorneys?",
            test_name="Right to Legal Representation",
            top_k=3
        )

        # Test 5: Asset Freezing
        test_query(
            rag=rag,
            query="Can authorities freeze assets without notice? What are the procedures for grievance?",
            test_name="Asset Freezing and Grievance Procedures",
            top_k=3
        )

        # Test 6: Appeal Rights
        test_query(
            rag=rag,
            query="What are the appeal rights and procedures in UAE criminal cases?",
            test_name="Appeal Rights and Procedures",
            top_k=3
        )

        print_header("TEST SUITE COMPLETED")
        print("✓ All tests executed successfully")

    except Exception as e:
        print(f"\n❌ Fatal Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()