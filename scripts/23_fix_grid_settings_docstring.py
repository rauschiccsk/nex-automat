r"""
Script 23: Oprava docstringu v grid_settings.py - raw string.
"""

from pathlib import Path

# Cesta k projektu
PROJECT_ROOT = Path("C:/Development/nex-automat")
TARGET_FILE = PROJECT_ROOT / "apps/supplier-invoice-editor/src/utils/grid_settings.py"


def main():
    """Opraví grid_settings.py - pridá 'r' pred docstring."""
    print(f"Opravujem: {TARGET_FILE}")

    if not TARGET_FILE.exists():
        print(f"❌ Súbor neexistuje: {TARGET_FILE}")
        return

    # Načítaj súbor
    content = TARGET_FILE.read_text(encoding='utf-8')

    # Nahraď """ na začiatku súboru za r"""
    if content.startswith('"""'):
        content = 'r' + content
        print("✅ Pridané 'r' pred prvý docstring")

    # Zapíš späť
    TARGET_FILE.write_text(content, encoding='utf-8')

    print(f"✅ Súbor opravený: {TARGET_FILE}")
    print("   Raw string docstring pre správne spracovanie C:\\NEX\\... ciest")
    print("\nSkús spustiť aplikáciu znova")


if __name__ == "__main__":
    main()