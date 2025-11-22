#!/usr/bin/env python3
"""
Fix NSSM UTF-16 encoding issue in manage_service.py

Problem: NSSM returns UTF-16LE (wide chars with null bytes)
Solution: Decode as UTF-16LE or strip null bytes
"""

from pathlib import Path
import re


def fix_manage_service():
    """Fix encoding issue in manage_service.py"""

    script_path = Path("scripts/manage_service.py")

    if not script_path.exists():
        print(f"❌ File not found: {script_path}")
        return False

    print(f"📖 Reading {script_path}...")
    content = script_path.read_text(encoding='utf-8')

    # Find the run_nssm function or wherever NSSM output is captured
    # We need to add encoding handling after subprocess.run

    # Pattern 1: Look for subprocess.run with NSSM
    old_pattern1 = '''        result = subprocess.run(
            nssm_cmd,
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        )'''

    new_pattern1 = '''        result = subprocess.run(
            nssm_cmd,
            capture_output=True,
            text=False,  # Get bytes, not text
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        )

        # NSSM returns UTF-16LE on Windows - decode properly
        try:
            stdout = result.stdout.decode('utf-16le').rstrip('\x00')
            stderr = result.stderr.decode('utf-16le').rstrip('\x00')
        except:
            # Fallback to UTF-8 if UTF-16 fails
            stdout = result.stdout.decode('utf-8', errors='ignore')
            stderr = result.stderr.decode('utf-8', errors='ignore')

        # Create new result with decoded strings
        class DecodedResult:
            def __init__(self, returncode, stdout, stderr):
                self.returncode = returncode
                self.stdout = stdout
                self.stderr = stderr

        result = DecodedResult(result.returncode, stdout, stderr)'''

    if old_pattern1 in content:
        content = content.replace(old_pattern1, new_pattern1)
        print("✅ Fixed NSSM encoding (pattern 1)")
    else:
        # Try alternative - just add null byte stripping
        # Look for any place where we use result.stdout
        print("⚠️  Pattern 1 not found, trying simpler fix...")

        # Add helper function at top of file
        helper_function = '''
def decode_nssm_output(result):
    """Decode NSSM output which may be UTF-16LE with null bytes"""
    try:
        if isinstance(result.stdout, bytes):
            stdout = result.stdout.decode('utf-16le').rstrip('\\x00')
        else:
            # Already string, just remove null bytes
            stdout = result.stdout.replace('\\x00', '')

        if isinstance(result.stderr, bytes):
            stderr = result.stderr.decode('utf-16le').rstrip('\\x00')
        else:
            stderr = result.stderr.replace('\\x00', '')

        class DecodedResult:
            def __init__(self, returncode, stdout, stderr):
                self.returncode = returncode
                self.stdout = stdout
                self.stderr = stderr

        return DecodedResult(result.returncode, stdout, stderr)
    except:
        # Fallback - just strip null bytes
        class DecodedResult:
            def __init__(self, returncode, stdout, stderr):
                self.returncode = returncode
                self.stdout = str(stdout).replace('\\x00', '')
                self.stderr = str(stderr).replace('\\x00', '')

        return DecodedResult(result.returncode, result.stdout, result.stderr)

'''

        # Insert after imports
        import_end = content.find('import subprocess') + len('import subprocess')
        if import_end > 0:
            # Find the next blank line after imports
            next_newline = content.find('\n\n', import_end)
            if next_newline > 0:
                content = content[:next_newline] + '\n' + helper_function + content[next_newline:]
                print("✅ Added decode_nssm_output helper function")

                # Now find all places where we call subprocess.run with nssm
                # and add result = decode_nssm_output(result) after

                lines = content.split('\n')
                new_lines = []
                i = 0
                while i < len(lines):
                    new_lines.append(lines[i])

                    # If this line has subprocess.run and next few lines close the paren
                    if 'result = subprocess.run(' in lines[i] and 'nssm' in lines[i]:
                        # Find closing paren
                        j = i + 1
                        while j < len(lines) and ')' not in lines[j]:
                            new_lines.append(lines[j])
                            j += 1
                        if j < len(lines):
                            new_lines.append(lines[j])
                            # Add decode call
                            indent = len(lines[i]) - len(lines[i].lstrip())
                            new_lines.append(' ' * indent + 'result = decode_nssm_output(result)')
                            i = j

                    i += 1

                content = '\n'.join(new_lines)
                print("✅ Added decode calls after subprocess.run")
            else:
                print("❌ Could not find place to insert helper")
                return False
        else:
            print("❌ Could not find imports section")
            return False

    # Write fixed content
    print(f"💾 Writing fixed content...")
    script_path.write_text(content, encoding='utf-8')

    print()
    print("✅ Fix completed!")
    print()
    print("Next steps:")
    print("1. Deploy to Deployment:")
    print("   python scripts\\deploy_to_deployment.py")
    print("2. Test service status:")
    print("   cd C:\\Deployment\\nex-automat")
    print("   python scripts\\manage_service.py status")
    print("3. Run preflight check:")
    print("   python scripts\\day5_preflight_check.py")

    return True


if __name__ == "__main__":
    print("=" * 70)
    print("  FIX NSSM UTF-16 ENCODING")
    print("=" * 70)
    print()

    success = fix_manage_service()

    if success:
        print()
        print("✅ SUCCESS")
    else:
        print()
        print("❌ FAILED")