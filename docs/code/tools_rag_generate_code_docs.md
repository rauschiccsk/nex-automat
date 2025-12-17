# generate_code_docs.py

**Path:** `tools\rag\generate_code_docs.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

Generate Markdown documentation from Python source code.
Extracts docstrings, classes, methods, functions, and CLI arguments.

Usage:
    python tools/rag/generate_code_docs.py

Output:
    docs/code/*.md files ready for RAG indexing

Location: tools/rag/generate_code_docs.py

---

## Classes

### CodeDocGenerator

Extract documentation from Python source files.

**Methods:**

#### `__init__(self, project_root)`

#### `extract_from_file(self, filepath)`

Extract documentation elements from a Python file.

#### `_is_top_level(self, tree, node)`

Check if a node is at the top level of the module.

#### `_get_name(self, node)`

Get name from various AST node types.

#### `_get_function_args(self, node)`

Extract function argument names.

#### `_extract_argparse(self, content)`

Extract argparse arguments from source code.

#### `generate_markdown(self, doc)`

Generate Markdown documentation from extracted data.

#### `process_directory(self, directory, recursive)`

Process all Python files in a directory.

---

## Functions

### `main()`

---
