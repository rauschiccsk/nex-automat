"""
Script 06: Find and show config template/customer files
"""

from pathlib import Path


def main():
    """Find config files"""

    dev_root = Path(r"C:\Development\nex-automat")
    config_dir = dev_root / "apps" / "supplier-invoice-loader" / "config"

    print(f"📁 Config directory: {config_dir}")
    print("=" * 60)

    if not config_dir.exists():
        print(f"❌ Config directory not found")
        return False

    # List all files
    print("\n📄 Files in config directory:")
    for file in sorted(config_dir.iterdir()):
        print(f"  - {file.name}")

    # Show config_template.py
    template_file = config_dir / "config_template.py"
    if template_file.exists():
        print(f"\n📝 Content of config_template.py:")
        print("=" * 60)
        content = template_file.read_text(encoding='utf-8')
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            print(f"{i:3d}: {line}")
        print("=" * 60)
    else:
        print(f"\n❌ config_template.py not found")

    # Check config_customer.py
    customer_file = config_dir / "config_customer.py"
    if customer_file.exists():
        print(f"\n📝 Content of config_customer.py:")
        print("=" * 60)
        content = customer_file.read_text(encoding='utf-8')
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            print(f"{i:3d}: {line}")
        print("=" * 60)
    else:
        print(f"\n⚠️  config_customer.py not found (using template)")

    return True


if __name__ == "__main__":
    main()