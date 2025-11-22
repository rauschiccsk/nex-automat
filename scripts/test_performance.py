#!/usr/bin/env python3
"""
Performance Baseline Test for NEX Automat v2.0
Creates initial performance metrics for future comparison
"""

import sys
import time
import json
import psutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def measure_pdf_processing() -> Dict:
    """Measure PDF processing performance"""
    print("\n" + "=" * 60)
    print("  MEASURING PDF PROCESSING")
    print("=" * 60)

    samples_dir = project_root / "apps" / "supplier-invoice-loader" / "tests" / "samples"

    if not samples_dir.exists():
        print(f"❌ Samples directory not found: {samples_dir}")
        return {"error": "samples_not_found"}

    pdf_files = list(samples_dir.glob("*.pdf"))
    if not pdf_files:
        print("❌ No PDF files found")
        return {"error": "no_pdfs"}

    print(f"Found {len(pdf_files)} PDF files")

    # Import PDF processing (lazy import to avoid issues if not available)
    try:
        import pypdf
        from PIL import Image
        import pdfplumber
    except ImportError as e:
        print(f"⚠️  PDF libraries not available: {e}")
        return {"error": f"import_error: {e}"}

    times = []
    sizes = []

    for pdf_file in pdf_files[:5]:  # Test first 5 PDFs
        file_size = pdf_file.stat().st_size

        start = time.perf_counter()

        try:
            # Simulate PDF processing
            with pdfplumber.open(pdf_file) as pdf:
                num_pages = len(pdf.pages)
                # Extract text from first page
                if num_pages > 0:
                    text = pdf.pages[0].extract_text()

            elapsed = time.perf_counter() - start
            times.append(elapsed)
            sizes.append(file_size)

            print(f"  {pdf_file.name}: {elapsed:.3f}s ({file_size / 1024:.1f} KB)")

        except Exception as e:
            print(f"  ❌ {pdf_file.name}: Error - {e}")

    if not times:
        return {"error": "no_successful_processing"}

    return {
        "count": len(times),
        "avg_time": sum(times) / len(times),
        "min_time": min(times),
        "max_time": max(times),
        "avg_size_kb": sum(sizes) / len(sizes) / 1024,
        "throughput_per_second": 1.0 / (sum(times) / len(times))
    }


def measure_database_operations() -> Dict:
    """Measure database operation performance"""
    print("\n" + "=" * 60)
    print("  MEASURING DATABASE OPERATIONS")
    print("=" * 60)

    try:
        import asyncpg
        import asyncio
    except ImportError:
        print("⚠️  asyncpg not available")
        return {"error": "asyncpg_not_available"}

    # Load config
    try:
        import yaml
        config_path = project_root / "apps" / "supplier-invoice-loader" / "config" / "config.yaml"
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)

        db_config = config['database']
    except Exception as e:
        print(f"⚠️  Could not load config: {e}")
        return {"error": f"config_error: {e}"}

    async def test_db():
        """Test database operations"""
        try:
            # Connect
            conn_start = time.perf_counter()
            conn = await asyncpg.connect(
                host=db_config['host'],
                port=db_config['port'],
                database=db_config['database'],
                user=db_config['user'],
                password=db_config.get('password', '')
            )
            conn_time = time.perf_counter() - conn_start
            print(f"  Connection: {conn_time:.3f}s")

            # Simple SELECT
            select_start = time.perf_counter()
            result = await conn.fetch("SELECT 1")
            select_time = time.perf_counter() - select_start
            print(f"  Simple SELECT: {select_time:.3f}s")

            # Table check
            table_start = time.perf_counter()
            tables = await conn.fetch(
                "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
            )
            table_time = time.perf_counter() - table_start
            print(f"  Table query: {table_time:.3f}s ({len(tables)} tables)")

            await conn.close()

            return {
                "connection_time": conn_time,
                "simple_select_time": select_time,
                "table_query_time": table_time,
                "tables_count": len(tables)
            }

        except Exception as e:
            print(f"  ❌ Database error: {e}")
            return {"error": str(e)}

    return asyncio.run(test_db())


def measure_memory_usage() -> Dict:
    """Measure current memory usage"""
    print("\n" + "=" * 60)
    print("  MEASURING MEMORY USAGE")
    print("=" * 60)

    process = psutil.Process()
    memory_info = process.memory_info()

    rss_mb = memory_info.rss / 1024 / 1024
    vms_mb = memory_info.vms / 1024 / 1024

    print(f"  RSS: {rss_mb:.1f} MB")
    print(f"  VMS: {vms_mb:.1f} MB")

    return {
        "rss_mb": rss_mb,
        "vms_mb": vms_mb
    }


def measure_system_resources() -> Dict:
    """Measure system resources"""
    print("\n" + "=" * 60)
    print("  MEASURING SYSTEM RESOURCES")
    print("=" * 60)

    cpu_count = psutil.cpu_count()
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()

    print(f"  CPU cores: {cpu_count}")
    print(f"  CPU usage: {cpu_percent}%")
    print(f"  Memory total: {memory.total / 1024 / 1024 / 1024:.1f} GB")
    print(f"  Memory available: {memory.available / 1024 / 1024 / 1024:.1f} GB")
    print(f"  Memory percent: {memory.percent}%")

    return {
        "cpu_cores": cpu_count,
        "cpu_percent": cpu_percent,
        "memory_total_gb": memory.total / 1024 / 1024 / 1024,
        "memory_available_gb": memory.available / 1024 / 1024 / 1024,
        "memory_percent": memory.percent
    }


def create_baseline():
    """Create performance baseline"""
    print("=" * 60)
    print("  NEX AUTOMAT v2.0 - PERFORMANCE BASELINE")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"Location: {project_root}")

    baseline = {
        "timestamp": datetime.now().isoformat(),
        "location": str(project_root),
        "pdf_processing": measure_pdf_processing(),
        "database_operations": measure_database_operations(),
        "memory_usage": measure_memory_usage(),
        "system_resources": measure_system_resources()
    }

    # Save to file
    output_dir = project_root / "test_results"
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / "performance_baseline.json"

    print("\n" + "=" * 60)
    print("  SAVING BASELINE")
    print("=" * 60)
    print(f"Output: {output_file}")

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(baseline, f, indent=2)

    print("✅ Baseline saved successfully")

    # Summary
    print("\n" + "=" * 60)
    print("  BASELINE SUMMARY")
    print("=" * 60)

    if "avg_time" in baseline["pdf_processing"]:
        print(f"PDF Processing: {baseline['pdf_processing']['avg_time']:.3f}s average")

    if "connection_time" in baseline["database_operations"]:
        print(f"DB Connection: {baseline['database_operations']['connection_time']:.3f}s")

    print(f"Memory: {baseline['memory_usage']['rss_mb']:.1f} MB")
    print(f"CPU: {baseline['system_resources']['cpu_percent']}%")

    print("\n✅ Performance baseline created successfully!")
    print(f"   File: {output_file}")

    return True


if __name__ == "__main__":
    try:
        success = create_baseline()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Error creating baseline: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)