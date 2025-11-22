"""
Diagnose Pillow Import Issue
=============================
Zistí prečo pillow import zlyháva napriek "pip install pillow" success.

Usage:
    cd C:\\Development\\nex-automat
    python scripts\\diagnose_pillow_import.py
"""

import sys
import site
from pathlib import Path

print("=" * 70)
print("  PILLOW IMPORT DIAGNOSIS")
print("=" * 70)

print(f"\nPython: {sys.executable}")
print(f"Version: {sys.version}")

# Test 1: Try importing PIL (not pillow!)
print("\n" + "=" * 70)
print("  TEST 1: IMPORT PIL (not pillow)")
print("=" * 70)

try:
    import PIL

    print(f"✅ PIL imported successfully")
    print(f"   Version: {PIL.__version__}")
    print(f"   Location: {PIL.__file__}")
except ImportError as e:
    print(f"❌ PIL import failed: {e}")

    # Check if Pillow package exists in site-packages
    print("\nSearching site-packages...")
    for sp in site.getsitepackages():
        sp_path = Path(sp)
        if not sp_path.exists():
            continue

        pil_dir = sp_path / "PIL"
        pillow_dist = list(sp_path.glob("Pillow-*.dist-info"))
        pillow_egg = list(sp_path.glob("Pillow-*.egg-info"))

        print(f"\n  Site-packages: {sp}")
        print(f"    PIL dir: {'✅ EXISTS' if pil_dir.exists() else '❌ NOT FOUND'}")
        print(f"    Pillow dist-info: {len(pillow_dist)} found")
        print(f"    Pillow egg-info: {len(pillow_egg)} found")

        if pil_dir.exists():
            print(f"    PIL directory contents:")
            pil_files = list(pil_dir.glob("*.py"))[:5]
            for f in pil_files:
                print(f"      - {f.name}")

# Test 2: Try the way test script imports it
print("\n" + "=" * 70)
print("  TEST 2: IMPORT METHOD USED IN TEST SCRIPT")
print("=" * 70)

try:
    __import__("pillow")
    print("✅ __import__('pillow') successful")
except ImportError as e:
    print(f"❌ __import__('pillow') failed: {e}")
    print("\n⚠️  FOUND THE ISSUE!")
    print("   Test script uses: __import__('pillow')")
    print("   Correct import is: import PIL")
    print("   Package name: pillow")
    print("   Import name: PIL")

# Test 3: Verify pillow is actually installed
print("\n" + "=" * 70)
print("  TEST 3: VERIFY PILLOW PACKAGE")
print("=" * 70)

try:
    import importlib.metadata

    version = importlib.metadata.version('pillow')
    print(f"✅ Pillow package version: {version}")
except Exception as e:
    print(f"❌ Could not get pillow version: {e}")

# Summary
print("\n" + "=" * 70)
print("  SUMMARY")
print("=" * 70)

print("\n🔍 ROOT CAUSE:")
print("   Test script uses: __import__('pillow')")
print("   Correct usage: import PIL (or __import__('PIL'))")
print("\n💡 SOLUTION:")
print("   Fix test script to use 'PIL' instead of 'pillow'")
print("   Package name ≠ Import name for Pillow!")