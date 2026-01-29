"""
Install FastAPI and uvicorn dependencies for RAG API server.
"""

import subprocess
import sys


def install_dependencies():
    """Install FastAPI and uvicorn."""
    print("=" * 60)
    print("Installing RAG API Server Dependencies")
    print("=" * 60)

    dependencies = ["fastapi>=0.104.0", "uvicorn[standard]>=0.24.0"]

    for dep in dependencies:
        print(f"\nInstalling {dep}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            print(f"[OK] {dep} installed")
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Failed to install {dep}: {e}")
            return False

    print("\n" + "=" * 60)
    print("[OK] All dependencies installed successfully")
    print("=" * 60)
    print("\nYou can now start the RAG API server:")
    print("  python -m tools.rag.server start")
    print("\nOr check the status:")
    print("  python -m tools.rag.server status")

    return True


if __name__ == "__main__":
    success = install_dependencies()
    sys.exit(0 if success else 1)
