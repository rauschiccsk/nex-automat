"""
scan_project_structure.py
Scan and document actual project structure of nex-automat
Output: docs/knowledge/PROJECT_STRUCTURE.md
"""

from pathlib import Path

# Output file - hardcoded
OUTPUT_FILE = Path(__file__).parent.parent / "docs" / "knowledge" / "PROJECT_STRUCTURE.md"

# Directories to skip
SKIP_DIRS = {
    "__pycache__",
    ".git",
    ".venv",
    "venv",
    "venv32",
    "node_modules",
    ".idea",
    ".vscode",
    "dist",
    "build",
    "*.egg-info",
    ".pytest_cache",
    ".mypy_cache",
    "htmlcov",
    ".tox",
    "eggs",
    ".eggs",
}


def should_skip(path: Path) -> bool:
    """Check if directory should be skipped."""
    return path.name in SKIP_DIRS or path.name.startswith(".")


def scan_directory(root: Path, prefix: str = "", max_depth: int = 4, current_depth: int = 0) -> list:
    """Recursively scan directory and build tree."""
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
        output_lines.extend(scan_directory(d, prefix + extension, max_depth, current_depth + 1))

    for i, f in enumerate(files):
        is_last = i == len(files) - 1
        connector = "└── " if is_last else "├── "
        size = f.stat().st_size
        size_str = f"{size:,}" if size < 10000 else f"{size / 1024:.1f}K"
        output_lines.append(f"{prefix}{connector}{f.name} ({size_str})")

    return output_lines


def main():
    project_root = Path(__file__).parent.parent
    lines = []

    lines.append("# NEX-AUTOMAT PROJECT STRUCTURE")
    lines.append("")
    lines.append("Generated from: `scripts/scan_project_structure.py`")
    lines.append("")

    # Scan apps/
    lines.append("## apps/")
    lines.append("")
    apps_dir = project_root / "apps"
    if apps_dir.exists():
        for app in sorted(apps_dir.iterdir()):
            if app.is_dir() and not should_skip(app):
                lines.append(f"### {app.name}/")
                lines.append("")
                lines.append("```")
                lines.extend(scan_directory(app, "", max_depth=3))
                lines.append("```")
                lines.append("")

    # Scan packages/
    lines.append("## packages/")
    lines.append("")
    packages_dir = project_root / "packages"
    if packages_dir.exists():
        for pkg in sorted(packages_dir.iterdir()):
            if pkg.is_dir() and not should_skip(pkg):
                lines.append(f"### {pkg.name}/")
                lines.append("")
                lines.append("```")
                lines.extend(scan_directory(pkg, "", max_depth=3))
                lines.append("```")
                lines.append("")

    # Scan docs/knowledge/
    lines.append("## docs/knowledge/")
    lines.append("")
    knowledge_dir = project_root / "docs" / "knowledge"
    if knowledge_dir.exists():
        lines.append("```")
        lines.extend(scan_directory(knowledge_dir, "", max_depth=2))
        lines.append("```")
        lines.append("")

    # Root files
    lines.append("## Root files")
    lines.append("")
    lines.append("```")
    for f in sorted(project_root.iterdir()):
        if f.is_file():
            size = f.stat().st_size
            size_str = f"{size:,}" if size < 10000 else f"{size / 1024:.1f}K"
            lines.append(f"{f.name} ({size_str})")
    lines.append("```")

    # Write to file
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text("\n".join(lines), encoding="utf-8")
    print(f"[OK] Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
