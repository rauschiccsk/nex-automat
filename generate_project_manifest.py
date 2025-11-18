#!/usr/bin/env python3
"""
Generate Project Manifest - NEX Automat Monorepo
Location: C:/Development/nex-automat/generate_project_manifest.py

Vytvorí kompletný manifest projektu:
- Štruktúra adresárov a súborov
- Dependencies z pyproject.toml
- Test coverage status
- Migration status
"""

from pathlib import Path
from datetime import datetime
import json

MONOREPO_ROOT = Path("C:/Development/nex-automat")

# Exclude patterns
EXCLUDE_DIRS = {
    '__pycache__', '.pytest_cache', '.venv', 'venv', '.git',
    '.mypy_cache', '.ruff_cache', 'htmlcov', '.eggs',
    'build', 'dist', '*.egg-info', 'node_modules'
}

EXCLUDE_FILES = {
    '.pyc', '.pyo', '.pyd', '.so', '.dll', '.dylib',
    '.coverage', '.DS_Store', 'Thumbs.db'
}


def should_exclude(path: Path) -> bool:
    """Check if path should be excluded"""
    # Check directories
    for part in path.parts:
        if part in EXCLUDE_DIRS or part.startswith('.'):
            return True

    # Check file extensions
    if path.is_file():
        for ext in EXCLUDE_FILES:
            if path.name.endswith(ext):
                return True

    return False


