"""
Script 11: Check NSSM Service Logs
===================================

Purpose: Find and display service logs

Usage:
    python scripts/11_check_nssm_logs.py
"""

import subprocess
from pathlib import Path


def run_command(cmd):
    """Execute shell command"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return -1, "", str(e)


def main():
    print("=" * 70)
    print("NSSM SERVICE LOG CHECK")
    print("=" * 70)

    # Get NSSM configuration for log paths
    print("\n[INFO] Checking NSSM configuration for log paths...")

    service_name = "NEX-Automat-Loader"

    # Check AppStdout (stdout log)
    code, stdout, stderr = run_command(f'nssm get "{service_name}" AppStdout')
    stdout_log = stdout.strip() if code == 0 else None

    # Check AppStderr (stderr log)
    code, stdout, stderr = run_command(f'nssm get "{service_name}" AppStderr')
    stderr_log = stdout.strip() if code == 0 else None

    print(f"\n[INFO] NSSM Log Configuration:")
    print(f"  AppStdout: {stdout_log}")
    print(f"  AppStderr: {stderr_log}")

    # Check if logs exist and display them
    logs_to_check = []

    if stdout_log:
        logs_to_check.append(("STDOUT", stdout_log))

    if stderr_log:
        logs_to_check.append(("STDERR", stderr_log))

    # Also check common log locations
    common_locations = [
        Path("C:/Deployment/nex-automat/apps/supplier-invoice-loader/logs"),
        Path("C:/Deployment/nex-automat/logs"),
        Path("C:/Deployment/nex-automat/apps/supplier-invoice-loader"),
    ]

    print("\n[INFO] Checking common log locations...")
    for location in common_locations:
        if location.exists():
            log_files = list(location.glob("*.log"))
            if log_files:
                print(f"\n[FOUND] Log files in {location}:")
                for log_file in log_files:
                    size = log_file.stat().st_size
                    print(f"  - {log_file.name} ({size} bytes)")
                    logs_to_check.append((log_file.name, str(log_file)))

    # Display log contents
    for log_name, log_path in logs_to_check:
        log_file = Path(log_path)

        print("\n" + "=" * 70)
        print(f"LOG: {log_name}")
        print("=" * 70)
        print(f"Path: {log_path}")

        if not log_file.exists():
            print("[WARNING] Log file does not exist")
            continue

        try:
            with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            if not content.strip():
                print("[INFO] Log file is empty")
            else:
                # Show last 100 lines
                lines = content.split('\n')
                if len(lines) > 100:
                    print(f"\n[INFO] Showing last 100 lines (total: {len(lines)} lines)\n")
                    print('\n'.join(lines[-100:]))
                else:
                    print(f"\n{content}")

        except Exception as e:
            print(f"[ERROR] Could not read log file: {e}")

    # Check Windows Event Log
    print("\n" + "=" * 70)
    print("WINDOWS EVENT LOG")
    print("=" * 70)

    print("\n[INFO] Checking Windows Event Log for service errors...")
    code, stdout, stderr = run_command(
        f'powershell -Command "Get-EventLog -LogName Application -Source NSSM -Newest 10 -ErrorAction SilentlyContinue | Format-Table -AutoSize"'
    )

    if code == 0 and stdout.strip():
        print(stdout)
    else:
        print("[INFO] No recent NSSM events in Windows Event Log")

    print("\n" + "=" * 70)
    print("NEXT STEPS")
    print("=" * 70)
    print("""
If logs show errors:
1. Check the specific error message
2. Fix the issue
3. Restart service: net start "NEX-Automat-Loader"

If no logs exist:
1. NSSM may not be configured for logging
2. Configure logs with NSSM:
   nssm set "NEX-Automat-Loader" AppStdout "C:\\Deployment\\nex-automat\\logs\\service-stdout.log"
   nssm set "NEX-Automat-Loader" AppStderr "C:\\Deployment\\nex-automat\\logs\\service-stderr.log"
    """)


if __name__ == "__main__":
    main()