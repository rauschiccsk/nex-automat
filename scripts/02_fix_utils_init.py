#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Fix Script: Oprava nex-shared/utils/__init__.py
GridSettings trieda neexistuje - importovať len clean_string a grid funkcie
"""
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).parent
DEV_ROOT = SCRIPT_DIR.parent
NEX_SHARED = DEV_ROOT / "packages" / "nex-shared"

print("="*80)
print("Fix Script: Oprava utils/__init__.py")
print("="*80)

# Fix utils/__init__.py - importovať len existujúce funkcie
utils_init = NEX_SHARED / "utils" / "__init__.py"

utils_init_content = '''"""NEX Shared - Utils Package"""
from .text_utils import clean_string
from .grid_settings import (
    get_grid_settings_db_path,
    init_grid_settings_db,
    get_current_user_id,
    load_column_settings,
    save_column_settings,
    load_grid_settings,
    save_grid_settings
)

__all__ = [
    'clean_string',
    'get_grid_settings_db_path',
    'init_grid_settings_db',
    'get_current_user_id',
    'load_column_settings',
    'save_column_settings',
    'load_grid_settings',
    'save_grid_settings'
]
'''

utils_init.write_text(utils_init_content, encoding='utf-8')
print(f"✅ Fixed: {utils_init}")

print("\n" + "="*80)
print("✅ Fix Complete!")
print("="*80)
print("\nNext steps:")
print("  1. cd packages\\nex-shared")
print("  2. pip install -e .")
print("  3. cd ..\\..\\apps\\supplier-invoice-loader")
print("  4. python main.py")
print("="*80)