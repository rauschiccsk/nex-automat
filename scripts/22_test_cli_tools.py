#!/usr/bin/env python
"""
Script 22: Test CLI Tools
Demonstrates RAG CLI and Init Prompt Helper.
"""

import subprocess
import sys


def run_command(cmd: str, description: str):
    """Run command and show output."""
    print(f"\n{'=' * 60}")
    print(f"📌 {description}")
    print(f"$ {cmd}")
    print("-" * 60)

    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True
    )

    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

    return result.returncode == 0


def main():
    print("=" * 60)
    print("RAG CLI TOOLS TEST")
    print("=" * 60)

    # Test 1: CLI --stats
    run_command(
        'python -m tools.rag --stats',
        'CLI: Show database stats'
    )

    # Test 2: CLI search
    run_command(
        'python -m tools.rag "supplier invoice workflow" --limit 3',
        'CLI: Hybrid search'
    )

    # Test 3: CLI vector mode
    run_command(
        'python -m tools.rag "Btrieve migration" --mode vector --limit 2',
        'CLI: Vector-only search'
    )

    # Test 4: CLI context mode
    run_command(
        'python -m tools.rag "stock management" --context --limit 2',
        'CLI: LLM context format'
    )

    # Test 5: CLI quiet mode
    run_command(
        'python -m tools.rag "deployment" --quiet --limit 3',
        'CLI: Quiet mode (minimal output)'
    )

    # Test 6: Init Prompt Helper
    run_command(
        'python -m tools.rag.init_prompt_helper "RAG implementation chunks embedding" --chunks 2',
        'Init Prompt Helper: Generate context'
    )

    print("\n" + "=" * 60)
    print("TEST COMPLETE ✅")
    print("=" * 60)
    print("\nUsage summary:")
    print("  python -m tools.rag 'query'              # Quick search")
    print("  python -m tools.rag 'query' --context    # LLM context")
    print("  python -m tools.rag --stats              # Database stats")
    print("  python -m tools.rag.init_prompt_helper 'topic'  # Init prompt context")
    print("  python -m tools.rag.init_prompt_helper -i       # Interactive mode")


if __name__ == "__main__":
    main()