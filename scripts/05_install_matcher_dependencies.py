"""
Session Script 05: Install ProductMatcher Dependencies
Installs rapidfuzz and unidecode for fuzzy matching
"""
import subprocess
import sys


def main():
    print("=" * 60)
    print("Phase 2: Installing Dependencies")
    print("=" * 60)

    deps = [
        'rapidfuzz>=3.0.0',
        'unidecode>=1.3.0'
    ]

    for dep in deps:
        print(f"\n[Installing] {dep}")
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'install', dep],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print(f"✅ {dep} installed")
        else:
            print(f"❌ Failed to install {dep}")
            print(result.stderr)
            return 1

    # Verify imports
    print("\n[Verifying] Imports...")
    try:
        import rapidfuzz
        import unidecode
        print(f"✅ rapidfuzz {rapidfuzz.__version__}")
        print(f"✅ unidecode installed")
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return 1

    print("\n" + "=" * 60)
    print("✅ Dependencies installed!")
    print("=" * 60)

    return 0


if __name__ == '__main__':
    sys.exit(main())