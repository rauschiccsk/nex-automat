"""
Krok 5: Oprava config.py
Prepíše config.py správnym obsahom
"""

from pathlib import Path


def fix_config():
    """Prepíše config.py správnym obsahom"""

    print("\n" + "=" * 60)
    print("KROK 5: Oprava config.py")
    print("=" * 60 + "\n")

    config_path = Path("C:/Development/nex-automat/tools/config.py")

    # Správny obsah config.py
    correct_content = '''# Claude Tools Configuration - nex-automat
# Generované: installer.py

PROJECT_ROOT = r"C:\\Development\\nex-automat"
TOOLS_DIR = r"C:\\Development\\nex-automat\\tools"
SESSION_NOTES_DIR = r"C:\\Development\\nex-automat\\SESSION_NOTES"

# Artifact Server
ARTIFACT_SERVER_PORT = 8765
ARTIFACT_SERVER_HOST = "localhost"

# Claude API (voliteľné - pre context compressor)
ANTHROPIC_API_KEY = ""  # Vlož sem svoj API key ak chceš použiť compressor

# Hotkeys (Ctrl+Alt+...)
HOTKEY_LOAD_INIT = "l"
HOTKEY_COPY_NOTES = "s"
HOTKEY_GIT_STATUS = "g"
HOTKEY_DEPLOYMENT_INFO = "d"
HOTKEY_NEW_CHAT = "n"
'''

    # Prepíš súbor
    print("Prepísujem config.py správnym obsahom...")
    config_path.write_text(correct_content, encoding='utf-8')

    print("✅ config.py opravený")

    # Overenie
    print("\nOverenie obsahu:")
    lines = config_path.read_text(encoding='utf-8').split('\n')
    for i, line in enumerate(lines[:6], 1):
        print(f"  {i}: {line}")

    print("\n" + "=" * 60)
    print("Teraz znova spusti: .\\start-claude-tools.ps1")
    print("=" * 60 + "\n")

    return True


if __name__ == "__main__":
    success = fix_config()
    exit(0 if success else 1)