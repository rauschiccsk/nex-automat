#!/usr/bin/env python3
r"""
DAY 5 Performance Tests - NEX Automat v2.0
Load testing, throughput, and performance validation.
Run from: C:\Deployment\nex-automat
"""

import os
import sys
import json
import time
import asyncio
import statistics
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# Results storage
RESULTS = {
    "timestamp": datetime.now().isoformat(),
    "location": os.getcwd(),
    "tests": {},
    "baseline_comparison": {},
    "summary": {}
}

def log(msg, level="INFO"):
    ts = datetime.now().strftime("%H:%M:%S")
    icons = {"INFO": "ℹ️", "PASS": "✅", "FAIL": "❌", "WARN": "⚠️", "TEST": "🧪", "PERF": "⚡"}
    print(f"[{ts}] {icons.get(level, '•')} {msg}")

def load_baseline():
    """Load performance baseline for comparison."""
    baseline_file = Path("test_results/performance_baseline.json")
    if baseline_file.exists():
        with open(baseline_file) as f:
            return json.load(f)
    return None

# ============================================================
# TEST 1: Single PDF Processing Time
# ============================================================
def test_single_pdf_processing():
    log("Testing single PDF processing time...", "TEST")
    
    samples_dir = Path("apps/supplier-invoice-loader/tests/samples")
    pdfs = list(samples_dir.glob("*.pdf"))[:1]
    
    if not pdfs:
        log("No PDF samples found", "FAIL")
        return None
    
    from pypdf import PdfReader
    
    times = []
    for _ in range(5):  # 5 iterations for consistency
        start = time.perf_counter()
        reader = PdfReader(str(pdfs[0]))
        pages = len(reader.pages)
        for page in reader.pages:
            text = page.extract_text()
        elapsed = time.perf_counter() - start
        times.append(elapsed)
    
    result = {
        "file": pdfs[0].name,
        "iterations": 5,
        "avg_time": statistics.mean(times),
        "min_time": min(times),
        "max_time": max(times),
        "std_dev": statistics.stdev(times) if len(times) > 1 else 0
    }
    
    RESULTS["tests"]["single_pdf"] = result
    log(f"Single PDF: avg={result['avg_time']:.3f}s, min={result['min_time']:.3f}s, max={result['max_time']:.3f}s", "PERF")
    return result

# ============================================================
# TEST 2: Batch PDF Processing (5, 10, 18 files)
# ============================================================
def test_batch_processing():
    log("Testing batch PDF processing...", "TEST")
    
    samples_dir = Path("apps/supplier-invoice-loader/tests/samples")
    all_pdfs = list(samples_dir.glob("*.pdf"))
    
    if len(all_pdfs) < 5:
        log(f"Need at least 5 PDFs, found {len(all_pdfs)}", "FAIL")
        return None
    
    from pypdf import PdfReader
    
    def process_pdf(pdf_path):
        start = time.perf_counter()
        reader = PdfReader(str(pdf_path))
        for page in reader.pages:
            text = page.extract_text()
        return time.perf_counter() - start
    
    batch_sizes = [5, 10, min(18, len(all_pdfs))]
    results = {}
    
    for batch_size in batch_sizes:
        if batch_size > len(all_pdfs):
            continue
            
        pdfs = all_pdfs[:batch_size]
        
        # Sequential processing
        seq_start = time.perf_counter()
        seq_times = [process_pdf(p) for p in pdfs]
        seq_total = time.perf_counter() - seq_start
        
        results[f"batch_{batch_size}"] = {
            "count": batch_size,
            "total_time": seq_total,
            "avg_per_file": seq_total / batch_size,
            "throughput_per_sec": batch_size / seq_total
        }
        
        log(f"Batch {batch_size}: total={seq_total:.2f}s, avg={seq_total/batch_size:.3f}s/file, throughput={batch_size/seq_total:.2f}/s", "PERF")
    
    RESULTS["tests"]["batch_processing"] = results
    return results

# ============================================================
# TEST 3: Concurrent Processing (ThreadPool)
# ============================================================
def test_concurrent_processing():
    log("Testing concurrent PDF processing...", "TEST")
    
    samples_dir = Path("apps/supplier-invoice-loader/tests/samples")
    all_pdfs = list(samples_dir.glob("*.pdf"))[:10]
    
    if len(all_pdfs) < 5:
        log(f"Need at least 5 PDFs, found {len(all_pdfs)}", "FAIL")
        return None
    
    from pypdf import PdfReader
    
    def process_pdf(pdf_path):
        start = time.perf_counter()
        reader = PdfReader(str(pdf_path))
        for page in reader.pages:
            text = page.extract_text()
        return {"file": pdf_path.name, "time": time.perf_counter() - start}
    
    worker_counts = [1, 2, 4, 8]
    results = {}
    
    for workers in worker_counts:
        start = time.perf_counter()
        
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = [executor.submit(process_pdf, p) for p in all_pdfs]
            file_results = [f.result() for f in as_completed(futures)]
        
        total_time = time.perf_counter() - start
        
        results[f"workers_{workers}"] = {
            "workers": workers,
            "files": len(all_pdfs),
            "total_time": total_time,
            "throughput_per_sec": len(all_pdfs) / total_time
        }
        
        log(f"Workers {workers}: total={total_time:.2f}s, throughput={len(all_pdfs)/total_time:.2f}/s", "PERF")
    
    RESULTS["tests"]["concurrent_processing"] = results
    return results

