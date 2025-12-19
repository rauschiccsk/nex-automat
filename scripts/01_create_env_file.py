"""
Create .env file for NEX Brain application.
"""
from pathlib import Path

# Paths
APP_DIR = Path(r"C:\Development\nex-automat\apps\nex-brain")
ENV_FILE = APP_DIR / ".env"

# .env content with defaults (can be customized per environment)
ENV_CONTENT = """# NEX Brain Configuration
# Generated: 2025-12-19

# Deployment Mode
# "multi-tenant" = one server serves multiple customers (ICC, ANDROS)
# "single-tenant" = dedicated server per customer
MODE=multi-tenant

# For single-tenant mode only
TENANT=

# For multi-tenant mode - comma-separated list
TENANTS=icc,andros

# RAG API endpoint
RAG_API_URL=https://rag-api.icc.sk

# Ollama LLM service
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b

# API Server
API_HOST=0.0.0.0
API_PORT=8001
"""


def main():
    print("=" * 60)
    print("NEX Brain - Create .env file")
    print("=" * 60)

    # Check if .env already exists
    if ENV_FILE.exists():
        print(f"\n⚠️  .env already exists: {ENV_FILE}")
        print("Current content:")
        print("-" * 40)
        print(ENV_FILE.read_text(encoding="utf-8"))
        print("-" * 40)

        response = input("\nOverwrite? (y/N): ").strip().lower()
        if response != 'y':
            print("Cancelled.")
            return

    # Create .env file
    ENV_FILE.write_text(ENV_CONTENT.strip() + "\n", encoding="utf-8")
    print(f"\n✅ Created: {ENV_FILE}")

    # Show content
    print("\nContent:")
    print("-" * 40)
    print(ENV_FILE.read_text(encoding="utf-8"))
    print("-" * 40)

    # Remind about .gitignore
    gitignore = APP_DIR / ".gitignore"
    if not gitignore.exists():
        gitignore.write_text(".env\n__pycache__/\n*.pyc\n", encoding="utf-8")
        print(f"\n✅ Created .gitignore (excludes .env)")
    elif ".env" not in gitignore.read_text():
        print(f"\n⚠️  Add '.env' to .gitignore to prevent committing secrets!")

    print("\n✅ DONE")


if __name__ == "__main__":
    main()