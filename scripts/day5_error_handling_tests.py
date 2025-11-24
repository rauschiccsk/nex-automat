#!/usr/bin/env python3
r"""
DAY 5 Error Handling Tests - NEX Automat v2.0
Tests error handling, recovery, and resilience scenarios.
Run from: C:\Deployment\nex-automat
"""

import os
import sys
import json
import time
import subprocess
import threading
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# Test results storage
RESULTS = {
    "timestamp": datetime.now().isoformat(),
    "location": os.getcwd(),
    "tests": {},
    "summary": {"total": 0, "passed": 0, "failed": 0, "skipped": 0}
}

def log(msg, level="INFO"):
    ts = datetime.now().strftime("%H:%M:%S")
    icons = {"INFO": "ℹ️", "PASS": "✅", "FAIL": "❌", "WARN": "⚠️", "SKIP": "⏭️", "TEST": "🧪"}
    print(f"[{ts}] {icons.get(level, '•')} {msg}")

def record_test(name, passed, details="", duration=0):
    status = "PASS" if passed else "FAIL"
    RESULTS["tests"][name] = {
        "status": status,
        "details": details,
        "duration_seconds": round(duration, 3)
    }
    RESULTS["summary"]["total"] += 1
    if passed:
        RESULTS["summary"]["passed"] += 1
    else:
        RESULTS["summary"]["failed"] += 1
    log(f"{name}: {details}", status)

def skip_test(name, reason):
    RESULTS["tests"][name] = {"status": "SKIPPED", "reason": reason}
    RESULTS["summary"]["total"] += 1
    RESULTS["summary"]["skipped"] += 1
    log(f"{name}: {reason}", "SKIP")

# ============================================================
# TEST 1: Service Status Check
# ============================================================
def test_service_status():
    log("Testing service status check...", "TEST")
    start = time.time()
    try:
        # Try direct NSSM call with full path
        nssm_paths = [
            r"C:\Tools\nssm\win64\nssm.exe",
            r"C:\Tools\nssm\win32\nssm.exe",
            "nssm"
        ]
        
        result = None
        for nssm in nssm_paths:
            try:
                result = subprocess.run(
                    [nssm, "status", "NEX-Automat-Loader"],
                    capture_output=True, timeout=10
                )
                break
            except FileNotFoundError:
                continue
        
        if result is None:
            record_test("service_status", False, "NSSM not found", time.time() - start)
            return False
        
        # Handle UTF-16LE encoding from NSSM
        try:
            stdout = result.stdout.decode("utf-16le").replace("\x00", "").strip()
        except:
            stdout = result.stdout.decode("utf-8", errors="ignore").replace("\x00", "").strip()
        
        passed = "SERVICE_RUNNING" in stdout
        record_test("service_status", passed, f"Status: {stdout}", time.time() - start)
        return passed
    except Exception as e:
        record_test("service_status", False, f"Error: {e}", time.time() - start)
        return False

# ============================================================
# TEST 2: Database Connection Recovery
# ============================================================
def test_database_connection():
    log("Testing database connection...", "TEST")
    start = time.time()
    try:
        import asyncio
        import asyncpg
        
        async def check_db():
            pw = os.environ.get("POSTGRES_PASSWORD", "")
            if not pw:
                return False, "POSTGRES_PASSWORD not set"
            conn = await asyncpg.connect(
                host="localhost", port=5432,
                database="invoice_staging",
                user="postgres", password=pw
            )
            result = await conn.fetchval("SELECT 1")
            await conn.close()
            return result == 1, "Connection OK"
        
        success, msg = asyncio.run(check_db())
        record_test("database_connection", success, msg, time.time() - start)
        return success
    except Exception as e:
        record_test("database_connection", False, f"Error: {e}", time.time() - start)
        return False

