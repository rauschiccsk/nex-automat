#!/usr/bin/env python3
"""
Script 31: Show actual content around line 183
Display raw content to see what's really there
"""

from pathlib import Path

# Target file
MAIN_WINDOW = Path("apps/supplier-invoice-editor/src/ui/main_window.py")


def main():
    """Show actual line content"""
    print("=" * 60)
    print("Showing actual content around line 183")
    print("=" * 60)

    if not MAIN_WINDOW.exists():
        print(f"❌ ERROR: File not found: {MAIN_WINDOW}")
        return False

    content = MAIN_WINDOW.read_text(encoding='utf-8')
    lines = content.split('\n')

    print(f"\nTotal lines: {len(lines)}")
    print("\n📝 Lines 175-190:")
    for i in range(174, min(190, len(lines))):
        marker = " >>>>" if i == 182 else "     "
        line = lines[i]
        # Show repr to see escape sequences
        print(f"{marker} {i + 1:3d}: {line}")
        if i == 182:
            print(f"          repr: {repr(line)}")

    # Try to compile and show exact error
    print("\n🔍 Trying to compile...")
    try:
        compile(content, str(MAIN_WINDOW), 'exec')
        print("✅ No syntax errors!")
    except SyntaxError as e:
        print(f"❌ Syntax error at line {e.lineno}: {e.msg}")
        if e.text:
            print(f"   Text: {e.text}")
            print(f"   Repr: {repr(e.text)}")

        # Show the problematic line
        if 0 < e.lineno <= len(lines):
            prob_line = lines[e.lineno - 1]
            print(f"\n   Problematic line {e.lineno}:")
            print(f"   Content: {prob_line}")
            print(f"   Repr: {repr(prob_line)}")

    print("\n" + "=" * 60)

    return True


if __name__ == "__main__":
    main()