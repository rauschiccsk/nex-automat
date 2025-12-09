"""
Script 12: Change Service Account to NetworkService
====================================================

Purpose: Change NEX-Automat-Loader service account from LocalSystem to NetworkService
         to fix WinError 10106 (asyncio Winsock initialization issue)

Why: LocalSystem account has issues with asyncio _overlapped module
     NetworkService has proper network/socket initialization

Usage:
    python scripts/12_change_service_account.py
"""

import subprocess


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
    service_name = "NEX-Automat-Loader"

    print("=" * 70)
    print("CHANGE SERVICE ACCOUNT TO NETWORKSERVICE")
    print("=" * 70)

    print(f"\n[INFO] Service: {service_name}")
    print("[INFO] Current account: LocalSystem")
    print("[INFO] New account: NT AUTHORITY\\NetworkService")

    # Step 1: Stop service
    print("\n" + "=" * 70)
    print("STEP 1: STOP SERVICE")
    print("=" * 70)

    print("\n[INFO] Stopping service...")
    code, stdout, stderr = run_command(f'net stop "{service_name}"')

    if code == 0 or "not started" in stderr.lower():
        print("[OK] Service stopped")
    else:
        print(f"[WARNING] {stderr}")

    # Step 2: Change account using sc config
    print("\n" + "=" * 70)
    print("STEP 2: CHANGE SERVICE ACCOUNT")
    print("=" * 70)

    print("\n[INFO] Changing service account to NetworkService...")
    cmd = f'sc config "{service_name}" obj= "NT AUTHORITY\\NetworkService"'
    code, stdout, stderr = run_command(cmd)

    if code == 0:
        print("[OK] Service account changed successfully")
        print(stdout)
    else:
        print(f"[ERROR] Failed to change service account: {stderr}")
        return

    # Step 3: Verify permissions on deployment directory
    print("\n" + "=" * 70)
    print("STEP 3: VERIFY PERMISSIONS")
    print("=" * 70)

    print("\n[INFO] Checking if NetworkService has access to deployment directory...")

    deployment_dir = "C:\\Deployment\\nex-automat"

    # Grant read/execute permissions to NetworkService
    cmd = f'icacls "{deployment_dir}" /grant "NT AUTHORITY\\NetworkService:(OI)(CI)RX" /T /Q'
    print(f"[INFO] Granting read/execute permissions...")
    code, stdout, stderr = run_command(cmd)

    if code == 0:
        print("[OK] Permissions granted")
    else:
        print(f"[WARNING] Permission grant: {stderr}")

    # Step 4: Start service
    print("\n" + "=" * 70)
    print("STEP 4: START SERVICE")
    print("=" * 70)

    print("\n[INFO] Starting service with new account...")
    code, stdout, stderr = run_command(f'net start "{service_name}"')

    if code == 0:
        print("[OK] Service started successfully")
        print(stdout)
    else:
        print(f"[ERROR] Service start failed: {stderr}")
        print("\n[INFO] Check service logs for details")
        return

    # Step 5: Verify service status
    print("\n" + "=" * 70)
    print("STEP 5: VERIFY SERVICE STATUS")
    print("=" * 70)

    import time
    print("\n[INFO] Waiting 5 seconds for service to initialize...")
    time.sleep(5)

    code, stdout, stderr = run_command(f'sc query "{service_name}"')

    if "RUNNING" in stdout:
        print("[OK] Service is RUNNING")
    elif "PAUSED" in stdout:
        print("[ERROR] Service is PAUSED - still has issues")
    elif "STOPPED" in stdout:
        print("[ERROR] Service is STOPPED - startup failed")
    else:
        print(f"[WARNING] Service status unknown:\n{stdout}")

    # Step 6: Test port
    print("\n" + "=" * 70)
    print("STEP 6: TEST API ENDPOINT")
    print("=" * 70)

    import socket
    print("\n[INFO] Testing if port 8001 is open...")

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex(('localhost', 8001))
        sock.close()

        if result == 0:
            print("[OK] Port 8001 is open - FastAPI is listening!")
            print("\n" + "=" * 70)
            print("[SUCCESS] SERVICE ACCOUNT CHANGE COMPLETE!")
            print("=" * 70)
            print("\n[INFO] Service is running under NetworkService account")
            print("[INFO] API is accessible on http://localhost:8001")
        else:
            print("[ERROR] Port 8001 is not open")
            print("[INFO] Check service logs for startup errors")
    except Exception as e:
        print(f"[ERROR] Failed to test port: {e}")

    print("\n" + "=" * 70)
    print("WHY THIS FIXES THE ISSUE")
    print("=" * 70)
    print("""
LocalSystem account limitations:
- Runs without interactive desktop session
- Some Winsock features unavailable
- Asyncio _overlapped module cannot initialize

NetworkService account benefits:
- Proper network/socket initialization
- Has necessary privileges for network services
- Standard account for network-facing services
- Still secure and limited in scope
    """)


if __name__ == "__main__":
    try:
        import ctypes

        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        if not is_admin:
            print("\n[ERROR] This script MUST run as Administrator")
            print("[ERROR] Run PowerShell as Administrator and try again\n")
            exit(1)
    except:
        pass

    main()