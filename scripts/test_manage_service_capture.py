#!/usr/bin/env python3
"""
Test what manage_service.py status actually returns in stdout/stderr
"""

import subprocess
import sys


def test_capture():
    """Test capturing output from manage_service.py"""

    print("=" * 70)
    print("  TESTING manage_service.py OUTPUT CAPTURE")
    print("=" * 70)
    print()

    try:
        print("Running: python scripts/manage_service.py status")
        print()

        result = subprocess.run(
            ["python", "scripts/manage_service.py", "status"],
            capture_output=True,
            text=True,
            timeout=10
        )

        print("=" * 70)
        print("  RESULTS")
        print("=" * 70)
        print(f"Return code: {result.returncode}")
        print()

        print("-" * 70)
        print("  STDOUT (captured):")
        print("-" * 70)
        print(f"Length: {len(result.stdout)} chars")
        print(f"Content: [{result.stdout!r}]")
        print()
        if result.stdout:
            print("Lines:")
            for i, line in enumerate(result.stdout.split('\n'), 1):
                print(f"  {i}: [{line!r}]")
        else:
            print("  (EMPTY!)")
        print()

        print("-" * 70)
        print("  STDERR (captured):")
        print("-" * 70)
        print(f"Length: {len(result.stderr)} chars")
        print(f"Content: [{result.stderr!r}]")
        print()
        if result.stderr:
            print("Lines:")
            for i, line in enumerate(result.stderr.split('\n'), 1):
                print(f"  {i}: [{line!r}]")
        else:
            print("  (EMPTY!)")
        print()

        print("=" * 70)
        print("  CHECKS")
        print("=" * 70)

        # Test all patterns
        patterns = [
            ("running", result.stdout.lower()),
            ("SERVICE_RUNNING", result.stdout),
            ("service_running", result.stdout.lower()),
            ("RUNNING", result.stdout.upper()),
        ]

        for pattern, haystack in patterns:
            found = pattern in haystack
            status = "✅" if found else "❌"
            print(f"{status} '{pattern}' in stdout: {found}")

        print()

        # Also check stderr
        print("Checking stderr:")
        for pattern, _ in patterns:
            found = pattern in result.stderr.lower()
            status = "✅" if found else "❌"
            print(f"{status} '{pattern}' in stderr: {found}")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_capture()