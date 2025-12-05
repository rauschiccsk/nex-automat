#!/usr/bin/env python3
"""
Read Project File - Local File Access for Claude
=================================================

Location: scripts/read_project_file.py

Načíta lokálny súbor z projektu a vypíše jeho obsah.
Používa sa keď Claude potrebuje vidieť aktuálny (uncommitted) stav súboru.

Usage:
    python scripts/read_project_file.py <relative_path>

Examples:
    python scripts/read_project_file.py apps/supplier-invoice-editor/src/ui/main_window.py
    python scripts/read_project_file.py apps/supplier-invoice-editor/config/config.yaml
"""

import sys
from pathlib import Path
import json

# Project root
PROJECT_ROOT = Path(__file__).parent.parent


def read_file(relative_path: str) -> dict:
    """
    Načíta súbor z projektu.

    Args:
        relative_path: Relatívna cesta od project root

    Returns:
        Dict s informáciami o súbore a jeho obsahom
    """
    file_path = PROJECT_ROOT / relative_path

    result = {
        "success": False,
        "path": str(file_path),
        "relative_path": relative_path,
        "exists": False,
        "content": None,
        "error": None,
        "metadata": {}
    }

    # Check existence
    if not file_path.exists():
        result["error"] = f"File does not exist: {file_path}"
        return result

    result["exists"] = True

    # Get metadata
    stat = file_path.stat()
    result["metadata"] = {
        "size_bytes": stat.st_size,
        "extension": file_path.suffix,
        "name": file_path.name
    }

    # Read content
    try:
        # Try UTF-8 first
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        result["content"] = content
        result["metadata"]["lines"] = len(content.splitlines())
        result["metadata"]["encoding"] = "utf-8"
        result["success"] = True

    except UnicodeDecodeError:
        # Try with different encoding
        try:
            with open(file_path, 'r', encoding='latin-1') as f:
                content = f.read()

            result["content"] = content
            result["metadata"]["lines"] = len(content.splitlines())
            result["metadata"]["encoding"] = "latin-1"
            result["success"] = True

        except Exception as e:
            result["error"] = f"Failed to read file: {e}"

    except Exception as e:
        result["error"] = f"Failed to read file: {e}"

    return result


def print_result(result: dict, verbose: bool = True):
    """Vypíše výsledok v čitateľnom formáte."""

    print("=" * 80)
    print("READ PROJECT FILE")
    print("=" * 80)

    print(f"\nFile: {result['relative_path']}")
    print(f"Path: {result['path']}")

    if not result["exists"]:
        print(f"\n❌ ERROR: {result['error']}")
        return

    if not result["success"]:
        print(f"\n❌ ERROR: {result['error']}")
        return

    # Metadata
    meta = result["metadata"]
    print(f"\n✅ File loaded successfully")
    print(f"   Size: {meta['size_bytes']:,} bytes")
    print(f"   Lines: {meta.get('lines', 'N/A')}")
    print(f"   Encoding: {meta.get('encoding', 'N/A')}")

    # Content
    if verbose:
        print("\n" + "-" * 80)
        print("CONTENT:")
        print("-" * 80)
        print(result["content"])
        print("-" * 80)
    else:
        # Just first 10 lines
        lines = result["content"].splitlines()
        print("\n" + "-" * 80)
        print(f"CONTENT (first 10 lines of {len(lines)}):")
        print("-" * 80)
        for line in lines[:10]:
            print(line)
        if len(lines) > 10:
            print(f"... ({len(lines) - 10} more lines)")
        print("-" * 80)

    print("\n" + "=" * 80)


def main():
    """Main entry point."""

    if len(sys.argv) < 2:
        print("Usage: python scripts/read_project_file.py <relative_path>")
        print("\nExamples:")
        print("  python scripts/read_project_file.py apps/supplier-invoice-editor/src/ui/main_window.py")
        print("  python scripts/read_project_file.py apps/supplier-invoice-editor/config/config.yaml")
        sys.exit(1)

    relative_path = sys.argv[1]

    # Check for flags
    verbose = "--verbose" in sys.argv or "-v" in sys.argv
    json_output = "--json" in sys.argv

    # Read file
    result = read_file(relative_path)

    # Output
    if json_output:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print_result(result, verbose=verbose)

    # Exit code
    sys.exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()