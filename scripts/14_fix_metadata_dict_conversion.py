"""
Session Script 14: Fix metadata dict() conversion in hybrid_search.py
Projekt: nex-automat
Dočasný skript - opraví ValueError pri konverzii metadata
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
    print_header("🔧 FIX: metadata dict() conversion")

    # Target file
    target_file = project_root / "tools" / "rag" / "hybrid_search.py"

    if not target_file.exists():
        print_error(f"File not found: {target_file}")
        return

    print_success(f"Found file: {target_file}")

    # Read content
    with open(target_file, 'r', encoding='utf-8') as f:
        content = f.read()

    print_info(f"File size: {len(content)} characters")

    # Fix the metadata conversion
    old_line = "                metadata=dict(r['metadata']) if r['metadata'] else None"
    new_line = "                metadata=r['metadata'] if r['metadata'] else None"

    if old_line not in content:
        print_error("Pattern not found - file may be already fixed or different")
        print_info("Looking for: metadata=dict(r['metadata'])")
        return

    print_info("Removing unnecessary dict() conversion...")
    content = content.replace(old_line, new_line)
    print_success("Pattern replaced")

    # Write fixed content
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print_success(f"Fixed file written: {target_file}")

    print_header("✅ OPRAVA DOKONČENÁ")
    print_info("Metadata je už dictionary z PostgreSQL, nepotrebuje dict() konverziu")
    print_info("Teraz spusti test: python scripts\\13_test_hybrid_search_direct.py")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print_error(f"\nFailed: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)