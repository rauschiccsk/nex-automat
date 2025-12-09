"""
Script 02: Add NEX Genesis configuration to config.py
Phase 4: Integration
"""

from pathlib import Path

def main():
    """Add NEX Genesis configuration parameters"""

    # Paths
    dev_root = Path(r"C:\Development\nex-automat")
    config_py = dev_root / "apps" / "supplier-invoice-loader" / "src" / "utils" / "config.py"

    if not config_py.exists():
        print(f"❌ File not found: {config_py}")
        return False

    print(f"📝 Reading: {config_py}")
    content = config_py.read_text(encoding='utf-8')

    # Check if already modified
    if 'NEX_GENESIS_ENABLED' in content:
        print("⚠️  NEX Genesis config already exists - skipping")
        return True

    # Find the end of class Config (before the last line or before config = Config())
    # Add NEX Genesis settings before the end of class

    # Look for "config = Config()" or end of class
    nex_config = '''
    # NEX Genesis Integration
    NEX_GENESIS_ENABLED: bool = os.getenv('NEX_GENESIS_ENABLED', 'true').lower() == 'true'
    NEX_DATA_PATH: str = os.getenv('NEX_DATA_PATH', 'C:/NEX/YEARACT/STORES')
'''

    # Find last attribute in Config class and add after it
    # Look for the last line before "config = Config()" or before end of file

    if 'config = Config()' in content:
        # Add before config = Config()
        config_instance = '\nconfig = Config()'
        content = content.replace(config_instance, nex_config + config_instance)
    else:
        # Add at the end of file
        content += nex_config + '\n\nconfig = Config()\n'

    # Write modified content
    print(f"💾 Writing modified file...")
    config_py.write_text(content, encoding='utf-8')

    print("✅ SUCCESS: config.py modified with NEX Genesis settings")
    print("\nAdded configuration:")
    print("  - NEX_GENESIS_ENABLED (default: true)")
    print("  - NEX_DATA_PATH (default: C:/NEX/YEARACT/STORES)")

    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)