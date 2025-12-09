"""
Session Script 16: Check NEX Genesis Files
List Btrieve .BTR files in NEX directory
"""
from pathlib import Path


def main():
    nex_path = Path(r"C:\NEX\YEARACT\STORES")

    print("=" * 60)
    print("Checking NEX Genesis Files")
    print("=" * 60)

    if not nex_path.exists():
        print(f"❌ Path does not exist: {nex_path}")
        return 1

    print(f"\nListing files in: {nex_path}\n")

    # List .BTR files
    btr_files = list(nex_path.glob("*.BTR"))

    if btr_files:
        print(f"✅ Found {len(btr_files)} .BTR files:")
        for f in sorted(btr_files):
            size_mb = f.stat().st_size / (1024 * 1024)
            print(f"   {f.name:20s} {size_mb:8.2f} MB")
    else:
        print("❌ No .BTR files found")

    # Check specific files
    print("\n" + "=" * 60)
    print("Checking specific files:")
    print("=" * 60)

    files_to_check = [
        'GSCAT.BTR',
        'BARCODE.BTR',
        'MGLST.BTR',
    ]

    for filename in files_to_check:
        filepath = nex_path / filename
        if filepath.exists():
            size_mb = filepath.stat().st_size / (1024 * 1024)
            print(f"✅ {filename:20s} {size_mb:8.2f} MB")
        else:
            print(f"❌ {filename:20s} NOT FOUND")

    # Check how repositories reference table names
    print("\n" + "=" * 60)
    print("Checking repository table names:")
    print("=" * 60)

    nexdata_path = Path(r"C:\Development\nex-automat\packages\nexdata\nexdata")

    repos = [
        ('gscat_repository.py', 'GSCATRepository'),
        ('barcode_repository.py', 'BARCODERepository'),
    ]

    for repo_file, repo_name in repos:
        repo_path = nexdata_path / "repositories" / repo_file

        if repo_path.exists():
            with open(repo_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

                for i, line in enumerate(lines):
                    if 'table_name' in line and 'def' in line:
                        print(f"\n{repo_name}.table_name:")
                        for j in range(5):
                            if i + j < len(lines):
                                print(f"  {lines[i + j].rstrip()}")
                        break

    print("\n" + "=" * 60)

    return 0


if __name__ == '__main__':
    import sys

    sys.exit(main())