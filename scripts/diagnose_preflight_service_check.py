#!/usr/bin/env python3
"""
Diagnose the exact code in day5_preflight_check.py around service status check
"""

from pathlib import Path


def diagnose_code():
    """Show the exact code around service check"""

    script_path = Path("scripts/day5_preflight_check.py")

    if not script_path.exists():
        print(f"❌ File not found: {script_path}")
        return

    content = script_path.read_text(encoding='utf-8')
    lines = content.split('\n')

    print("=" * 70)
    print("  SEARCHING FOR SERVICE STATUS CHECK")
    print("=" * 70)
    print()

    # Find all relevant sections
    found_sections = []

    for i, line in enumerate(lines):
        # Look for service status related code
        if any(keyword in line.lower() for keyword in ['service', 'running', 'status', 'manage_service']):
            found_sections.append((i, line))

    print(f"Found {len(found_sections)} lines with service-related code")
    print()

    # Show context around key lines
    for i, line in found_sections:
        if 'if ' in line and ('running' in line.lower() or 'SERVICE_RUNNING' in line):
            print(f"📍 CRITICAL CHECK at line {i + 1}:")
            print("-" * 70)
            # Show 5 lines before and 5 lines after
            start = max(0, i - 5)
            end = min(len(lines), i + 6)

            for j in range(start, end):
                marker = ">>>" if j == i else "   "
                print(f"{marker} {j + 1:4d}: {lines[j]}")
            print()

    # Also search for the specific problem area
    print("=" * 70)
    print("  SEARCHING FOR SERVICE_OK VARIABLE")
    print("=" * 70)
    print()

    for i, line in enumerate(lines):
        if 'service_ok' in line.lower():
            print(f"{i + 1:4d}: {line}")

    print()
    print("=" * 70)
    print("  SEARCHING FOR SERVICE STATUS PRINT STATEMENTS")
    print("=" * 70)
    print()

    for i, line in enumerate(lines):
        if 'Service is' in line or 'NOT running' in line:
            start = max(0, i - 3)
            end = min(len(lines), i + 4)
            print(f"Found at line {i + 1}:")
            print("-" * 70)
            for j in range(start, end):
                marker = ">>>" if j == i else "   "
                print(f"{marker} {j + 1:4d}: {lines[j]}")
            print()


if __name__ == "__main__":
    diagnose_code()