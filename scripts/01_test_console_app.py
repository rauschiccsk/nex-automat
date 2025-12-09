"""
Script 01: Test NEX Automat Loader as Console Application
==========================================================

Purpose: Test if supplier-invoice-loader works as console app
         to isolate if problem is code-specific or service-specific

What this does:
1. Stops the NEX-Automat-Loader service
2. Runs main.py as console application
3. Monitors startup and checks if FastAPI starts
4. Provides diagnostic information

Expected result:
- If console works: Problem is service-specific (LocalSystem account/Winsock)
- If console fails: Problem is environment/system-specific

Usage:
    python scripts/01_test_console_app.py
"""

import subprocess
import sys
import time
import socket
from pathlib import Path

def run_command(cmd, capture_output=True):
    """Execute shell command"""
    try:
        if capture_output:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            return result.returncode, result.stdout, result.stderr
        else:
            # For interactive process
            process = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8'
            )
            return process
    except Exception as e:
        return -1, "", str(e)

def check_service_status():
    """Check if service is running"""
    code, stdout, stderr = run_command('sc query "NEX-Automat-Loader"')
    if "RUNNING" in stdout:
        return "RUNNING"
    elif "PAUSED" in stdout:
        return "PAUSED"
    elif "STOPPED" in stdout:
        return "STOPPED"
    else:
        return "UNKNOWN"

def stop_service():
    """Stop the service if running"""
    status = check_service_status()
    print(f"\n🔍 Service status: {status}")

    if status in ["RUNNING", "PAUSED"]:
        print("⏸️  Stopping service...")
        code, stdout, stderr = run_command('net stop "NEX-Automat-Loader"')
        if code == 0:
            print("✅ Service stopped")
            time.sleep(2)
            return True
        else:
            print(f"❌ Failed to stop service: {stderr}")
            return False
    else:
        print("ℹ️  Service already stopped")
        return True

def test_port_open(port=8001, max_attempts=10):
    """Test if port is open (FastAPI listening)"""
    print(f"\n🔍 Testing if port {port} is open...")

    for i in range(max_attempts):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex(('localhost', port))
            sock.close()

            if result == 0:
                print(f"✅ Port {port} is open - FastAPI is listening!")
                return True
        except Exception as e:
            pass

        print(f"⏳ Attempt {i+1}/{max_attempts} - waiting for server...")
        time.sleep(2)

    print(f"❌ Port {port} not open")
    return False

def main():
    print("=" * 70)
    print("NEX AUTOMAT LOADER - CONSOLE APPLICATION TEST")
    print("=" * 70)

    # Check deployment directory
    deployment_dir = Path("C:/Deployment/nex-automat")
    app_dir = deployment_dir / "apps" / "supplier-invoice-loader"
    main_py = app_dir / "main.py"
    python_exe = deployment_dir / "venv32" / "Scripts" / "python.exe"

    print(f"\n📁 Checking paths:")
    print(f"   Deployment: {deployment_dir}")
    print(f"   App dir: {app_dir}")
    print(f"   main.py: {main_py}")
    print(f"   Python: {python_exe}")

    if not deployment_dir.exists():
        print(f"\n❌ ERROR: Deployment directory not found: {deployment_dir}")
        return

    if not main_py.exists():
        print(f"\n❌ ERROR: main.py not found: {main_py}")
        return

    if not python_exe.exists():
        print(f"\n❌ ERROR: Python executable not found: {python_exe}")
        return

    print("✅ All paths verified")

    # Stop service
    if not stop_service():
        print("\n⚠️  WARNING: Could not stop service, continuing anyway...")

    # Build command
    cmd = f'"{python_exe}" "{main_py}"'

    print("\n" + "=" * 70)
    print("STARTING CONSOLE APPLICATION")
    print("=" * 70)
    print(f"\nCommand: {cmd}")
    print("\n🚀 Starting application...")
    print("   Press CTRL+C to stop")
    print("   Watching for startup messages...\n")

    try:
        # Start process
        process = run_command(cmd, capture_output=False)

        # Give it time to start
        time.sleep(5)

        # Check if process is still running
        if process.poll() is not None:
            stdout, stderr = process.communicate()
            print("\n❌ ERROR: Process terminated immediately")
            print("\n📋 STDOUT:")
            print(stdout if stdout else "(empty)")
            print("\n📋 STDERR:")
            print(stderr if stderr else "(empty)")
            return

        # Test health endpoint
        if test_port_open():
            print("\n" + "=" * 70)
            print("✅ SUCCESS - CONSOLE APPLICATION WORKS!")
            print("=" * 70)
            print("\n📊 DIAGNOSIS:")
            print("   ✅ Code is working correctly")
            print("   ✅ FastAPI starts successfully")
            print("   ✅ Port 8001 is listening")
            print("\n🔍 CONCLUSION:")
            print("   Problem is SERVICE-SPECIFIC, not code-specific")
            print("\n💡 SOLUTIONS TO TRY:")
            print("   1. Change service account to NetworkService")
            print("   2. Fix Winsock (netsh winsock reset + reboot)")
            print("   3. Use Task Scheduler instead of NSSM")
            print("\n⏸️  Press CTRL+C to stop the application")

            # Keep running until interrupted
            process.wait()
        else:
            print("\n" + "=" * 70)
            print("❌ FAILED - CONSOLE APPLICATION HAS ISSUES")
            print("=" * 70)
            print("\n📊 DIAGNOSIS:")
            print("   ❌ Application started but FastAPI not responding")
            print("\n🔍 Check the output above for errors")

            # Terminate process
            process.terminate()
            process.wait(timeout=5)

    except KeyboardInterrupt:
        print("\n\n⏸️  Stopping application...")
        try:
            process.terminate()
            process.wait(timeout=5)
        except:
            process.kill()
        print("✅ Application stopped")

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        try:
            process.terminate()
        except:
            pass

if __name__ == "__main__":
    # Check if running as administrator
    try:
        import ctypes
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        if not is_admin:
            print("\n⚠️  WARNING: Not running as Administrator")
            print("   Some operations may fail")
            print("   Run PowerShell as Administrator for best results\n")
    except:
        pass

    main()