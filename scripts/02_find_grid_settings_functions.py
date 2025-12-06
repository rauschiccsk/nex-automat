"""
Find: Hľadá funkcie pre grid settings v nex-automat projekte
Hľadáme: load_column_settings, save_column_settings, load_grid_settings, save_grid_settings
Location: C:\Development\nex-automat\scripts\02_find_grid_settings_functions.py
"""
from pathlib import Path
import re

# Paths
SCRIPT_DIR = Path(__file__).parent
DEV_ROOT = SCRIPT_DIR.parent

# Functions to find
FUNCTIONS = [
    "load_column_settings",
    "save_column_settings",
    "load_grid_settings",
    "save_grid_settings"
]


def find_functions():
    """Nájdi všetky Python súbory obsahujúce grid settings funkcie"""

    print("=" * 80)
    print("HĽADÁM GRID SETTINGS FUNKCIE")
    print("=" * 80)

    results = {}

    # Hľadaj v celom projekte
    for py_file in DEV_ROOT.rglob("*.py"):
        # Skip venv a cache
        if any(skip in str(py_file) for skip in ['.venv', 'venv32', '__pycache__', '.git']):
            continue

        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Hľadaj každú funkciu
            for func_name in FUNCTIONS:
                # Pattern pre def funkcie
                pattern = rf'^def {func_name}\s*\('
                if re.search(pattern, content, re.MULTILINE):
                    if func_name not in results:
                        results[func_name] = []
                    results[func_name].append(py_file)

        except Exception as e:
            pass

    # Výpis výsledkov
    if not results:
        print("\n❌ NENAŠIEL SOM ŽIADNE FUNKCIE!\n")
        return

    for func_name in FUNCTIONS:
        print(f"\n{'=' * 80}")
        print(f"Funkcia: {func_name}")
        print(f"{'=' * 80}")

        if func_name in results:
            for file_path in results[func_name]:
                rel_path = file_path.relative_to(DEV_ROOT)
                print(f"  ✓ {rel_path}")

                # Ukáž import path
                if "packages" in str(rel_path):
                    parts = rel_path.parts
                    if parts[0] == "packages":
                        pkg_name = parts[1]
                        # Remove .py and convert path to import
                        module_parts = list(parts[2:-1]) + [parts[-1].replace('.py', '')]
                        import_path = '.'.join(module_parts)
                        print(f"    Import: from {pkg_name}.{import_path} import {func_name}")

                elif "apps" in str(rel_path):
                    parts = rel_path.parts
                    if parts[0] == "apps":
                        app_name = parts[1]
                        # Skip apps, app_name, src
                        module_parts = list(parts[3:-1]) + [parts[-1].replace('.py', '')]
                        import_path = '.'.join(module_parts)
                        print(f"    Import: from {import_path} import {func_name}")
        else:
            print(f"  ❌ NENAŠIEL SOM")

    print(f"\n{'=' * 80}\n")


if __name__ == "__main__":
    find_functions()