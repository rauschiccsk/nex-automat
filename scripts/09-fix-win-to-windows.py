"""
Fix hotkey modifier: 'win' -> 'windows' (correct keyboard module syntax)
"""
from pathlib import Path

PROJECT_ROOT = Path(r"C:\Development\nex-automat")


def fix_claude_hotkeys():
    """Zmení 'ctrl+win+' na 'ctrl+windows+' v hotkey strings"""
    file_path = PROJECT_ROOT / "tools" / "claude-hotkeys.py"
    content = file_path.read_text(encoding='utf-8')

    # Zmení 'ctrl+win+' na 'ctrl+windows+' (len v hotkey definíciách)
    content = content.replace("'ctrl+win+", "'ctrl+windows+")
    content = content.replace('"ctrl+win+', '"ctrl+windows+')

    file_path.write_text(content, encoding='utf-8')
    print(f"✅ Opravené: {file_path}")


def main():
    print("=" * 70)
    print("FIX HOTKEY SYNTAX: 'win' → 'windows'")
    print("Dôvod: keyboard modul používa 'windows' nie 'win'")
    print("=" * 70)

    fix_claude_hotkeys()

    print("\n" + "=" * 70)
    print("✅ HOTFIX DOKONČENÝ")
    print("=" * 70)
    print("\nNasledujúce kroky:")
    print("1. Zastaviť procesy: .\\stop-claude-tools.ps1")
    print("2. Spustiť znova: .\\start-claude-tools.ps1")
    print("3. Test: Ctrl+Win+I")


if __name__ == "__main__":
    main()