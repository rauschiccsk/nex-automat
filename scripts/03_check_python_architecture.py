#!/usr/bin/env python3
"""
Script 03: Check Python Architecture
Session: RAG Implementation Phase 2

Checks if Python is 32-bit or 64-bit
Location: scripts/03_check_python_architecture.py
"""

import sys
import platform
from pathlib import Path


def print_header(text):
    """Print formatted header"""
    print(f"\n{'=' * 60}")
    print(f"  {text}")
    print(f"{'=' * 60}\n")


def main():
    print_header("Python Architecture Check")

    # Python version
    print(f"Python version: {sys.version}")
    print()

    # Architecture
    arch = platform.architecture()[0]
    machine = platform.machine()

    print(f"Architecture: {arch}")
    print(f"Machine type: {machine}")
    print(f"Executable: {sys.executable}")
    print()

    # Determine if 32-bit or 64-bit
    if arch == "64bit" or machine in ["AMD64", "x86_64"]:
        print("✓ This is 64-bit Python")
        print("\n✓ SUITABLE for RAG (sentence-transformers + torch)")
        result = 0
    elif arch == "32bit" or machine == "x86":
        print("⚠ This is 32-bit Python")
        print("\n✗ NOT RECOMMENDED for RAG")
        print("\nRAG requires 64-bit Python for:")
        print("  - sentence-transformers")
        print("  - torch (PyTorch)")
        print("  - Better performance")
        print("\nRecommendation: Install 64-bit Python and recreate venv")
        result = 1
    else:
        print(f"⚠ Unknown architecture: {arch}")
        result = 2

    print_header("Check Complete")

    return result


if __name__ == "__main__":
    sys.exit(main())