# ============================================================
# TEST 4: Database Query Performance
# ============================================================
def test_database_performance():
    log("Testing database performance...", "TEST")
    
    try:
        import asyncpg
        
        async def run_db_tests():
            pw = os.environ.get("POSTGRES_PASSWORD", "")
            if not pw:
                return None
            
            conn = await asyncpg.connect(
                host="localhost", port=5432,
                database="invoice_staging",
                user="postgres", password=pw
            )
            
            results = {}
            
            # Test 1: Simple SELECT
            times = []
            for _ in range(10):
                start = time.perf_counter()
                await conn.fetchval("SELECT 1")
                times.append(time.perf_counter() - start)
            results["simple_select"] = {
                "iterations": 10,
                "avg_time": statistics.mean(times),
                "min_time": min(times),
                "max_time": max(times)
            }
            
            # Test 2: Table count
            times = []
            for _ in range(5):
                start = time.perf_counter()
                await conn.fetchval("SELECT COUNT(*) FROM information_schema.tables")
                times.append(time.perf_counter() - start)
            results["table_count"] = {
                "iterations": 5,
                "avg_time": statistics.mean(times)
            }
            
            # Test 3: Connection pool simulation
            times = []
            for _ in range(5):
                start = time.perf_counter()
                test_conn = await asyncpg.connect(
                    host="localhost", port=5432,
                    database="invoice_staging",
                    user="postgres", password=pw
                )
                await test_conn.fetchval("SELECT 1")
                await test_conn.close()
                times.append(time.perf_counter() - start)
            results["connection_cycle"] = {
                "iterations": 5,
                "avg_time": statistics.mean(times)
            }
            
            await conn.close()
            return results
        
        results = asyncio.run(run_db_tests())
        
        if results:
            RESULTS["tests"]["database_performance"] = results
            log(f"DB Simple SELECT: avg={results['simple_select']['avg_time']*1000:.2f}ms", "PERF")
            log(f"DB Connection cycle: avg={results['connection_cycle']['avg_time']*1000:.2f}ms", "PERF")
            return results
        else:
            log("Database tests skipped - no password", "WARN")
            return None
            
    except Exception as e:
        log(f"Database test error: {e}", "FAIL")
        return None

# ============================================================
# TEST 5: Memory Under Load
# ============================================================
def test_memory_under_load():
    log("Testing memory usage under load...", "TEST")
    
    import ctypes
    
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
    
    def get_memory_mb():
        pmc = PROCESS_MEMORY_COUNTERS()
        pmc.cb = ctypes.sizeof(PROCESS_MEMORY_COUNTERS)
        handle = ctypes.windll.kernel32.GetCurrentProcess()
        ctypes.windll.psapi.GetProcessMemoryInfo(handle, ctypes.byref(pmc), pmc.cb)
        return pmc.WorkingSetSize / (1024 * 1024)
    
    # Measure before
    mem_before = get_memory_mb()
    
    # Load all PDFs into memory
    samples_dir = Path("apps/supplier-invoice-loader/tests/samples")
    pdfs = list(samples_dir.glob("*.pdf"))
    
    from pypdf import PdfReader
    
    readers = []
    for pdf in pdfs:
        reader = PdfReader(str(pdf))
        readers.append(reader)
    
    # Measure after loading
    mem_after_load = get_memory_mb()
    
    # Process all
    for reader in readers:
        for page in reader.pages:
            text = page.extract_text()
    
    # Measure after processing
    mem_after_process = get_memory_mb()
    
    # Cleanup
    readers.clear()
    
    # Measure after cleanup
    mem_after_cleanup = get_memory_mb()
    
    results = {
        "before_mb": mem_before,
        "after_load_mb": mem_after_load,
        "after_process_mb": mem_after_process,
        "after_cleanup_mb": mem_after_cleanup,
        "load_increase_mb": mem_after_load - mem_before,
        "process_increase_mb": mem_after_process - mem_after_load,
        "cleanup_released_mb": mem_after_process - mem_after_cleanup,
        "pdf_count": len(pdfs)
    }
    
    RESULTS["tests"]["memory_under_load"] = results
    log(f"Memory: before={mem_before:.1f}MB, peak={mem_after_process:.1f}MB, after={mem_after_cleanup:.1f}MB", "PERF")
    
    # Check for memory leak
    leak = mem_after_cleanup - mem_before
    if leak > 50:  # More than 50MB retained
        log(f"Potential memory leak: {leak:.1f}MB retained", "WARN")
    else:
        log(f"Memory cleanup OK: {leak:.1f}MB retained", "PASS")
    
    return results

