"""
Krok 4: Oprava installer.py
Opravuje escape sequences a uvicorn inštaláciu
"""

from pathlib import Path


def fix_installer():
    """Opraví installer.py"""

    print("\n" + "=" * 60)
    print("KROK 4: Oprava installer.py")
    print("=" * 60 + "\n")

    installer_path = Path("C:/Development/nex-automat/tools/installer.py")

    if not installer_path.exists():
        print(f"❌ Súbor neexistuje: {installer_path}")
        return False

    print("Čítam installer.py...")
    content = installer_path.read_text(encoding='utf-8')

    # Oprava 1: Escape sequences v config_content
    print("  🔧 Opravujem escape sequences...")
    content = content.replace(
        'PROJECT_ROOT = r"C:\\\\Development\\\\nex-automat"',
        'PROJECT_ROOT = r"C:\\Development\\nex-automat"'
    )
    content = content.replace(
        'TOOLS_DIR = r"C:\\\\Development\\\\nex-automat\\\\tools"',
        'TOOLS_DIR = r"C:\\Development\\nex-automat\\tools"'
    )
    content = content.replace(
        'SESSION_NOTES_DIR = r"C:\\\\Development\\\\nex-automat\\\\SESSION_NOTES"',
        'SESSION_NOTES_DIR = r"C:\\Development\\nex-automat\\SESSION_NOTES"'
    )

    # Oprava 2: uvicorn[standard] -> uvicorn (bez standard)
    print("  🔧 Opravujem uvicorn dependency...")
    content = content.replace(
        '"uvicorn[standard]"',
        '"uvicorn"'
    )

    # Ulož opravený súbor
    installer_path.write_text(content, encoding='utf-8')

    print("\n✅ installer.py opravený")
    print("\nOpravy:")
    print("  ✅ Escape sequences v config_content")
    print("  ✅ uvicorn[standard] -> uvicorn")

    print("\n" + "=" * 60)
    print("Teraz znova spusti: python installer.py")
    print("=" * 60 + "\n")

    return True


if __name__ == "__main__":
    success = fix_installer()
    exit(0 if success else 1)