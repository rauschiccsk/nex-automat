#!/usr/bin/env python3
"""
Script 12: Diagnose MainWindow initialization
Check what MainWindow.__init__ expects
"""

from pathlib import Path
import re

# Target file
MAIN_WINDOW = Path("apps/supplier-invoice-editor/src/ui/main_window.py")
SRC_DIR = Path("apps/supplier-invoice-editor/src")


def extract_init_signature(content: str) -> str:
    """Extract __init__ method signature"""
    # Find __init__ method
    pattern = r'def __init__\(self[^)]*\):'
    match = re.search(pattern, content)
    if match:
        return match.group(0)
    return None


def list_src_modules():
    """List all Python modules in src/"""
    modules = []
    for py_file in SRC_DIR.rglob("*.py"):
        if '__pycache__' in str(py_file):
            continue
        rel_path = py_file.relative_to(SRC_DIR)
        modules.append(str(rel_path))
    return sorted(modules)


def main():
    """Diagnose MainWindow initialization"""
    print("=" * 60)
    print("Diagnosing MainWindow initialization")
    print("=" * 60)

    # Check if main_window.py exists
    if not MAIN_WINDOW.exists():
        print(f"❌ ERROR: File not found: {MAIN_WINDOW}")
        return False

    # Read and analyze MainWindow
    content = MAIN_WINDOW.read_text(encoding='utf-8')

    # Extract __init__ signature
    init_sig = extract_init_signature(content)
    if init_sig:
        print(f"\n📝 MainWindow.__init__ signature:")
        print(f"   {init_sig}")
    else:
        print("\n⚠️  Could not find __init__ signature")

    # Check for parent class
    if 'class MainWindow(BaseWindow)' in content:
        print("\n✅ MainWindow extends BaseWindow")
        print("   → BaseWindow.__init__ expects (parent=None)")
    elif 'class MainWindow(QMainWindow)' in content:
        print("\n✅ MainWindow extends QMainWindow")

    # List src modules
    print("\n📁 Available modules in src/:")
    modules = list_src_modules()
    for module in modules[:20]:  # Show first 20
        print(f"   - {module}")
    if len(modules) > 20:
        print(f"   ... and {len(modules) - 20} more")

    # Check if config.py exists
    config_file = SRC_DIR / "config.py"
    if config_file.exists():
        print(f"\n✅ Found: {config_file}")
    else:
        print(f"\n❌ NOT FOUND: {config_file}")

    # Check imports in MainWindow
    print("\n📋 Imports in main_window.py:")
    imports = [line.strip() for line in content.split('\n')
               if line.strip().startswith('from') or line.strip().startswith('import')]
    for imp in imports[:15]:
        print(f"   {imp}")

    print("\n" + "=" * 60)
    print("DIAGNOSIS COMPLETE")
    print("=" * 60)

    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)