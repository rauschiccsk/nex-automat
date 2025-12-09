"""
Session Script 15c: Check BtrieveClient Usage
How is BtrieveClient initialized in existing code?
"""
from pathlib import Path


def main():
    nexdata_path = Path(r"C:\Development\nex-automat\packages\nexdata\nexdata")

    print("=" * 60)
    print("Checking BtrieveClient Usage")
    print("=" * 60)

    # 1. Check BtrieveClient __init__
    btrieve_client = nexdata_path / "btrieve" / "btrieve_client.py"

    print("\n[1] BtrieveClient.__init__ signature:")
    with open(btrieve_client, 'r', encoding='utf-8') as f:
        lines = f.readlines()

        for i, line in enumerate(lines):
            if 'def __init__' in line:
                # Show next 15 lines
                for j in range(15):
                    if i + j < len(lines):
                        print(f"{i + j + 1:3d}: {lines[i + j].rstrip()}")
                break

    # 2. Check how repositories create BtrieveClient
    print("\n" + "=" * 60)
    print("[2] How do repositories initialize?")
    print("=" * 60)

    base_repo = nexdata_path / "repositories" / "base_repository.py"

    with open(base_repo, 'r', encoding='utf-8') as f:
        lines = f.readlines()

        for i, line in enumerate(lines):
            if 'def __init__' in line:
                print("\nBaseRepository.__init__:")
                for j in range(10):
                    if i + j < len(lines):
                        print(f"{i + j + 1:3d}: {lines[i + j].rstrip()}")
                break

    # 3. Check example usage in tests or apps
    print("\n" + "=" * 60)
    print("[3] Searching for BtrieveClient() usage examples...")
    print("=" * 60)

    root = Path(r"C:\Development\nex-automat")

    for py_file in root.rglob("*.py"):
        if 'test' in str(py_file).lower() or 'example' in str(py_file).lower():
            with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

                if 'BtrieveClient(' in content:
                    print(f"\n✅ Found in: {py_file.relative_to(root)}")

                    # Show the line
                    for line in content.split('\n'):
                        if 'BtrieveClient(' in line:
                            print(f"   {line.strip()}")

    print("\n" + "=" * 60)

    return 0


if __name__ == '__main__':
    import sys

    sys.exit(main())