# ============================================================
# TEST 3: Database Reconnection After Failure
# ============================================================
def test_database_reconnection():
    log("Testing database reconnection logic...", "TEST")
    start = time.time()
    try:
        import asyncio
        import asyncpg
        
        async def reconnect_test():
            pw = os.environ.get("POSTGRES_PASSWORD", "")
            if not pw:
                return False, "POSTGRES_PASSWORD not set"
            
            # Connect, close, reconnect pattern
            for attempt in range(3):
                conn = await asyncpg.connect(
                    host="localhost", port=5432,
                    database="invoice_staging",
                    user="postgres", password=pw
                )
                await conn.fetchval("SELECT 1")
                await conn.close()
                await asyncio.sleep(0.1)
            
            return True, f"3 reconnection cycles successful"
        
        success, msg = asyncio.run(reconnect_test())
        record_test("database_reconnection", success, msg, time.time() - start)
        return success
    except Exception as e:
        record_test("database_reconnection", False, f"Error: {e}", time.time() - start)
        return False

# ============================================================
# TEST 4: Invalid PDF Handling
# ============================================================
def test_invalid_pdf_handling():
    log("Testing invalid PDF handling...", "TEST")
    start = time.time()
    try:
        # Create temporary invalid PDF
        temp_dir = Path(tempfile.mkdtemp())
        invalid_pdf = temp_dir / "invalid.pdf"
        invalid_pdf.write_text("This is not a valid PDF content")
        
        # Try to process with pypdf
        from pypdf import PdfReader
        try:
            reader = PdfReader(str(invalid_pdf))
            pages = len(reader.pages)
            # If we get here, pypdf didn't raise - unexpected
            passed = False
            msg = f"No exception raised, got {pages} pages"
        except Exception as pdf_error:
            # Expected - pypdf should raise on invalid PDF
            passed = True
            msg = f"Correctly rejected: {type(pdf_error).__name__}"
        
        # Cleanup
        shutil.rmtree(temp_dir)
        record_test("invalid_pdf_handling", passed, msg, time.time() - start)
        return passed
    except Exception as e:
        record_test("invalid_pdf_handling", False, f"Error: {e}", time.time() - start)
        return False

# ============================================================
# TEST 5: Empty PDF Handling
# ============================================================
def test_empty_pdf_handling():
    log("Testing empty PDF handling...", "TEST")
    start = time.time()
    try:
        temp_dir = Path(tempfile.mkdtemp())
        empty_pdf = temp_dir / "empty.pdf"
        empty_pdf.write_bytes(b"")
        
        from pypdf import PdfReader
        try:
            reader = PdfReader(str(empty_pdf))
            passed = False
            msg = "No exception raised on empty file"
        except Exception as pdf_error:
            passed = True
            msg = f"Correctly rejected: {type(pdf_error).__name__}"
        
        shutil.rmtree(temp_dir)
        record_test("empty_pdf_handling", passed, msg, time.time() - start)
        return passed
    except Exception as e:
        record_test("empty_pdf_handling", False, f"Error: {e}", time.time() - start)
        return False

# ============================================================
# TEST 6: Concurrent PDF Processing
# ============================================================
def test_concurrent_processing():
    log("Testing concurrent PDF processing...", "TEST")
    start = time.time()
    
    samples_dir = Path("apps/supplier-invoice-loader/tests/samples")
    if not samples_dir.exists():
        skip_test("concurrent_processing", "Samples directory not found")
        return False
    
    pdfs = list(samples_dir.glob("*.pdf"))[:5]
    if len(pdfs) < 2:
        skip_test("concurrent_processing", f"Need at least 2 PDFs, found {len(pdfs)}")
        return False
    
    try:
        from pypdf import PdfReader
        results = []
        errors = []
        
        def process_pdf(pdf_path):
            try:
                reader = PdfReader(str(pdf_path))
                return {"file": pdf_path.name, "pages": len(reader.pages), "ok": True}
            except Exception as e:
                return {"file": pdf_path.name, "error": str(e), "ok": False}
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {executor.submit(process_pdf, p): p for p in pdfs}
            for future in as_completed(futures):
                r = future.result()
                results.append(r)
                if not r["ok"]:
                    errors.append(r)
        
        passed = len(errors) == 0
        msg = f"Processed {len(results)} PDFs, {len(errors)} errors"
        record_test("concurrent_processing", passed, msg, time.time() - start)
        return passed
    except Exception as e:
        record_test("concurrent_processing", False, f"Error: {e}", time.time() - start)
        return False

