# NEX Automat - Monorepo Guide

**Version:** 2.0.0  
**Last Updated:** 2025-11-19

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Structure](#structure)
3. [Getting Started](#getting-started)
4. [Adding New Projects](#adding-new-projects)
5. [Development Workflow](#development-workflow)
6. [Testing Guidelines](#testing-guidelines)
7. [Dependencies Management](#dependencies-management)
8. [Manifest Generation](#manifest-generation)
9. [Troubleshooting](#troubleshooting)

---

## Overview

NEX Automat je monorepo projekt obsahujúci viacero aplikácií a zdieľaných packages pre automatizáciu fakturačných procesov.

### Key Characteristics

- **Python Version:** 3.13.7 32-bit (Btrieve compatibility)
- **Virtual Environment:** Single `venv32` for entire monorepo
- **Package Manager:** pip (UV má problémy s 32-bit packages)
- **Testing:** pytest with asyncio support
- **Code Quality:** black, ruff

### Why 32-bit Python?

Všetky projekty, ktoré pracujú s NEX Genesis ERP (Btrieve databázy), vyžadujú 32-bit Python. Pre konzistenciu používame 32-bit pre celé monorepo.

---

## Structure

```
nex-automat/
├── apps/                           # Aplikácie
│   ├── supplier-invoice-loader/    # Invoice loader service
│   └── supplier-invoice-editor/    # Invoice editor webapp
│
├── packages/                       # Zdieľané packages
│   ├── invoice-shared/             # Invoice utilities
│   └── nex-shared/                 # NEX Genesis utilities
│
├── docs/                           # Dokumentácia
│   ├── SESSION_NOTES.md
│   ├── MONOREPO_GUIDE.md          # This file
│   ├── PROJECT_MANIFEST.json      # Root manifest
│   ├── apps/*.json                # Per-app manifests
│   └── packages/*.json            # Per-package manifests
│
├── tools/                          # Development tools
│   └── scripts/
│
├── venv32/                         # Virtual environment (gitignored)
├── pyproject.toml                  # Root workspace config
├── generate_project_manifest.py   # TXT manifest generator
├── generate_projects_access.py    # JSON manifests generator
└── README.md
```

---

## Getting Started

### 1. Prerequisites

- **Python 3.13.7 32-bit** installed at `C:\Program Files (x86)\Python313-32\`
- **Git** installed
- **PyCharm** (optional but recommended)

### 2. Clone Repository

```bash
git clone https://github.com/[username]/nex-automat.git
cd nex-automat
```

### 3. Create Virtual Environment

```powershell
# Create venv32
& "C:\Program Files (x86)\Python313-32\python.exe" -m venv venv32

# Activate
.\venv32\Scripts\Activate.ps1

# Verify
python --version  # Should be Python 3.13.7
```

### 4. Install Dependencies

**Important:** Install packages in correct order (shared packages first):

```powershell
# Upgrade pip
python -m pip install --upgrade pip

# Install shared packages
pip install -e packages/invoice-shared
pip install -e packages/nex-shared

# Install applications
pip install -e apps/supplier-invoice-loader
pip install -e apps/supplier-invoice-editor

# Install dev tools
pip install pytest pytest-asyncio pytest-cov black ruff
```

### 5. Run Tests

```bash
# Test all
pytest

# Test specific app
pytest apps/supplier-invoice-loader/tests/ -v

# Quick summary
pytest --tb=no -q
```

### 6. PyCharm Setup

1. **File → Settings → Project: nex-automat → Python Interpreter**
2. **Add Interpreter → Select existing**
3. Browse to: `C:\Development\nex-automat\venv32\Scripts\python.exe`
4. **Apply**

---

## Adding New Projects

### Add New Application

#### 1. Create Directory Structure

```bash
mkdir apps/my-new-app
cd apps/my-new-app

# Create structure
mkdir src tests scripts
touch pyproject.toml README.md
```

#### 2. Create pyproject.toml

```toml
[project]
name = "my-new-app"
version = "1.0.0"
description = "Description of my app"
requires-python = ">=3.13"
dependencies = [
    "fastapi>=0.104.0",
    "invoice-shared",  # If needed
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
python_classes = "Test*"
python_functions = "test_*"
```

#### 3. Install in Development Mode

```bash
# From monorepo root with venv32 activated
pip install -e apps/my-new-app
```

#### 4. Generate Manifest

```bash
python generate_projects_access.py
```

### Add New Shared Package

#### 1. Create Directory Structure

```bash
mkdir packages/my-shared-package
cd packages/my-shared-package

# Create package directory
mkdir my_shared_package
touch my_shared_package/__init__.py
```

#### 2. Create pyproject.toml

```toml
[project]
name = "my-shared-package"
version = "1.0.0"
description = "Shared utilities"
requires-python = ">=3.13"
dependencies = [
    "asyncpg>=0.29.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["my_shared_package"]
```

#### 3. Install

```bash
pip install -e packages/my-shared-package
```

---

## Development Workflow

### Daily Workflow

```bash
# 1. Activate venv
.\venv32\Scripts\Activate.ps1

# 2. Pull latest changes
git pull origin main

# 3. Update dependencies if needed
pip install -e packages/invoice-shared -e apps/supplier-invoice-loader

# 4. Work on your feature
# ... make changes ...

# 5. Run tests
pytest apps/your-app/tests/ -v

# 6. Format code
black .
ruff check .

# 7. Commit
git add .
git commit -m "feat: your feature description"
git push
```

### Feature Branch Workflow

```bash
# Create feature branch
git checkout -b feature/my-feature

# Work and commit
git add .
git commit -m "feat: implement feature X"

# Push branch
git push origin feature/my-feature

# Create Pull Request on GitHub
```

---

## Testing Guidelines

### Test Structure

```
apps/my-app/
└── tests/
    ├── unit/           # Unit tests
    │   ├── test_api.py
    │   └── test_utils.py
    ├── integration/    # Integration tests
    │   └── test_workflow.py
    └── conftest.py     # Shared fixtures
```

### Writing Tests

```python
# tests/unit/test_example.py
import pytest

def test_basic_functionality():
    """Test description"""
    result = my_function()
    assert result == expected_value

@pytest.mark.asyncio
async def test_async_function():
    """Test async function"""
    result = await my_async_function()
    assert result is not None
```

### Running Tests

```bash
# All tests
pytest

# Specific file
pytest apps/my-app/tests/unit/test_api.py

# Verbose output
pytest -v

# With coverage
pytest --cov=src --cov-report=html

# Quick summary
pytest --tb=no -q

# Stop on first failure
pytest -x

# Run specific test
pytest apps/my-app/tests/unit/test_api.py::test_function_name
```

### Test Markers

```python
@pytest.mark.skip(reason="Not implemented yet")
def test_future_feature():
    pass

@pytest.mark.integration
def test_external_api():
    """Requires --run-integration flag"""
    pass
```

Run integration tests:
```bash
pytest --run-integration
```

---

## Dependencies Management

### Adding Dependencies

#### To Application

Edit `apps/my-app/pyproject.toml`:

```toml
[project]
dependencies = [
    "fastapi>=0.104.0",
    "new-package>=1.0.0",  # Add here
]
```

Then reinstall:
```bash
pip install -e apps/my-app
```

#### To Shared Package

Edit `packages/my-package/pyproject.toml` and reinstall:

```bash
pip install -e packages/my-package
```

### Updating Dependencies

```bash
# Update single package
pip install --upgrade package-name

# Update all packages
pip list --outdated
pip install --upgrade package-name1 package-name2

# Freeze dependencies
pip freeze > requirements.txt
```

### Optional Dependencies

For 32-bit compatibility issues:

```python
# In code
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

# Use conditionally
if PSUTIL_AVAILABLE:
    cpu = psutil.cpu_percent()
```

---

## Manifest Generation

### Why Manifests?

Hierarchické JSON manifesty umožňujú:
- **Lazy loading** - načítaj len potrebné projekty
- **Rýchlu inicializáciu** - root manifest < 20KB
- **Claude AI context** - efektívne nahrávanie cez GitHub

### Generate Manifests

```bash
# TXT format (human-readable)
python generate_project_manifest.py

# JSON format (hierarchical)
python generate_projects_access.py
```

### Output

```
docs/
├── PROJECT_MANIFEST.txt           # Human-readable overview
├── PROJECT_MANIFEST.json          # Root JSON manifest
├── apps/
│   ├── supplier-invoice-loader.json
│   └── supplier-invoice-editor.json
└── packages/
    ├── invoice-shared.json
    └── nex-shared.json
```

### Usage in Claude Sessions

```python
# Load root for overview
web_fetch('https://raw.githubusercontent.com/.../docs/PROJECT_MANIFEST.json')

# Load specific app when working on it
web_fetch('https://raw.githubusercontent.com/.../docs/apps/supplier-invoice-loader.json')
```

---

## Troubleshooting

### "Invalid Python Interpreter" in PyCharm

**Solution:**
1. File → Settings → Project → Python Interpreter
2. Select existing: `C:\Development\nex-automat\venv32\Scripts\python.exe`

### "No matching distribution found for invoice-shared"

**Problem:** Installing apps before shared packages

**Solution:** Install in correct order:
```bash
pip install -e packages/invoice-shared
pip install -e apps/supplier-invoice-loader
```

### Import Errors

**Problem:** Package not installed in editable mode

**Solution:**
```bash
pip install -e packages/your-package
pip install -e apps/your-app
```

### Tests Failing After Changes

```bash
# Reinstall all packages
pip install -e packages/invoice-shared -e packages/nex-shared
pip install -e apps/supplier-invoice-loader -e apps/supplier-invoice-editor

# Run tests
pytest
```

### 32-bit vs 64-bit Issues

**Symptom:** Package installation fails with "no matching wheel"

**Solution:** 
- Verify 32-bit Python: `python -c "import struct; print(struct.calcsize('P')*8)"`
- Make dependency optional if no 32-bit wheel available
- Use alternative package

### PowerShell Execution Policy

**Problem:** `.\venv32\Scripts\Activate.ps1` fails

**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## Best Practices

### 1. Always Use venv32

```bash
# Before any work
.\venv32\Scripts\Activate.ps1
```

### 2. Install Order Matters

```bash
# Correct order
pip install -e packages/*
pip install -e apps/*
```

### 3. Run Tests Before Commit

```bash
pytest --tb=no -q
```

### 4. Format Code

```bash
black .
ruff check .
```

### 5. Update Manifests

After structural changes:
```bash
python generate_projects_access.py
git add docs/
```

### 6. Keep Dependencies Minimal

Only add what you actually use.

### 7. Document Changes

Update SESSION_NOTES.md for significant changes.

---

## Related Documentation

- [SESSION_NOTES.md](../SESSION_NOTES.md) - Current status and history
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines
- [README.md](../../README.md) - Project overview

---

**Questions?** Contact: Zoltán Rausch (rausch@icc.sk)  
**Project:** NEX Automat v2.0.0  
**Organization:** ICC Komárno - Innovation & Consulting Center