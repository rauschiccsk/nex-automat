"""
Fix Manage Service Emoji Issue
===============================
Odstráni emoji z manage_service.py (Unicode encoding problém).

Usage:
    cd C:\\Development\\nex-automat
    python scripts\\fix_manage_service_emoji.py
"""

from pathlib import Path


def fix_manage_service():
    """Remove emojis from manage_service.py."""

    script_path = Path("scripts/manage_service.py")

    if not script_path.exists():
        print(f"❌ Not found: {script_path}")
        return False

    try:
        content = script_path.read_text(encoding='utf-8')

        # Find and replace emoji patterns
        replacements = [
            # Warning emoji
            (r'print(f"\u26a0\ufe0f  {status}")', 'print(f"⚠️  {status}")'),
            (r'print(f"\u26a0\ufe0f  {status}")', 'print(f"WARNING: {status}")'),
            ('\\u26a0\\ufe0f', '⚠️'),
            ('\\u26a0\\ufe0f', 'WARNING:'),

            # Check mark emoji
            ('\\u2705', '✅'),
            ('\\u2705', 'OK:'),

            # Cross mark emoji
            ('\\u274c', '❌'),
            ('\\u274c', 'ERROR:'),
        ]

        modified = False

        # Strategy 1: Replace unicode escapes with ASCII text
        if '\\u26a0' in content or '\\u2705' in content or '\\u274c' in content:
            print("Found unicode escape sequences")

            # Replace all emoji unicode escapes with ASCII
            content = content.replace('\\u26a0\\ufe0f', 'WARNING:')
            content = content.replace('\\u2705', 'OK:')
            content = content.replace('\\u274c', 'ERROR:')

            modified = True
            print("✅ Replaced unicode escapes with ASCII")

        # Strategy 2: Look for emoji characters directly
        emoji_chars = ['⚠️', '✅', '❌', '🟢', '🔴', '🟡']
        has_emoji = any(emoji in content for emoji in emoji_chars)

        if has_emoji:
            print("Found emoji characters")

            # Replace with ASCII alternatives
            content = content.replace('⚠️', 'WARNING:')
            content = content.replace('✅', 'OK:')
            content = content.replace('❌', 'ERROR:')
            content = content.replace('🟢', '[GREEN]')
            content = content.replace('🔴', '[RED]')
            content = content.replace('🟡', '[YELLOW]')

            modified = True
            print("✅ Replaced emoji chars with ASCII")

        if not modified:
            print("⚠️  No emoji found - may already be fixed")
            return True

        # Write back
        script_path.write_text(content, encoding='utf-8')

        print("\n✅ manage_service.py fixed")
        print("✅ All emojis replaced with ASCII text")

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """Run fix."""
    print("=" * 70)
    print("  FIX MANAGE_SERVICE.PY EMOJI ISSUE")
    print("=" * 70)

    print("\nProblem: Unicode emoji crash in cp1250 encoding")
    print("Solution: Replace all emojis with ASCII alternatives")

    if fix_manage_service():
        print("\n" + "=" * 70)
        print("  NEXT STEPS")
        print("=" * 70)
        print("\n1. Redeploy to Deployment:")
        print("   python scripts\\deploy_to_deployment.py")
        print("\n2. Test service status in Deployment:")
        print("   cd C:\\Deployment\\nex-automat")
        print("   python scripts\\manage_service.py status")
        print("\n3. Run preflight check:")
        print("   python scripts\\day5_preflight_check.py")
        return True
    else:
        print("\n❌ Fix failed")
        return False


if __name__ == "__main__":
    import sys

    sys.exit(0 if main() else 1)