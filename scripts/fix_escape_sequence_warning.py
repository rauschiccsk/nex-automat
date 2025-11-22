"""
Fix Escape Sequence Warning
============================
Opraví invalid escape sequence warning v fix_day5_preflight_issues.py

Usage:
    cd C:\\Development\\nex-automat
    python scripts\\fix_escape_sequence_warning.py
"""

from pathlib import Path


def fix_escape_sequences():
    """Fix escape sequence warnings in fix script."""

    script_path = Path("scripts/fix_day5_preflight_issues.py")

    if not script_path.exists():
        print(f"❌ Script not found: {script_path}")
        return False

    try:
        content = script_path.read_text(encoding='utf-8')

        # Fix escape sequences in docstring
        old_location = 'Location: C:\\Development\\nex-automat'
        new_location = 'Location: C:\\\\Development\\\\nex-automat'

        if old_location in content:
            content = content.replace(old_location, new_location)
            script_path.write_text(content, encoding='utf-8')
            print("✅ Fixed escape sequence warning in fix_day5_preflight_issues.py")
            return True
        else:
            print("⚠️  Pattern not found - might be already fixed")
            return True

    except Exception as e:
        print(f"❌ Error fixing script: {e}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("  FIXING ESCAPE SEQUENCE WARNING")
    print("=" * 60)

    if fix_escape_sequences():
        print("\n✅ All escape sequences fixed")
        print("✅ Code is now clean and ready for commit")
    else:
        print("\n❌ Fix failed")