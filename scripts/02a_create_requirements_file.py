#!/usr/bin/env python3
"""
Script 02a: Create requirements-rag.txt file
Session: RAG Implementation Phase 2
"""

from pathlib import Path

REQUIREMENTS_CONTENT = """# RAG Implementation Dependencies
# NEX Automat Project
# Phase 2: Python Environment Setup

# Core RAG dependencies
sentence-transformers==2.5.1
asyncpg==0.29.0
pydantic==2.10.5
pydantic-settings==2.7.1
tiktoken==0.6.0
numpy==1.26.3
PyYAML==6.0.1

# Optional but recommended
python-dotenv==1.0.1
tqdm==4.66.1
"""


def main():
    print("=== Script 02a: Creating requirements-rag.txt ===\n")

    requirements_file = Path("requirements-rag.txt")

    print(f"Creating: {requirements_file.absolute()}")
    requirements_file.write_text(REQUIREMENTS_CONTENT)
    print(f"✓ Created: {requirements_file}\n")

    print("Next: Run script 02 again")
    print("  python scripts/02_install_rag_dependencies.py")

    return 0


if __name__ == "__main__":
    main()