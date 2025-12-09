"""
Script 10: Deploy to Production
================================

Purpose: Pull changes to Deployment and restart service

Usage:
    python scripts/10_deploy_to_production.py
"""

import subprocess
from pathlib import Path


def run_command(cmd, cwd=None):
    """Execute shell command"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8',
            cwd=cwd
        )
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return -1, "", str(e)


def main():
    deployment_dir = Path("C:/Deployment/nex-automat")

    print("=" * 70)
    print("DEPLOYMENT TO PRODUCTION")
    print("=" * 70)

    if not deployment_dir.exists():
        print(f"\n[ERROR] Deployment directory not found: {deployment_dir}")
        return

    print(f"\n[INFO] Deployment directory: {deployment_dir}")

    # Step 1: Git pull
    print("\n" + "=" * 70)
    print("STEP 1: GIT PULL")
    print("=" * 70)

    print("\n[INFO] Pulling latest changes from Git...")
    code, stdout, stderr = run_command("git pull", cwd=deployment_dir)

    if code == 0:
        print("[OK] Git pull successful")
        print(stdout)
    else:
        print(f"[ERROR] Git pull failed: {stderr}")
        return

    # Step 2: Stop service
    print("\n" + "=" * 70)
    print("STEP 2: STOP SERVICE")
    print("=" * 70)

    print("\n[INFO] Stopping NEX-Automat-Loader service...")
    code, stdout, stderr = run_command('net stop "NEX-Automat-Loader"')

    if code == 0 or "not started" in stderr.lower():
        print("[OK] Service stopped")
    else:
        print(f"[WARNING] Service stop: {stderr}")

    # Step 3: Start service
    print("\n" + "=" * 70)
    print("STEP 3: START SERVICE")
    print("=" * 70)

    print("\n[INFO] Starting NEX-Automat-Loader service...")
    code, stdout, stderr = run_command('net start "NEX-Automat-Loader"')

    if code == 0:
        print("[OK] Service started successfully")
        print(stdout)
    else:
        print(f"[ERROR] Service start failed: {stderr}")
        print("\n[INFO] Check service logs for details")
        return

    # Step 4: Check service status
    print("\n" + "=" * 70)
    print("STEP 4: VERIFY SERVICE STATUS")
    print("=" * 70)

    import time
    print("\n[INFO] Waiting 5 seconds for service to initialize...")
    time.sleep(5)

    code, stdout, stderr = run_command('sc query "NEX-Automat-Loader"')

    if "RUNNING" in stdout:
        print("[OK] Service is RUNNING")
    elif "PAUSED" in stdout:
        print("[WARNING] Service is PAUSED")
    elif "STOPPED" in stdout:
        print("[ERROR] Service is STOPPED")
    else:
        print(f"[WARNING] Service status unknown:\n{stdout}")

    # Step 5: Test port
    print("\n" + "=" * 70)
    print("STEP 5: TEST API ENDPOINT")
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
            print("[SUCCESS] DEPLOYMENT COMPLETE!")
            print("=" * 70)
            print("\n[INFO] Service is running and API is accessible")
            print("[INFO] API Documentation: http://localhost:8001/docs")
        else:
            print("[ERROR] Port 8001 is not open")
            print("[INFO] Check service logs for startup errors")
    except Exception as e:
        print(f"[ERROR] Failed to test port: {e}")

    print("\n" + "=" * 70)
    print("NEXT STEPS")
    print("=" * 70)
    print("""
1. Check service logs:
   python scripts/27_check_service_logs.py

2. Test Mágerstav verification:
   - Upload invoice
   - Verify NEX enrichment works

3. Monitor service for stability
    """)


if __name__ == "__main__":
    try:
        import ctypes

        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        if not is_admin:
            print("\n[WARNING] Not running as Administrator")
            print("[WARNING] Service operations may fail")
            print("[WARNING] Run PowerShell as Administrator\n")
    except:
        pass

    main()