r"""
Script 16: Pridanie grid identifikátorov do constants.py.

Pridá konštanty pre identifikáciu gridov v aplikácii.
"""

from pathlib import Path

# Cesta k projektu
PROJECT_ROOT = Path("C:/Development/nex-automat")
TARGET_FILE = PROJECT_ROOT / "apps/supplier-invoice-editor/src/utils/constants.py"


def main():
    """Pridá grid identifikátory do constants.py."""
    print(f"Upravujem: {TARGET_FILE}")

    if not TARGET_FILE.exists():
        print(f"❌ Súbor neexistuje: {TARGET_FILE}")
        return

    content = TARGET_FILE.read_text(encoding='utf-8')

    # Skontroluj či už grid konštanty existujú
    if 'GRID_INVOICE_LIST' in content:
        print("✅ Grid konštanty už existujú")
        return

    # Pridaj grid konštanty na koniec súboru
    grid_constants = """

# Grid identifiers
GRID_INVOICE_LIST = "invoice_list"
GRID_INVOICE_ITEMS = "invoice_items"
"""

    content += grid_constants

    # Zapíš späť
    TARGET_FILE.write_text(content, encoding='utf-8')

    print(f"✅ Súbor upravený: {TARGET_FILE}")
    print(f"   Riadkov: {len(content.splitlines())}")
    print("\nPridané konštanty:")
    print("  ✅ GRID_INVOICE_LIST = 'invoice_list'")
    print("  ✅ GRID_INVOICE_ITEMS = 'invoice_items'")


if __name__ == "__main__":
    main()