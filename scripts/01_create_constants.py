"""
Script 01: Vytvorenie constants.py pre window identifikátory.

Vytvorí súbor src/utils/constants.py s konštantami pre identifikáciu okien.
Použije prefix "sie" (Supplier Invoice Editor) pre odlíšenie od iných aplikácií.
"""

from pathlib import Path

# Cesta k projektu
PROJECT_ROOT = Path("C:/Development/nex-automat")
TARGET_FILE = PROJECT_ROOT / "apps/supplier-invoice-editor/src/utils/constants.py"

# Obsah súboru
CONTENT = '''"""
Konštanty pre identifikáciu okien a dialógov.

Window names používajú prefix 'sie' (Supplier Invoice Editor) 
pre odlíšenie od iných aplikácií v zdieľanej window_settings.db.
"""

# Application prefix pre rozlíšenie okien rôznych aplikácií
APP_PREFIX = "sie"

# Main windows
WINDOW_MAIN = f"{APP_PREFIX}_main_window"
WINDOW_INVOICE_DETAIL = f"{APP_PREFIX}_invoice_detail"

# Dialogs (pre budúcnosť)
DIALOG_SETTINGS = f"{APP_PREFIX}_settings_dialog"
DIALOG_ABOUT = f"{APP_PREFIX}_about_dialog"

# Future windows (rezervované pre dokumentáciu)
# WINDOW_REPORTS = f"{APP_PREFIX}_reports_window"
# WINDOW_STATISTICS = f"{APP_PREFIX}_statistics_window"
'''


def main():
    """Vytvorí constants.py súbor."""
    print(f"Vytváram: {TARGET_FILE}")

    # Vytvor priečinok ak neexistuje
    TARGET_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Zapíš obsah
    TARGET_FILE.write_text(CONTENT.strip(), encoding='utf-8')

    print(f"✅ Súbor vytvorený: {TARGET_FILE}")
    print(f"   Veľkosť: {TARGET_FILE.stat().st_size} bytes")
    print(f"   Riadkov: {len(CONTENT.strip().splitlines())}")
    print("\nDefinované konštanty:")
    print("  - APP_PREFIX = 'sie'")
    print("  - WINDOW_MAIN = 'sie_main_window'")
    print("  - WINDOW_INVOICE_DETAIL = 'sie_invoice_detail'")
    print("  - DIALOG_SETTINGS = 'sie_settings_dialog'")
    print("  - DIALOG_ABOUT = 'sie_about_dialog'")


if __name__ == "__main__":
    main()