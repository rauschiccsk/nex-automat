#!/usr/bin/env python3
"""
Show exact problematic code and fix it
"""

from pathlib import Path


def show_and_fix():
    """Show the exact problem and fix it"""

    script_path = Path("scripts/day5_preflight_check.py")

    if not script_path.exists():
        print(f"❌ File not found: {script_path}")
        return False

    print(f"📖 Reading {script_path}...")
    content = script_path.read_text(encoding='utf-8')
    lines = content.split('\n')

    print("\n" + "=" * 70)
    print("  SHOWING LINES 40-55 (problem area)")
    print("=" * 70)

    for i in range(40, min(55, len(lines))):
        print(f"{i + 1:3d}: |{lines[i]}|")

    print("\n" + "=" * 70)
    print("  FIXING THE CODE")
    print("=" * 70)

    # Complete replacement of the check_service_status function
    # Find function start
    func_start = None
    for i, line in enumerate(lines):
        if 'def check_service_status()' in line:
            func_start = i
            break

    if func_start is None:
        print("❌ Could not find check_service_status function")
        return False

    # Find function end (next def or end of try block)
    func_end = None
    for i in range(func_start + 1, len(lines)):
        if lines[i].strip().startswith('def ') and 'check_service_status' not in lines[i]:
            func_end = i
            break

    if func_end is None:
        func_end = len(lines)

    print(f"Function spans lines {func_start + 1} to {func_end}")

    # Create the corrected function
    new_function = '''def check_service_status() -> bool:
    """Check if NEX-Automat-Loader service is running."""
    print_section("1. SERVICE STATUS")

    try:
        result = subprocess.run(
            ["python", "scripts/manage_service.py", "status"],
            capture_output=True,
            text=False,  # Get bytes to handle UTF-16
            timeout=10
        )

        # Decode NSSM output (may be UTF-16LE with null bytes)
        try:
            stdout = result.stdout.decode('utf-16le').rstrip('\\x00')
        except:
            try:
                stdout = result.stdout.decode('utf-8', errors='ignore')
            except:
                stdout = str(result.stdout).replace('\\x00', '')

        # Print decoded output
        print(stdout)

        # Check if service is running
        stdout_lower = stdout.lower()
        has_running = "running" in stdout_lower
        has_service_running = "service_running" in stdout_lower

        # Check if service is running - check for both patterns
        if has_running or has_service_running or "SERVICE_RUNNING" in stdout:
            print("✅ Service is RUNNING")
            return True
        else:
            print("❌ Service is NOT running")
            print("   Run: python scripts/manage_service.py start")
            return False

    except Exception as e:
        print(f"❌ Error checking service: {e}")
        return False

'''

    # Replace the function
    new_lines = lines[:func_start] + new_function.split('\n') + lines[func_end:]

    # Write back
    content = '\n'.join(new_lines)
    script_path.write_text(content, encoding='utf-8')

    print("✅ Function completely rewritten with correct indentation")
    print()
    print("Next: Deploy and test")

    return True


if __name__ == "__main__":
    print("=" * 70)
    print("  SHOW AND FIX INDENTATION")
    print("=" * 70)

    success = show_and_fix()

    if success:
        print()
        print("✅ SUCCESS")
    else:
        print()
        print("❌ FAILED")