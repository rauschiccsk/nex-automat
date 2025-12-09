"""
Script 10: Fix config.py - create config wrapper object
Phase 4: Integration fix
"""

from pathlib import Path


def main():
    """Fix config.py to create config object from imported variables"""

    dev_root = Path(r"C:\Development\nex-automat")
    config_py = dev_root / "apps" / "supplier-invoice-loader" / "src" / "utils" / "config.py"

    if not config_py.exists():
        print(f"❌ File not found: {config_py}")
        return False

    print(f"📝 Reading: {config_py}")
    content = config_py.read_text(encoding='utf-8')

    # Replace config = Config() with proper wrapper
    new_config = '''# -*- coding: utf-8 -*-
"""
Supplier Invoice Loader - Configuration Loader
"""

try:
    from config.config_customer import *
except ImportError:
    print("WARNING: config_customer.py not found, using template")
    from config.config_template import *


# Create config object from imported variables
class _Config:
    """Config wrapper to convert module variables into object attributes"""
    def __init__(self):
        # Import all variables from current module
        import sys
        current_module = sys.modules[__name__]
        for name in dir(current_module):
            if not name.startswith('_') and name != 'Config':
                setattr(self, name, getattr(current_module, name))

config = _Config()
'''

    # Write new content
    print(f"💾 Writing fixed config.py...")
    config_py.write_text(new_config, encoding='utf-8')

    print("✅ SUCCESS: config.py fixed with wrapper object")
    print("   Config now creates object from imported variables")

    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)