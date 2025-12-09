"""
Script 05: Show config.py structure for debugging
"""

from pathlib import Path


def main():
    """Display config.py content"""

    dev_root = Path(r"C:\Development\nex-automat")
    config_py = dev_root / "apps" / "supplier-invoice-loader" / "src" / "utils" / "config.py"

    if not config_py.exists():
        print(f"❌ File not found: {config_py}")
        return False

    print(f"📝 Content of: {config_py}")
    print("=" * 60)

    content = config_py.read_text(encoding='utf-8')

    # Print with line numbers
    lines = content.split('\n')
    for i, line in enumerate(lines, 1):
        print(f"{i:3d}: {line}")

    print("=" * 60)
    print(f"Total lines: {len(lines)}")

    return True


if __name__ == "__main__":
    main()