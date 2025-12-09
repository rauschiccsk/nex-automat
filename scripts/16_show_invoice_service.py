"""
Script 16: Show invoice_service.py - find where items are loaded
"""

from pathlib import Path


def main():
    """Display invoice_service.py"""

    dev_root = Path(r"C:\Development\nex-automat")
    service_file = dev_root / "apps" / "supplier-invoice-editor" / "src" / "business" / "invoice_service.py"

    if not service_file.exists():
        print(f"❌ File not found: {service_file}")
        return False

    print(f"📝 Content of: {service_file.relative_to(dev_root)}")
    print("=" * 60)

    content = service_file.read_text(encoding='utf-8')
    lines = content.split('\n')

    for i, line in enumerate(lines, 1):
        print(f"{i:3d}: {line}")

    print("=" * 60)
    print(f"Total lines: {len(lines)}")

    return True


if __name__ == "__main__":
    main()