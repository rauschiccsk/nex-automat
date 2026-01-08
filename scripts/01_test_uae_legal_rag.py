"""
Session Script 01: Test UAE Legal Documentation in RAG System
Projekt: nex-automat
Dočasný testovací skript
"""

import sys
import requests
from datetime import datetime
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


def test_rag_search(query, tenant="uae", limit=5):
    """Test RAG search API"""
    url = "https://rag-api.icc.sk/search"
    params = {
        "query": query,
        "limit": limit,
        "tenant": tenant
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print_error(f"RAG search failed: {e}")
        return None


def test_nexbrain_chat(message, tenant="uae"):
    """Test NexBrain chat API"""
    url = "http://127.0.0.1:8003/api/v1/chat"
    payload = {
        "message": message,
        "tenant": tenant,
        "conversation_id": f"test_uae_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    }

    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print_error(f"NexBrain chat failed: {e}")
        return None


def test_nexbrain_tenants():
    """Test NexBrain tenants endpoint"""
    url = "http://127.0.0.1:8003/api/v1/tenants"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print_error(f"NexBrain tenants check failed: {e}")
        return None


def display_search_results(results, query):
    """Display RAG search results"""
    if not results or 'results' not in results:
        print_error("No results returned")
        return

    print(f"\n{Colors.BOLD}Query:{Colors.RESET} {query}")
    print(f"{Colors.BOLD}Found:{Colors.RESET} {len(results['results'])} results")

    for i, result in enumerate(results['results'], 1):
        print(f"\n{Colors.YELLOW}Result {i}:{Colors.RESET}")
        print(f"  Score: {result.get('score', 0):.4f}")

        # Extract metadata
        metadata = result.get('metadata', {})

        # Get source from metadata
        source = metadata.get('filepath', 'N/A')
        if source != 'N/A':
            # Extract just filename from full path
            source = source.split('\\')[-1] if '\\' in source else source.split('/')[-1]

        # Get tenant from metadata
        tenant = metadata.get('tenant', 'N/A')

        print(f"  Source: {source}")
        print(f"  Tenant: {tenant}")

        content = result.get('content', '')
        preview = content[:200] + "..." if len(content) > 200 else content
        print(f"  Content: {preview}")


def run_test_suite():
    """Run complete UAE legal documentation test suite"""

    print_header("🧪 UAE LEGAL DOCUMENTATION TEST SUITE")
    print_info(f"Starting test at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Test 1: Check tenants
    print_header("TEST 1: NexBrain Tenants Configuration")
    tenants = test_nexbrain_tenants()
    if tenants:
        print_success("NexBrain API is accessible")
        print_info(f"Available tenants: {tenants.get('tenants', [])}")
        if 'uae' in tenants.get('tenants', []):
            print_success("UAE tenant is configured")
        else:
            print_warning("UAE tenant not found in configuration")
    else:
        print_error("Cannot connect to NexBrain API")

    # Test 2: RAG Search Tests
    print_header("TEST 2: RAG Search - Business Setup")
    queries = [
        "How to register a company in UAE free zone?",
        "What are the costs of mainland company formation?",
        "Dubai trade license requirements",
        "Offshore company advantages UAE",
        "Visa requirements for business owners"
    ]

    for query in queries:
        print(f"\n{Colors.CYAN}Testing query:{Colors.RESET} {query}")
        results = test_rag_search(query, tenant="uae", limit=3)
        if results:
            display_search_results(results, query)
        else:
            print_error(f"Search failed for: {query}")

    # Test 3: Legal Topics
    print_header("TEST 3: RAG Search - Legal Topics")
    legal_queries = [
        "Employment law regulations UAE",
        "Contract law requirements",
        "Intellectual property protection",
        "Banking and finance regulations",
        "Tax compliance requirements"
    ]

    for query in legal_queries:
        print(f"\n{Colors.CYAN}Testing query:{Colors.RESET} {query}")
        results = test_rag_search(query, tenant="uae", limit=3)
        if results:
            display_search_results(results, query)
        else:
            print_error(f"Search failed for: {query}")

    # Test 4: NexBrain Chat Integration
    print_header("TEST 4: NexBrain Chat - Conversational Queries")
    chat_questions = [
        "What are the steps to establish a business in Dubai?",
        "Tell me about visa options for entrepreneurs in UAE",
        "What legal documents do I need for company formation?"
    ]

    for question in chat_questions:
        print(f"\n{Colors.CYAN}Chat query:{Colors.RESET} {question}")
        response = test_nexbrain_chat(question, tenant="uae")
        if response:
            print_success("Chat response received")
            answer = response.get('response', '')
            preview = answer[:300] + "..." if len(answer) > 300 else answer
            print(f"{Colors.BOLD}Response:{Colors.RESET}\n{preview}")

            if 'sources' in response:
                print(f"\n{Colors.BOLD}Sources used:{Colors.RESET} {len(response['sources'])}")
        else:
            print_error(f"Chat failed for: {question}")

    # Test 5: Cross-tenant isolation
    print_header("TEST 5: Tenant Isolation Test")
    print_info("Testing that UAE content is isolated from other tenants")

    # Search for UAE-specific content with different tenants
    uae_query = "Dubai free zone company formation"

    for tenant in ["uae", "icc", "andros"]:
        print(f"\n{Colors.CYAN}Searching with tenant:{Colors.RESET} {tenant}")
        results = test_rag_search(uae_query, tenant=tenant, limit=2)
        if results and results.get('results'):
            found_tenants = set(r.get('metadata', {}).get('tenant') for r in results['results'])
            print_info(f"Results from tenants: {found_tenants}")
            if tenant == "uae" and "uae" in found_tenants:
                print_success("UAE tenant correctly returns UAE content")
            elif tenant != "uae" and "uae" not in found_tenants:
                print_success(f"{tenant} tenant correctly excludes UAE content")
            else:
                print_warning(f"Unexpected tenant isolation behavior for {tenant}")

    # Summary
    print_header("📊 TEST SUMMARY")
    print_info(f"Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print_success("UAE Legal Documentation testing finished")
    print_info("Review results above for any errors or warnings")


if __name__ == "__main__":
    try:
        run_test_suite()
    except KeyboardInterrupt:
        print_warning("\n\nTest interrupted by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"\n\nTest failed with error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)