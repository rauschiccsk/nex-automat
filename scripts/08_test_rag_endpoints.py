"""
Session Script 08: Test RAG Endpoints
Projekt: nex-automat
Dočasný skript - porovnať odpovede z oboch RAG serverov
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


def test_endpoint(url, params):
    """Test RAG search endpoint"""
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}


def main():
    print_header("🔍 TEST RAG ENDPOINTS")

    query = "UAE force majeure"

    # Test 1: Localhost port 8765 (RAG-API)
    print_header("1. Localhost:8765 (RAG-API Development)")
    url_8765 = "http://127.0.0.1:8765/search"
    params = {"query": query, "limit": 3}

    result_8765 = test_endpoint(url_8765, params)

    if "error" in result_8765:
        print_error(f"Error: {result_8765['error']}")
    else:
        print_success(f"Response received")
        results = result_8765.get('results', [])
        print_info(f"Found: {len(results)} results")
        for i, r in enumerate(results, 1):
            print(f"  {i}. Score: {r.get('score', 0):.4f}")
            print(f"     Metadata: {r.get('metadata', {})}")

    # Test 2: Localhost port 8003 (NEX-Brain-API)
    print_header("2. Localhost:8003 (NEX-Brain-API)")
    url_8003 = "http://127.0.0.1:8003/api/v1/search"

    result_8003 = test_endpoint(url_8003, params)

    if "error" in result_8003:
        print_error(f"Error: {result_8003['error']}")
        print_info("NEX-Brain nemá /search endpoint, má /chat")
    else:
        print_success(f"Response received")
        results = result_8003.get('results', [])
        print_info(f"Found: {len(results)} results")

    # Test 3: Cloudflare tunnel (rag-api.icc.sk)
    print_header("3. Cloudflare Tunnel (https://rag-api.icc.sk)")
    url_cf = "https://rag-api.icc.sk/search"

    result_cf = test_endpoint(url_cf, params)

    if "error" in result_cf:
        print_error(f"Error: {result_cf['error']}")
    else:
        print_success(f"Response received")
        results = result_cf.get('results', [])
        print_info(f"Found: {len(results)} results")
        for i, r in enumerate(results, 1):
            print(f"  {i}. Score: {r.get('score', 0):.4f}")
            print(f"     Metadata: {r.get('metadata', {})}")

    # Comparison
    print_header("📊 POROVNANIE")

    count_8765 = len(result_8765.get('results', [])) if "error" not in result_8765 else 0
    count_cf = len(result_cf.get('results', [])) if "error" not in result_cf else 0

    print(f"Port 8765: {count_8765} results")
    print(f"Cloudflare: {count_cf} results")

    if count_8765 == 0 and count_cf > 0:
        print_success("Cloudflare tunnel smeruje NA INÝ RAG server (nie port 8765)")
    elif count_8765 > 0 and count_cf > 0:
        if count_8765 == count_cf:
            print_success("Cloudflare tunnel smeruje NA port 8765")
        else:
            print_info("Cloudflare a port 8765 vracajú rozdielne výsledky")
    elif count_8765 == 0 and count_cf == 0:
        print_error("Oba servery vracajú prázdne výsledky")


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