#!/usr/bin/env python3
"""
Script 01: Setup tools/setup/ directory structure
Session: RAG Implementation Phase 2
Creates directory and saves create_venv.py utility

Location: scripts/01_setup_tools_setup_dir.py
"""

import sys
from pathlib import Path


def main():
    print("=== Script 01: Setting up tools/setup/ directory ===\n")

    # Define paths
    project_root = Path("C:/Development/nex-automat")
    tools_dir = project_root / "tools"
    setup_dir = tools_dir / "setup"

    # Create directories
    print(f"1. Creating directory: {setup_dir}")
    setup_dir.mkdir(parents=True, exist_ok=True)
    print(f"   ✓ Created: {setup_dir}\n")

    # Create __init__.py
    print(f"2. Creating __init__.py")
    init_file = setup_dir / "__init__.py"
    init_file.write_text('"""Setup utilities for NEX Automat project"""\n')
    print(f"   ✓ Created: {init_file}\n")

    # Instructions
    print("3. Next steps:")
    print("   - Save create_venv.py artifact to: tools/setup/create_venv.py")
    print("   - Run: python tools/setup/create_venv.py")
    print("\n✓ Script 01 complete")

    return 0


if __name__ == "__main__":
    sys.exit(main())