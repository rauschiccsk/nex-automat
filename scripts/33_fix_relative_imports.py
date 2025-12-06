"""
Zmení relative imports na absolute v nex-shared moduloch
"""
from pathlib import Path


def fix_file(filepath, replacements):
    """Fix imports v súbore."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    changed = False
    for old, new in replacements.items():
        if old in content:
            content = content.replace(old, new)
            changed = True
            print(f"  ✅ {old} → {new}")

    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def main():
    print("=" * 80)
    print("FIX: Relative imports → Absolute imports")
    print("=" * 80)

    # 1. base_window.py
    base_window = Path("packages/nex-shared/ui/base_window.py")
    print(f"\n1. {base_window}")
    replacements = {
        'from ..database.window_settings_db import WindowSettingsDB':
            'from database.window_settings_db import WindowSettingsDB',
        'from .window_persistence import WindowPersistenceManager':
            'from ui.window_persistence import WindowPersistenceManager',
    }
    fix_file(base_window, replacements)

    # 2. ui/__init__.py
    ui_init = Path("packages/nex-shared/ui/__init__.py")
    print(f"\n2. {ui_init}")
    replacements = {
        'from .base_window import BaseWindow':
            'from ui.base_window import BaseWindow',
        'from .window_persistence import WindowPersistenceManager':
            'from ui.window_persistence import WindowPersistenceManager',
    }
    fix_file(ui_init, replacements)

    # 3. database/__init__.py
    db_init = Path("packages/nex-shared/database/__init__.py")
    print(f"\n3. {db_init}")
    replacements = {
        'from .window_settings_db import WindowSettingsDB':
            'from database.window_settings_db import WindowSettingsDB',
    }
    fix_file(db_init, replacements)

    # 4. top-level __init__.py
    top_init = Path("packages/nex-shared/__init__.py")
    print(f"\n4. {top_init}")
    replacements = {
        'from .ui import BaseWindow, WindowPersistenceManager':
            'from ui import BaseWindow, WindowPersistenceManager',
        'from .database import WindowSettingsDB':
            'from database import WindowSettingsDB',
    }
    fix_file(top_init, replacements)

    print("\n" + "=" * 80)
    print("HOTOVO")
    print("=" * 80)
    print("Všetky relative imports zmenené na absolute")

    print("\n" + "=" * 80)
    print("TEST:")
    print("=" * 80)
    print("python scripts\\32_diagnose_basewindow_import.py")
    print("  → Import MUSÍ byť úspešný ✅")
    print("=" * 80)


if __name__ == '__main__':
    main()