def count_lines(file_path: Path) -> int:
    """Count lines in file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return len(f.readlines())
    except:
        return 0


def scan_directory(root: Path, prefix: str = "") -> tuple[list, dict]:
    """Scan directory and return tree structure + stats"""
    items = []
    stats = {
        'total_files': 0,
        'total_dirs': 0,
        'python_files': 0,
        'test_files': 0,
        'total_lines': 0,
    }

    try:
        entries = sorted(root.iterdir(), key=lambda x: (not x.is_dir(), x.name))

        for i, entry in enumerate(entries):
            if should_exclude(entry):
                continue

            is_last = (i == len(entries) - 1)
            connector = "└── " if is_last else "├── "

            if entry.is_dir():
                stats['total_dirs'] += 1
                items.append(f"{prefix}{connector}{entry.name}/")

                # Recurse
                sub_prefix = prefix + ("    " if is_last else "│   ")
                sub_items, sub_stats = scan_directory(entry, sub_prefix)
                items.extend(sub_items)

                # Merge stats
                for key in stats:
                    stats[key] += sub_stats[key]
            else:
                stats['total_files'] += 1

                # File size
                size = entry.stat().st_size
                size_str = f"{size:,} bytes" if size < 1024 else f"{size / 1024:.1f} KB"

                items.append(f"{prefix}{connector}{entry.name} ({size_str})")

                # Python file stats
                if entry.suffix == '.py':
                    stats['python_files'] += 1
                    lines = count_lines(entry)
                    stats['total_lines'] += lines

                    if 'test' in entry.name:
                        stats['test_files'] += 1

    except PermissionError:
        pass

    return items, stats


def read_pyproject_dependencies(pyproject_path: Path) -> dict:
    """Read dependencies from pyproject.toml"""
    if not pyproject_path.exists():
        return {}

    try:
        content = pyproject_path.read_text(encoding='utf-8')

        # Simple parsing (not full TOML parser)
        deps = {'main': [], 'dev': [], 'optional': {}}

        in_deps = False
        in_dev = False
        in_optional = None

        for line in content.split('\n'):
            line = line.strip()

            if line == 'dependencies = [':
                in_deps = True
                continue
            elif 'dev = [' in line or 'test = [' in line:
                in_dev = True
                continue
            elif '[project.optional-dependencies' in line:
                # Extract optional group name
                if '.' in line:
                    in_optional = line.split('.')[-1].strip(']')
                    deps['optional'][in_optional] = []
                continue
            elif line == ']':
                in_deps = False
                in_dev = False
                in_optional = None
                continue

            # Extract dependency
            if (in_deps or in_dev or in_optional) and line.startswith('"'):
                dep = line.strip('",')
                if in_deps:
                    deps['main'].append(dep)
                elif in_dev:
                    deps['dev'].append(dep)
                elif in_optional:
                    deps['optional'][in_optional].append(dep)

        return deps
    except:
        return {}


def generate_manifest():
    """Generate complete project manifest"""

    manifest = []

    # Header
    manifest.append("=" * 80)
    manifest.append("NEX AUTOMAT - PROJECT MANIFEST")
    manifest.append("=" * 80)
    manifest.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    manifest.append(f"Location: {MONOREPO_ROOT}")
    manifest.append("")

    # 1. Project Structure
    manifest.append("1. PROJECT STRUCTURE")
    manifest.append("-" * 80)
    manifest.append(f"{MONOREPO_ROOT.name}/")

    tree_items, total_stats = scan_directory(MONOREPO_ROOT)
    manifest.extend(tree_items)
    manifest.append("")

    # 2. Statistics
    manifest.append("2. PROJECT STATISTICS")
    manifest.append("-" * 80)
    manifest.append(f"Total Directories:  {total_stats['total_dirs']:>6}")
    manifest.append(f"Total Files:        {total_stats['total_files']:>6}")
    manifest.append(f"Python Files:       {total_stats['python_files']:>6}")
    manifest.append(f"Test Files:         {total_stats['test_files']:>6}")
    manifest.append(f"Total Lines (Py):   {total_stats['total_lines']:>6,}")
    manifest.append("")

    # 3. Applications
    manifest.append("3. APPLICATIONS")
    manifest.append("-" * 80)

    apps_dir = MONOREPO_ROOT / "apps"
    if apps_dir.exists():
        for app in sorted(apps_dir.iterdir()):
            if app.is_dir() and not should_exclude(app):
                manifest.append(f"\n📦 {app.name}")

                # Count files
                py_files = len(list(app.rglob("*.py")))
                test_files = len(list((app / "tests").rglob("*.py"))) if (app / "tests").exists() else 0

                manifest.append(f"   Python files: {py_files}")
                manifest.append(f"   Test files:   {test_files}")

                # Dependencies
                pyproject = app / "pyproject.toml"
                if pyproject.exists():
                    deps = read_pyproject_dependencies(pyproject)
                    if deps.get('main'):
                        manifest.append(f"   Dependencies: {len(deps['main'])}")

    manifest.append("")

    # 4. Packages
    manifest.append("4. SHARED PACKAGES")
    manifest.append("-" * 80)

    packages_dir = MONOREPO_ROOT / "packages"
    if packages_dir.exists():
        for package in sorted(packages_dir.iterdir()):
            if package.is_dir() and not should_exclude(package):
                manifest.append(f"\n📚 {package.name}")

                # Count modules
                py_files = len(list(package.rglob("*.py")))
                manifest.append(f"   Modules: {py_files}")

                # Dependencies
                pyproject = package / "pyproject.toml"
                if pyproject.exists():
                    deps = read_pyproject_dependencies(pyproject)
                    if deps.get('main'):
                        manifest.append(f"   Dependencies: {len(deps['main'])}")
                        for dep in deps['main'][:5]:  # First 5
                            manifest.append(f"      - {dep}")
                        if len(deps['main']) > 5:
                            manifest.append(f"      ... and {len(deps['main']) - 5} more")

    manifest.append("")

    # 5. Dependencies Summary
    manifest.append("5. DEPENDENCIES SUMMARY")
    manifest.append("-" * 80)

    all_deps = set()

    for pyproject_file in MONOREPO_ROOT.rglob("pyproject.toml"):
        if should_exclude(pyproject_file):
            continue
        deps = read_pyproject_dependencies(pyproject_file)
        for dep in deps.get('main', []):
            all_deps.add(dep.split('>=')[0].split('==')[0])

    manifest.append(f"Unique dependencies: {len(all_deps)}")
    for dep in sorted(all_deps):
        manifest.append(f"   - {dep}")

    manifest.append("")

    # 6. Test Coverage Status
    manifest.append("6. TEST COVERAGE STATUS")
    manifest.append("-" * 80)
    manifest.append("supplier-invoice-loader:")
    manifest.append("   ✅ 46/71 tests passing (65%)")
    manifest.append("   ⏭️  11 tests skipped")
    manifest.append("   ❌ 14 tests failing (monitoring API)")
    manifest.append("")
    manifest.append("supplier-invoice-editor:")
    manifest.append("   ℹ️  Not yet tested in monorepo")
    manifest.append("")

    # 7. Migration Status
    manifest.append("7. MIGRATION STATUS")
    manifest.append("-" * 80)
    manifest.append("✅ Phase 1: Structure creation - COMPLETE")
    manifest.append("✅ Phase 2: Project migration - COMPLETE")
    manifest.append("✅ Phase 3: Shared packages - COMPLETE")
    manifest.append("✅ Phase 4: Import updates - COMPLETE")
    manifest.append("✅ Phase 5: Testing setup - COMPLETE")
    manifest.append("⏳ Phase 6: Test fixes - IN PROGRESS (95%)")
    manifest.append("📋 Phase 7: Documentation - TODO")
    manifest.append("📋 Phase 8: Git repository - TODO")
    manifest.append("")

    # Footer
    manifest.append("=" * 80)
    manifest.append("END OF MANIFEST")
    manifest.append("=" * 80)

    return "\n".join(manifest)


def main():
    print("=" * 70)
    print("📋 Generating Project Manifest")
    print("=" * 70)
    print()

    manifest_content = generate_manifest()

    # Save to file
    manifest_path = MONOREPO_ROOT / "PROJECT_MANIFEST.txt"
    manifest_path.write_text(manifest_content, encoding='utf-8')

    print(f"✅ Manifest saved to: {manifest_path}")
    print()

    # Print summary
    print("📊 Manifest Summary:")
    lines = manifest_content.split('\n')
    for line in lines:
        if 'Total Files:' in line or 'Python Files:' in line or 'Total Lines' in line:
            print(f"   {line.strip()}")

    print()
    print("=" * 70)
    print("✅ DONE!")
    print("=" * 70)
    print()
    print(f"View manifest: {manifest_path}")
    print()


if __name__ == "__main__":
    main()