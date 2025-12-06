"""
Fix all hotkeys: Ctrl+Alt+... -> Ctrl+Shift+...
Reason: Ctrl+Alt = AltGr on Slovak keyboard (generates special chars)
"""
from pathlib import Path

PROJECT_ROOT = Path(r"C:\Development\nex-automat")


def fix_claude_hotkeys():
    """Zmení všetky hotkeys v claude-hotkeys.py"""
    file_path = PROJECT_ROOT / "tools" / "claude-hotkeys.py"
    content = file_path.read_text(encoding='utf-8')

    # Zmení 'ctrl+alt+' na 'ctrl+shift+'
    content = content.replace("'ctrl+alt+", "'ctrl+shift+")
    content = content.replace('"ctrl+alt+', '"ctrl+shift+')

    # Zmení texty v komentároch a výpisoch
    content = content.replace("Ctrl+Alt+", "Ctrl+Shift+")

    file_path.write_text(content, encoding='utf-8')
    print(f"✅ Opravené: {file_path}")


def fix_config():
    """Zmení hotkeys v config.py"""
    file_path = PROJECT_ROOT / "tools" / "config.py"
    content = file_path.read_text(encoding='utf-8')

    # Zmení Ctrl+Alt+ na Ctrl+Shift+ vo všetkých komentároch
    content = content.replace("Ctrl+Alt+", "Ctrl+Shift+")

    file_path.write_text(content, encoding='utf-8')
    print(f"✅ Opravené: {file_path}")


def fix_init_prompt():
    """Zmení hotkeys v INIT_PROMPT_NEW_CHAT.md"""
    file_path = PROJECT_ROOT / "SESSION_NOTES" / "INIT_PROMPT_NEW_CHAT.md"

    if not file_path.exists():
        print(f"⚠️  Súbor neexistuje: {file_path}")
        return

    content = file_path.read_text(encoding='utf-8')

    # Zmení všetky výskyty Ctrl+Alt+ na Ctrl+Shift+
    content = content.replace("Ctrl+Alt+", "Ctrl+Shift+")

    file_path.write_text(content, encoding='utf-8')
    print(f"✅ Opravené: {file_path}")


def fix_session_notes():
    """Zmení hotkeys v SESSION_NOTES.md"""
    file_path = PROJECT_ROOT / "SESSION_NOTES" / "SESSION_NOTES.md"

    if not file_path.exists():
        print(f"⚠️  Súbor neexistuje: {file_path}")
        return

    content = file_path.read_text(encoding='utf-8')

    # Zmení všetky výskyty Ctrl+Alt+ na Ctrl+Shift+
    content = content.replace("Ctrl+Alt+", "Ctrl+Shift+")

    file_path.write_text(content, encoding='utf-8')
    print(f"✅ Opravené: {file_path}")


def fix_start_script():
    """Zmení hotkeys v start-claude-tools.ps1"""
    file_path = PROJECT_ROOT / "tools" / "start-claude-tools.ps1"
    content = file_path.read_text(encoding='utf-8')

    # Zmení všetky výskyty Ctrl+Alt+ na Ctrl+Shift+
    content = content.replace("Ctrl+Alt+", "Ctrl+Shift+")

    file_path.write_text(content, encoding='utf-8')
    print(f"✅ Opravené: {file_path}")


def main():
    print("=" * 70)
    print("FIX ALL HOTKEYS: Ctrl+Alt+... → Ctrl+Shift+...")
    print("Dôvod: Ctrl+Alt = AltGr na SK klávesnici (generuje špeciálne znaky)")
    print("=" * 70)

    fix_claude_hotkeys()
    fix_config()
    fix_init_prompt()
    fix_session_notes()
    fix_start_script()

    print("\n" + "=" * 70)
    print("✅ HOTFIX DOKONČENÝ")
    print("=" * 70)
    print("\nNové hotkeys:")
    print("  Ctrl+Shift+S - Copy Session Notes")
    print("  Ctrl+Shift+G - Git Status")
    print("  Ctrl+Shift+D - Deployment Info")
    print("  Ctrl+Shift+N - New Chat Template")
    print("  Ctrl+Shift+P - Load Init Prompt")
    print("  Ctrl+Shift+I - Show Project Info")
    print("\nNasledujúce kroky:")
    print("1. Zastaviť procesy: .\\stop-claude-tools.ps1")
    print("2. Spustiť znova: .\\start-claude-tools.ps1")
    print("3. Test: Ctrl+Shift+I")


if __name__ == "__main__":
    main()