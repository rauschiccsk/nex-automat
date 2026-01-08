"""
Session Script 16: Fix api.py - preserve metadata (v2 - without unpacking)
Projekt: nex-automat
Dočasný skript - opraví api.py pomocou dict.update() namiesto unpacking
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'=' * 70}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'=' * 70}{Colors.RESET}\n")


def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")


def print_error(text):
    print(f"{Colors.RED}✗ {text}{Colors.RESET}")


def print_info(text):
    print(f"{Colors.BLUE}ℹ {text}{Colors.RESET}")


def main():
    print_header("🔧 FIX: api.py - preserve metadata (v2)")

    # Target file
    target_file = project_root / "tools" / "rag" / "api.py"

    if not target_file.exists():
        print_error(f"File not found: {target_file}")
        return

    print_success(f"Found file: {target_file}")

    # Read content
    with open(target_file, 'r', encoding='utf-8') as f:
        content = f.read()

    print_info(f"File size: {len(content)} characters")

    # Find and replace - looking for the unpacking version from script 15
    old_code = """        # Convert hybrid_search.SearchResult to api.SearchResult
        search_results = [
            SearchResult(
                filename=r.filename,
                content=r.content,
                score=r.combined_score,  # Use combined_score as main score
                chunk_id=str(r.chunk_id),
                section=None,  # hybrid_search doesn't have section
                metadata={
                    **(r.metadata or {}),  # Include original metadata (tenant, filepath, etc.)
                    'similarity': r.similarity,
                    'keyword_score': r.keyword_score,
                    'document_id': r.document_id,
                    'chunk_index': r.chunk_index
                }
            )
            for r in results
        ]"""

    new_code = """        # Convert hybrid_search.SearchResult to api.SearchResult
        search_results = []
        for r in results:
            # Start with original metadata from hybrid_search
            result_metadata = dict(r.metadata) if r.metadata else {}
            # Add search-specific metadata
            result_metadata.update({
                'similarity': r.similarity,
                'keyword_score': r.keyword_score,
                'document_id': r.document_id,
                'chunk_index': r.chunk_index
            })

            search_results.append(SearchResult(
                filename=r.filename,
                content=r.content,
                score=r.combined_score,
                chunk_id=str(r.chunk_id),
                section=None,
                metadata=result_metadata
            ))"""

    if old_code not in content:
        print_error("Pattern with unpacking not found")
        print_info("Trying to find original pattern...")

        # Try original pattern
        old_code_original = """        # Convert hybrid_search.SearchResult to api.SearchResult
        search_results = [
            SearchResult(
                filename=r.filename,
                content=r.content,
                score=r.combined_score,  # Use combined_score as main score
                chunk_id=str(r.chunk_id),
                section=None,  # hybrid_search doesn't have section
                metadata={
                    'similarity': r.similarity,
                    'keyword_score': r.keyword_score,
                    'document_id': r.document_id,
                    'chunk_index': r.chunk_index
                }
            )
            for r in results
        ]"""

        if old_code_original in content:
            print_info("Found original pattern (without unpacking)")
            content = content.replace(old_code_original, new_code)
            print_success("Pattern replaced")
        else:
            print_error("Could not find any matching pattern")
            return
    else:
        print_info("Found pattern with unpacking")
        content = content.replace(old_code, new_code)
        print_success("Pattern replaced")

    # Write fixed content
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print_success(f"Fixed file written: {target_file}")

    print_header("✅ OPRAVA DOKONČENÁ")
    print_info("api.py teraz používa dict.update() namiesto unpacking")
    print_info("Potrebné kroky:")
    print_info("1. Reštartuj RAG-API server (port 8765)")
    print_info("2. Spusti test: python scripts\\01_test_uae_legal_rag.py")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print_error(f"\nFailed: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)