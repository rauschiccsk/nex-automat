# -*- coding: utf-8 -*-
"""
04_scan_project_structure.py
Scan and document actual project structure of nex-automat
"""

from pathlib import Path
import os

# Directories to skip
SKIP_DIRS = {
    '__pycache__', '.git', '.venv', 'venv', 'venv32', 'node_modules',
    '.idea', '.vscode', 'dist', 'build', '*.egg-info', '.pytest_cache',
    '.mypy_cache', 'htmlcov', '.tox', 'eggs', '.eggs'
}

# File extensions to include
INCLUDE_EXT = {'.py', '.md', '.sql', '.yaml', '.yml', '.json', '.txt', '.env', '.bat', '.ps1', '.sh'}


def should_skip(path: Path) -> bool:
    """Check if directory should be skipped."""
    return path.name in SKIP_DIRS or path.name.startswith('.')


def scan_directory(root: Path, prefix: str = "", output_lines: list = None, max_depth: int = 4, current_depth: int = 0):
    """Recursively scan directory and build tree."""
    if output_lines is None:
        output_lines = []

    if current_depth > max_depth:
        output_lines.append(f"{prefix}... (max depth reached)")
        return output_lines

    try:
        items = sorted(root.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
    except PermissionError:
        return output_lines

    dirs = [i for i in items if i.is_dir() and not should_skip(i)]
    files = [i for i in items if i.is_file()]

    for i, d in enumerate(dirs):
        is_last_dir = (i == len(dirs) - 1) and len(files) == 0
        connector = "└── " if is_last_dir else "├── "
        output_lines.append(f"{prefix}{connector}{d.name}/")

        extension = "    " if is_last_dir else "│   "
        scan_directory(d, prefix + extension, output_lines, max_depth, current_depth + 1)

    for i, f in enumerate(files):
        is_last = i == len(files) - 1
        connector = "└── " if is_last else "├── "
        size = f.stat().st_size
        size_str = f"{size:,}" if size < 10000 else f"{size / 1024:.1f}K"
        output_lines.append(f"{prefix}{connector}{f.name} ({size_str})")

    return output_lines


def main():
    project_root = Path(".")

    print("=" * 70)
    print("NEX-AUTOMAT PROJECT STRUCTURE SCAN")
    print("=" * 70)
    print(f"Root: {project_root.absolute()}")
    print("=" * 70)

    # Scan apps/
    print("\n## apps/\n")
    apps_dir = project_root / "apps"
    if apps_dir.exists():
        for app in sorted(apps_dir.iterdir()):
            if app.is_dir() and not should_skip(app):
                print(f"\n### {app.name}/\n")
                print("```")
                lines = scan_directory(app, "", [], max_depth=3)
                for line in lines:
                    print(line)
                print("```")

    # Scan packages/
    print("\n" + "=" * 70)
    print("\n## packages/\n")
    packages_dir = project_root / "packages"
    if packages_dir.exists():
        for pkg in sorted(packages_dir.iterdir()):
            if pkg.is_dir() and not should_skip(pkg):
                print(f"\n### {pkg.name}/\n")
                print("```")
                lines = scan_directory(pkg, "", [], max_depth=3)
                for line in lines:
                    print(line)
                print("```")

    # Scan docs/knowledge/ (just list)
    print("\n" + "=" * 70)
    print("\n## docs/knowledge/\n")
    knowledge_dir = project_root / "docs" / "knowledge"
    if knowledge_dir.exists():
        print("```")
        lines = scan_directory(knowledge_dir, "", [], max_depth=2)
        for line in lines:
            print(line)
        print("```")

    # Root files
    print("\n" + "=" * 70)
    print("\n## Root files\n")
    print("```")
    for f in sorted(project_root.iterdir()):
        if f.is_file():
            size = f.stat().st_size
            size_str = f"{size:,}" if size < 10000 else f"{size / 1024:.1f}K"
            print(f"{f.name} ({size_str})")
    print("```")

    print("\n" + "=" * 70)
    print("[OK] Scan complete")


if __name__ == "__main__":
    main()