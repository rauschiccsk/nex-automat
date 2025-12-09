"""
Script 08: Fix main config.py - remove incorrectly added lines
Phase 4: Integration fix
"""

from pathlib import Path


def main():
    """Remove incorrectly added NEX Genesis config from main config.py"""

    # Paths
    dev_root = Path(r"C:\Development\nex-automat")
    config_py = dev_root / "apps" / "supplier-invoice-loader" / "src" / "utils" / "config.py"

    if not config_py.exists():
        print(f"❌ File not found: {config_py}")
        return False

    print(f"📝 Reading: {config_py}")
    content = config_py.read_text(encoding='utf-8')

    # Check if incorrect lines exist
    if 'NEX_GENESIS_ENABLED' not in content:
        print("✅ Already clean - no incorrect lines found")
        return True

    # Remove lines 11-13 (the incorrectly added NEX Genesis config)
    lines = content.split('\n')
    new_lines = []

    for i, line in enumerate(lines):
        # Skip lines 11-13 (but keep checking in case line numbers changed)
        # Just skip any line that contains NEX_GENESIS config
        if 'NEX_GENESIS_ENABLED' in line or 'NEX_DATA_PATH' in line:
            print(f"Removing line {i + 1}: {line[:60]}")
            continue
        # Also skip the comment before if it exists
        if '# NEX Genesis Integration' in line:
            print(f"Removing line {i + 1}: {line[:60]}")
            continue

        new_lines.append(line)

    content = '\n'.join(new_lines)

    # Write cleaned content
    print(f"💾 Writing cleaned file...")
    config_py.write_text(content, encoding='utf-8')

    print("✅ SUCCESS: config.py cleaned")
    print("   Removed incorrectly placed NEX Genesis config")
    print("   Config now properly imports from config_customer.py")

    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)