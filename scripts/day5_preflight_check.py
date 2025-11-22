"""
DAY 5 Pre-Flight Check
=====================
Verifies system readiness before starting error handling and recovery testing.

Checks:
1. Service status (NEX-Automat-Loader)
2. Database connectivity (PostgreSQL + SQLite)
3. Dependencies verification
4. KNOWN_ISSUES.md existence
5. Test data availability
6. Performance baseline validation

Usage:
    cd C:\\Deployment\\nex-automat
    python scripts\\day5_preflight_check.py
"""

import sys
import subprocess
import json
import os
from pathlib import Path
from datetime import datetime

def print_section(title: str):
    """Print formatted section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def check_service_status() -> bool:
    """Check if NEX-Automat-Loader service is running."""
    print_section("1. SERVICE STATUS")

    try:
        result = subprocess.run(
            ["python", "scripts/manage_service.py", "status"],
            capture_output=True,
            text=True,
            timeout=10
        )

        print(result.stdout)

        # Check if service is running
        if "running" in result.stdout.lower():
            print("✅ Service is RUNNING")
            return True
        else:
            print("❌ Service is NOT running")
            print("   Run: python scripts/manage_service.py start")
            return False

    except Exception as e:
        print(f"❌ Error checking service: {e}")
        return False

def check_database_connectivity() -> bool:
    """Check PostgreSQL and SQLite connectivity."""
    print_section("2. DATABASE CONNECTIVITY")

    success = True

    # PostgreSQL check - use environment variable for password
    try:
        import pg8000.native
        pg_password = os.environ.get("POSTGRES_PASSWORD", "postgres")

        conn = pg8000.native.Connection(
            host="localhost",
            port=5432,
            database="invoice_staging",
            user="postgres",
            password=pg_password
        )
        conn.close()
        print("✅ PostgreSQL: Connected (localhost:5432/invoice_staging)")
    except Exception as e:
        print(f"❌ PostgreSQL: Failed - {e}")
        print("   Hint: Set POSTGRES_PASSWORD environment variable")
        success = False

    # SQLite check - only if configured in config.yaml
    sqlite_required = False
    sqlite_path = None

    try:
        config_path = Path("apps/supplier-invoice-loader/config/config.yaml")
        if config_path.exists():
            import yaml
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                db_config = config.get('database', {})

                # Check if SQLite is configured
                sqlite_path_str = db_config.get('sqlite_path')
                db_type = db_config.get('type', '').lower()

                sqlite_required = db_type == 'sqlite' or sqlite_path_str is not None

                if sqlite_path_str:
                    sqlite_path = Path(sqlite_path_str)
    except Exception as e:
        print(f"⚠️  Could not read config for SQLite check: {e}")

    # Perform SQLite check if required
    if sqlite_required:
        if sqlite_path and sqlite_path.exists():
            print(f"✅ SQLite: Database exists ({sqlite_path})")
        elif sqlite_path:
            print(f"❌ SQLite: Database NOT found at {sqlite_path}")
            success = False
        else:
            print("❌ SQLite: Required but path not configured in config.yaml")
            success = False
    else:
        print("✅ SQLite: Not required (using PostgreSQL primary)")

    return success


def check_dependencies() -> bool:
    """Verify critical dependencies are installed."""
    print_section("3. DEPENDENCIES")

    required = [
        "fastapi",
        "uvicorn", 
        "pdfplumber",
        "pg8000",
        "pypdf",
        "PIL",
        "httpx",
        "pydantic"
    ]

    missing = []

    for package in required:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - MISSING")
            missing.append(package)

    if missing:
        print(f"\n❌ Missing {len(missing)} packages: {', '.join(missing)}")
        print("   Run: pip install " + " ".join(missing))
        return False
    else:
        print(f"\n✅ All {len(required)} dependencies installed")
        return True

def check_known_issues() -> bool:
    """Check if KNOWN_ISSUES.md exists and display summary."""
    print_section("4. KNOWN ISSUES REVIEW")

    known_issues_path = Path("docs/deployment/KNOWN_ISSUES.md")

    if not known_issues_path.exists():
        print("⚠️  KNOWN_ISSUES.md not found")
        print("   This file should contain DAY 4 lessons learned")
        return False

    try:
        content = known_issues_path.read_text(encoding='utf-8')

        # Extract critical issues
        lines = content.split('\n')
        critical_count = sum(1 for line in lines if '❌' in line or 'CRITICAL' in line.upper())
        resolved_count = sum(1 for line in lines if '✅' in line)

        print(f"✅ KNOWN_ISSUES.md found ({len(lines)} lines)")
        print(f"   Resolved issues: {resolved_count}")
        print(f"   Critical issues: {critical_count}")

        if critical_count > 0:
            print("\n⚠️  ATTENTION: Active critical issues present!")
            # Show first 5 critical lines
            critical_lines = [line for line in lines if 'CRITICAL' in line.upper()][:5]
            for line in critical_lines:
                print(f"   {line.strip()}")

        return True

    except Exception as e:
        print(f"❌ Error reading KNOWN_ISSUES.md: {e}")
        return False

def check_test_data() -> bool:
    """Verify test data availability."""
    print_section("5. TEST DATA")

    test_samples = Path("apps/supplier-invoice-loader/tests/samples")

    if not test_samples.exists():
        print(f"❌ Test samples directory not found: {test_samples}")
        return False

    pdf_files = list(test_samples.glob("*.pdf"))

    if len(pdf_files) == 0:
        print("⚠️  No PDF test files found")
        return False

    print(f"✅ Found {len(pdf_files)} test PDF files")
    for pdf in pdf_files[:5]:  # Show first 5
        size_kb = pdf.stat().st_size / 1024
        print(f"   - {pdf.name} ({size_kb:.1f} KB)")

    if len(pdf_files) > 5:
        print(f"   ... and {len(pdf_files) - 5} more")

    return True

def check_performance_baseline() -> bool:
    """Verify performance baseline data exists."""
    print_section("6. PERFORMANCE BASELINE")

    # Check if we have performance test results
    perf_results = Path("test_results/performance_baseline.json")

    if not perf_results.exists():
        print("⚠️  No performance baseline found")
        print("   Expected: test_results/performance_baseline.json")
        print("   Run: python scripts/test_performance.py")
        return False

    try:
        data = json.loads(perf_results.read_text())

        print("✅ Performance baseline found")
        print(f"   Baseline date: {data.get('timestamp', 'unknown')}")
        print(f"   Health endpoint: {data.get('health_avg_ms', 'N/A')}ms avg")
        print(f"   Processing time: {data.get('processing_avg_s', 'N/A')}s avg")

        return True

    except Exception as e:
        print(f"❌ Error reading baseline: {e}")
        return False

def generate_summary(results: dict) -> str:
    """Generate final summary report."""
    print_section("SUMMARY")

    total = len(results)
    passed = sum(1 for v in results.values() if v)
    failed = total - passed

    status = "🟢 READY" if failed == 0 else "🟡 WARNINGS" if failed <= 2 else "🔴 NOT READY"

    print(f"\nChecks: {passed}/{total} passed")
    print(f"Status: {status}\n")

    for check, result in results.items():
        icon = "✅" if result else "❌"
        print(f"{icon} {check}")

    if failed > 0:
        print(f"\n⚠️  {failed} check(s) failed - review issues above")
        print("   Fix all critical issues before starting DAY 5 tests")
    else:
        print("\n✅ All systems GO - ready for DAY 5 testing")

    return status

def main():
    """Run all pre-flight checks."""
    print("\n" + "="*60)
    print("  NEX AUTOMAT v2.0 - DAY 5 PRE-FLIGHT CHECK")
    print("="*60)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"Location: {Path.cwd()}")

    results = {
        "Service Status": check_service_status(),
        "Database Connectivity": check_database_connectivity(),
        "Dependencies": check_dependencies(),
        "Known Issues": check_known_issues(),
        "Test Data": check_test_data(),
        "Performance Baseline": check_performance_baseline()
    }

    status = generate_summary(results)

    # Exit code
    if status == "🟢 READY":
        sys.exit(0)
    elif status == "🟡 WARNINGS":
        sys.exit(1)
    else:
        sys.exit(2)

if __name__ == "__main__":
    main()
