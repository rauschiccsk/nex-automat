"""
Session Script 12: Patch hybrid_search.py - pridať metadata support
Projekt: nex-automat
Dočasný skript - opraví hybrid_search.py na vrátenie metadata (tenant, source)
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


def print_warning(text):
    print(f"{Colors.YELLOW}⚠ {text}{Colors.RESET}")


def main():
    print_header("🔧 PATCH: hybrid_search.py - Pridať metadata support")

    # Target file
    target_file = project_root / "tools" / "rag" / "hybrid_search.py"

    if not target_file.exists():
        print_error(f"File not found: {target_file}")
        return

    print_success(f"Found file: {target_file}")

    # Read original content
    with open(target_file, 'r', encoding='utf-8') as f:
        content = f.read()

    print_info(f"Original file size: {len(content)} characters")

    # Check if already patched
    if "metadata: Optional[Dict[str, Any]] = None" in content:
        print_warning("File already patched (metadata field exists in SearchResult)")
        return

    print_header("Aplikujem 3 zmeny:")

    # PATCH 1: Add metadata to SearchResult dataclass
    print_info("1. Pridávam 'metadata' pole do SearchResult dataclass...")

    old_dataclass = """    combined_score: float


class HybridSearch:"""

    new_dataclass = """    combined_score: float
    metadata: Optional[Dict[str, Any]] = None


class HybridSearch:"""

    if old_dataclass in content:
        content = content.replace(old_dataclass, new_dataclass)
        print_success("   ✓ SearchResult dataclass updated")
    else:
        print_error("   ✗ SearchResult pattern not found")
        return

    # PATCH 2: Add d.metadata to SQL queries (both tenant and non-tenant versions)
    print_info("2. Pridávam 'd.metadata' do SQL SELECT...")

    # Tenant query
    old_sql_tenant = """                SELECT 
                    c.id as chunk_id,
                    c.document_id,
                    d.filename,
                    c.chunk_index,
                    c.content,
                    1 - (c.embedding <=> $1::vector) as similarity"""

    new_sql_tenant = """                SELECT 
                    c.id as chunk_id,
                    c.document_id,
                    d.filename,
                    c.chunk_index,
                    c.content,
                    d.metadata,
                    1 - (c.embedding <=> $1::vector) as similarity"""

    if old_sql_tenant in content:
        content = content.replace(old_sql_tenant, new_sql_tenant, 2)  # Replace both occurrences
        print_success("   ✓ SQL queries updated (both tenant and non-tenant)")
    else:
        print_error("   ✗ SQL pattern not found")
        return

    # PATCH 3: Add metadata to SearchResult construction
    print_info("3. Pridávam 'metadata' do SearchResult konštrukcie...")

    old_construction = """            search_results.append(SearchResult(
                chunk_id=r['chunk_id'],
                document_id=r['document_id'],
                filename=r['filename'],
                chunk_index=r['chunk_index'],
                content=r['content'],
                similarity=r['similarity'],
                keyword_score=keyword_score,
                combined_score=combined_score
            ))"""

    new_construction = """            search_results.append(SearchResult(
                chunk_id=r['chunk_id'],
                document_id=r['document_id'],
                filename=r['filename'],
                chunk_index=r['chunk_index'],
                content=r['content'],
                similarity=r['similarity'],
                keyword_score=keyword_score,
                combined_score=combined_score,
                metadata=dict(r['metadata']) if r['metadata'] else None
            ))"""

    if old_construction in content:
        content = content.replace(old_construction, new_construction)
        print_success("   ✓ SearchResult construction updated")
    else:
        print_error("   ✗ SearchResult construction pattern not found")
        return

    # Create backup
    backup_file = target_file.with_suffix('.py.backup')
    print_header("Vytvárám zálohu...")

    with open(backup_file, 'w', encoding='utf-8') as f:
        # Read original again for backup
        with open(target_file, 'r', encoding='utf-8') as orig:
            f.write(orig.read())

    print_success(f"Backup created: {backup_file}")

    # Write patched content
    print_header("Zapisujem opravený súbor...")

    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print_success(f"Patched file written: {target_file}")
    print_info(f"New file size: {len(content)} characters")

    print_header("✅ PATCH ÚSPEŠNE APLIKOVANÝ")
    print_warning("Potrebné kroky:")
    print_info("1. Reštartuj RAG-API server (Ctrl+C a znova spusti)")
    print_info("2. Spusti test: python scripts\\01_test_uae_legal_rag.py")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⚠ Interrupted{Colors.RESET}")
        sys.exit(1)
    except Exception as e:
        print_error(f"\nFailed: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)