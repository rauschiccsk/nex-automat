"""
Reinstall NEX Shared Package
Odinštaluje a znovu nainštaluje nex-shared
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd: list, description: str) -> bool:
    """Spusti príkaz"""
    print(f"\n{description}...")
    print(f"Command: {' '.join(cmd)}")
    print("-" * 60)

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )

        print(result.stdout)
        if result.stderr:
            print(result.stderr)

        print(f"✅ {description} - SUCCESS")
        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - FAILED")
        print(f"Error: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Stderr: {e.stderr}")
        return False


def main():
    """Main execution"""

    print("=" * 60)
    print("REINSTALLING NEX-SHARED PACKAGE")
    print("=" * 60)

    venv_python = Path("C:/Development/nex-automat/venv32/Scripts/python.exe")
    package_path = Path("C:/Development/nex-automat/packages/nex-shared")

    # Check paths
    if not venv_python.exists():
        print(f"❌ Python not found: {venv_python}")
        sys.exit(1)

    if not package_path.exists():
        print(f"❌ Package not found: {package_path}")
        sys.exit(1)

    # 1. Uninstall
    success = run_command(
        [str(venv_python), "-m", "pip", "uninstall", "-y", "nex-shared"],
        "Uninstalling nex-shared"
    )

    if not success:
        print("\n⚠️  Uninstall failed, but continuing...")

    # 2. Install
    success = run_command(
        [str(venv_python), "-m", "pip", "install", "-e", str(package_path)],
        "Installing nex-shared"
    )

    if not success:
        print("\n❌ Installation failed!")
        sys.exit(1)

    # 3. Verify
    print("\n" + "=" * 60)
    print("VERIFYING INSTALLATION")
    print("=" * 60)

    success = run_command(
        [str(venv_python), "-m", "pip", "show", "nex-shared"],
        "Checking installation"
    )

    if success:
        print("\n" + "=" * 60)
        print("✅ REINSTALLATION COMPLETE")
        print("=" * 60)
        print("\nNext step:")
        print("  python scripts/test_nex_shared_import.py")
    else:
        print("\n❌ Verification failed")
        sys.exit(1)


if __name__ == "__main__":
    main()