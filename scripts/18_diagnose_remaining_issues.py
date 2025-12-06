#!/usr/bin/env python3
"""
Script 18: Diagnose remaining issues
Find self.config usages and closeEvent implementation
"""

from pathlib import Path
import re

# Target files
INVOICE_SERVICE = Path("apps/supplier-invoice-editor/src/business/invoice_service.py")
MAIN_WINDOW = Path("apps/supplier-invoice-editor/src/ui/main_window.py")


def find_config_usages(file_path: Path):
    """Find all self.config usages in file"""
    if not file_path.exists():
        print(f"⚠️  File not found: {file_path}")
        return

    content = file_path.read_text(encoding='utf-8')

    # Find self.config usages
    matches = re.findall(r'self\.config\.[a-zA-Z_][a-zA-Z0-9_.]*', content)

    if matches:
        print(f"\n📝 {file_path.name} - Found {len(matches)} self.config usages:")
        for match in sorted(set(matches)):
            # Find line number
            for i, line in enumerate(content.split('\n'), 1):
                if match in line:
                    print(f"   Line {i:3d}: {match}")
                    print(f"            {line.strip()}")
                    break
    else:
        print(f"\n✅ {file_path.name} - No self.config usages")


def find_close_event(file_path: Path):
    """Find closeEvent implementation"""
    if not file_path.exists():
        print(f"⚠️  File not found: {file_path}")
        return

    content = file_path.read_text(encoding='utf-8')

    # Find closeEvent method
    match = re.search(r'def closeEvent\(self[^)]*\):.*?(?=\n    def |\Z)', content, re.DOTALL)

    if match:
        print(f"\n📝 {file_path.name} - closeEvent implementation:")
        lines = match.group(0).split('\n')
        for i, line in enumerate(lines[:20]):
            print(f"   {line}")
        if len(lines) > 20:
            print(f"   ... and {len(lines) - 20} more lines")
    else:
        print(f"\n⚠️  {file_path.name} - No closeEvent found")


def main():
    """Diagnose remaining issues"""
    print("=" * 60)
    print("Diagnosing remaining issues")
    print("=" * 60)

    # Check for self.config usages
    print("\n" + "=" * 60)
    print("1. Checking for self.config usages")
    print("=" * 60)
    find_config_usages(INVOICE_SERVICE)
    find_config_usages(MAIN_WINDOW)

    # Check closeEvent
    print("\n" + "=" * 60)
    print("2. Checking closeEvent implementation")
    print("=" * 60)
    find_close_event(MAIN_WINDOW)

    print("\n" + "=" * 60)
    print("DIAGNOSIS COMPLETE")
    print("=" * 60)

    return True


if __name__ == "__main__":
    main()