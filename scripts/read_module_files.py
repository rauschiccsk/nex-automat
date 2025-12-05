#!/usr/bin/env python3
"""
Read Module Files - Batch File Loading
=======================================

Location: scripts/read_module_files.py

Načíta viacero súborov naraz (celý modul, package, alebo custom list).

Usage:
    # Load entire module
    python scripts/read_module_files.py --module ui/widgets

    # Load specific files
    python scripts/read_module_files.py file1.py file2.py file3.py

    # Load from manifest pattern
    python scripts/read_module_files.py --pattern "*/invoice_*.py"
"""

import sys
from pathlib import Path
import json
from typing import List, Dict

PROJECT_ROOT = Path(__file__).parent.parent


def find_files_by_pattern(pattern: str) -> List[Path]:
    """Nájde súbory podľa glob pattern."""
    return list(PROJECT_ROOT.glob(pattern))


def find_files_in_module(module_path: str) -> List[Path]:
    """Nájde všetky Python súbory v module."""
    module_dir = PROJECT_ROOT / module_path

    if not module_dir.exists():
        return []

    return list(module_dir.rglob("*.py"))


def read_file_safe(file_path: Path) -> Dict:
    """Načíta súbor bezpečne."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        return {
            "success": True,
            "path": str(file_path),
            "relative_path": str(file_path.relative_to(PROJECT_ROOT)),
            "content": content,
            "lines": len(content.splitlines()),
            "size": file_path.stat().st_size
        }
    except Exception as e:
        return {
            "success": False,
            "path": str(file_path),
            "error": str(e)
        }


def main():
    """Main entry point."""

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python scripts/read_module_files.py --module <module_path>")
        print("  python scripts/read_module_files.py --pattern <glob_pattern>")
        print("  python scripts/read_module_files.py <file1> <file2> ...")
        sys.exit(1)

    # Parse arguments
    files_to_read = []

    if sys.argv[1] == "--module":
        module_path = sys.argv[2]
        files_to_read = find_files_in_module(module_path)
        print(f"Loading module: {module_path}")

    elif sys.argv[1] == "--pattern":
        pattern = sys.argv[2]
        files_to_read = find_files_by_pattern(pattern)
        print(f"Loading pattern: {pattern}")

    else:
        # Direct file paths
        files_to_read = [PROJECT_ROOT / path for path in sys.argv[1:]]

    # Read all files
    results = []

    print(f"\nFound {len(files_to_read)} files")
    print("=" * 80)

    for file_path in files_to_read:
        result = read_file_safe(file_path)
        results.append(result)

        if result["success"]:
            print(f"\n✅ {result['relative_path']}")
            print(f"   Lines: {result['lines']}, Size: {result['size']} bytes")
            print(f"\n{'-' * 80}")
            print(result['content'])
            print(f"{'-' * 80}")
        else:
            print(f"\n❌ {result['path']}")
            print(f"   Error: {result['error']}")

    print("\n" + "=" * 80)
    print(f"Total: {len(results)} files")
    print(f"Success: {sum(1 for r in results if r['success'])}")
    print(f"Failed: {sum(1 for r in results if not r['success'])}")
    print("=" * 80)


if __name__ == "__main__":
    main()