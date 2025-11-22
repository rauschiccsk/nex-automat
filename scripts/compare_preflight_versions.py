#!/usr/bin/env python3
"""
Compare day5_preflight_check.py in Development vs Deployment
Show exact service check code in both locations
"""

from pathlib import Path


def show_service_check_function(file_path: Path, location_name: str):
    """Extract and show the check_service_status function"""

    if not file_path.exists():
        print(f"❌ {location_name}: File not found at {file_path}")
        return None

    content = file_path.read_text(encoding='utf-8')
    lines = content.split('\n')

    # Find the function
    start_line = None
    end_line = None

    for i, line in enumerate(lines):
        if 'def check_service_status()' in line:
            start_line = i
        if start_line is not None and i > start_line and line.strip().startswith(
                'def ') and 'check_service_status' not in line:
            end_line = i
            break

    if start_line is None:
        print(f"❌ {location_name}: Function check_service_status() not found")
        return None

    if end_line is None:
        # Function goes to end of file or until next section
        for i in range(start_line + 1, len(lines)):
            if lines[i].strip() and not lines[i].startswith(' ') and not lines[i].startswith('\t'):
                end_line = i
                break
        if end_line is None:
            end_line = len(lines)

    print(f"\n{'=' * 70}")
    print(f"  {location_name}")
    print(f"  {file_path}")
    print(f"  Lines {start_line + 1} to {end_line}")
    print(f"{'=' * 70}")

    for i in range(start_line, min(end_line, start_line + 30)):  # Show max 30 lines
        print(f"{i + 1:4d}: {lines[i]}")

    if end_line > start_line + 30:
        print(f"     ... ({end_line - start_line - 30} more lines)")

    return lines[start_line:end_line]


def main():
    print("=" * 70)
    print("  COMPARE PREFLIGHT VERSIONS")
    print("=" * 70)

    dev_path = Path("C:/Development/nex-automat/scripts/day5_preflight_check.py")
    dep_path = Path("C:/Deployment/nex-automat/scripts/day5_preflight_check.py")

    dev_func = show_service_check_function(dev_path, "DEVELOPMENT")
    dep_func = show_service_check_function(dep_path, "DEPLOYMENT")

    if dev_func and dep_func:
        print(f"\n{'=' * 70}")
        print("  COMPARISON")
        print(f"{'=' * 70}")

        if dev_func == dep_func:
            print("✅ Both versions are IDENTICAL")
        else:
            print("❌ Versions are DIFFERENT!")
            print(f"\n   Development: {len(dev_func)} lines")
            print(f"   Deployment:  {len(dep_func)} lines")

            # Show first difference
            for i, (dev_line, dep_line) in enumerate(zip(dev_func, dep_func)):
                if dev_line != dep_line:
                    print(f"\n   First difference at line {i + 1}:")
                    print(f"   DEV: {dev_line}")
                    print(f"   DEP: {dep_line}")
                    break

    print(f"\n{'=' * 70}")
    print("  FILE SIZES")
    print(f"{'=' * 70}")

    if dev_path.exists():
        print(f"Development: {dev_path.stat().st_size:,} bytes")
    if dep_path.exists():
        print(f"Deployment:  {dep_path.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()