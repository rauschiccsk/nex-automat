"""
Vytvorí folder štruktúru pre nex-shared UI package
"""
from pathlib import Path

BASE_PATH = Path("packages/nex-shared")


def main():
    print("=" * 80)
    print("VYTVORENIE NEX-SHARED UI ŠTRUKTÚRY")
    print("=" * 80)

    # Definícia štruktúry
    folders = [
        BASE_PATH / "ui",
        BASE_PATH / "database",
        BASE_PATH / "utils",
    ]

    files = [
        BASE_PATH / "ui" / "__init__.py",
        BASE_PATH / "ui" / "base_window.py",
        BASE_PATH / "ui" / "window_persistence.py",
        BASE_PATH / "database" / "__init__.py",
        BASE_PATH / "database" / "window_settings_db.py",
        BASE_PATH / "utils" / "__init__.py",
        BASE_PATH / "utils" / "monitor_utils.py",
    ]

    # Vytvor folders
    print("\n📁 Vytváram foldery:")
    for folder in folders:
        folder.mkdir(parents=True, exist_ok=True)
        print(f"  ✅ {folder}")

    # Vytvor prázdne súbory ak neexistujú
    print("\n📄 Vytváram súbory:")
    for file in files:
        if not file.exists():
            file.touch()
            print(f"  ✅ {file}")
        else:
            print(f"  ⏭️  {file} (už existuje)")

    print("\n" + "=" * 80)
    print("ŠTRUKTÚRA VYTVORENÁ")
    print("=" * 80)
    print("\nVýsledná štruktúra:")
    print("""
packages/nex-shared/
├── ui/
│   ├── __init__.py
│   ├── base_window.py
│   └── window_persistence.py
├── database/
│   ├── __init__.py
│   └── window_settings_db.py
└── utils/
    ├── __init__.py
    └── monitor_utils.py
""")

    print("\n" + "=" * 80)
    print("ĎALŠÍ KROK:")
    print("=" * 80)
    print("Implementácia core modulov:")
    print("  1. window_settings_db.py - DB operácie")
    print("  2. window_persistence.py - Persistence logika")
    print("  3. base_window.py - BaseWindow trieda")
    print("=" * 80)


if __name__ == '__main__':
    main()