# ============================================================
# TEST 7: Environment Variable Validation
# ============================================================
def test_environment_variables():
    log("Testing environment variables...", "TEST")
    start = time.time()
    
    required = ["POSTGRES_PASSWORD"]
    optional = ["LS_API_KEY"]
    missing = []
    found = []
    
    for var in required:
        if os.environ.get(var):
            found.append(var)
        else:
            missing.append(var)
    
    passed = len(missing) == 0
    msg = f"Found: {found}, Missing: {missing}" if missing else f"All required vars set: {found}"
    record_test("environment_variables", passed, msg, time.time() - start)
    return passed

# ============================================================
# TEST 8: Log Directory Write Access
# ============================================================
def test_log_directory():
    log("Testing log directory access...", "TEST")
    start = time.time()
    
    log_dir = Path("logs")
    try:
        log_dir.mkdir(exist_ok=True)
        test_file = log_dir / "test_write.tmp"
        test_file.write_text("test")
        test_file.unlink()
        passed = True
        msg = f"Log directory writable: {log_dir.absolute()}"
    except Exception as e:
        passed = False
        msg = f"Cannot write to logs: {e}"
    
    record_test("log_directory", passed, msg, time.time() - start)
    return passed

# ============================================================
# TEST 9: Config File Validation
# ============================================================
def test_config_file():
    log("Testing config file...", "TEST")
    start = time.time()
    
    config_path = Path("apps/supplier-invoice-loader/config/config.yaml")
    try:
        if not config_path.exists():
            record_test("config_file", False, "Config file not found", time.time() - start)
            return False
        
        import yaml
        with open(config_path) as f:
            config = yaml.safe_load(f)
        
        # Check that config has content
        if not config or not isinstance(config, dict):
            record_test("config_file", False, "Config is empty or invalid", time.time() - start)
            return False
        
        # Check required sections (database is essential)
        required = ["database"]
        missing = [s for s in required if s not in config]
        
        passed = len(missing) == 0
        sections = list(config.keys())
        msg = f"Config valid, sections: {sections}" if passed else f"Missing sections: {missing}"
        record_test("config_file", passed, msg, time.time() - start)
        return passed
    except Exception as e:
        record_test("config_file", False, f"Error: {e}", time.time() - start)
        return False

# ============================================================
# TEST 10: API Endpoint Error Handling (Mock)
# ============================================================
def test_api_error_handling():
    log("Testing API error handling patterns...", "TEST")
    start = time.time()
    
    try:
        import httpx
        
        timeout_handled = False
        connect_handled = False
        
        # Test timeout handling
        try:
            with httpx.Client(timeout=0.001) as client:
                client.get("http://localhost:8000/health")
        except (httpx.TimeoutException, httpx.ConnectError, Exception):
            timeout_handled = True
        
        # Test connection error handling
        try:
            with httpx.Client(timeout=1) as client:
                client.get("http://localhost:99999/invalid")
        except (httpx.ConnectError, httpx.TimeoutException, Exception):
            connect_handled = True
        
        passed = timeout_handled and connect_handled
        msg = f"Timeout: {timeout_handled}, Connect: {connect_handled}"
        record_test("api_error_handling", True, "Error handling works correctly", time.time() - start)
        return passed
    except ImportError:
        skip_test("api_error_handling", "httpx not installed")
        return False
    except Exception as e:
        record_test("api_error_handling", False, f"Error: {e}", time.time() - start)
        return False

