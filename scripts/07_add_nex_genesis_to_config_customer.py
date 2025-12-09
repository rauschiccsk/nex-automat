"""
Script 07: Add NEX Genesis configuration to config_customer.py
Phase 4: Integration fix
"""

from pathlib import Path

def main():
    """Add NEX Genesis enrichment config to config_customer.py"""

    # Paths
    dev_root = Path(r"C:\Development\nex-automat")
    config_customer = dev_root / "apps" / "supplier-invoice-loader" / "config" / "config_customer.py"

    if not config_customer.exists():
        print(f"❌ File not found: {config_customer}")
        return False

    print(f"📝 Reading: {config_customer}")
    content = config_customer.read_text(encoding='utf-8')

    # Check if already added
    if 'NEX_GENESIS_ENABLED' in content:
        print("⚠️  NEX Genesis config already exists - skipping")
        return True

    # Add NEX Genesis config after NEX_GENESIS_API_KEY section (line 20)
    # Insert after line with NEX_GENESIS_API_KEY

    nex_config = r'''
# NEX Genesis Product Enrichment (v2.4)
NEX_GENESIS_ENABLED = True  # Enable automatic product enrichment
NEX_DATA_PATH = r"C:\NEX\YEARACT\STORES"  # Path to NEX Genesis Btrieve database
'''

    # Find the line with NEX_GENESIS_API_KEY and insert after it
    lines = content.split('\n')
    new_lines = []
    inserted = False

    for i, line in enumerate(lines):
        new_lines.append(line)

        # Insert after NEX_GENESIS_API_KEY line
        if 'NEX_GENESIS_API_KEY' in line and not inserted:
            new_lines.append('')
            for config_line in nex_config.strip().split('\n'):
                new_lines.append(config_line)
            inserted = True

    if not inserted:
        print("❌ Could not find insertion point (NEX_GENESIS_API_KEY)")
        return False

    content = '\n'.join(new_lines)

    # Write modified content
    print(f"💾 Writing modified file...")
    config_customer.write_text(content, encoding='utf-8')

    print("✅ SUCCESS: config_customer.py updated with NEX Genesis enrichment config")
    print("\nAdded configuration:")
    print("  - NEX_GENESIS_ENABLED = True")
    print("  - NEX_DATA_PATH = C:\\NEX\\YEARACT\\STORES")

    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)