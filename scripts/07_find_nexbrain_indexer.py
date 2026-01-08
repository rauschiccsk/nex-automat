"""
Session Script 07: Find NexBrain Indexer
Projekt: nex-automat
Dočasný skript - nájsť indexačný proces v apps/nex-brain/
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


def find_python_files(directory, keywords):
    """Find Python files containing specific keywords"""
    results = []

    for py_file in directory.rglob("*.py"):
        try:
            content = py_file.read_text(encoding='utf-8')
            matches = [kw for kw in keywords if kw.lower() in content.lower()]

            if matches:
                results.append({
                    'file': py_file,
                    'matches': matches,
                    'size': py_file.stat().st_size
                })
        except Exception as e:
            pass

    return results


def show_file_content(file_path, max_lines=50):
    """Show beginning of file content"""
    try:
        lines = file_path.read_text(encoding='utf-8').split('\n')
        print(f"\n{Colors.BOLD}Content preview ({len(lines)} lines total):{Colors.RESET}")
        for i, line in enumerate(lines[:max_lines], 1):
            print(f"{i:3}: {line}")

        if len(lines) > max_lines:
            print(f"\n{Colors.YELLOW}... (showing first {max_lines} of {len(lines)} lines){Colors.RESET}")
    except Exception as e:
        print_error(f"Cannot read file: {e}")


def main():
    print_header("🔍 HĽADANIE NEXBRAIN INDEXAČNÉHO PROCESU")

    nex_brain_dir = project_root / "apps" / "nex-brain"

    if not nex_brain_dir.exists():
        print_error(f"NexBrain directory not found: {nex_brain_dir}")
        return

    print_success(f"NexBrain directory found: {nex_brain_dir}")

    # 1. Find indexing-related files
    print_header("1. Hľadanie súborov s indexačnými kľúčovými slovami")

    keywords = [
        "index", "indexing", "embed", "chromadb", "chroma",
        "vector", "vectorstore", "ingest", "load_documents"
    ]

    results = find_python_files(nex_brain_dir, keywords)

    if results:
        print_success(f"Found {len(results)} relevant files:")
        for result in sorted(results, key=lambda x: len(x['matches']), reverse=True):
            rel_path = result['file'].relative_to(project_root)
            matches_str = ", ".join(result['matches'])
            print(f"  📄 {rel_path}")
            print(f"     Matches: {matches_str}")
            print(f"     Size: {result['size']} bytes")
    else:
        print_warning("No indexing files found")

    # 2. Check for README or documentation
    print_header("2. Dokumentácia")
    docs = []
    for pattern in ["README.md", "README.txt", "SETUP.md", "docs/*.md"]:
        docs.extend(nex_brain_dir.rglob(pattern))

    if docs:
        print_success(f"Found {len(docs)} documentation files:")
        for doc in docs:
            rel_path = doc.relative_to(project_root)
            print(f"  📖 {rel_path}")
    else:
        print_warning("No documentation found")

    # 3. Check .env file
    print_header("3. Konfigurácia (.env)")
    env_file = nex_brain_dir / ".env"

    if env_file.exists():
        print_success(f"Found .env: {env_file}")
        try:
            content = env_file.read_text(encoding='utf-8')
            print(f"\n{Colors.BOLD}.env content:{Colors.RESET}")
            for line in content.split('\n'):
                if line.strip() and not line.startswith('#'):
                    print(f"  {line}")
        except Exception as e:
            print_error(f"Cannot read .env: {e}")
    else:
        print_warning(".env file not found")

    # 4. Show most relevant file
    if results:
        print_header("4. Najrelevantnejší súbor - obsah")
        top_file = results[0]['file']
        print_info(f"File: {top_file.relative_to(project_root)}")
        show_file_content(top_file, max_lines=100)

    # 5. List all Python scripts
    print_header("5. Všetky Python skripty v NexBrain")
    all_scripts = sorted(nex_brain_dir.rglob("*.py"))

    if all_scripts:
        print_success(f"Found {len(all_scripts)} Python files:")
        for script in all_scripts:
            rel_path = script.relative_to(nex_brain_dir)
            size = script.stat().st_size
            print(f"  {rel_path} ({size} bytes)")

    print_header("📊 HĽADANIE DOKONČENÉ")
    print_info("Skontroluj výsledky vyššie pre identifikáciu indexačného procesu")


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