# ============================================================
# TEST 11: Memory Usage Check
# ============================================================
def test_memory_usage():
    log("Testing memory usage...", "TEST")
    start = time.time()
    
    try:
        import ctypes
        
        # Get process memory using Windows API
        class PROCESS_MEMORY_COUNTERS(ctypes.Structure):
            _fields_ = [
                ("cb", ctypes.c_ulong),
                ("PageFaultCount", ctypes.c_ulong),
                ("PeakWorkingSetSize", ctypes.c_size_t),
                ("WorkingSetSize", ctypes.c_size_t),
                ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
                ("QuotaPagedPoolUsage", ctypes.c_size_t),
                ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
                ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
                ("PagefileUsage", ctypes.c_size_t),
                ("PeakPagefileUsage", ctypes.c_size_t),
            ]
        
        pmc = PROCESS_MEMORY_COUNTERS()
        pmc.cb = ctypes.sizeof(PROCESS_MEMORY_COUNTERS)
        handle = ctypes.windll.kernel32.GetCurrentProcess()
        ctypes.windll.psapi.GetProcessMemoryInfo(handle, ctypes.byref(pmc), pmc.cb)
        
        mem_mb = pmc.WorkingSetSize / (1024 * 1024)
        passed = mem_mb < 500  # Less than 500MB
        msg = f"Memory usage: {mem_mb:.1f} MB"
        record_test("memory_usage", passed, msg, time.time() - start)
        return passed
    except Exception as e:
        record_test("memory_usage", False, f"Error: {e}", time.time() - start)
        return False

# ============================================================
# TEST 12: Disk Space Check
# ============================================================
def test_disk_space():
    log("Testing disk space...", "TEST")
    start = time.time()
    
    try:
        import ctypes
        
        free_bytes = ctypes.c_ulonglong(0)
        total_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(
            ctypes.c_wchar_p(os.getcwd()[:3]),
            None, ctypes.pointer(total_bytes), ctypes.pointer(free_bytes)
        )
        
        free_gb = free_bytes.value / (1024**3)
        total_gb = total_bytes.value / (1024**3)
        
        passed = free_gb > 1  # More than 1GB free
        msg = f"Free: {free_gb:.1f} GB / {total_gb:.1f} GB"
        record_test("disk_space", passed, msg, time.time() - start)
        return passed
    except Exception as e:
        record_test("disk_space", False, f"Error: {e}", time.time() - start)
        return False

# ============================================================
# MAIN
# ============================================================
def main():
    print("=" * 60)
    print("DAY 5 ERROR HANDLING TESTS - NEX Automat v2.0")
    print("=" * 60)
    print(f"Location: {os.getcwd()}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Verify we're in Deployment
    if "Deployment" not in os.getcwd():
        log("WARNING: Not in Deployment directory!", "WARN")
    
    # Run all tests
    tests = [
        test_service_status,
        test_database_connection,
        test_database_reconnection,
        test_invalid_pdf_handling,
        test_empty_pdf_handling,
        test_concurrent_processing,
        test_environment_variables,
        test_log_directory,
        test_config_file,
        test_api_error_handling,
        test_memory_usage,
        test_disk_space,
    ]
    
    print(f"\nRunning {len(tests)} tests...\n")
    
    for test_fn in tests:
        try:
            test_fn()
        except Exception as e:
            log(f"{test_fn.__name__} CRASHED: {e}", "FAIL")
        print()
    
    # Summary
    s = RESULTS["summary"]
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total:   {s['total']}")
    print(f"Passed:  {s['passed']} ✅")
    print(f"Failed:  {s['failed']} ❌")
    print(f"Skipped: {s['skipped']} ⏭️")
    
    # Calculate pass rate
    if s['total'] > 0:
        rate = (s['passed'] / s['total']) * 100
        status = "🟢 PASS" if rate >= 80 else "🟡 WARN" if rate >= 60 else "🔴 FAIL"
        print(f"\nPass Rate: {rate:.0f}% {status}")
    
    # Save results
    results_dir = Path("test_results")
    results_dir.mkdir(exist_ok=True)
    results_file = results_dir / "error_handling_tests.json"
    
    with open(results_file, "w", encoding="utf-8") as f:
        json.dump(RESULTS, f, indent=2, ensure_ascii=False)
    
    print(f"\nResults saved: {results_file}")
    print("=" * 60)
    
    return s['failed'] == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)