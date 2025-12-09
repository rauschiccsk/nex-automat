"""
Session Script 11a: Check nexdata Structure
Find correct paths for repositories
"""
from pathlib import Path


def main():
    nexdata_path = Path(r"C:\Development\nex-automat\packages\nexdata")

    print("=" * 60)
    print("Checking nexdata Structure")
    print("=" * 60)

    if not nexdata_path.exists():
        print(f"❌ {nexdata_path} does not exist")
        return 1

    print(f"\nSearching in: {nexdata_path}")
    print("\nDirectory structure:")

    # List all directories
    for item in sorted(nexdata_path.rglob("*")):
        if item.is_dir():
            rel_path = item.relative_to(nexdata_path)
            print(f"  📁 {rel_path}")

    print("\nSearching for repository files:")

    # Find repository files
    repo_files = list(nexdata_path.rglob("*repository.py"))

    if repo_files:
        print(f"\n✅ Found {len(repo_files)} repository files:")
        for f in repo_files:
            print(f"  - {f.relative_to(nexdata_path)}")
            print(f"    Full: {f}")
    else:
        print("\n❌ No repository files found")

    print("\nSearching for model files:")

    # Find model files
    model_files = list(nexdata_path.rglob("*models*.py"))

    if model_files:
        print(f"\n✅ Found {len(model_files)} model files:")
        for f in model_files:
            print(f"  - {f.relative_to(nexdata_path)}")

    print("\n" + "=" * 60)

    return 0


if __name__ == '__main__':
    import sys

    sys.exit(main())