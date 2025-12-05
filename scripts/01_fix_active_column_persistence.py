#!/usr/bin/env python3
"""
Fix Active Column Persistence - Grid Settings
==============================================

Location: scripts/01_fix_active_column_persistence.py

Opraví ukladanie a načítanie aktívneho stĺpca v grid settings.

Problém:
- Controller sa volá `self.search_controller`
- Ale kód používa neexistujúci `self.quick_search`

Riešenie:
- Opraviť odkazy z `self.quick_search` na `self.search_controller`
"""

from pathlib import Path
import sys

# Get project root
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Cesta k súboru
TARGET_FILE = PROJECT_ROOT / "apps" / "supplier-invoice-editor" / "src" / "ui" / "widgets" / "invoice_list_widget.py"


def fix_active_column_persistence():
    """Opraví odkazy na search controller."""

    print("=" * 80)
    print("FIX ACTIVE COLUMN PERSISTENCE")
    print("=" * 80)

    # 1. Načítaj súbor
    print(f"\n1. Načítavam: {TARGET_FILE}")

    if not TARGET_FILE.exists():
        print(f"❌ Súbor neexistuje: {TARGET_FILE}")
        return False

    with open(TARGET_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    print(f"✅ Súbor načítaný ({len(content)} znakov)")

    # 2. Vytvor backup
    backup_file = TARGET_FILE.with_suffix('.py.backup_active_column')
    print(f"\n2. Vytváram backup: {backup_file.name}")

    with open(backup_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ Backup vytvorený")

    # 3. Opravy
    print(f"\n3. Aplikujem opravy...")

    fixes = []

    # Fix 1: Riadok ~295 - načítanie aktívneho stĺpca
    old_code_1 = """if grid_settings and 'active_column' in grid_settings:
            active_col = grid_settings['active_column']
            # Nastav aktívny stĺpec v quick search
            if hasattr(self, 'quick_search') and self.quick_search:
                self.quick_search.set_active_column(active_col)"""

    new_code_1 = """if grid_settings and 'active_column' in grid_settings:
            active_col = grid_settings['active_column']
            # Nastav aktívny stĺpec v quick search
            if hasattr(self, 'search_controller') and self.search_controller:
                self.search_controller.set_active_column(active_col)
                self.logger.info(f"Loaded active column: {active_col}")"""

    if old_code_1 in content:
        content = content.replace(old_code_1, new_code_1)
        fixes.append("Fix 1: Načítanie aktívneho stĺpca (riadok ~295)")
        print("  ✅ Fix 1: Načítanie aktívneho stĺpca")
    else:
        print("  ⚠️  Fix 1: Pattern nenájdený")

    # Fix 2: Riadok ~317 - ukladanie aktívneho stĺpca
    old_code_2 = """# Zozbieraj grid settings (active column)
        active_column = None
        if hasattr(self, 'quick_search') and self.quick_search:
            active_column = self.quick_search.get_active_column()"""

    new_code_2 = """# Zozbieraj grid settings (active column)
        active_column = None
        if hasattr(self, 'search_controller') and self.search_controller:
            active_column = self.search_controller.get_active_column()
            self.logger.info(f"Saving active column: {active_column}")"""

    if old_code_2 in content:
        content = content.replace(old_code_2, new_code_2)
        fixes.append("Fix 2: Ukladanie aktívneho stĺpca (riadok ~317)")
        print("  ✅ Fix 2: Ukladanie aktívneho stĺpca")
    else:
        print("  ⚠️  Fix 2: Pattern nenájdený")

    # 4. Ulož opravený súbor
    print(f"\n4. Ukladám opravený súbor...")

    with open(TARGET_FILE, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ Súbor uložený: {TARGET_FILE}")

    # 5. Zhrnutie
    print("\n" + "=" * 80)
    print("✅ HOTOVO - Active Column Persistence FIXED")
    print("=" * 80)
    print(f"\nAplikované opravy:")
    for fix in fixes:
        print(f"  • {fix}")

    print(f"\nBackup: {backup_file}")
    print(f"Fixed:  {TARGET_FILE}")

    print("\n" + "=" * 80)
    print("TESTOVANIE:")
    print("=" * 80)
    print("1. Spusti aplikáciu")
    print("2. Zmeň aktívny stĺpec (←/→ šípky)")
    print("3. Zatvor aplikáciu")
    print("4. Znovu spusti aplikáciu")
    print("5. Over že aktívny stĺpec zostal rovnaký (zelený header)")
    print("=" * 80)

    return True


if __name__ == "__main__":
    success = fix_active_column_persistence()
    exit(0 if success else 1)