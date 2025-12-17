#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate Projects Access - NEX Automat Monorepo
Location: C:/Development/nex-automat/tools/generate_projects_access.py

Vytvára hierarchické JSON manifesty:
- init_chat/PROJECT_MANIFEST.json - root overview
- init_chat/apps/{app_name}.json - per-app manifests
- init_chat/packages/{package_name}.json - per-package manifests
- init_chat/tools/tools.json - Claude Tools manifest
- init_chat/docs/docs.json - Documentation manifest

Pre efektívne lazy loading v Claude sessions.
"""

from pathlib import Path
from datetime import datetime
import json

MONOREPO_ROOT = Path("/")
INIT_CHAT_DIR = MONOREPO_ROOT / "init_chat"  # ✅ UPDATED: SESSION_NOTES → init_chat
APPS_MANIFEST_DIR = INIT_CHAT_DIR / "apps"
PACKAGES_MANIFEST_DIR = INIT_CHAT_DIR / "packages"
TOOLS_MANIFEST_DIR = INIT_CHAT_DIR / "tools"
DOCS_MANIFEST_DIR = INIT_CHAT_DIR / "docs"

# GitHub Configuration
GITHUB_REPO = "rauschiccsk/nex-automat"
GITHUB_BRANCH = "develop"

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
                "extension": item.suffix,
                "github_raw": f"https://raw.githubusercontent.com/{GITHUB_REPO}/{GITHUB_BRANCH}/{str(rel_path).replace(chr(92), '/')}"
            }

            # Python-specific info
            if item.suffix == '.py':
                file_info["lines"] = count_lines(item)
                file_info["type"] = "test" if "test" in item.name else "source"

            # PowerShell-specific info
            if item.suffix == '.ps1':
                file_info["lines"] = count_lines(item)
                file_info["type"] = "script"

            # Markdown-specific info
            if item.suffix == '.md':
                file_info["lines"] = count_lines(item)
                file_info["type"] = "documentation"

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
        'powershell_files': 0,
        'markdown_files': 0,
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

                if item.suffix == '.ps1':
                    stats['powershell_files'] += 1
                    stats['total_lines'] += count_lines(item)

                if item.suffix == '.md':
                    stats['markdown_files'] += 1
                    stats['total_lines'] += count_lines(item)

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


def generate_tools_manifest(tools_dir: Path) -> dict:
    """Generate manifest for Claude Tools"""
    print(f"   🔧 Generating manifest for: Claude Tools")

    manifest = {
        "name": "claude-tools",
        "type": "tools",
        "location": str(tools_dir.relative_to(MONOREPO_ROOT)).replace('\\', '/'),
        "generated": datetime.now().isoformat(),
        "description": "Claude Tools - Automatizacia workflow pre claude.ai",
        "statistics": get_directory_stats(tools_dir),
        "structure": {
            "has_browser_extension": (tools_dir / "browser-extension").exists(),
            "has_config": (tools_dir / "config.py").exists(),
            "has_log": (tools_dir / "claude-tools.log").exists()
        },
        "components": {
            "installer": {
                "file": "installer.py",
                "description": "Automatická inštalácia dependencies a setup"
            },
            "chat_loader": {
                "file": "claude-chat-loader.py",
                "description": "Auto-load init promptu (Ctrl+Alt+L)",
                "hotkey": "Ctrl+Alt+L"
            },
            "hotkeys": {
                "file": "claude-hotkeys.py",
                "description": "Globálne klávesové skratky",
                "hotkeys": {
                    "Ctrl+Alt+L": "Load init prompt",
                    "Ctrl+Alt+S": "Copy session notes",
                    "Ctrl+Alt+G": "Git status",
                    "Ctrl+Alt+D": "Deployment info",
                    "Ctrl+Alt+N": "New chat template",
                    "Ctrl+Alt+I": "Show project info"
                }
            },
            "artifact_server": {
                "file": "artifact-server.py",
                "description": "FastAPI server pre artifacts",
                "port": 8765,
                "url": "http://localhost:8765"
            },
            "session_notes_manager": {
                "file": "session-notes-manager.py",
                "description": "Správa session notes",
                "commands": ["enhance", "validate", "template"]
            },
            "context_compressor": {
                "file": "context-compressor.py",
                "description": "Kompresia histórie cez Claude API",
                "requires": "ANTHROPIC_API_KEY"
            }
        },
        "scripts": {
            "startup": "start-claude-tools.ps1",
            "shutdown": "stop-claude-tools.ps1"
        },
        "browser_extension": {
            "available": (tools_dir / "browser-extension" / "claude-artifact-saver").exists(),
            "manifest": "browser-extension/claude-artifact-saver/manifest.json"
        },
        "files": scan_files(tools_dir, MONOREPO_ROOT)
    }

    # Key files
    key_files = []
    for pattern in ["*.py", "*.ps1", "config.py", "*.md"]:
        for file in tools_dir.glob(pattern):
            if not should_exclude(file):
                key_files.append(str(file.relative_to(MONOREPO_ROOT)).replace('\\', '/'))
    manifest["key_files"] = key_files

    return manifest


def generate_docs_manifest(docs_dir: Path) -> dict:
    """Generate manifest for Documentation"""
    print(f"   📖 Generating manifest for: Documentation")

    manifest = {
        "name": "documentation",
        "type": "docs",
        "location": str(docs_dir.relative_to(MONOREPO_ROOT)).replace('\\', '/'),
        "generated": datetime.now().isoformat(),
        "description": "Komplexná dokumentácia NEX Automat projektu",
        "statistics": get_directory_stats(docs_dir),
        "files": scan_files(docs_dir, MONOREPO_ROOT)
    }

    # Organize docs by category
    categories = {
        "guides": [],
        "database": [],
        "migration": [],
        "api": [],
        "testing": [],
        "deployment": [],
        "other": []
    }

    # Scan all markdown files and categorize
    for md_file in docs_dir.rglob("*.md"):
        if should_exclude(md_file):
            continue

        rel_path = str(md_file.relative_to(docs_dir)).replace('\\', '/')
        doc_info = {
            "name": md_file.name,
            "path": rel_path,
            "full_path": str(md_file.relative_to(MONOREPO_ROOT)).replace('\\', '/'),
            "size": md_file.stat().st_size,
            "lines": count_lines(md_file),
            "github_raw": f"https://raw.githubusercontent.com/{GITHUB_REPO}/{GITHUB_BRANCH}/{str(md_file.relative_to(MONOREPO_ROOT)).replace(chr(92), '/')}"
        }

        # Categorize by path or name
        path_lower = rel_path.lower()
        if 'guide' in path_lower or md_file.parent.name == 'guides':
            categories["guides"].append(doc_info)
        elif 'database' in path_lower or 'schema' in path_lower or md_file.parent.name == 'database':
            categories["database"].append(doc_info)
        elif 'migration' in path_lower or md_file.parent.name == 'migration':
            categories["migration"].append(doc_info)
        elif 'api' in path_lower or md_file.parent.name == 'api':
            categories["api"].append(doc_info)
        elif 'test' in path_lower or md_file.parent.name == 'testing':
            categories["testing"].append(doc_info)
        elif 'deploy' in path_lower or md_file.parent.name == 'deployment':
            categories["deployment"].append(doc_info)
        else:
            categories["other"].append(doc_info)

    manifest["categories"] = categories

    # Find key documentation files
    key_docs = {}

    # README files
    for readme in docs_dir.rglob("README.md"):
        if not should_exclude(readme):
            rel_path = str(readme.relative_to(docs_dir)).replace('\\', '/')
            key_name = "main_readme" if rel_path == "README.md" else f"readme_{readme.parent.name}"
            key_docs[key_name] = {
                "path": str(readme.relative_to(MONOREPO_ROOT)).replace('\\', '/'),
                "github_raw": f"https://raw.githubusercontent.com/{GITHUB_REPO}/{GITHUB_BRANCH}/{str(readme.relative_to(MONOREPO_ROOT)).replace(chr(92), '/')}"
            }

    manifest["key_files"] = key_docs

    # Document structure
    structure = {
        "has_guides": len(categories["guides"]) > 0,
        "has_database_docs": len(categories["database"]) > 0,
        "has_migration_docs": len(categories["migration"]) > 0,
        "has_api_docs": len(categories["api"]) > 0,
        "has_testing_docs": len(categories["testing"]) > 0,
        "has_deployment_docs": len(categories["deployment"]) > 0
    }

    manifest["structure"] = structure

    return manifest


def get_documentation_summary() -> dict:
    """Get summary of documentation for root manifest"""
    docs_dir = MONOREPO_ROOT / "docs"

    summary = {
        "manifest": "init_chat/docs/docs.json",  # ✅ UPDATED
        "exists": docs_dir.exists()
    }

    if docs_dir.exists():
        stats = get_directory_stats(docs_dir)
        summary["markdown_files"] = stats["markdown_files"]
        summary["total_lines"] = stats["total_lines"]

    # Key documentation files (init_chat)
    init_prompt = INIT_CHAT_DIR / "INIT_PROMPT_NEW_CHAT.md"
    if init_prompt.exists():
        summary["init_prompt"] = {
            "path": "init_chat/INIT_PROMPT_NEW_CHAT.md",  # ✅ UPDATED
            "exists": True,
            "size": init_prompt.stat().st_size,
            "github_raw": f"https://raw.githubusercontent.com/{GITHUB_REPO}/{GITHUB_BRANCH}/init_chat/INIT_PROMPT_NEW_CHAT.md"  # ✅ UPDATED
        }

    return summary


def generate_root_manifest() -> dict:
    """Generate root manifest with overview"""
    print("📋 Generating root manifest...")

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
                    "manifest": f"init_chat/apps/{app.name}.json",  # ✅ UPDATED
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
                    "manifest": f"init_chat/packages/{package.name}.json",  # ✅ UPDATED
                    "python_files": stats["python_files"],
                    "dependencies_count": len(deps["main"])
                })

    # Get tools info
    tools_dir = MONOREPO_ROOT / "tools"
    tools_info = None
    if tools_dir.exists():
        stats = get_directory_stats(tools_dir)
        tools_info = {
            "name": "claude-tools",
            "location": "tools",
            "manifest": "init_chat/tools/tools.json",  # ✅ UPDATED
            "python_files": stats["python_files"],
            "powershell_files": stats["powershell_files"],
            "type": "automation"
        }

    # Get documentation summary
    docs_summary = get_documentation_summary()

    # Collect all dependencies
    all_deps = set()
    for pyproject_file in MONOREPO_ROOT.rglob("pyproject.toml"):
        if should_exclude(pyproject_file):
            continue
        deps = read_pyproject_dependencies(pyproject_file)
        for dep in deps.get('main', []):
            all_deps.add(dep.split('>=')[0].split('==')[0].split('[')[0])

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
            "tools": tools_info is not None,
            "docs": docs_summary["exists"]
        },
        "statistics": get_directory_stats(MONOREPO_ROOT),
        "applications": apps_list,
        "packages": packages_list,
        "tools": tools_info,
        "documentation": docs_summary,
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
        "claude_tools_status": {
            "installed": tools_info is not None,
            "artifact_server": "running on :8765",
            "hotkeys": "active",
            "browser_extension": "available (optional)"
        },
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
    print(f"Output:   {INIT_CHAT_DIR}")  # ✅ UPDATED
    print(f"GitHub:   {GITHUB_REPO} (branch: {GITHUB_BRANCH})")
    print()

    # Create manifest directories
    APPS_MANIFEST_DIR.mkdir(parents=True, exist_ok=True)
    PACKAGES_MANIFEST_DIR.mkdir(parents=True, exist_ok=True)
    TOOLS_MANIFEST_DIR.mkdir(parents=True, exist_ok=True)
    DOCS_MANIFEST_DIR.mkdir(parents=True, exist_ok=True)
    print(f"✅ Created manifest directories in init_chat/")  # ✅ UPDATED
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

    # 3. Generate tools manifest
    print("3️⃣ Generating tools manifest...")
    tools_dir = MONOREPO_ROOT / "tools"
    tools_count = 0

    if tools_dir.exists():
        tools_manifest = generate_tools_manifest(tools_dir)

        # Save to JSON
        manifest_file = TOOLS_MANIFEST_DIR / "tools.json"
        with open(manifest_file, 'w', encoding='utf-8') as f:
            json.dump(tools_manifest, f, indent=2, ensure_ascii=False)

        tools_count = 1
        print(f"      ✅ {manifest_file.relative_to(MONOREPO_ROOT)}")

    print(f"   Generated {tools_count} tools manifest")
    print()

    # 4. Generate docs manifest
    print("4️⃣ Generating documentation manifest...")
    docs_dir = MONOREPO_ROOT / "docs"
    docs_count = 0

    if docs_dir.exists():
        docs_manifest = generate_docs_manifest(docs_dir)

        # Save to JSON
        manifest_file = DOCS_MANIFEST_DIR / "docs.json"
        with open(manifest_file, 'w', encoding='utf-8') as f:
            json.dump(docs_manifest, f, indent=2, ensure_ascii=False)

        docs_count = 1
        print(f"      ✅ {manifest_file.relative_to(MONOREPO_ROOT)}")

    print(f"   Generated {docs_count} documentation manifest")
    print()

    # 5. Generate root manifest
    print("5️⃣ Generating root manifest...")
    root_manifest = generate_root_manifest()

    # Save to JSON
    root_manifest_file = INIT_CHAT_DIR / "PROJECT_MANIFEST.json"
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
    print(f"   Apps:     {app_count} manifests in init_chat/apps/")  # ✅ UPDATED
    print(f"   Packages: {package_count} manifests in init_chat/packages/")  # ✅ UPDATED
    print(f"   Tools:    {tools_count} manifest in init_chat/tools/")  # ✅ UPDATED
    print(f"   Docs:     {docs_count} manifest in init_chat/docs/")  # ✅ UPDATED
    print()
    print(f"📦 Total files tracked: {root_manifest['statistics']['total_files']}")
    print(f"🐍 Python files: {root_manifest['statistics']['python_files']}")
    print(f"📜 PowerShell files: {root_manifest['statistics']['powershell_files']}")
    print(f"📖 Markdown files: {root_manifest['statistics']['markdown_files']}")
    print(f"📏 Total lines: {root_manifest['statistics']['total_lines']:,}")
    print()
    print(f"🌿 Branch: {GITHUB_BRANCH}")
    print()
    print("=" * 70)
    print("USAGE IN CLAUDE:")
    print("=" * 70)
    print("# Load root manifest:")
    print(f"web_fetch('https://raw.githubusercontent.com/{GITHUB_REPO}/{GITHUB_BRANCH}/init_chat/PROJECT_MANIFEST.json')")  # ✅ UPDATED
    print()
    print("# Load specific app:")
    print(f"web_fetch('https://raw.githubusercontent.com/{GITHUB_REPO}/{GITHUB_BRANCH}/init_chat/apps/supplier-invoice-loader.json')")  # ✅ UPDATED
    print()
    print("# Load documentation:")
    print(f"web_fetch('https://raw.githubusercontent.com/{GITHUB_REPO}/{GITHUB_BRANCH}/init_chat/docs/docs.json')")  # ✅ UPDATED
    print()
    print("# Load Claude Tools manifest:")
    print(f"web_fetch('https://raw.githubusercontent.com/{GITHUB_REPO}/{GITHUB_BRANCH}/init_chat/tools/tools.json')")  # ✅ UPDATED
    print()
    print("=" * 70)


if __name__ == "__main__":
    main()