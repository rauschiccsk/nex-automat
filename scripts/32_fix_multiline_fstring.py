#!/usr/bin/env python3
"""
Script 32: Fix multiline f-string
Replace lines 183-185 with single-line f-string
"""

from pathlib import Path

# Target file
MAIN_WINDOW = Path("apps/supplier-invoice-editor/src/ui/main_window.py")


def main():
    """Fix multiline f-string"""
    print("=" * 60)
    print("Fixing multiline f-string")
    print("=" * 60)

    if not MAIN_WINDOW.exists():
        print(f"❌ ERROR: File not found: {MAIN_WINDOW}")
        return False

    content = MAIN_WINDOW.read_text(encoding='utf-8')
    lines = content.split('\n')

    # Find and fix lines 183-185
    # Line 183: f"Nepodarilo sa načítať faktúry:
    # Line 184: (empty)
    # Line 185: {str(e)}"

    # Replace with single line
    if 182 < len(lines):
        print(f"Original lines 183-185:")
        print(f"  183: {repr(lines[182])}")
        print(f"  184: {repr(lines[183])}")
        print(f"  185: {repr(lines[184])}")

        # Replace line 183 with correct f-string
        lines[182] = '                f"Nepodarilo sa načítať faktúry:\\n\\n{str(e)}"'

        # Remove lines 184-185 (they are part of the broken multiline string)
        del lines[183:185]

        print(f"\nFixed to:")
        print(f"  183: {repr(lines[182])}")

    # Reconstruct content
    new_content = '\n'.join(lines)

    # Write fixed content
    MAIN_WINDOW.write_text(new_content, encoding='utf-8')
    print(f"\n✅ Written: {MAIN_WINDOW}")

    # Verify syntax
    try:
        compile(new_content, str(MAIN_WINDOW), 'exec')
        print("✅ Python syntax valid")
    except SyntaxError as e:
        print(f"❌ Syntax error at line {e.lineno}: {e.msg}")
        if e.text:
            print(f"   {e.text.strip()}")
        return False

    print("\n" + "=" * 60)
    print("ÚSPECH: F-string fixed")
    print("=" * 60)
    print("\nNext step: Test application")
    print("cd apps/supplier-invoice-editor")
    print("python main.py")

    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)