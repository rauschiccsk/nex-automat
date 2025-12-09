"""
Script 09: Show current config.py state
"""

from pathlib import Path


def main():
    """Display current config.py"""

    dev_root = Path(r"C:\Development\nex-automat")
    config_py = dev_root / "apps" / "supplier-invoice-loader" / "src" / "utils" / "config.py"

    print(f"📝 Current content of: {config_py}")
    print("=" * 60)

    content = config_py.read_text(encoding='utf-8')
    lines = content.split('\n')
    for i, line in enumerate(lines, 1):
        print(f"{i:3d}: {line}")

    print("=" * 60)

    return True


if __name__ == "__main__":
    main()