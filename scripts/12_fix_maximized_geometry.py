#!/usr/bin/env python3
"""
Fix Maximized Geometry
=======================
Session: 2025-12-05
Location: scripts/12_fix_maximized_geometry.py

Pri maximalizovanom okne ukladá normalGeometry() namiesto geometry().
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
TARGET = PROJECT_ROOT / "apps/supplier-invoice-editor/src/ui/main_window.py"


def fix_maximized_geometry():
    """Opraví closeEvent aby používal normalGeometry() pre maximalizované okno"""

    print("=" * 80)
    print("FIX MAXIMIZED GEOMETRY")
    print("=" * 80)

    with open(TARGET, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    print("\n1. Upravujem closeEvent()...")

    # Starý kód - používa self.x(), self.y()
    old_code = """        # Validuj pozíciu pred uložením
        x, y = self.x(), self.y()
        width, height = self.width(), self.height()"""

    # Nový kód - pri maximalizovanom použije normalGeometry()
    new_code = """        # Validuj pozíciu pred uložením
        # Pri maximalizovanom okne použiť normalGeometry() (pozícia pred maximalizáciou)
        if self.isMaximized():
            norm_geom = self.normalGeometry()
            x, y = norm_geom.x(), norm_geom.y()
            width, height = norm_geom.width(), norm_geom.height()
        else:
            x, y = self.x(), self.y()
            width, height = self.width(), self.height()"""

    if old_code in content:
        content = content.replace(old_code, new_code)
        print("   ✅ closeEvent() opravený")
    else:
        print("   ⚠️  Pattern nenájdený")
        return False

    # Kontrola
    if content == original:
        print("\n   ❌ Žiadne zmeny")
        return False

    # Ulož
    print("\n2. Ukladám...")
    with open(TARGET, 'w', encoding='utf-8') as f:
        f.write(content)

    print("   ✅ Uložené")

    print("\n" + "=" * 80)
    print("✅ HOTOVO - Maximized Geometry Fixed")
    print("=" * 80)
    print("\nZmeny:")
    print("  • Pri maximalizovanom okne ukladá normalGeometry()")
    print("  • Validné súradnice aj pre maximalizované okno")

    print("\n" + "=" * 80)
    print("TEST:")
    print("=" * 80)
    print("1. Spusti aplikáciu")
    print("2. Maximalizuj (Windows + ↑)")
    print("3. Zatvor (ESC)")
    print("4. Log by mal ukazovať: 'Window settings saved: ... maximized'")
    print("5. Spusti znovu - malo by sa otvoriť maximalizované")
    print("=" * 80)

    return True


if __name__ == "__main__":
    success = fix_maximized_geometry()
    exit(0 if success else 1)