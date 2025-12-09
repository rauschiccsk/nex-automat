"""
Session Script 01: Setup Dependencies v2.4
Installs dependencies for NEX Genesis enrichment
"""
import subprocess
import sys
from pathlib import Path


def run_cmd(cmd, cwd=None, check=True):
    """Execute command and print output"""
    print(f"\n> {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=check)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
    return result


def main():
    dev_path = Path(r"C:\Development\nex-automat")

    print("=" * 60)
    print("Setup: NEX Genesis Enrichment v2.4")
    print("=" * 60)

    # 1. Git operations
    print("\n[1/3] Switching to develop branch...")

    # Checkout develop
    run_cmd(['git', 'checkout', 'develop'], cwd=dev_path)

    # Pull latest
    run_cmd(['git', 'pull', 'origin', 'develop'], cwd=dev_path)

    # 2. Install dependencies
    print("\n[2/3] Installing dependencies...")

    deps = [
        'rapidfuzz>=3.0.0',
        'unidecode>=1.3.0'
    ]

    for dep in deps:
        run_cmd([sys.executable, '-m', 'pip', 'install', dep])

    # 3. Verify setup
    print("\n[3/3] Verifying setup...")

    try:
        import rapidfuzz
        import unidecode
        print(f"✅ rapidfuzz: {rapidfuzz.__version__}")
        print(f"✅ unidecode installed")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return 1

    # Check git status
    run_cmd(['git', 'status', '--short'], cwd=dev_path)

    print("\n" + "=" * 60)
    print("✅ Setup complete!")
    print("=" * 60)
    print(f"Branch: develop")
    print(f"Location: {dev_path}")
    print(f"Dependencies: rapidfuzz, unidecode")
    print("\nReady for Phase 1 implementation")

    return 0


if __name__ == '__main__':
    sys.exit(main())