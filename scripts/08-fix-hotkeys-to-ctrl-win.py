"""
Fix all hotkeys: Ctrl+Shift+... -> Ctrl+Win+...
Reason: Ctrl+Shift+... conflicts with browser shortcuts (DevTools, Incognito)
"""
from pathlib import Path

PROJECT_ROOT = Path(r"C:\Development\nex-automat")


def fix_claude_hotkeys():
    """Zmení všetky hotkeys v claude-hotkeys.py"""
    file_path = PROJECT_ROOT / "tools" / "claude-hotkeys.py"
    content = file_path.read_text(encoding='utf-8')

    # Zmení 'ctrl+shift+' na 'ctrl+win+'
    content = content.replace("'ctrl+shift+", "'ctrl+win+")
    content = content.replace('"ctrl+shift+', '"ctrl+win+')

    # Zmení texty v komentároch a výpisoch
    content = content.replace("Ctrl+Shift+", "Ctrl+Win+")

    file_path.write_text(content, encoding='utf-8')
    print(f"✅ Opravené: {file_path}")


def fix_config():
    """Zmení hotkeys v config.py"""
    file_path = PROJECT_ROOT / "tools" / "config.py"
    content = file_path.read_text(encoding='utf-8')

    # Zmení Ctrl+Shift+ na Ctrl+Win+ vo všetkých komentároch
    content = content.replace("Ctrl+Shift+", "Ctrl+Win+")

    file_path.write_text(content, encoding='utf-8')
    print(f"✅ Opravené: {file_path}")


def fix_init_prompt():
    """Zmení hotkeys v INIT_PROMPT_NEW_CHAT.md"""
    file_path = PROJECT_ROOT / "SESSION_NOTES" / "INIT_PROMPT_NEW_CHAT.md"

    if not file_path.exists():
        print(f"⚠️  Súbor neexistuje: {file_path}")
        return

    content = file_path.read_text(encoding='utf-8')

    # Zmení všetky výskyty Ctrl+Shift+ na Ctrl+Win+
    content = content.replace("Ctrl+Shift+", "Ctrl+Win+")

    file_path.write_text(content, encoding='utf-8')
    print(f"✅ Opravené: {file_path}")


def fix_session_notes():
    """Zmení hotkeys v SESSION_NOTES.md"""
    file_path = PROJECT_ROOT / "SESSION_NOTES" / "SESSION_NOTES.md"

    if not file_path.exists():
        print(f"⚠️  Súbor neexistuje: {file_path}")
        return

    content = file_path.read_text(encoding='utf-8')

    # Zmení všetky výskyty Ctrl+Shift+ na Ctrl+Win+
    content = content.replace("Ctrl+Shift+", "Ctrl+Win+")

    file_path.write_text(content, encoding='utf-8')
    print(f"✅ Opravené: {file_path}")


def fix_start_script():
    """Zmení hotkeys v start-claude-tools.ps1"""
    file_path = PROJECT_ROOT / "tools" / "start-claude-tools.ps1"
    content = file_path.read_text(encoding='utf-8')

    # Zmení všetky výskyty Ctrl+Shift+ na Ctrl+Win+
    content = content.replace("Ctrl+Shift+", "Ctrl+Win+")

    file_path.write_text(content, encoding='utf-8')
    print(f"✅ Opravené: {file_path}")


def main():
    print("=" * 70)
    print("FIX ALL HOTKEYS: Ctrl+Shift+... → Ctrl+Win+...")
    print("Dôvod: Ctrl+Shift+... koliduje s browser shortcuts (DevTools, Incognito)")
    print("=" * 70)

    fix_claude_hotkeys()
    fix_config()
    fix_init_prompt()
    fix_session_notes()
    fix_start_script()

    print("\n" + "=" * 70)
    print("✅ HOTFIX DOKONČENÝ")
    print("=" * 70)
    print("\nNové hotkeys (Win = Windows key):")
    print("  Ctrl+Win+S - Copy Session Notes")
    print("  Ctrl+Win+G - Git Status")
    print("  Ctrl+Win+D - Deployment Info")
    print("  Ctrl+Win+N - New Chat Template")
    print("  Ctrl+Win+P - Load Init Prompt")
    print("  Ctrl+Win+I - Show Project Info")
    print("\nNasledujúce kroky:")
    print("1. Zastaviť procesy: .\\stop-claude-tools.ps1")
    print("2. Spustiť znova: .\\start-claude-tools.ps1")
    print("3. Test: Ctrl+Win+I")


if __name__ == "__main__":
    main()