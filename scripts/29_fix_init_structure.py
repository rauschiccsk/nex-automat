r"""
Script 29: Oprava __init__ metódy - odstránenie alebo pridanie _connect_signals.
"""

from pathlib import Path

# Cesta k projektu
PROJECT_ROOT = Path("C:/Development/nex-automat")
TARGET_FILE = PROJECT_ROOT / "apps/supplier-invoice-editor/src/ui/widgets/invoice_list_widget.py"


def main():
    """Opraví __init__ metódu."""
    print(f"Analyzujem: {TARGET_FILE}")

    if not TARGET_FILE.exists():
        print(f"❌ Súbor neexistuje: {TARGET_FILE}")
        return

    content = TARGET_FILE.read_text(encoding='utf-8')
    lines = content.splitlines()

    # Nájdi __init__ metódu
    print("\n__INIT__ METÓDA:")
    print("-" * 70)

    for i, line in enumerate(lines, 1):
        if 'def __init__(self' in line and i > 130:  # InvoiceListWidget __init__
            # Zobraz 10 riadkov
            for j in range(i - 1, min(i + 10, len(lines))):
                print(f"  {j + 1:4d}: {lines[j]}")
            break

    # Skontroluj či existuje _connect_signals metóda
    has_connect_signals = 'def _connect_signals(self):' in content

    print(f"\n_connect_signals metóda: {'✅ existuje' if has_connect_signals else '❌ neexistuje'}")

    if not has_connect_signals:
        print("\nRIEŠENIE 1: Odstrániť volanie self._connect_signals()")
        print("RIEŠENIE 2: Vytvoriť prázdnu metódu _connect_signals()")
        print("\nPoužijem RIEŠENIE 1 - odstránim volanie")

        # Odstráň riadok s self._connect_signals()
        new_lines = []
        removed = False

        for line in lines:
            if 'self._connect_signals()' in line and not removed:
                print(f"❌ Odstraňujem: {line.strip()}")
                removed = True
                continue
            new_lines.append(line)

        if removed:
            # Zapíš späť
            content = '\n'.join(new_lines)
            TARGET_FILE.write_text(content, encoding='utf-8')

            print(f"\n✅ Súbor upravený: {TARGET_FILE}")
            print(f"   Nové riadky: {len(new_lines)}")
            print("\nTeraz spusti aplikáciu znova!")
        else:
            print("\n⚠️  Volanie self._connect_signals() nenájdené")
    else:
        print("\n✅ Metóda existuje - problém je niekde inde")


if __name__ == "__main__":
    main()