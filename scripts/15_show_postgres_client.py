"""
Script 15: Show postgres_client.py structure
"""

from pathlib import Path


def main():
    """Display postgres_client.py"""

    dev_root = Path(r"C:\Development\nex-automat")
    postgres_file = dev_root / "apps" / "supplier-invoice-editor" / "src" / "database" / "postgres_client.py"

    if not postgres_file.exists():
        print(f"❌ File not found: {postgres_file}")
        return False

    print(f"📝 Content of: {postgres_file.relative_to(dev_root)}")
    print("=" * 60)

    content = postgres_file.read_text(encoding='utf-8')
    lines = content.split('\n')

    for i, line in enumerate(lines, 1):
        print(f"{i:3d}: {line}")

    print("=" * 60)
    print(f"Total lines: {len(lines)}")

    return True


if __name__ == "__main__":
    main()