"""
Session Script 20: Test local RAG-API endpoint directly
Projekt: nex-automat
Dočasný skript - test RAG-API na localhost:8765
"""

import sys
import requests
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
    print_header("🧪 TEST: Local RAG-API Endpoint")

    # Test local RAG-API directly
    url = "http://127.0.0.1:8765/search"
    params = {
        "query": "UAE force majeure",
        "max_results": 3,
        "tenant": "uae"
    }

    print_info(f"Testing: {url}")
    print_info(f"Params: {params}\n")

    try:
        response = requests.get(url, params=params, timeout=10)

        print_info(f"Status code: {response.status_code}")

        if response.status_code == 200:
            print_success("Request successful!")
            data = response.json()

            print(f"\nQuery: {data.get('query')}")
            print(f"Count: {data.get('count')}")
            print(f"Results: {len(data.get('results', []))}\n")

            for i, result in enumerate(data.get('results', [])[:3], 1):
                print(f"{Colors.YELLOW}Result {i}:{Colors.RESET}")
                print(f"  Filename: {result.get('filename')}")
                print(f"  Score: {result.get('score', 0):.4f}")
                metadata = result.get('metadata', {})
                print(f"  Tenant: {metadata.get('tenant', 'N/A')}")
                print(f"  Filepath: {metadata.get('filepath', 'N/A')[:80]}...")
                print()
        else:
            print_error(f"Request failed with status {response.status_code}")
            print(f"\nResponse text:\n{response.text}")

    except Exception as e:
        print_error(f"Request failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⚠ Interrupted{Colors.RESET}")
        sys.exit(1)