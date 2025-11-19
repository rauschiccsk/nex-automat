#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate Projects Access - NEX Automat Monorepo
Location: C:/Development/nex-automat/generate_projects_access.py

Vytvorí hierarchické JSON manifesty:
- docs/PROJECT_MANIFEST.json - root overview
- docs/apps/{app_name}.json - per-app manifests
- docs/packages/{package_name}.json - per-package manifests

Pre efektívne lazy loading v Claude sessions.
"""

from pathlib import Path
from datetime import datetime
import json

MONOREPO_ROOT = Path("C:/Development/nex-automat")
DOCS_DIR = MONOREPO_ROOT / "docs"
APPS_MANIFEST_DIR = DOCS_DIR / "apps"
PACKAGES_MANIFEST_DIR = DOCS_DIR / "packages"

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
    for part in path.parts:
        if part in EXCLUDE_DIRS or part.startswith('.'):
            return True

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


def scan_files(root: Path, relative_to: Path = None) -> list[dict]:
    """Scan files and return structured list"""
    files = []
    base = relative_to or root

    try:
        for item in root.rglob("*"):
            if should_exclude(item) or item.is_dir():
                continue

            rel_path = item.relative_to(base)
            file_info = {
                "path": str(rel_path).replace('\\', '/'),
                "name": item.name,
                "size": item.stat().st_size,
                "extension": item.suffix
            }

            # Python-specific info
            if item.suffix == '.py':
                file_info["lines"] = count_lines(item)
                file_info["type"] = "test" if "test" in item.name else "source"

            files.append(file_info)

    except PermissionError:
        pass

    return sorted(files, key=lambda x: x["path"])


def get_directory_stats(root: Path) -> dict:
    """Get statistics for directory"""
    stats = {
        'total_files': 0,
        'total_dirs': 0,
        'python_files': 0,
        'test_files': 0,
        'total_lines': 0,
        'total_size': 0
    }

    try:
        for item in root.rglob("*"):
            if should_exclude(item):
                continue

            if item.is_dir():
                stats['total_dirs'] += 1
            else:
                stats['total_files'] += 1
                stats['total_size'] += item.stat().st_size

                if item.suffix == '.py':
                    stats['python_files'] += 1
                    stats['total_lines'] += count_lines(item)

                    if 'test' in item.name:
                        stats['test_files'] += 1

    except PermissionError:
        pass

    return stats


def read_pyproject_dependencies(pyproject_path: Path) -> dict:
    """Read dependencies from pyproject.toml"""
    if not pyproject_path.exists():
        return {'main': [], 'dev': [], 'optional': {}}

    try:
        content = pyproject_path.read_text(encoding='utf-8')
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
                if '.' in line:
                    in_optional = line.split('.')[-1].strip(']')
                    deps['optional'][in_optional] = []
                continue
            elif line == ']':
                in_deps = False
                in_dev = False
                in_optional = None
                continue

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
        return {'main': [], 'dev': [], 'optional': {}}


def get_test_status(app_dir: Path) -> dict:
    """Get test status for application"""
    tests_dir = app_dir / "tests"
    if not tests_dir.exists():
        return {
            "has_tests": False,
            "test_files": 0
        }

    test_files = list(tests_dir.rglob("test_*.py"))

    return {
        "has_tests": True,
        "test_files": len(test_files),
        "test_directories": len([d for d in tests_dir.rglob("*") if d.is_dir() and not should_exclude(d)])
    }


def generate_app_manifest(app_dir: Path) -> dict:
    """Generate manifest for single application"""
    app_name = app_dir.name

    print(f"   📦 Generating manifest for: {app_name}")

    manifest = {
        "name": app_name,
        "type": "application",
        "location": str(app_dir.relative_to(MONOREPO_ROOT)).replace('\\', '/'),
        "generated": datetime.now().isoformat(),
        "statistics": get_directory_stats(app_dir),
        "structure": {
            "has_src": (app_dir / "src").exists(),
            "has_tests": (app_dir / "tests").exists(),
            "has_scripts": (app_dir / "scripts").exists(),
            "has_docs": (app_dir / "docs").exists()
        },
        "dependencies": read_pyproject_dependencies(app_dir / "pyproject.toml"),
        "tests": get_test_status(app_dir),
        "files": scan_files(app_dir, MONOREPO_ROOT)
    }

    # Add key files
    key_files = []
    for pattern in ["main.py", "app.py", "pyproject.toml", "README.md"]:
        for file in app_dir.rglob(pattern):
            if not should_exclude(file):
                key_files.append(str(file.relative_to(MONOREPO_ROOT)).replace('\\', '/'))
    manifest["key_files"] = key_files

    return manifest


def generate_package_manifest(package_dir: Path) -> dict:
    """Generate manifest for single package"""
    package_name = package_dir.name

    print(f"   📚 Generating manifest for: {package_name}")

    manifest = {
        "name": package_name,
        "type": "package",
        "location": str(package_dir.relative_to(MONOREPO_ROOT)).replace('\\', '/'),
        "generated": datetime.now().isoformat(),
        "statistics": get_directory_stats(package_dir),
        "dependencies": read_pyproject_dependencies(package_dir / "pyproject.toml"),
        "files": scan_files(package_dir, MONOREPO_ROOT)
    }

    # Add modules info
    package_src = package_dir / package_name.replace('-', '_')
    if package_src.exists():
        modules = []
        for py_file in package_src.rglob("*.py"):
            if not should_exclude(py_file) and py_file.name != "__init__.py":
                modules.append({
                    "name": py_file.stem,
                    "path": str(py_file.relative_to(package_src)).replace('\\', '/'),
                    "lines": count_lines(py_file)
                })
        manifest["modules"] = modules
    else:
        manifest["modules"] = []

    return manifest



def get_documentation_files() -> dict:
    """Get key documentation files from docs/"""
    docs = {}

    # Session notes - najdôležitejší súbor
    session_notes = DOCS_DIR / "SESSION_NOTES.md"
    if session_notes.exists():
        docs["session_notes"] = {
            "path": "docs/SESSION_NOTES.md",
            "exists": True,
            "size": session_notes.stat().st_size,
            "github_raw": "https://raw.githubusercontent.com/[username]/nex-automat/main/docs/SESSION_NOTES.md"
        }

    # Ostatné kľúčové dokumenty
    key_docs = {
        "guides/MONOREPO_GUIDE.md": "Monorepo development guide",
        "guides/CONTRIBUTING.md": "Contribution guidelines",
        "guides/TESTING_GUIDE.md": "Testing guide"
    }

    for doc_path, description in key_docs.items():
        full_path = DOCS_DIR / doc_path
        if full_path.exists():
            docs[doc_path.replace('/', '_').replace('.md', '')] = {
                "path": f"docs/{doc_path}",
                "description": description,
                "exists": True,
                "github_raw": f"https://raw.githubusercontent.com/[username]/nex-automat/main/docs/{doc_path}"
            }

    return docs

def generate_root_manifest() -> dict:
    """Generate root manifest with overview"""
    print("🔨 Generating root manifest...")

    # Get all apps
    apps_dir = MONOREPO_ROOT / "apps"
    apps_list = []
    if apps_dir.exists():
        for app in sorted(apps_dir.iterdir()):
            if app.is_dir() and not should_exclude(app):
                stats = get_directory_stats(app)
                deps = read_pyproject_dependencies(app / "pyproject.toml")
                tests = get_test_status(app)

                apps_list.append({
                    "name": app.name,
                    "location": f"apps/{app.name}",
                    "manifest": f"docs/apps/{app.name}.json",
                    "python_files": stats["python_files"],
                    "test_files": tests["test_files"],
                    "dependencies_count": len(deps["main"])
                })

    # Get all packages
    packages_dir = MONOREPO_ROOT / "packages"
    packages_list = []
    if packages_dir.exists():
        for package in sorted(packages_dir.iterdir()):
            if package.is_dir() and not should_exclude(package):
                stats = get_directory_stats(package)
                deps = read_pyproject_dependencies(package / "pyproject.toml")

                packages_list.append({
                    "name": package.name,
                    "location": f"packages/{package.name}",
                    "manifest": f"docs/packages/{package.name}.json",
                    "python_files": stats["python_files"],
                    "dependencies_count": len(deps["main"])
                })

    # Collect all dependencies
    all_deps = set()
    for pyproject_file in MONOREPO_ROOT.rglob("pyproject.toml"):
        if should_exclude(pyproject_file):
            continue
        deps = read_pyproject_dependencies(pyproject_file)
        for dep in deps.get('main', []):
            all_deps.add(dep.split('>=')[0].split('==')[0].split('[')[0])

    # Get documentation files
    docs_files = get_documentation_files()

    # Root manifest
    manifest = {
        "project": "nex-automat",
        "type": "monorepo",
        "version": "2.0.0",
        "description": "Multi-customer SaaS for automated invoice processing",
        "location": str(MONOREPO_ROOT),
        "generated": datetime.now().isoformat(),
        "structure": {
            "apps": len(apps_list),
            "packages": len(packages_list),
            "docs": (DOCS_DIR).exists(),
            "tools": (MONOREPO_ROOT / "tools").exists()
        },
        "statistics": get_directory_stats(MONOREPO_ROOT),
        "applications": apps_list,
        "packages": packages_list,
        "dependencies": {
            "unique_count": len(all_deps),
            "list": sorted(list(all_deps))
        },
        "migration_status": {
            "phase_1_structure": "complete",
            "phase_2_migration": "complete",
            "phase_3_shared_packages": "complete",
            "phase_4_imports": "complete",
            "phase_5_testing": "complete",
            "phase_6_test_fixes": "complete",
            "phase_7_documentation": "in_progress",
            "phase_8_git": "todo"
        },
        "documentation": docs_files,
                "test_status": {
            "supplier_invoice_loader": {
                "total": 72,
                "passed": 61,
                "failed": 0,
                "skipped": 11,
                "coverage": "85%"
            },
            "supplier_invoice_editor": {
                "status": "not_tested_yet"
            }
        }
    }

    return manifest


def main():
    """Main script execution"""
    print("=" * 70)
    print("📋 GENERATE PROJECTS ACCESS - JSON MANIFESTS")
    print("=" * 70)
    print()
    print(f"Monorepo: {MONOREPO_ROOT}")
    print()

    # Create manifest directories
    APPS_MANIFEST_DIR.mkdir(parents=True, exist_ok=True)
    PACKAGES_MANIFEST_DIR.mkdir(parents=True, exist_ok=True)
    print(f"✅ Created manifest directories")
    print()

    # 1. Generate per-app manifests
    print("1️⃣ Generating application manifests...")
    apps_dir = MONOREPO_ROOT / "apps"
    app_count = 0

    if apps_dir.exists():
        for app in sorted(apps_dir.iterdir()):
            if app.is_dir() and not should_exclude(app):
                app_manifest = generate_app_manifest(app)

                # Save to JSON
                manifest_file = APPS_MANIFEST_DIR / f"{app.name}.json"
                with open(manifest_file, 'w', encoding='utf-8') as f:
                    json.dump(app_manifest, f, indent=2, ensure_ascii=False)

                app_count += 1
                print(f"      ✅ {manifest_file.relative_to(MONOREPO_ROOT)}")

    print(f"   Generated {app_count} application manifests")
    print()

    # 2. Generate per-package manifests
    print("2️⃣ Generating package manifests...")
    packages_dir = MONOREPO_ROOT / "packages"
    package_count = 0

    if packages_dir.exists():
        for package in sorted(packages_dir.iterdir()):
            if package.is_dir() and not should_exclude(package):
                package_manifest = generate_package_manifest(package)

                # Save to JSON
                manifest_file = PACKAGES_MANIFEST_DIR / f"{package.name}.json"
                with open(manifest_file, 'w', encoding='utf-8') as f:
                    json.dump(package_manifest, f, indent=2, ensure_ascii=False)

                package_count += 1
                print(f"      ✅ {manifest_file.relative_to(MONOREPO_ROOT)}")

    print(f"   Generated {package_count} package manifests")
    print()

    # 3. Generate root manifest
    print("3️⃣ Generating root manifest...")
    root_manifest = generate_root_manifest()

    # Save to JSON
    root_manifest_file = DOCS_DIR / "PROJECT_MANIFEST.json"
    with open(root_manifest_file, 'w', encoding='utf-8') as f:
        json.dump(root_manifest, f, indent=2, ensure_ascii=False)

    print(f"   ✅ {root_manifest_file.relative_to(MONOREPO_ROOT)}")
    print()

    # Summary
    print("=" * 70)
    print("✅ MANIFEST GENERATION COMPLETE!")
    print("=" * 70)
    print()
    print(f"📊 Generated manifests:")
    print(f"   Root:     {root_manifest_file}")
    print(f"   Apps:     {app_count} manifests in docs/apps/")
    print(f"   Packages: {package_count} manifests in docs/packages/")
    print()
    print(f"📁 Total files tracked: {root_manifest['statistics']['total_files']}")
    print(f"🐍 Python files: {root_manifest['statistics']['python_files']}")
    print(f"📝 Total lines: {root_manifest['statistics']['total_lines']:,}")
    print()
    print("=" * 70)
    print("USAGE IN CLAUDE:")
    print("=" * 70)
    print("# Load root manifest:")
    print("web_fetch('https://raw.githubusercontent.com/.../docs/PROJECT_MANIFEST.json')")
    print()
    print("# Load specific app:")
    print("web_fetch('https://raw.githubusercontent.com/.../docs/apps/supplier-invoice-loader.json')")
    print()
    print("=" * 70)


if __name__ == "__main__":
    main()