#!/usr/bin/env python3
"""
Script 05: Smart fix for main_window.py
Intelligently removes sys.path blocks while preserving code structure
"""

from pathlib import Path

# Target file
MAIN_WINDOW = Path("apps/supplier-invoice-editor/src/ui/main_window.py")


def smart_fix_main_window(content: str) -> str:
    """
    Intelligently remove sys.path manipulation blocks
    Handles if __name__ == '__main__' blocks that contain only sys.path code
    """
    lines = content.split('\n')
    result = []
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Detect if block with sys.path code
        if stripped.startswith('if ') and '__name__' in stripped and '__main__' in stripped:
            # This is: if __name__ == '__main__':
            # Check if next lines are only sys.path related
            block_start = i
            i += 1
            block_lines = []

            # Collect indented block
            if i < len(lines):
                base_indent = len(lines[i]) - len(lines[i].lstrip())

                while i < len(lines):
                    curr_line = lines[i]
                    curr_stripped = curr_line.strip()

                    # Empty line
                    if not curr_stripped:
                        block_lines.append(curr_line)
                        i += 1
                        continue

                    # Check indent
                    curr_indent = len(curr_line) - len(curr_line.lstrip())

                    # End of block
                    if curr_indent < base_indent and curr_stripped:
                        break

                    # Line in block
                    block_lines.append(curr_line)
                    i += 1

                # Analyze block - is it only sys.path related?
                code_lines = [l for l in block_lines if l.strip() and not l.strip().startswith('#')]
                sys_path_only = all(
                    'sys.path' in l or 'import sys' in l or 'from pathlib import Path' in l or 'Path(' in l
                    for l in code_lines
                )

                if sys_path_only:
                    # Skip entire if __name__ == '__main__' block
                    continue
                else:
                    # Keep the if block
                    result.append(lines[block_start])
                    result.extend(block_lines)
            else:
                # Empty if block, skip it
                continue

        # Regular line - check if it's sys.path related at module level
        elif 'sys.path' in stripped or (stripped == 'import sys' and i + 1 < len(lines) and 'sys.path' in lines[i + 1]):
            # Skip sys.path lines at module level
            i += 1
            continue

        # Keep regular line
        else:
            result.append(line)
            i += 1

    # Clean up excessive empty lines
    cleaned = '\n'.join(result)
    while '\n\n\n' in cleaned:
        cleaned = cleaned.replace('\n\n\n', '\n\n')

    return cleaned


def main():
    """Fix main_window.py file"""
    print("=" * 60)
    print("Smart fixing main_window.py")
    print("=" * 60)

    if not MAIN_WINDOW.exists():
        print(f"❌ ERROR: File not found: {MAIN_WINDOW}")
        return False

    # Read current content
    current = MAIN_WINDOW.read_text(encoding='utf-8')
    print(f"\n📝 Current file size: {len(current)} chars")
    print(f"📝 Current lines: {len(current.splitlines())}")

    # Apply smart fix
    fixed = smart_fix_main_window(current)

    # Update import if needed
    if 'from ui.base_window import BaseWindow' in fixed:
        fixed = fixed.replace(
            'from ui.base_window import BaseWindow',
            'from nex_shared.ui import BaseWindow'
        )
        print("✅ Updated BaseWindow import to nex_shared")

    # Write fixed content
    MAIN_WINDOW.write_text(fixed, encoding='utf-8')
    print(f"✅ Fixed: {MAIN_WINDOW}")

    # Verify
    new_content = MAIN_WINDOW.read_text(encoding='utf-8')
    print(f"✅ New file size: {len(new_content)} chars")
    print(f"✅ New lines: {len(new_content.splitlines())}")

    # Check syntax
    try:
        compile(new_content, str(MAIN_WINDOW), 'exec')
        print("✅ Python syntax valid")
    except SyntaxError as e:
        print(f"❌ Syntax error at line {e.lineno}: {e.msg}")
        print(f"   Text: {e.text}")
        return False

    print("\n" + "=" * 60)
    print("ÚSPECH: main_window.py fixed")
    print("=" * 60)
    print("\nNext step: Test application")
    print("cd apps/supplier-invoice-editor")
    print("python main.py")

    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)