"""
Fix: set_active_column() v quick_search.py - pridať header highlight
Location: C:\Development\nex-automat\scripts\11_fix_active_column_highlight.py
"""
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).parent
DEV_ROOT = SCRIPT_DIR.parent
QUICK_SEARCH = DEV_ROOT / "apps" / "supplier-invoice-editor" / "src" / "ui" / "widgets" / "quick_search.py"


def fix_highlight():
    """Oprav set_active_column() aby aktualizoval header"""

    print("=" * 80)
    print("FIX: quick_search.py - set_active_column()")
    print("=" * 80)

    with open(QUICK_SEARCH, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find set_active_column method and fix it
    old_method = '''    def set_active_column(self, column):
        """
        Nastaví aktívny stĺpec a aktualizuje UI.

        Args:
            column: Index stĺpca
        """
        if 0 <= column < self.table_view.model().columnCount():
            self.current_column = column
            self._sort_by_column(column)
            self.search_container.set_column(column)
            self.logger.info(f"Active column set to {column}")'''

    new_method = '''    def set_active_column(self, column):
        """
        Nastaví aktívny stĺpec a aktualizuje UI.

        Args:
            column: Index stĺpca
        """
        model = self.table_view.model()
        if model and 0 <= column < model.columnCount():
            self.current_column = column
            self._sort_by_column(column)
            self.search_container.set_column(column)
            # IMPORTANT: Update header highlight
            self.search_container._highlight_header(column)
            self.logger.info(f"Active column set to {column} with header highlight")'''

    if old_method in content:
        content = content.replace(old_method, new_method)
        print("✓ Opravená set_active_column() - pridaný _highlight_header() call")
    else:
        print("❌ Nenašiel som očakávanú set_active_column() metódu")
        print("Skúsim alternatívny pattern...")

        # Try alternative pattern
        old_alt = '''            self.search_container.set_column(column)
            self.logger.info(f"Active column set to {column}")'''

        new_alt = '''            self.search_container.set_column(column)
            # IMPORTANT: Update header highlight
            self.search_container._highlight_header(column)
            self.logger.info(f"Active column set to {column} with header highlight")'''

        if old_alt in content:
            content = content.replace(old_alt, new_alt)
            print("✓ Opravená set_active_column() - pridaný _highlight_header() call (alt pattern)")
        else:
            print("❌ Ani alternatívny pattern nezapadá!")
            return False

    # Write back
    with open(QUICK_SEARCH, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"\n✓ File updated: {QUICK_SEARCH.relative_to(DEV_ROOT)}")
    print("\nTeraz:")
    print("  1. Vymaž DB: del C:\\NEX\\YEARACT\\SYSTEM\\SQLITE\\grid_settings.db")
    print("  2. Spusti aplikáciu")
    print("  3. Šípkami zmeň active column v oboch gridoch (zelený header)")
    print("  4. Zatvor a znova spusti - zelené headery by mali sedieť")
    return True


if __name__ == "__main__":
    fix_highlight()