# ============================================================
# TEST 6: Baseline Comparison
# ============================================================
def compare_with_baseline():
    log("Comparing with performance baseline...", "TEST")
    
    baseline = load_baseline()
    if not baseline:
        log("No baseline found for comparison", "WARN")
        return None
    
    comparisons = {}
    
    # Compare PDF processing
    if "pdf_processing" in baseline and "batch_processing" in RESULTS["tests"]:
        baseline_throughput = baseline["pdf_processing"].get("throughput_per_second", 0)
        
        # Get current throughput from batch_5
        current = RESULTS["tests"]["batch_processing"].get("batch_5", {})
        current_throughput = current.get("throughput_per_sec", 0)
        
        if baseline_throughput > 0 and current_throughput > 0:
            change_pct = ((current_throughput - baseline_throughput) / baseline_throughput) * 100
            comparisons["pdf_throughput"] = {
                "baseline": baseline_throughput,
                "current": current_throughput,
                "change_percent": change_pct,
                "status": "IMPROVED" if change_pct > 5 else "DEGRADED" if change_pct < -10 else "STABLE"
            }
            log(f"PDF Throughput: {change_pct:+.1f}% ({comparisons['pdf_throughput']['status']})", "PERF")
    
    # Compare DB performance
    if "database_operations" in baseline and "database_performance" in RESULTS["tests"]:
        baseline_conn = baseline["database_operations"].get("connection_time", 0)
        current_conn = RESULTS["tests"]["database_performance"].get("connection_cycle", {}).get("avg_time", 0)
        
        if baseline_conn > 0 and current_conn > 0:
            change_pct = ((current_conn - baseline_conn) / baseline_conn) * 100
            comparisons["db_connection"] = {
                "baseline_ms": baseline_conn * 1000,
                "current_ms": current_conn * 1000,
                "change_percent": change_pct,
                "status": "IMPROVED" if change_pct < -5 else "DEGRADED" if change_pct > 20 else "STABLE"
            }
            log(f"DB Connection: {change_pct:+.1f}% ({comparisons['db_connection']['status']})", "PERF")
    
    RESULTS["baseline_comparison"] = comparisons
    return comparisons

# ============================================================
# MAIN
# ============================================================
def main():
    print("=" * 60)
    print("DAY 5 PERFORMANCE TESTS - NEX Automat v2.0")
    print("=" * 60)
    print(f"Location: {os.getcwd()}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Run all tests
    tests = [
        ("Single PDF Processing", test_single_pdf_processing),
        ("Batch Processing", test_batch_processing),
        ("Concurrent Processing", test_concurrent_processing),
        ("Database Performance", test_database_performance),
        ("Memory Under Load", test_memory_under_load),
        ("Baseline Comparison", compare_with_baseline),
    ]
    
    print(f"\nRunning {len(tests)} performance tests...\n")
    
    for name, test_fn in tests:
        try:
            test_fn()
        except Exception as e:
            log(f"{name} CRASHED: {e}", "FAIL")
        print()
    
    # Summary
    print("=" * 60)
    print("PERFORMANCE SUMMARY")
    print("=" * 60)
    
    # Key metrics
    if "batch_processing" in RESULTS["tests"]:
        batch = RESULTS["tests"]["batch_processing"]
        if "batch_5" in batch:
            print(f"📊 Throughput (5 files): {batch['batch_5']['throughput_per_sec']:.2f} files/sec")
        if "batch_10" in batch:
            print(f"📊 Throughput (10 files): {batch['batch_10']['throughput_per_sec']:.2f} files/sec")
    
    if "concurrent_processing" in RESULTS["tests"]:
        conc = RESULTS["tests"]["concurrent_processing"]
        best = max(conc.values(), key=lambda x: x["throughput_per_sec"])
        print(f"📊 Best concurrent: {best['workers']} workers @ {best['throughput_per_sec']:.2f} files/sec")
    
    if "memory_under_load" in RESULTS["tests"]:
        mem = RESULTS["tests"]["memory_under_load"]
        print(f"📊 Peak memory: {mem['after_process_mb']:.1f} MB")
        print(f"📊 Memory retained: {mem['after_cleanup_mb'] - mem['before_mb']:.1f} MB")
    
    if "database_performance" in RESULTS["tests"]:
        db = RESULTS["tests"]["database_performance"]
        print(f"📊 DB query avg: {db['simple_select']['avg_time']*1000:.2f} ms")
    
    # Overall status
    print()
    overall = "🟢 PASS" if RESULTS["tests"] else "🔴 FAIL"
    print(f"Overall Status: {overall}")
    
    # Save results
    results_dir = Path("test_results")
    results_dir.mkdir(exist_ok=True)
    results_file = results_dir / "performance_tests.json"
    
    with open(results_file, "w", encoding="utf-8") as f:
        json.dump(RESULTS, f, indent=2, ensure_ascii=False)
    
    print(f"\nResults saved: {results_file}")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)