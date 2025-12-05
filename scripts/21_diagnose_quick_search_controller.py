r"""
Script 21: Diagnostika QuickSearchController - kde je active_column.
"""

from pathlib import Path

# Cesta k projektu
PROJECT_ROOT = Path("C:/Development/nex-automat")
TARGET_FILE = PROJECT_ROOT / "apps/supplier-invoice-editor/src/ui/widgets/quick_search.py"


def main():
    """Analyzuje QuickSearchController."""
    print(f"Analyzujem: {TARGET_FILE}")
    print("=" * 70)

    if not TARGET_FILE.exists():
        print(f"❌ Súbor neexistuje: {TARGET_FILE}")
        return

    content = TARGET_FILE.read_text(encoding='utf-8')
    lines = content.splitlines()

    # 1. Nájdi QuickSearchController triedu
    print("\n1. TRIEDA QuickSearchController:")
    print("-" * 70)

    controller_line = 0
    for i, line in enumerate(lines, 1):
        if 'class QuickSearchController' in line:
            controller_line = i
            print(f"✅ Nájdená na riadku {i}: {line.strip()}")
            break

    if controller_line == 0:
        print("❌ QuickSearchController nenájdená!")
        return

    # 2. Nájdi __init__
    print("\n2. __INIT__ METÓDA:")
    print("-" * 70)

    for i, line in enumerate(lines, 1):
        if i > controller_line and 'def __init__' in line:
            # Zobraz 20 riadkov
            for j in range(i - 1, min(i + 20, len(lines))):
                print(f"  {j + 1:4d}: {lines[j]}")
            break

    # 3. Hľadaj active_column
    print("\n3. ACTIVE_COLUMN:")
    print("-" * 70)

    found_active = False
    for i, line in enumerate(lines, 1):
        if 'active_column' in line.lower():
            print(f"  {i:4d}: {line.strip()}")
            found_active = True

    if not found_active:
        print("❌ active_column nenájdené v kóde!")

    # 4. Hľadaj metódy set/get
    print("\n4. EXISTUJÚCE SET/GET METÓDY:")
    print("-" * 70)

    has_set = False
    has_get = False

    for i, line in enumerate(lines, 1):
        if i > controller_line:
            if 'def set_active_column' in line:
                print(f"  ✅ {i:4d}: {line.strip()}")
                has_set = True
            if 'def get_active_column' in line:
                print(f"  ✅ {i:4d}: {line.strip()}")
                has_get = True

    if not has_set:
        print("  ❌ set_active_column() neexistuje")
    if not has_get:
        print("  ❌ get_active_column() neexistuje")

    # 5. Hľadaj ako sa mení aktívny stĺpec
    print("\n5. AKO SA MENÍ AKTÍVNY STĹPEC:")
    print("-" * 70)

    for i, line in enumerate(lines, 1):
        if i > controller_line:
            if 'self.current_column' in line or 'self._active_column' in line:
                print(f"  {i:4d}: {line.strip()}")

    print("\n" + "=" * 70)
    print("ZÁVER:")
    if has_set and has_get:
        print("  ✅ Metódy už existujú - nič netreba pridávať!")
    else:
        print("  ❌ Potrebujem pridať metódy set_active_column() a get_active_column()")


if __name__ == "__main__":
    main()