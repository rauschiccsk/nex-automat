"""
Fix: Oprava invoice_items_grid.py - odstránenie hardcoded column widths
Location: C:\Development\nex-automat\scripts\10_fix_invoice_items_grid.py
"""
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).parent
DEV_ROOT = SCRIPT_DIR.parent
WIDGET_FILE = DEV_ROOT / "apps" / "supplier-invoice-editor" / "src" / "ui" / "widgets" / "invoice_items_grid.py"


def fix_widget():
    """Odstráň _setup_custom_ui() volanie z __init__"""

    print("=" * 80)
    print("FIX: invoice_items_grid.py")
    print("=" * 80)

    with open(WIDGET_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Find and comment out _setup_custom_ui() call and the method itself
    new_lines = []
    in_setup_method = False
    method_indent = None

    for i, line in enumerate(lines):
        # Check if this is the call to _setup_custom_ui
        if '        self._setup_custom_ui()' in line:
            new_lines.append('        # REMOVED: self._setup_custom_ui() - BaseGrid loads settings from DB\n')
            print(f"✓ Line {i + 1}: Commented out _setup_custom_ui() call")
            continue

        # Check if this is the start of _setup_custom_ui method
        if '    def _setup_custom_ui(self):' in line:
            in_setup_method = True
            method_indent = len(line) - len(line.lstrip())
            new_lines.append('    # REMOVED: _setup_custom_ui() - BaseGrid loads settings from DB\n')
            new_lines.append('    # If you need default widths, set them in first run only\n')
            print(f"✓ Line {i + 1}: Commented out _setup_custom_ui() method definition")
            continue

        # Skip lines in _setup_custom_ui method
        if in_setup_method:
            current_indent = len(line) - len(line.lstrip())
            # If we hit another method or class-level code, exit
            if line.strip() and current_indent <= method_indent:
                in_setup_method = False
                new_lines.append(line)
            else:
                # Skip this line (part of _setup_custom_ui)
                if line.strip():  # Only log non-empty lines
                    print(f"  Skipped line {i + 1}: {line.strip()[:60]}...")
                continue
        else:
            new_lines.append(line)

    # Write back
    with open(WIDGET_FILE, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

    print(f"\n✓ File updated: {WIDGET_FILE.relative_to(DEV_ROOT)}")
    print("\nTeraz:")
    print("  1. Vymaž databázu: del C:\\NEX\\YEARACT\\SYSTEM\\SQLITE\\grid_settings.db")
    print("  2. Spusti aplikáciu")
    print("  3. Nastav šírky podľa potreby v OBOCH gridoch")
    print("  4. Zatvor a znova spusti - VŠETKO by malo fungovať")


if __name__ == "__main__":
    fix_widget()