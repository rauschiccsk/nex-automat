"""
Fix hotkey Ctrl+Alt+L -> Ctrl+Alt+P (collision with Slovak keyboard)
"""
from pathlib import Path

PROJECT_ROOT = Path(r"C:\Development\nex-automat")


def fix_claude_hotkeys():
    """Opraví hotkey v claude-hotkeys.py"""
    file_path = PROJECT_ROOT / "tools" / "claude-hotkeys.py"
    content = file_path.read_text(encoding='utf-8')

    # Zmení 'ctrl+alt+l' na 'ctrl+alt+p'
    content = content.replace("'ctrl+alt+l'", "'ctrl+alt+p'")
    content = content.replace('"ctrl+alt+l"', '"ctrl+alt+p"')

    # Zmení popis v komentároch
    content = content.replace("Ctrl+Alt+L", "Ctrl+Alt+P")

    file_path.write_text(content, encoding='utf-8')
    print(f"✅ Opravené: {file_path}")


def fix_config():
    """Opraví hotkey v config.py"""
    file_path = PROJECT_ROOT / "tools" / "config.py"
    content = file_path.read_text(encoding='utf-8')

    # Zmení L na P v HOTKEYS dictionary
    content = content.replace("'L': 'Load", "'P': 'Load")
    content = content.replace('"L": "Load', '"P": "Load')

    file_path.write_text(content, encoding='utf-8')
    print(f"✅ Opravené: {file_path}")


def fix_init_prompt():
    """Opraví hotkey v INIT_PROMPT_NEW_CHAT.md"""
    file_path = PROJECT_ROOT / "SESSION_NOTES" / "INIT_PROMPT_NEW_CHAT.md"

    if not file_path.exists():
        print(f"⚠️  Súbor neexistuje: {file_path}")
        return

    content = file_path.read_text(encoding='utf-8')

    # Zmení L na P v tabuľke hotkeys
    content = content.replace("| **L** | Load init prompt", "| **P** | Load init prompt")
    content = content.replace("Ctrl+Alt+L", "Ctrl+Alt+P")

    file_path.write_text(content, encoding='utf-8')
    print(f"✅ Opravené: {file_path}")


def main():
    print("=" * 60)
    print("FIX HOTKEY: Ctrl+Alt+L → Ctrl+Alt+P")
    print("Dôvod: Kolízia so slovenskou klávesnicou")
    print("=" * 60)

    fix_claude_hotkeys()
    fix_config()
    fix_init_prompt()

    print("\n" + "=" * 60)
    print("✅ HOTFIX DOKONČENÝ")
    print("=" * 60)
    print("\nNasledujúce kroky:")
    print("1. Reštartuj claude-hotkeys: .\\stop-claude-tools.ps1")
    print("2. Spusti znova: .\\start-claude-tools.ps1")
    print("3. Test: Ctrl+Alt+P v novom claude.ai chate")


if __name__ == "__main__":
    main()