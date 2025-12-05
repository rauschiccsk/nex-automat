r"""
Script 04: Úprava main_window.py pre ukladanie pozície a veľkosti okna.

Pridá:
1. Import window_settings a constants
2. Metódu _load_geometry() do __init__
3. Úpravu closeEvent() pre ukladanie
"""

from pathlib import Path
import re

# Cesta k projektu
PROJECT_ROOT = Path("C:/Development/nex-automat")
TARGET_FILE = PROJECT_ROOT / "apps/supplier-invoice-editor/src/ui/main_window.py"


def main():
    """Upraví main_window.py."""
    print(f"Upravujem: {TARGET_FILE}")

    # Načítaj pôvodný súbor
    if not TARGET_FILE.exists():
        print(f"❌ Súbor neexistuje: {TARGET_FILE}")
        return

    content = TARGET_FILE.read_text(encoding='utf-8')
    original_lines = len(content.splitlines())

    # Záloha
    backup_path = TARGET_FILE.with_suffix('.py.backup')
    TARGET_FILE.rename(backup_path)
    print(f"📦 Záloha vytvorená: {backup_path}")

    # 1. Pridaj importy na začiatok (po existujúcich importoch)
    # Nájdi kde sú importy z utils
    import_pattern = r'(from utils\..*? import .*?\n)'

    new_imports = """from utils.constants import WINDOW_MAIN
from utils.window_settings import load_window_settings, save_window_settings
"""

    # Pridaj importy za existujúce utils importy
    if 'from utils.' in content:
        # Nájdi posledný utils import
        matches = list(re.finditer(import_pattern, content))
        if matches:
            last_match = matches[-1]
            insert_pos = last_match.end()
            content = content[:insert_pos] + new_imports + content[insert_pos:]
    else:
        # Ak nie sú žiadne utils importy, pridaj za ostatné importy
        # Hľadaj "class MainWindow"
        class_match = re.search(r'class MainWindow', content)
        if class_match:
            insert_pos = class_match.start()
            content = content[:insert_pos] + new_imports + "\n\n" + content[insert_pos:]

    # 2. Pridaj _load_geometry() metódu
    # Nájdi koniec __init__ metódy
    init_pattern = r'(    def __init__\(self.*?\):.*?)((?=\n    def )|(?=\nclass )|$)'

    load_geometry_method = """
    def _load_geometry(self):
        \"\"\"Načíta a aplikuje uloženú pozíciu a veľkosť okna.\"\"\"
        settings = load_window_settings(window_name=WINDOW_MAIN)
        if settings:
            self.setGeometry(
                settings['x'],
                settings['y'],
                settings['width'],
                settings['height']
            )
"""

    # Nájdi __init__ a pridaj volanie _load_geometry na koniec
    init_match = re.search(r'    def __init__\(self.*?\):(.*?)(?=\n    def |\nclass |$)', content, re.DOTALL)
    if init_match:
        init_content = init_match.group(1)
        # Nájdi posledný riadok v __init__ (pred ďalšou metódou)
        lines = init_content.split('\n')
        # Nájdi posledný neprázdny riadok s odsadením
        for i in range(len(lines) - 1, -1, -1):
            if lines[i].strip() and lines[i].startswith('        '):
                # Pridaj volanie _load_geometry
                lines.insert(i + 1, '        self._load_geometry()')
                break

        new_init_content = '\n'.join(lines)
        content = content.replace(init_content, new_init_content)

    # Pridaj metódu _load_geometry za __init__
    content = re.sub(
        r'(    def __init__\(self.*?\):.*?)(\n    def )',
        r'\1' + load_geometry_method + r'\2',
        content,
        flags=re.DOTALL
    )

    # 3. Uprav closeEvent pre ukladanie
    # Nájdi closeEvent metódu
    close_event_pattern = r'(    def closeEvent\(self, event\):.*?)(        event\.accept\(\))'

    save_code = """        # Ulož pozíciu a veľkosť okna
        save_window_settings(
            window_name=WINDOW_MAIN,
            x=self.x(),
            y=self.y(),
            width=self.width(),
            height=self.height()
        )
        """

    # Pridaj save_window_settings pred event.accept()
    content = re.sub(
        close_event_pattern,
        r'\1' + save_code + r'\2',
        content,
        flags=re.DOTALL
    )

    # Zapíš upravený súbor
    TARGET_FILE.write_text(content, encoding='utf-8')

    new_lines = len(content.splitlines())
    print(f"✅ Súbor upravený: {TARGET_FILE}")
    print(f"   Pôvodné riadky: {original_lines}")
    print(f"   Nové riadky: {new_lines}")
    print(f"   Pridané: {new_lines - original_lines} riadkov")
    print("\nUpravy:")
    print("  ✅ Pridané importy: WINDOW_MAIN, load_window_settings, save_window_settings")
    print("  ✅ Pridaná metóda: _load_geometry()")
    print("  ✅ Upravená metóda: closeEvent() - ukladá pozíciu/veľkosť")


if __name__ == "__main__":
    main()