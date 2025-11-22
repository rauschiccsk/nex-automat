"""
Fix Manage Service Complete
============================
1. Opraví emoji v manage_service.py (Development)
2. Pridá manage_service.py do deploy scriptu
3. Pripraví na redeploy

Usage:
    cd C:\\Development\\nex-automat
    python scripts\\fix_manage_service_complete.py
"""

from pathlib import Path
import re


def print_section(title: str):
    """Print section header."""
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print(f"{'=' * 70}")


def fix_emoji_in_manage_service() -> bool:
    """Remove emoji from manage_service.py prints."""
    print_section("1. FIXING EMOJI IN MANAGE_SERVICE.PY")

    script_path = Path("scripts/manage_service.py")

    if not script_path.exists():
        print(f"❌ Not found: {script_path}")
        return False

    try:
        content = script_path.read_text(encoding='utf-8')
        original_content = content

        # Find all print statements with emojis
        # Look for f-strings with unicode escapes or actual emojis

        # Replace unicode escape sequences
        patterns = [
            (r'f"\\u26a0\\ufe0f\s+{', 'f"WARNING: {'),
            (r'f"\\u2705\s+{', 'f"OK: {'),
            (r'f"\\u274c\s+{', 'f"ERROR: {'),
            (r'\\u26a0\\ufe0f', 'WARNING:'),
            (r'\\u2705', 'OK:'),
            (r'\\u274c', 'ERROR:'),
        ]

        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content)

        # Replace actual emoji characters
        emoji_replacements = {
            '⚠️': 'WARNING:',
            '✅': 'OK:',
            '❌': 'ERROR:',
            '🟢': '[OK]',
            '🔴': '[ERROR]',
            '🟡': '[WARNING]',
        }

        for emoji, text in emoji_replacements.items():
            if emoji in content:
                content = content.replace(emoji, text)
                print(f"  Replaced: {emoji} → {text}")

        if content != original_content:
            script_path.write_text(content, encoding='utf-8')
            print("\n✅ Emoji replaced with ASCII in manage_service.py")
            return True
        else:
            print("\n⚠️  No emojis found to replace")
            # Check if file actually contains problematic code
            if 'print(f"' in content:
                print("  File contains print statements, checking line 173...")
                lines = content.split('\n')
                if len(lines) > 172:
                    line_173 = lines[172]
                    print(f"  Line 173: {repr(line_173)}")
            return False

    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def add_manage_service_to_deploy() -> bool:
    """Add manage_service.py to deploy script."""
    print_section("2. UPDATING DEPLOY SCRIPT")

    deploy_script = Path("scripts/deploy_to_deployment.py")

    if not deploy_script.exists():
        print(f"❌ Not found: {deploy_script}")
        return False

    try:
        content = deploy_script.read_text(encoding='utf-8')

        # Check if manage_service.py already in list
        if '"scripts/manage_service.py"' in content or "'scripts/manage_service.py'" in content:
            print("✅ manage_service.py already in deploy list")
            return True

        # Find files_to_deploy list and add manage_service.py
        # Look for the list definition
        files_section_start = content.find('files_to_deploy = [')

        if files_section_start == -1:
            print("❌ Could not find files_to_deploy list")
            return False

        # Find the first item after "# Core preflight scripts"
        insert_pos = content.find('"scripts/day5_preflight_check.py"', files_section_start)

        if insert_pos == -1:
            print("❌ Could not find insertion point")
            return False

        # Insert manage_service.py before day5_preflight_check.py
        insertion = '        # Service management\n        "scripts/manage_service.py",\n        \n'

        content = content[:insert_pos] + insertion + content[insert_pos:]

        deploy_script.write_text(content, encoding='utf-8')
        print("✅ Added manage_service.py to deploy list")
        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """Run all fixes."""
    print("=" * 70)
    print("  FIX MANAGE_SERVICE.PY - COMPLETE")
    print("=" * 70)

    print("\nIssue: UnicodeEncodeError when printing emoji in cp1250")
    print("Solution: Replace all emoji with ASCII text")

    results = {
        "Fix Emoji": fix_emoji_in_manage_service(),
        "Update Deploy Script": add_manage_service_to_deploy()
    }

    print_section("SUMMARY")

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for check, result in results.items():
        icon = "✅" if result else "❌"
        print(f"{icon} {check}")

    if passed >= 1:  # At least deploy script updated
        print("\n" + "=" * 70)
        print("  NEXT STEPS")
        print("=" * 70)
        print("\n1. Redeploy to Deployment:")
        print("   python scripts\\deploy_to_deployment.py")
        print("\n2. Test service status:")
        print("   cd C:\\Deployment\\nex-automat")
        print("   python scripts\\manage_service.py status")
        print("\n3. Run preflight check:")
        print("   python scripts\\day5_preflight_check.py")
        return True
    else:
        print("\n❌ Fixes failed")
        return False


if __name__ == "__main__":
    import sys

    sys.exit(0 if main() else 1)