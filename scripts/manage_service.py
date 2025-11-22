"""
Service Management Script for NEX-Automat-Loader
=================================================
Manage Windows Service operations: start, stop, restart, status, logs

Usage:
    python scripts/manage_service.py <command>

Commands:
    start    - Start the service (requires Administrator)
    stop     - Stop the service (requires Administrator)
    restart  - Restart the service (requires Administrator)
    status   - Show service status
    logs     - Show recent logs (last 50 lines)
    tail     - Monitor logs in real-time (Ctrl+C to exit)

Location: C:\\Deployment\\nex-automat\\scripts\\manage_service.py
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def decode_nssm_output(result):
    """Decode NSSM output which may be UTF-16LE with null bytes"""
    try:
        if isinstance(result.stdout, bytes):
            stdout = result.stdout.decode('utf-16le').rstrip('\x00')
        else:
            # Already string, just remove null bytes
            stdout = result.stdout.replace('\x00', '')

        if isinstance(result.stderr, bytes):
            stderr = result.stderr.decode('utf-16le').rstrip('\x00')
        else:
            stderr = result.stderr.replace('\x00', '')

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
                self.stdout = str(stdout).replace('\x00', '')
                self.stderr = str(stderr).replace('\x00', '')

        return DecodedResult(result.returncode, result.stdout, result.stderr)



# Service configuration
SERVICE_NAME = "NEX-Automat-Loader"
NSSM_PATH = Path(__file__).parent.parent / "tools" / "nssm" / "win32" / "nssm.exe"
LOGS_DIR = Path(__file__).parent.parent / "logs"


def is_admin():
    """Check if script is running with administrator privileges"""
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False


def run_nssm_command(command_args):
    """Run NSSM command and return result"""
    try:
        result = subprocess.run(
            [str(NSSM_PATH)] + command_args,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return -1, "", str(e)


def get_service_status():
    """Get current service status"""
    code, stdout, stderr = run_nssm_command(["status", SERVICE_NAME])

    if code == 0:
        return stdout
    else:
        return None


def start_service():
    """Start the service"""
    if not is_admin():
        print("ERROR: This command requires Administrator privileges")
        print("Please run PowerShell as Administrator")
        return 1

    print(f"Starting service '{SERVICE_NAME}'...")

    code, stdout, stderr = run_nssm_command(["start", SERVICE_NAME])

    if code == 0:
        print("OK: Service started successfully")
        time.sleep(2)
        status = get_service_status()
        if status:
            print(f"   Status: {status}")
        return 0
    else:
        print(f"ERROR: Failed to start service")
        if stderr:
            print(f"   Error: {stderr}")
        return 1


def stop_service():
    """Stop the service"""
    if not is_admin():
        print("ERROR: This command requires Administrator privileges")
        print("Please run PowerShell as Administrator")
        return 1

    print(f"Stopping service '{SERVICE_NAME}'...")

    code, stdout, stderr = run_nssm_command(["stop", SERVICE_NAME])

    if code == 0:
        print("OK: Service stopped successfully")
        time.sleep(2)
        status = get_service_status()
        if status:
            print(f"   Status: {status}")
        return 0
    else:
        print(f"ERROR: Failed to stop service")
        if stderr:
            print(f"   Error: {stderr}")
        return 1


def restart_service():
    """Restart the service"""
    if not is_admin():
        print("ERROR: This command requires Administrator privileges")
        print("Please run PowerShell as Administrator")
        return 1

    print(f"Restarting service '{SERVICE_NAME}'...")

    # Stop
    print("  1. Stopping...")
    code, stdout, stderr = run_nssm_command(["stop", SERVICE_NAME])
    if code != 0:
        print(f"     WARNING: Stop failed: {stderr}")

    time.sleep(2)

    # Start
    print("  2. Starting...")
    code, stdout, stderr = run_nssm_command(["start", SERVICE_NAME])

    if code == 0:
        print("OK: Service restarted successfully")
        time.sleep(2)
        status = get_service_status()
        if status:
            print(f"   Status: {status}")
        return 0
    else:
        print(f"ERROR: Failed to restart service")
        if stderr:
            print(f"   Error: {stderr}")
        return 1


def show_status():
    """Show service status"""
    print(f"Service: {SERVICE_NAME}")

    status = get_service_status()

    if status:
        print(f"Status: {status}")

        if "RUNNING" in status:
            return 0
        else:
            return 1
    else:
        print("Status: ERROR (Cannot get status)")
        return 1


def show_logs(lines=50):
    """Show recent logs"""
    stdout_log = LOGS_DIR / "service-stdout.log"
    stderr_log = LOGS_DIR / "service-stderr.log"

    print("=" * 70)
    print(f"STDOUT LOG (last {lines} lines)")
    print("=" * 70)

    if stdout_log.exists():
        try:
            with open(stdout_log, 'r', encoding='utf-8', errors='ignore') as f:
                all_lines = f.readlines()
                recent_lines = all_lines[-lines:]
                print(''.join(recent_lines))
        except Exception as e:
            print(f"ERROR: Cannot read stdout log: {e}")
    else:
        print("(No stdout log yet)")

    print()
    print("=" * 70)
    print(f"STDERR LOG (last {lines} lines)")
    print("=" * 70)

    if stderr_log.exists():
        try:
            with open(stderr_log, 'r', encoding='utf-8', errors='ignore') as f:
                all_lines = f.readlines()
                recent_lines = all_lines[-lines:]
                if recent_lines:
                    print(''.join(recent_lines))
                else:
                    print("(Empty - no errors)")
        except Exception as e:
            print(f"ERROR: Cannot read stderr log: {e}")
    else:
        print("(No stderr log yet)")

    print()
    return 0


def tail_logs():
    """Monitor logs in real-time"""
    stdout_log = LOGS_DIR / "service-stdout.log"

    print("=" * 70)
    print("MONITORING LOGS (Press Ctrl+C to exit)")
    print("=" * 70)
    print()

    if not stdout_log.exists():
        print("ERROR: No log file yet. Start the service first.")
        return 1

    try:
        # Read existing content first
        with open(stdout_log, 'r', encoding='utf-8', errors='ignore') as f:
            # Jump to end
            f.seek(0, 2)

            print("Waiting for new log entries...")
            print()

            while True:
                line = f.readline()
                if line:
                    print(line.rstrip())
                else:
                    time.sleep(0.5)

    except KeyboardInterrupt:
        print()
        print("Monitoring stopped.")
        return 0
    except Exception as e:
        print(f"ERROR: {e}")
        return 1


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print(__doc__)
        return 1

    command = sys.argv[1].lower()

    # Check NSSM exists
    if not NSSM_PATH.exists():
        print(f"ERROR: NSSM not found at {NSSM_PATH}")
        print("Run: python scripts/install_nssm.py")
        return 1

    # Check logs directory
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    # Execute command
    if command == "start":
        return start_service()
    elif command == "stop":
        return stop_service()
    elif command == "restart":
        return restart_service()
    elif command == "status":
        return show_status()
    elif command == "logs":
        return show_logs()
    elif command == "tail":
        return tail_logs()
    else:
        print(f"ERROR: Unknown command: {command}")
        print(__doc__)
        return 1


if __name__ == "__main__":
    sys.exit(main())
