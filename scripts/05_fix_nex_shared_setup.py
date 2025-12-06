"""
Fix: Oprava nex-shared package - pridať utils do setup.py a opraviť importy
Location: C:\Development\nex-automat\scripts\05_fix_nex_shared_setup.py
"""
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).parent
DEV_ROOT = SCRIPT_DIR.parent
NEX_SHARED = DEV_ROOT / "packages" / "nex-shared"
SETUP_PY = NEX_SHARED / "setup.py"
INIT_PY = NEX_SHARED / "__init__.py"


def fix_setup_py():
    """Pridaj utils do packages v setup.py"""

    print("=" * 80)
    print("FIX: setup.py - pridať nex_shared.utils")
    print("=" * 80)

    with open(SETUP_PY, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find and replace packages section
    old_packages = """    packages=[
        'nex_shared.ui',
        'nex_shared.database',
    ],"""

    new_packages = """    packages=[
        'nex_shared.ui',
        'nex_shared.database',
        'nex_shared.utils',
    ],"""

    if old_packages in content:
        content = content.replace(old_packages, new_packages)
        print("\n✓ Pridané: 'nex_shared.utils' do packages")
    else:
        print("\n❌ Nenašiel som očakávaný packages block!")
        print("Kontrolujem manuálne...")
        return False

    # Add utils to package_data
    old_data = """    package_data={
        'nex_shared.ui': ['*.py'],
        'nex_shared.database': ['*.py'],
    },"""

    new_data = """    package_data={
        'nex_shared.ui': ['*.py'],
        'nex_shared.database': ['*.py'],
        'nex_shared.utils': ['*.py'],
    },"""

    if old_data in content:
        content = content.replace(old_data, new_data)
        print("✓ Pridané: 'nex_shared.utils' do package_data")

    # Write back
    with open(SETUP_PY, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✓ Uložené: {SETUP_PY.relative_to(DEV_ROOT)}")
    return True


def fix_init_py():
    """Oprav importy v hlavnom __init__.py"""

    print("\n" + "=" * 80)
    print("FIX: __init__.py - oprava importov")
    print("=" * 80)

    new_content = '''"""
NEX Shared Package
Zdieľané komponenty pre NEX Automat systém.
"""
from .ui import BaseWindow, WindowPersistenceManager
from .database import WindowSettingsDB

__version__ = '2.0.0'

__all__ = [
    'BaseWindow',
    'WindowPersistenceManager',
    'WindowSettingsDB',
]
'''

    with open(INIT_PY, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"\n✓ Opravené importy: from ui -> from .ui")
    print(f"✓ Uložené: {INIT_PY.relative_to(DEV_ROOT)}")


def main():
    """Oprav setup.py aj __init__.py"""

    if not fix_setup_py():
        return

    fix_init_py()

    print("\n" + "=" * 80)
    print("HOTOVO - Teraz preinštaluj package")
    print("=" * 80)

    print("\nSpusť:")
    print("  cd packages\\nex-shared")
    print("  pip install -e .")
    print("\nPotom testuj aplikáciu")


if __name__ == "__main__":
    main()