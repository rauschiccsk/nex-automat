#!/usr/bin/env python3
"""
Fix create_baseline.py to not require psutil
Use only Python built-in modules
"""

from pathlib import Path


def fix_baseline_script():
    """Remove psutil dependency from create_baseline.py"""

    script_path = Path("scripts/create_baseline.py")

    if not script_path.exists():
        print(f"❌ File not found: {script_path}")
        return False

    print(f"📖 Reading {script_path}...")
    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove psutil import
    content = content.replace('import psutil\n', '')

    # Replace measure_memory_usage function
    old_memory = '''def measure_memory_usage() -> Dict:
    """Measure current memory usage"""
    print("\\n" + "="*60)
    print("  MEASURING MEMORY USAGE")
    print("="*60)

    process = psutil.Process()
    memory_info = process.memory_info()

    rss_mb = memory_info.rss / 1024 / 1024
    vms_mb = memory_info.vms / 1024 / 1024

    print(f"  RSS: {rss_mb:.1f} MB")
    print(f"  VMS: {vms_mb:.1f} MB")

    return {
        "rss_mb": rss_mb,
        "vms_mb": vms_mb
    }'''

    new_memory = '''def measure_memory_usage() -> Dict:
    """Measure current memory usage - simplified without psutil"""
    print("\\n" + "="*60)
    print("  MEASURING MEMORY USAGE")
    print("="*60)

    # psutil not available on Windows 32-bit Python 3.13
    # Skip memory measurement
    print("  ⚠️  Memory measurement skipped (psutil not available)")

    return {
        "skipped": "psutil_not_available"
    }'''

    content = content.replace(old_memory, new_memory)

    # Replace measure_system_resources function
    old_resources = '''def measure_system_resources() -> Dict:
    """Measure system resources"""
    print("\\n" + "="*60)
    print("  MEASURING SYSTEM RESOURCES")
    print("="*60)

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
    }'''

    new_resources = '''def measure_system_resources() -> Dict:
    """Measure system resources - simplified without psutil"""
    print("\\n" + "="*60)
    print("  MEASURING SYSTEM RESOURCES")
    print("="*60)

    import os
    import platform

    cpu_count = os.cpu_count() or 0

    print(f"  CPU cores: {cpu_count}")
    print(f"  Platform: {platform.system()} {platform.release()}")
    print(f"  Python: {platform.python_version()}")
    print("  ⚠️  CPU/Memory usage skipped (psutil not available)")

    return {
        "cpu_cores": cpu_count,
        "platform": platform.system(),
        "platform_release": platform.release(),
        "python_version": platform.python_version()
    }'''

    content = content.replace(old_resources, new_resources)

    # Update summary section
    old_summary = '''    print(f"✅ Memory: {baseline['memory_usage']['rss_mb']:.1f} MB")
    print(f"✅ CPU: {baseline['system_resources']['cpu_percent']}%")'''

    new_summary = '''    if 'rss_mb' in baseline['memory_usage']:
        print(f"✅ Memory: {baseline['memory_usage']['rss_mb']:.1f} MB")
    else:
        print(f"⚠️  Memory: {baseline['memory_usage'].get('skipped', 'N/A')}")

    print(f"✅ CPU cores: {baseline['system_resources']['cpu_cores']}")'''

    content = content.replace(old_summary, new_summary)

    # Write back
    print(f"💾 Writing fixed script...")
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print()
    print("✅ Script fixed - no longer requires psutil!")
    print()
    print("Next steps:")
    print("1. Deploy:")
    print("   python scripts\\deploy_to_deployment.py")
    print("2. Create baseline:")
    print("   cd C:\\Deployment\\nex-automat")
    print("   python scripts\\create_baseline.py")

    return True


if __name__ == "__main__":
    print("=" * 70)
    print("  FIX CREATE_BASELINE - REMOVE PSUTIL DEPENDENCY")
    print("=" * 70)
    print()

    success = fix_baseline_script()

    if success:
        print()
        print("✅ SUCCESS")
    else:
        print()
        print("❌ FAILED")