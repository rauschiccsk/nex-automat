"""
Aktualizuje __init__.py exports pre nex-shared package
"""
from pathlib import Path


def main():
    print("=" * 80)
    print("AKTUALIZÁCIA __init__.py EXPORTS")
    print("=" * 80)

    # 1. packages/nex-shared/ui/__init__.py
    ui_init = Path("packages/nex-shared/ui/__init__.py")
    ui_content = '''"""
NEX Shared UI Components
"""
from .base_window import BaseWindow
from .window_persistence import WindowPersistenceManager

__all__ = [
    'BaseWindow',
    'WindowPersistenceManager',
]
'''

    with open(ui_init, 'w', encoding='utf-8') as f:
        f.write(ui_content)
    print(f"✅ {ui_init}")

    # 2. packages/nex-shared/database/__init__.py
    db_init = Path("packages/nex-shared/database/__init__.py")
    db_content = '''"""
NEX Shared Database Components
"""
from .window_settings_db import WindowSettingsDB

__all__ = [
    'WindowSettingsDB',
]
'''

    with open(db_init, 'w', encoding='utf-8') as f:
        f.write(db_content)
    print(f"✅ {db_init}")

    # 3. packages/nex-shared/__init__.py (top-level)
    top_init = Path("packages/nex-shared/__init__.py")

    # Skontroluj či existuje
    if not top_init.exists():
        top_content = '''"""
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
        with open(top_init, 'w', encoding='utf-8') as f:
            f.write(top_content)
        print(f"✅ {top_init} (created)")
    else:
        print(f"⏭️  {top_init} (already exists)")

    print("\n" + "=" * 80)
    print("EXPORTS READY")
    print("=" * 80)

    print("\nTeraz je možné použiť:")
    print("  from nex_shared.ui import BaseWindow")
    print("  from nex_shared.database import WindowSettingsDB")

    print("\n" + "=" * 80)
    print("ĎALŠÍ KROK:")
    print("=" * 80)
    print("Test BaseWindow v samostatnom scripte")
    print("=" * 80)


if __name__ == '__main__':
    main()