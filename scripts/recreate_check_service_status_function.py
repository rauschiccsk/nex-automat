#!/usr/bin/env python3
"""
Completely recreate check_service_status function with proper encoding handling
"""

from pathlib import Path


def recreate_function():
    """Recreate the function from scratch"""

    script_path = Path("scripts/day5_preflight_check.py")

    if not script_path.exists():
        print(f"❌ File not found: {script_path}")
        return False

    print(f"📖 Reading {script_path}...")
    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')

    # Find function boundaries
    func_start = None
    func_end = None

    for i, line in enumerate(lines):
        if 'def check_service_status()' in line:
            func_start = i
        if func_start is not None and i > func_start:
            if line.strip().startswith('def ') and 'check_service_status' not in line:
                func_end = i
                break

    if func_start is None:
        print("❌ Could not find function")
        return False

    if func_end is None:
        func_end = len(lines)

    print(f"Replacing function at lines {func_start + 1} to {func_end}")

    # New function - using raw string to preserve \x00
    new_function_lines = [
        'def check_service_status() -> bool:',
        '    """Check if NEX-Automat-Loader service is running."""',
        '    print_section("1. SERVICE STATUS")',
        '',
        '    try:',
        '        result = subprocess.run(',
        '            ["python", "scripts/manage_service.py", "status"],',
        '            capture_output=True,',
        '            text=False,  # Get bytes to handle UTF-16',
        '            timeout=10',
        '        )',
        '        ',
        '        # Decode NSSM output (may be UTF-16LE with null bytes)',
        '        try:',
        '            # Try UTF-16LE decoding first',
        r'            stdout = result.stdout.decode("utf-16le").rstrip("\x00")',
        '        except:',
        '            try:',
        '                # Fallback to UTF-8',
        r'                stdout = result.stdout.decode("utf-8", errors="ignore")',
        '            except:',
        '                # Last resort - convert to string and strip nulls',
        r'                stdout = str(result.stdout).replace("\x00", "")',
        '        ',
        '        # Print decoded output',
        '        print(stdout)',
        '',
        '        # Check if service is running',
        '        stdout_lower = stdout.lower()',
        '        has_running = "running" in stdout_lower',
        '        has_service_running = "service_running" in stdout_lower',
        '',
        '        # Check if service is running - check for both patterns',
        '        if has_running or has_service_running or "SERVICE_RUNNING" in stdout:',
        '            print("✅ Service is RUNNING")',
        '            return True',
        '        else:',
        '            print("❌ Service is NOT running")',
        '            print("   Run: python scripts/manage_service.py start")',
        '            return False',
        '',
        '    except Exception as e:',
        '        print(f"❌ Error checking service: {e}")',
        '        return False',
        ''
    ]

    # Reconstruct file
    new_lines = lines[:func_start] + new_function_lines + lines[func_end:]
    new_content = '\n'.join(new_lines)

    # Write back
    print(f"💾 Writing fixed content...")
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print("✅ Function recreated with proper encoding handling")
    print()
    print("Deploy and test:")
    print("  python scripts\\deploy_to_deployment.py")
    print("  cd C:\\Deployment\\nex-automat")
    print("  python scripts\\day5_preflight_check.py")

    return True


if __name__ == "__main__":
    print("=" * 70)
    print("  RECREATE check_service_status() FUNCTION")
    print("=" * 70)
    print()

    success = recreate_function()

    if success:
        print()
        print("✅ SUCCESS")
    else:
        print()
        print("❌ FAILED")