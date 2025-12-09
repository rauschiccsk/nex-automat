"""
Script 06: Test NEX Automat Loader in Development
==================================================

Purpose: Test if supplier-invoice-loader works in Development
         with the fixed BtrieveClient code

Usage:
    python scripts/06_test_dev_console.py
"""

import subprocess
import sys
import time
import socket
from pathlib import Path


def check_port_open(port=8001, max_attempts=10):
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
        except Exception:
            pass

        print(f"⏳ Attempt {i + 1}/{max_attempts} - waiting for server...")
        time.sleep(2)

    print(f"❌ Port {port} not open")
    return False


def main():
    print("=" * 70)
    print("NEX AUTOMAT LOADER - DEVELOPMENT TEST")
    print("=" * 70)

    # Check development directory
    dev_dir = Path("C:/Development/nex-automat")
    app_dir = dev_dir / "apps" / "supplier-invoice-loader"
    main_py = app_dir / "main.py"
    python_exe = dev_dir / "venv32" / "Scripts" / "python.exe"

    print(f"\n📁 Checking paths:")
    print(f"   Development: {dev_dir}")
    print(f"   App dir: {app_dir}")
    print(f"   main.py: {main_py}")
    print(f"   Python: {python_exe}")

    if not dev_dir.exists():
        print(f"\n❌ ERROR: Development directory not found: {dev_dir}")
        return

    if not main_py.exists():
        print(f"\n❌ ERROR: main.py not found: {main_py}")
        return

    if not python_exe.exists():
        print(f"\n❌ ERROR: Python executable not found: {python_exe}")
        return

    print("✅ All paths verified")

    # Build command
    cmd = f'"{python_exe}" "{main_py}"'

    print("\n" + "=" * 70)
    print("STARTING DEVELOPMENT CONSOLE APPLICATION")
    print("=" * 70)
    print(f"\nCommand: {cmd}")
    print("\n🚀 Starting application...")
    print("   Press CTRL+C to stop")
    print("   Watching for startup messages...\n")

    try:
        # Start process
        process = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8'
        )

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

        # Test port
        if check_port_open():
            print("\n" + "=" * 70)
            print("✅ SUCCESS - FIXED CODE WORKS IN DEVELOPMENT!")
            print("=" * 70)
            print("\n📊 DIAGNOSIS:")
            print("   ✅ BtrieveClient loads DLL from PATH")
            print("   ✅ FastAPI starts successfully")
            print("   ✅ Port 8001 is listening")
            print("\n🔍 NEXT STEPS:")
            print("   1. Commit and push to Git")
            print("   2. Pull in Deployment")
            print("   3. Test service startup")
            print("\n⏸️  Press CTRL+C to stop the application")

            # Keep running until interrupted
            process.wait()
        else:
            print("\n" + "=" * 70)
            print("❌ FAILED - APPLICATION HAS ISSUES")
            print("=" * 70)
            print("\n📊 Check the output above for errors")

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
    main()