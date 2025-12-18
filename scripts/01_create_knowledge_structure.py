#!/usr/bin/env python3
"""
Create knowledge directory structure for RAG indexing.
Location: Run from C:\Development\nex-automat
"""

from pathlib import Path

PROJECT_ROOT = Path(r"C:\Development\nex-automat")

KNOWLEDGE_DIRS = [
    "docs/knowledge/decisions",  # Architektonické rozhodnutia
    "docs/knowledge/development",  # Dev poznatky, patterns
    "docs/knowledge/deployment",  # Deployment postupy
    "docs/knowledge/scripts",  # Permanentné scripty ako .md
    "docs/knowledge/specifications",  # Technické špecifikácie (DB, API)
]


def main():
    print("Creating knowledge directory structure...")
    print()

    for dir_path in KNOWLEDGE_DIRS:
        full_path = PROJECT_ROOT / dir_path
        full_path.mkdir(parents=True, exist_ok=True)

        # Create .gitkeep to preserve empty dirs
        gitkeep = full_path / ".gitkeep"
        if not gitkeep.exists():
            gitkeep.touch()

        print(f"  ✓ {dir_path}/")

    print()
    print("Done! Knowledge structure created.")
    print()
    print("Usage:")
    print("  decisions/      - Architektonické rozhodnutia")
    print("  development/    - Dev poznatky, patterns, best practices")
    print("  deployment/     - Deployment postupy, konfigurácie")
    print("  scripts/        - Permanentné Python scripty ako .md")
    print("  specifications/ - Technické špecifikácie (DB schémy, API)")


if __name__ == "__main__":
    main()
