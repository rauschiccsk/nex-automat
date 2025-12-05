r"""
Script 05: Obnovenie a správna úprava main_window.py.

Obnoví z backupu a správne pridá window settings funkčnosť.
"""

from pathlib import Path
import re

# Cesta k projektu
PROJECT_ROOT = Path("C:/Development/nex-automat")
TARGET_FILE = PROJECT_ROOT / "apps/supplier-invoice-editor/src/ui/main_window.py"
BACKUP_FILE = TARGET_FILE.with_suffix('.py.backup')


def main():
    """Obnoví a správne upraví main_window.py."""
    print(f"Opravujem: {TARGET_FILE}")

    # Obnov z backupu
    if not BACKUP_FILE.exists():
        print(f"❌ Backup neexistuje: {BACKUP_FILE}")
        return

    print(f"📦 Obnovujem z: {BACKUP_FILE}")
    content = BACKUP_FILE.read_text(encoding='utf-8')

    # 1. Pridaj importy za existujúce utils importy
    # Nájdi kde sú z utils importy
    import_section = re.search(r'(from utils\.quick_search.*?\n)', content)
    if import_section:
        insert_pos = import_section.end()
        new_imports = "from utils.constants import WINDOW_MAIN\nfrom utils.window_settings import load_window_settings, save_window_settings\n"
        content = content[:insert_pos] + new_imports + content[insert_pos:]
        print("✅ Pridané importy")

    # 2. Pridaj _load_geometry metódu za __init__
    # Nájdi koniec __init__ metódy
    init_end = re.search(r'(        # Prepare tab widget.*?\n        self\.prepare_tabs\(\)\n)', content)
    if init_end:
        insert_pos = init_end.end()
        load_call = "        self._load_geometry()\n"
        content = content[:insert_pos] + load_call + content[insert_pos:]
        print("✅ Pridané volanie _load_geometry() do __init__")

    # Pridaj metódu _load_geometry za __init__
    init_method_end = re.search(
        r'(    def __init__\(self.*?\n        self\.prepare_tabs\(\)\n        self\._load_geometry\(\)\n)', content,
        re.DOTALL)
    if init_method_end:
        insert_pos = init_method_end.end()
        method_code = '''
    def _load_geometry(self):
        """Načíta a aplikuje uloženú pozíciu a veľkosť okna."""
        settings = load_window_settings(window_name=WINDOW_MAIN)
        if settings:
            self.setGeometry(
                settings['x'],
                settings['y'],
                settings['width'],
                settings['height']
            )
'''
        content = content[:insert_pos] + method_code + content[insert_pos:]
        print("✅ Pridaná metóda _load_geometry()")

    # 3. Upraviť closeEvent - pridať ukladanie pred event.accept()
    close_event = re.search(r'(    def closeEvent\(self, event\):.*?)(        event\.accept\(\))', content, re.DOTALL)
    if close_event:
        before_accept = close_event.group(1)
        save_code = '''        # Ulož pozíciu a veľkosť okna
        save_window_settings(
            window_name=WINDOW_MAIN,
            x=self.x(),
            y=self.y(),
            width=self.width(),
            height=self.height()
        )
        '''
        new_close = before_accept + save_code + "event.accept()"
        content = content[:close_event.start()] + new_close + content[close_event.end():]
        print("✅ Upravená metóda closeEvent()")

    # Zapíš
    TARGET_FILE.write_text(content, encoding='utf-8')

    lines = len(content.splitlines())
    print(f"\n✅ Súbor úspešne upravený: {TARGET_FILE}")
    print(f"   Celkom riadkov: {lines}")
    print("\nSkús spustiť aplikáciu:")
    print("  python main.py")


if __name__ == "__main__":
    main()