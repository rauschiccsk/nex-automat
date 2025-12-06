#!/usr/bin/env python3
"""
Script 27: Remove self.config = config from wrong places
It should only be in __init__, not in _load_invoices
"""

from pathlib import Path

# Target file
MAIN_WINDOW = Path("apps/supplier-invoice-editor/src/ui/main_window.py")


def main():
    """Remove misplaced self.config = config lines"""
    print("=" * 60)
    print("Removing self.config = config from wrong places")
    print("=" * 60)

    if not MAIN_WINDOW.exists():
        print(f"❌ ERROR: File not found: {MAIN_WINDOW}")
        return False

    content = MAIN_WINDOW.read_text(encoding='utf-8')
    lines = content.split('\n')

    # Find and remove self.config = config lines that are NOT in __init__
    in_init = False
    cleaned_lines = []

    for i, line in enumerate(lines):
        # Track if we're in __init__
        if 'def __init__' in line:
            in_init = True
        elif line.strip().startswith('def ') and in_init:
            in_init = False

        # Skip self.config = config if NOT in __init__
        if 'self.config = config' in line and not in_init:
            print(f"   Removing line {i + 1}: {line.strip()}")
            continue

        cleaned_lines.append(line)

    # Write cleaned content
    new_content = '\n'.join(cleaned_lines)
    MAIN_WINDOW.write_text(new_content, encoding='utf-8')

    print("\n✅ Removed misplaced self.config = config lines")

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
    print("ÚSPECH: Syntax fixed")
    print("=" * 60)
    print("\nNext step: Test application")
    print("cd apps/supplier-invoice-editor")
    print("python main.py")

    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)