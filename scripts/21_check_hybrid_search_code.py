"""
Session Script 21: Check hybrid_search.py metadata handling
Projekt: nex-automat
Dočasný skript - zobrazí ako hybrid_search.py spracováva metadata
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def main():
    print("🔍 Checking hybrid_search.py metadata handling...\n")

    target_file = project_root / "tools" / "rag" / "hybrid_search.py"

    with open(target_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Find lines with 'metadata'
    print("Lines containing 'metadata':\n")
    for i, line in enumerate(lines, 1):
        if 'metadata' in line.lower() and not line.strip().startswith('#'):
            print(f"{i:4}: {line.rstrip()}")

    # Find the SearchResult construction
    print("\n" + "=" * 70)
    print("SearchResult construction:")
    print("=" * 70 + "\n")

    in_construction = False
    construction_lines = []

    for i, line in enumerate(lines, 1):
        if 'search_results.append(SearchResult(' in line:
            in_construction = True

        if in_construction:
            construction_lines.append(f"{i:4}: {line.rstrip()}")
            if '))' in line and in_construction:
                break

    for line in construction_lines:
        print(line)


if __name__ == "__main__":
    main()