"""
Session Script 15a: Find BtrieveClient Location
Find correct import path for BtrieveClient
"""
from pathlib import Path


def main():
    nexdata_path = Path(r"C:\Development\nex-automat\packages\nexdata")

    print("=" * 60)
    print("Finding BtrieveClient")
    print("=" * 60)

    print("\nSearching for BtrieveClient class...")

    # Search in all Python files
    for py_file in nexdata_path.rglob("*.py"):
        with open(py_file, 'r', encoding='utf-8') as f:
            content = f.read()

            if 'class BtrieveClient' in content:
                rel_path = py_file.relative_to(nexdata_path)
                print(f"\n✅ Found in: {rel_path}")
                print(f"   Full path: {py_file}")

                # Show import statement
                import_parts = list(rel_path.parts)
                import_parts[-1] = import_parts[-1].replace('.py', '')
                import_path = '.'.join(import_parts)
                print(f"   Import: from {import_path} import BtrieveClient")

    print("\n" + "=" * 60)
    print("Checking existing repository imports...")
    print("=" * 60)

    # Check how repositories import btrieve
    gscat_repo = nexdata_path / "nexdata" / "repositories" / "gscat_repository.py"

    if gscat_repo.exists():
        with open(gscat_repo, 'r', encoding='utf-8') as f:
            lines = f.readlines()

            print("\nImports in gscat_repository.py:")
            for line in lines[:20]:  # First 20 lines
                if 'import' in line:
                    print(f"  {line.strip()}")

    print("\n" + "=" * 60)

    return 0


if __name__ == '__main__':
    import sys

    sys.exit(main())