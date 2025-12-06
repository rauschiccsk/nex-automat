"""
Pridá sys.path fix do main.py pre nex-shared package
"""
from pathlib import Path

MAIN_PY_PATH = Path("apps/supplier-invoice-editor/main.py")


def main():
    print("=" * 80)
    print("PRIDÁVANIE sys.path FIX")
    print("=" * 80)

    # Načítaj súbor
    with open(MAIN_PY_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Skontroluj či už sys.path fix existuje
    has_fix = any('nex-shared' in line for line in lines[:20])

    if has_fix:
        print("⏭️  sys.path fix už existuje")
        return

    # Nájdi prvý import
    first_import = 0
    for i, line in enumerate(lines):
        if line.strip().startswith('import ') or line.strip().startswith('from '):
            first_import = i
            break

    print(f"✅ Prvý import na riadku {first_import + 1}")

    # Pridaj sys.path fix pred prvý import
    path_fix = [
        "import sys\n",
        "from pathlib import Path\n",
        "\n",
        "# Add nex-shared to path\n",
        "nex_shared_path = Path(__file__).parent.parent.parent / 'packages' / 'nex-shared'\n",
        "if str(nex_shared_path) not in sys.path:\n",
        "    sys.path.insert(0, str(nex_shared_path))\n",
        "\n"
    ]

    # Vložíme pred prvý import
    new_lines = lines[:first_import] + path_fix + lines[first_import:]

    # Ulož súbor
    with open(MAIN_PY_PATH, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

    print(f"✅ sys.path fix pridaný do {MAIN_PY_PATH}")
    print("\nPridané riadky:")
    for line in path_fix:
        print(f"  {line}", end='')

    print("\n" + "=" * 80)
    print("TEST:")
    print("=" * 80)
    print("cd apps\\supplier-invoice-editor")
    print("python main.py")
    print("  → Aplikácia by sa mala spustiť ✅")
    print("=" * 80)


if __name__ == '__main__':
    main()