# Check service logs for errors

from pathlib import Path
from datetime import datetime, timedelta

DEPLOY_ROOT = Path(r"C:\Deployment\nex-automat")
LOGS_DIR = DEPLOY_ROOT / "logs"

print("=" * 70)
print("CHECK SERVICE LOGS")
print("=" * 70)

# Find log directory
if not LOGS_DIR.exists():
    # Try alternative locations
    alt_logs = [
        DEPLOY_ROOT / "apps" / "supplier-invoice-loader" / "logs",
        DEPLOY_ROOT / "log",
    ]
    for alt in alt_logs:
        if alt.exists():
            LOGS_DIR = alt
            break

print(f"Log directory: {LOGS_DIR}")
print("=" * 70)

if not LOGS_DIR.exists():
    print(f"❌ Log directory not found: {LOGS_DIR}")
    print("\nTry checking NSSM logs:")
    print("  Get-EventLog -LogName Application -Source nssm -Newest 10")
    exit(1)

# List all log files
print("\nSTEP 1: Available log files")
print("-" * 70)
log_files = sorted(LOGS_DIR.glob("*.log"), key=lambda f: f.stat().st_mtime, reverse=True)

if not log_files:
    print("⚪ No .log files found")

    # Check for any files
    all_files = list(LOGS_DIR.glob("*"))
    if all_files:
        print(f"\nFound {len(all_files)} other files:")
        for f in sorted(all_files, key=lambda x: x.stat().st_mtime, reverse=True)[:10]:
            size = f.stat().st_size
            mtime = datetime.fromtimestamp(f.stat().st_mtime)
            print(f"  {f.name} ({size:,} bytes, {mtime:%Y-%m-%d %H:%M:%S})")
else:
    for log_file in log_files[:5]:  # Show top 5 most recent
        size = log_file.stat().st_size
        mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
        age = datetime.now() - mtime

        status = "🔴" if age < timedelta(minutes=5) else "⚪"
        print(f"{status} {log_file.name}")
        print(f"   Size: {size:,} bytes")
        print(f"   Modified: {mtime:%Y-%m-%d %H:%M:%S} ({age.seconds // 60} min ago)")

# Read most recent log
if log_files:
    print("\nSTEP 2: Recent log entries")
    print("-" * 70)

    most_recent = log_files[0]
    print(f"Reading: {most_recent.name}\n")

    try:
        content = most_recent.read_text(encoding='utf-8', errors='ignore')
        lines = content.split('\n')

        # Show last 50 lines
        print(f"Last 50 lines (total: {len(lines)}):")
        print("=" * 70)
        for line in lines[-50:]:
            if line.strip():
                print(line)

        # Look for errors
        print("\n" + "=" * 70)
        print("SEARCHING FOR ERRORS:")
        print("-" * 70)

        error_keywords = ['ERROR', 'CRITICAL', 'Exception', 'Traceback', 'Failed']
        recent_errors = []

        for i, line in enumerate(lines[-200:], start=len(lines) - 200):  # Last 200 lines
            if any(keyword in line for keyword in error_keywords):
                recent_errors.append((i, line))

        if recent_errors:
            print(f"Found {len(recent_errors)} error lines in last 200 lines:")
            for line_num, line in recent_errors[-10:]:  # Show last 10 errors
                print(f"  Line {line_num}: {line[:100]}")
        else:
            print("✅ No obvious errors in recent log entries")

    except Exception as e:
        print(f"❌ Could not read log: {e}")

# Check NSSM stderr/stdout
print("\n" + "=" * 70)
print("STEP 3: Check NSSM output files")
print("-" * 70)

nssm_logs = [
    LOGS_DIR / "nssm-stderr.log",
    LOGS_DIR / "nssm-stdout.log",
    LOGS_DIR / "stderr.log",
    LOGS_DIR / "stdout.log",
]

for nssm_log in nssm_logs:
    if nssm_log.exists():
        size = nssm_log.stat().st_size
        print(f"\n📄 {nssm_log.name} ({size:,} bytes)")

        if size > 0:
            try:
                content = nssm_log.read_text(encoding='utf-8', errors='ignore')
                lines = content.split('\n')
                print(f"   Last 20 lines:")
                for line in lines[-20:]:
                    if line.strip():
                        print(f"   {line}")
            except Exception as e:
                print(f"   ❌ Could not read: {e}")
        else:
            print("   (empty)")

print("\n" + "=" * 70)
print("LOG CHECK COMPLETE")
print("=" * 70)