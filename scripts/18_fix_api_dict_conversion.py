"""
Session Script 18: Fix api.py - remove dict() conversion
Projekt: nex-automat
Dočasný skript - opraví ValueError pri dict(r.metadata)
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
    print_header("🔧 FIX: api.py - remove dict() conversion")

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

    # Fix the dict() conversion
    old_line = "            result_metadata = dict(r.metadata) if r.metadata else {}"
    new_line = "            result_metadata = r.metadata.copy() if r.metadata else {}"

    if old_line not in content:
        print_error("Pattern not found - file may be already fixed or different")
        print_info("Looking for: result_metadata = dict(r.metadata)")
        return

    print_info("Removing unnecessary dict() conversion...")
    content = content.replace(old_line, new_line)
    print_success("Pattern replaced")

    # Write fixed content
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print_success(f"Fixed file written: {target_file}")

    print_header("✅ OPRAVA DOKONČENÁ")
    print_info("r.metadata je už dictionary, používame .copy() namiesto dict()")
    print_info("Teraz spusti test: python scripts\\17_test_api_direct.py")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print_error(f"\nFailed: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)