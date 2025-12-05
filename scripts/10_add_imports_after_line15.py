r"""
Script 10: Pridanie importov window_settings na správne miesto - za riadok 15.
"""

from pathlib import Path

# Cesta k projektu
PROJECT_ROOT = Path("C:/Development/nex-automat")
TARGET_FILE = PROJECT_ROOT / "apps/supplier-invoice-editor/src/ui/main_window.py"


def main():
    """Pridá importy za riadok 15."""
    print(f"Upravujem: {TARGET_FILE}")

    if not TARGET_FILE.exists():
        print(f"❌ Súbor neexistuje: {TARGET_FILE}")
        return

    # Načítaj súbor
    content = TARGET_FILE.read_text(encoding='utf-8')
    lines = content.splitlines()

    # Skontroluj či už importy existujú
    if any('save_window_settings' in line for line in lines[:20]):
        print("✅ Importy už existujú")
        return

    # Pridaj za riadok 15 (index 15 pretože indexy začínajú od 0)
    # Riadok 15 je: "from business.invoice_service import InvoiceService"

    new_lines = []
    for i, line in enumerate(lines):
        new_lines.append(line)

        # Za riadok 15 pridaj importy
        if i == 14:  # Riadok 15 má index 14
            new_lines.append('from utils.constants import WINDOW_MAIN')
            new_lines.append('from utils.window_settings import load_window_settings, save_window_settings')
            print(f"✅ Pridané importy za riadok {i + 1}")

    # Zapíš späť
    content = '\n'.join(new_lines)
    TARGET_FILE.write_text(content, encoding='utf-8')

    print(f"✅ Súbor upravený: {TARGET_FILE}")
    print(f"   Pôvodné riadky: {len(lines)}")
    print(f"   Nové riadky: {len(new_lines)}")
    print("\nPridané importy:")
    print("  ✅ from utils.constants import WINDOW_MAIN")
    print("  ✅ from utils.window_settings import load_window_settings, save_window_settings")
    print("\nSkús spustiť aplikáciu znova")


if __name__ == "__main__":
    main()