#!/usr/bin/env python3
"""
Script 30: Patch f-string literal error
Direct fix for line with escaped newlines
"""

from pathlib import Path

# Target file
MAIN_WINDOW = Path("apps/supplier-invoice-editor/src/ui/main_window.py")


def main():
    """Patch f-string error"""
    print("=" * 60)
    print("Patching f-string literal error")
    print("=" * 60)

    if not MAIN_WINDOW.exists():
        print(f"❌ ERROR: File not found: {MAIN_WINDOW}")
        return False

    # Read file
    content = MAIN_WINDOW.read_text(encoding='utf-8')

    # Replace the problematic line
    # Wrong: f"Nepodarilo sa načítať faktúry:\\n\\n{str(e)}"
    # Correct: f"Nepodarilo sa načítať faktúry:\n\n{str(e)}"

    # Try multiple possible wrong patterns
    patterns_to_fix = [
        (r'f"Nepodarilo sa načítať faktúry:\\n\\n{str\(e\)}"',
         r'f"Nepodarilo sa načítať faktúry:\n\n{str(e)}"'),
        (r"f'Nepodarilo sa načítať faktúry:\\n\\n{str\(e\)}'",
         r'f"Nepodarilo sa načítať faktúry:\n\n{str(e)}"'),
    ]

    import re
    fixed = False
    for old_pattern, new_text in patterns_to_fix:
        if re.search(old_pattern, content):
            content = re.sub(old_pattern, new_text, content)
            fixed = True
            print(f"✅ Fixed pattern: {old_pattern[:50]}...")
            break

    if not fixed:
        # Direct string replacement as fallback
        old_str = 'f"Nepodarilo sa načítať faktúry:\\n\\n{str(e)}"'
        new_str = 'f"Nepodarilo sa načítať faktúry:\n\n{str(e)}"'

        if old_str in content:
            content = content.replace(old_str, new_str)
            print(f"✅ Fixed via direct replacement")
            fixed = True

    if not fixed:
        print("⚠️  Could not find problematic f-string")
        # Show the actual line
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            if 'Nepodarilo sa načítať faktúry' in line and 'str(e)' in line:
                print(f"   Line {i}: {line}")
        return False

    # Write fixed content
    MAIN_WINDOW.write_text(content, encoding='utf-8')
    print(f"✅ Written: {MAIN_WINDOW}")

    # Verify syntax
    try:
        compile(content, str(MAIN_WINDOW), 'exec')
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