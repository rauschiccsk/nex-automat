#!/usr/bin/env python3
"""
Generate Markdown documentation from Python source code.
Extracts docstrings, classes, methods, functions, and CLI arguments.

Usage:
    python tools/rag/generate_code_docs.py

Output:
    docs/code/*.md files ready for RAG indexing

Location: tools/rag/generate_code_docs.py
"""

import ast
from datetime import datetime
from pathlib import Path
from typing import Any


class CodeDocGenerator:
    """Extract documentation from Python source files."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.output_dir = project_root / "docs" / "code"

    def extract_from_file(self, filepath: Path) -> dict[str, Any]:
        """Extract documentation elements from a Python file."""
        try:
            with open(filepath, encoding="utf-8") as f:
                content = f.read()

            tree = ast.parse(content)
        except (SyntaxError, UnicodeDecodeError) as e:
            return {"error": str(e), "filepath": str(filepath)}

        doc = {
            "filepath": str(filepath.relative_to(self.project_root)),
            "module_docstring": ast.get_docstring(tree),
            "classes": [],
            "functions": [],
            "imports": [],
            "cli_args": [],
        }

        for node in ast.walk(tree):
            # Extract classes
            if isinstance(node, ast.ClassDef):
                class_doc = {
                    "name": node.name,
                    "docstring": ast.get_docstring(node),
                    "methods": [],
                    "bases": [self._get_name(base) for base in node.bases],
                }

                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        method_doc = {
                            "name": item.name,
                            "docstring": ast.get_docstring(item),
                            "args": self._get_function_args(item),
                            "is_async": False,
                        }
                        class_doc["methods"].append(method_doc)
                    elif isinstance(item, ast.AsyncFunctionDef):
                        method_doc = {
                            "name": item.name,
                            "docstring": ast.get_docstring(item),
                            "args": self._get_function_args(item),
                            "is_async": True,
                        }
                        class_doc["methods"].append(method_doc)

                doc["classes"].append(class_doc)

            # Extract top-level functions
            elif isinstance(node, ast.FunctionDef) and isinstance(
                node, ast.FunctionDef
            ):
                # Check if it's a top-level function (not inside a class)
                if self._is_top_level(tree, node):
                    func_doc = {
                        "name": node.name,
                        "docstring": ast.get_docstring(node),
                        "args": self._get_function_args(node),
                        "is_async": False,
                    }
                    doc["functions"].append(func_doc)

            elif isinstance(node, ast.AsyncFunctionDef):
                if self._is_top_level(tree, node):
                    func_doc = {
                        "name": node.name,
                        "docstring": ast.get_docstring(node),
                        "args": self._get_function_args(node),
                        "is_async": True,
                    }
                    doc["functions"].append(func_doc)

        # Extract CLI arguments from argparse
        doc["cli_args"] = self._extract_argparse(content)

        return doc

    def _is_top_level(self, tree: ast.Module, node: ast.AST) -> bool:
        """Check if a node is at the top level of the module."""
        return node in tree.body

    def _get_name(self, node: ast.AST) -> str:
        """Get name from various AST node types."""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        return "Unknown"

    def _get_function_args(self, node: ast.FunctionDef) -> list[str]:
        """Extract function argument names."""
        args = []
        for arg in node.args.args:
            args.append(arg.arg)
        return args

    def _extract_argparse(self, content: str) -> list[dict[str, str]]:
        """Extract argparse arguments from source code."""
        args = []
        lines = content.split("\n")

        for line in lines:
            if "add_argument" in line:
                # Simple extraction of argument names
                if "'--" in line or '"--' in line:
                    start = line.find("--")
                    end = (
                        line.find("'", start)
                        if "'" in line[start:]
                        else line.find('"', start)
                    )
                    if end == -1:
                        end = line.find(",", start)
                    if start != -1 and end != -1:
                        arg_name = line[start:end].strip("'\",")

                        # Try to extract help text
                        help_text = ""
                        if "help=" in line:
                            help_start = line.find("help=") + 5
                            help_text = line[help_start:].strip().strip("'\")")
                            if "," in help_text:
                                help_text = help_text[: help_text.find(",")]

                        args.append({"name": arg_name, "help": help_text.strip("'\"")})

        return args

    def generate_markdown(self, doc: dict[str, Any]) -> str:
        """Generate Markdown documentation from extracted data."""
        lines = []

        filepath = doc["filepath"]
        filename = Path(filepath).name

        lines.append(f"# {filename}")
        lines.append("")
        lines.append(f"**Path:** `{filepath}`  ")
        lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}  ")
        lines.append("**Type:** Python Source Code")
        lines.append("")
        lines.append("---")
        lines.append("")

        # Module docstring
        if doc.get("module_docstring"):
            lines.append("## Overview")
            lines.append("")
            lines.append(doc["module_docstring"])
            lines.append("")
            lines.append("---")
            lines.append("")

        # CLI Arguments
        if doc.get("cli_args"):
            lines.append("## CLI Arguments")
            lines.append("")
            lines.append("| Argument | Description |")
            lines.append("|----------|-------------|")
            for arg in doc["cli_args"]:
                lines.append(f"| `{arg['name']}` | {arg['help']} |")
            lines.append("")
            lines.append("---")
            lines.append("")

        # Classes
        if doc.get("classes"):
            lines.append("## Classes")
            lines.append("")

            for cls in doc["classes"]:
                bases = f"({', '.join(cls['bases'])})" if cls["bases"] else ""
                lines.append(f"### {cls['name']}{bases}")
                lines.append("")

                if cls["docstring"]:
                    lines.append(cls["docstring"])
                    lines.append("")

                if cls["methods"]:
                    lines.append("**Methods:**")
                    lines.append("")

                    for method in cls["methods"]:
                        async_prefix = "async " if method["is_async"] else ""
                        args_str = ", ".join(method["args"])
                        lines.append(
                            f"#### `{async_prefix}{method['name']}({args_str})`"
                        )
                        lines.append("")
                        if method["docstring"]:
                            lines.append(method["docstring"])
                            lines.append("")

                lines.append("---")
                lines.append("")

        # Functions
        if doc.get("functions"):
            lines.append("## Functions")
            lines.append("")

            for func in doc["functions"]:
                async_prefix = "async " if func["is_async"] else ""
                args_str = ", ".join(func["args"])
                lines.append(f"### `{async_prefix}{func['name']}({args_str})`")
                lines.append("")
                if func["docstring"]:
                    lines.append(func["docstring"])
                    lines.append("")
                lines.append("---")
                lines.append("")

        return "\n".join(lines)

    def process_directory(self, directory: Path, recursive: bool = True) -> list[Path]:
        """Process all Python files in a directory."""
        self.output_dir.mkdir(parents=True, exist_ok=True)

        if recursive:
            files = list(directory.rglob("*.py"))
        else:
            files = list(directory.glob("*.py"))

        # Filter out unwanted directories
        exclude_dirs = {"venv", "__pycache__", ".git", "node_modules", ".pytest_cache"}
        files = [f for f in files if not any(d in f.parts for d in exclude_dirs)]

        generated_files = []

        for filepath in files:
            # Skip __init__.py if it's empty or just imports
            if filepath.name == "__init__.py":
                content = filepath.read_text(encoding="utf-8")
                if len(content.strip()) < 100:
                    continue

            doc = self.extract_from_file(filepath)

            # Skip if no useful content
            if (
                not doc.get("classes")
                and not doc.get("functions")
                and not doc.get("module_docstring")
            ):
                continue

            if "error" in doc:
                print(f"  ⚠ Skipping {filepath.name}: {doc['error']}")
                continue

            markdown = self.generate_markdown(doc)

            # Create output filename
            rel_path = filepath.relative_to(self.project_root)
            output_name = (
                str(rel_path).replace("/", "_").replace("\\", "_").replace(".py", ".md")
            )
            output_path = self.output_dir / output_name

            output_path.write_text(markdown, encoding="utf-8")
            generated_files.append(output_path)
            print(f"  ✓ {output_name}")

        return generated_files


def main():
    project_root = Path(__file__).parent.parent.parent

    print("=" * 60)
    print("Generate Code Documentation for RAG")
    print("=" * 60)
    print()

    generator = CodeDocGenerator(project_root)

    # Directories to process
    dirs_to_process = [
        project_root / "tools",
        project_root / "apps",
        project_root / "packages",
    ]

    all_generated = []

    for directory in dirs_to_process:
        if directory.exists():
            print(f"Processing: {directory.name}/")
            generated = generator.process_directory(directory)
            all_generated.extend(generated)
            print()

    print("=" * 60)
    print(f"Generated {len(all_generated)} documentation files")
    print(f"Output directory: {generator.output_dir}")
    print("=" * 60)
    print()
    print("Next step: Index to RAG with:")
    print("  python tools/rag/rag_reindex.py --dir docs/code/")


if __name__ == "__main__":
    main()
