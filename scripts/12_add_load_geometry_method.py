r"""
Script 12: Pridanie metódy _load_geometry() a jej volania v __init__.
"""

from pathlib import Path

# Cesta k projektu
PROJECT_ROOT = Path("C:/Development/nex-automat")
TARGET_FILE = PROJECT_ROOT / "apps/supplier-invoice-editor/src/ui/main_window.py"


def main():
    """Pridá _load_geometry metódu a volanie."""
    print(f"Upravujem: {TARGET_FILE}")

    if not TARGET_FILE.exists():
        print(f"❌ Súbor neexistuje: {TARGET_FILE}")
        return

    content = TARGET_FILE.read_text(encoding='utf-8')
    lines = content.splitlines()

    # Nájdi koniec __init__ metódy (riadok 38)
    init_end = 0
    for i, line in enumerate(lines):
        if 'def __init__(self' in line:
            # Hľadaj koniec __init__ - ďalšia metóda alebo koniec triedy
            for j in range(i + 1, len(lines)):
                if lines[j].strip().startswith('def ') and not lines[j].strip().startswith('def __init__'):
                    init_end = j - 1  # Posledný riadok __init__ je pred ďalšou metódou
                    break
            break

    if init_end == 0:
        print("❌ Nepodarilo sa nájsť koniec __init__")
        return

    print(f"✅ __init__ končí na riadku {init_end + 1}")

    # 1. Pridaj volanie self._load_geometry() na koniec __init__ (pred posledný riadok)
    # Nájdi posledný riadok s kódom v __init__ (nie prázdny)
    last_code_line = init_end
    for i in range(init_end, -1, -1):
        if lines[i].strip() and not lines[i].strip().startswith('#'):
            last_code_line = i
            break

    # Pridaj volanie za posledný riadok kódu
    lines.insert(last_code_line + 1, '        self._load_geometry()')
    print(f"✅ Pridané volanie self._load_geometry() na riadok {last_code_line + 2}")

    # 2. Pridaj metódu _load_geometry hneď za __init__
    method_code = [
        '',
        '    def _load_geometry(self):',
        '        """Načíta a aplikuje uloženú pozíciu a veľkosť okna."""',
        '        settings = load_window_settings(window_name=WINDOW_MAIN)',
        '        if settings:',
        '            self.setGeometry(',
        '                settings[\'x\'],',
        '                settings[\'y\'],',
        '                settings[\'width\'],',
        '                settings[\'height\']',
        '            )',
    ]

    # Pridaj metódu za __init__ (za novovložený riadok volania)
    insert_pos = last_code_line + 2
    for line in reversed(method_code):
        lines.insert(insert_pos, line)

    print(f"✅ Pridaná metóda _load_geometry() za riadok {insert_pos}")

    # Zapíš späť
    content = '\n'.join(lines)
    TARGET_FILE.write_text(content, encoding='utf-8')

    print(f"\n✅ Súbor upravený: {TARGET_FILE}")
    print(f"   Pôvodné riadky: {len(lines) - len(method_code) - 1}")
    print(f"   Nové riadky: {len(lines)}")
    print(f"   Pridané: {len(method_code) + 1} riadkov")
    print("\nUpravy:")
    print("  ✅ Pridané volanie: self._load_geometry() do __init__")
    print("  ✅ Pridaná metóda: _load_geometry()")
    print("\nSkús spustiť aplikáciu znova")


if __name__ == "__main__":
    main()