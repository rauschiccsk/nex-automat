#!/usr/bin/env python3
"""
Script 02: Verify nex-shared package installation
Overí, či aplikácia používa správnu verziu base_window.py
"""

import sys
import importlib.util
from pathlib import Path


def verify_package():
    """Overí, odkiaľ sa importuje nex_shared a či je to editable install"""

    print("=" * 80)
    print("NEX-SHARED PACKAGE VERIFICATION")
    print("=" * 80)

    # 1. Skús importovať nex_shared
    try:
        import nex_shared.ui.base_window as bw
        print(f"✓ nex_shared.ui.base_window imported successfully")
        print(f"  Location: {bw.__file__}")

        # Overenie, či je to z Development alebo z site-packages
        if "Development\\nex-automat\\packages" in bw.__file__:
            print(f"  ✅ CORRECT: Importing from Development (editable install)")
        elif "site-packages" in bw.__file__:
            print(f"  ⚠️  WARNING: Importing from site-packages (not editable!)")
        else:
            print(f"  ❓ UNKNOWN: Unexpected location")

        # 2. Overenie obsahu _save_settings metódy
        source_file = Path(bw.__file__)
        if source_file.exists():
            content = source_file.read_text(encoding='utf-8')

            has_always_save = "ALWAYS save" in content
            has_correct_logic = "width, height = self.width(), self.height()" in content

            print(f"\n📊 Code verification:")
            print(f"  ✓ Contains 'ALWAYS save' comment: {has_always_save}")
            print(f"  ✓ Contains 'width, height = self.width(), self.height()': {has_correct_logic}")

            if has_always_save and has_correct_logic:
                print(f"  ✅ Code is CORRECT in imported module")
            else:
                print(f"  ❌ Code is OUTDATED in imported module!")
                print(f"     → Need to reinstall: pip install -e packages/nex-shared")

    except ImportError as e:
        print(f"❌ Failed to import nex_shared: {e}")
        print(f"   → Need to install: pip install -e packages/nex-shared")

    # 3. Overenie pip list
    print(f"\n" + "=" * 80)
    print("PIP LIST CHECK:")
    print("=" * 80)
    import subprocess
    result = subprocess.run(
        [sys.executable, "-m", "pip", "list"],
        capture_output=True,
        text=True
    )

    for line in result.stdout.split('\n'):
        if 'nex-shared' in line.lower():
            print(f"  {line}")
            if 'editable' in line.lower() or 'Development' in line:
                print(f"  ✅ Installed as editable")
            else:
                print(f"  ⚠️  Not editable - should reinstall!")


if __name__ == "__main__":
    verify_package()