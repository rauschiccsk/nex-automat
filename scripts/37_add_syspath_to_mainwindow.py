"""
Pridá sys.path fix na začiatok main_window.py
"""
from pathlib import Path

MAIN_WINDOW_PATH = Path("apps/supplier-invoice-editor/src/ui/main_window.py")


def main():
    print("=" * 80)
    print("PRIDANIE sys.path FIX DO main_window.py")
    print("=" * 80)

    # Načítaj súbor
    with open(MAIN_WINDOW_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Skontroluj či už sys.path fix existuje
    has_fix = any('nex-shared' in line for line in lines[:10])

    if has_fix:
        print("⏭️  sys.path fix už existuje")
        return

    # Pridaj sys.path fix na začiatok súboru (pred všetky importy)
    path_fix = [
        '"""Main window module"""\n',
        'import sys\n',
        'from pathlib import Path\n',
        '\n',
        '# Add nex-shared to path\n',
        'nex_shared_path = Path(__file__).parent.parent.parent.parent.parent / "packages" / "nex-shared"\n',
        'if str(nex_shared_path) not in sys.path:\n',
        '    sys.path.insert(0, str(nex_shared_path))\n',
        '\n',
    ]

    # Nájdi prvý import alebo docstring
    insert_pos = 0
    for i, line in enumerate(lines):
        if line.strip().startswith('"""') or line.strip().startswith('import') or line.strip().startswith('from'):
            insert_pos = i
            break

    # Ak prvý riadok je docstring, vložiť za ňou
    if lines[insert_pos].strip().startswith('"""'):
        # Nájdi koniec docstringu
        for i in range(insert_pos + 1, len(lines)):
            if '"""' in lines[i]:
                insert_pos = i + 1
                break

    print(f"✅ Vkladám sys.path fix na pozíciu {insert_pos + 1}")

    # Vložiť path_fix (bez docstringu ak už existuje)
    if lines[0].strip().startswith('"""'):
        # Docstring už existuje, netreba pridávať
        new_lines = lines[:insert_pos] + path_fix[1:] + lines[insert_pos:]
    else:
        new_lines = path_fix + lines[insert_pos:]

    # Ulož súbor
    with open(MAIN_WINDOW_PATH, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

    print(f"✅ Súbor opravený: {MAIN_WINDOW_PATH}")

    print("\n" + "=" * 80)
    print("VERIFY - prvých 15 riadkov:")
    print("=" * 80)
    for i in range(min(15, len(new_lines))):
        print(f"{i + 1:3d}: {new_lines[i]}", end='')

    print("\n" + "=" * 80)
    print("TEST:")
    print("=" * 80)
    print("cd apps\\supplier-invoice-editor")
    print("python main.py")
    print("  → Aplikácia by sa MUSELA spustiť! ✅")
    print("=" * 80)


if __name__ == '__main__':
    main()"""
Pridá sys.path fix do ui/__init__.py PRED import main_window
"""
from pathlib import Path

UI_INIT_PATH = Path("apps/supplier-invoice-editor/src/ui/__init__.py")

def main():
    print("=" * 80)
    print("PRIDANIE sys.path FIX DO ui/__init__.py")
    print("=" * 80)

    # Načítaj súbor
    with open(UI_INIT_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Skontroluj či už sys.path fix existuje
    has_fix = any('nex-shared' in line for line in lines)

    if has_fix:
        print("⏭️  sys.path fix už existuje")
        return

    # Nová implementácia s sys.path fix
    new_content = '''"""UI package"""
import sys
from pathlib import Path

# Add nex-shared to path BEFORE any imports
nex_shared_path = Path(__file__).parent.parent.parent.parent / "packages" / "nex-shared"
if str(nex_shared_path) not in sys.path:
    sys.path.insert(0, str(nex_shared_path))

from .main_window import MainWindow

__all__ = ['MainWindow']
'''

    # Zapíš nový súbor
    with open(UI_INIT_PATH, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"✅ Súbor prepísaný: {UI_INIT_PATH}")
    print("\nNový obsah:")
    print(new_content)

    print("\n" + "=" * 80)
    print("FINÁLNY TEST:")
    print("=" * 80)
    print("cd apps\\supplier-invoice-editor")
    print("python main.py")
    print("  → MUSÍ sa spustiť! ✅")
    print("  → Maximize + Close + Run again")
    print("  → MUSÍ byť maximalized! ✅✅✅")
    print("=" * 80)

if __name__ == '__main__':
    main()