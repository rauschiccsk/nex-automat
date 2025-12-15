# Contributing to NEX Automat

**Kategória:** Development  
**Status:** 🟢 Complete  
**Vytvorené:** 2025-11-26  
**Aktualizované:** 2025-12-15  
**Related:** [GIT_WORKFLOW.md](GIT_WORKFLOW.md), [SETUP_GUIDE.md](SETUP_GUIDE.md), [TESTING_STRATEGY.md](TESTING_STRATEGY.md)

---

Ďakujeme za záujem prispieť do projektu NEX Automat! Tento dokument obsahuje pravidlá a best practices pre prispievanie.

---

## 📋 Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Process](#development-process)
4. [Code Style](#code-style)
5. [Commit Messages](#commit-messages)
6. [Testing](#testing)
7. [Pull Request Process](#pull-request-process)
8. [Documentation](#documentation)
9. [Release Process](#release-process)
10. [Getting Help](#getting-help)

---

## Code of Conduct

- **Profesionalita** - komunikuj profesionálne a s rešpektom
- **Kvalita** - dodávaj kvalitný, otestovaný kód
- **Dokumentácia** - dokumentuj svoje zmeny
- **Spolupráca** - pomáhaj ostatným

---

## Getting Started

### 1. Fork & Clone

```bash
# Fork repository on GitHub, then:
git clone https://github.com/[your-username]/nex-automat.git
cd nex-automat
```

### 2. Setup Environment

```powershell
# Create venv32
& "C:\Program Files (x86)\Python313-32\python.exe" -m venv venv32

# Activate
.\venv32\Scripts\Activate.ps1

# Install dependencies
pip install -e packages/invoice-shared -e packages/nex-shared
pip install -e apps/supplier-invoice-loader -e apps/supplier-invoice-editor
pip install pytest pytest-asyncio pytest-cov black ruff
```

### 3. Verify Setup

```bash
# Run tests
pytest --tb=no -q

# Should see: 61+ passed, 0 failed
```

---

## Development Process

### Branch Naming

```bash
# Feature
git checkout -b feature/invoice-validation

# Bugfix
git checkout -b fix/api-error-handling

# Documentation
git checkout -b docs/update-readme

# Hotfix
git checkout -b hotfix/critical-bug
```

### Workflow

```bash
# 1. Create branch
git checkout -b feature/my-feature

# 2. Make changes
# ... edit files ...

# 3. Format code
black .
ruff check . --fix

# 4. Run tests
pytest

# 5. Commit
git add .
git commit -m "feat: add invoice validation"

# 6. Push
git push origin feature/my-feature

# 7. Create Pull Request on GitHub
```

---

## Code Style

### Python Code Style

Používame **Black** a **Ruff** pre code formatting a linting.

#### Black Configuration

```bash
# Format all files
black .

# Check without formatting
black --check .

# Format specific file
black apps/my-app/src/main.py
```

#### Ruff Configuration

```bash
# Check all files
ruff check .

# Auto-fix issues
ruff check . --fix

# Check specific file
ruff check apps/my-app/src/main.py
```

### Code Quality Rules

#### 1. Imports

```python
# Standard library
import os
import sys
from pathlib import Path

# Third-party
import fastapi
from pydantic import BaseModel

# Local
from invoice_shared.database import PostgresStagingClient
from src.utils import config
```

#### 2. Type Hints

```python
def process_invoice(invoice_id: int) -> dict:
    """Process invoice and return result"""
    result: dict = {"status": "success"}
    return result

async def fetch_data(url: str) -> list[dict]:
    """Fetch data from API"""
    pass
```

#### 3. Docstrings

```python
def calculate_total(items: list[dict]) -> float:
    """
    Calculate total amount from items.
    
    Args:
        items: List of item dictionaries with 'price' and 'quantity'
        
    Returns:
        Total amount as float
        
    Raises:
        ValueError: If items list is empty
    """
    if not items:
        raise ValueError("Items list cannot be empty")
    
    return sum(item['price'] * item['quantity'] for item in items)
```

#### 4. Error Handling

```python
# Good - specific exceptions
try:
    result = process_data(data)
except ValueError as e:
    logger.error(f"Invalid data: {e}")
    raise
except KeyError as e:
    logger.error(f"Missing key: {e}")
    return None

# Bad - catching everything
try:
    result = process_data(data)
except Exception:
    pass
```

#### 5. Logging

```python
import logging

logger = logging.getLogger(__name__)

# Use appropriate levels
logger.debug("Detailed debug information")
logger.info("Invoice processed successfully")
logger.warning("API rate limit approaching")
logger.error("Failed to process invoice")
logger.critical("Database connection lost")
```

---

## Commit Messages

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: Nová funkcionalita
- `fix`: Oprava chyby
- `docs`: Dokumentácia
- `style`: Formátovanie (black, ruff)
- `refactor`: Refaktoring kódu
- `test`: Pridanie/oprava testov
- `chore`: Maintenance, dependencies

### Examples

#### Simple Commit

```
feat: add invoice duplicate detection

Implement duplicate detection based on supplier ICO and invoice number.
Checks PostgreSQL staging database before processing.
```

#### Complex Commit

```
feat(loader): add batch invoice processing

- Add batch processing endpoint /invoices/batch
- Support processing multiple invoices in single request
- Implement parallel processing with asyncio.gather()
- Add progress tracking and error reporting

Closes #123
```

#### Fix Commit

```
fix(api): handle missing invoice date gracefully

Previously crashed when invoice_date was None. Now returns 400 with
clear error message.

Fixes #456
```

#### Breaking Change

```
feat(shared)!: change PostgresStagingClient API

BREAKING CHANGE: PostgresStagingClient constructor now requires
explicit config dict instead of environment variables.

Migration guide:
```python
# Old
client = PostgresStagingClient()

# New
config = {
    'host': 'localhost',
    'port': 5432,
    'database': 'staging'
}
client = PostgresStagingClient(config)
```

Closes #789
```

### Scope Examples

- `loader` - supplier-invoice-loader
- `editor` - supplier-invoice-editor
- `shared` - invoice-shared package
- `docs` - dokumentácia
- `ci` - CI/CD

---

## Testing

### Test Requirements

**Každá zmena musí mať testy:**

- ✅ Nová funkcionalita → nové testy
- ✅ Bugfix → test reprodukujúci bug
- ✅ Refaktoring → existujúce testy musia prechádzať

### Writing Tests

#### Unit Test

```python
# tests/unit/test_validation.py
import pytest
from src.utils.validation import validate_invoice_number

def test_validate_invoice_number_valid():
    """Test valid invoice number"""
    assert validate_invoice_number("INV-2025-001") is True

def test_validate_invoice_number_invalid():
    """Test invalid invoice number"""
    assert validate_invoice_number("") is False
    assert validate_invoice_number(None) is False

def test_validate_invoice_number_format():
    """Test invoice number format validation"""
    with pytest.raises(ValueError):
        validate_invoice_number("INVALID")
```

#### Async Test

```python
@pytest.mark.asyncio
async def test_fetch_invoice_data():
    """Test async invoice data fetching"""
    result = await fetch_invoice_data(123)
    
    assert result is not None
    assert result['invoice_id'] == 123
    assert 'total_amount' in result
```

#### Integration Test

```python
@pytest.mark.integration
def test_full_invoice_processing(client, api_key):
    """Integration test for full workflow"""
    # Requires --run-integration flag
    response = client.post(
        "/invoice",
        headers={"X-API-Key": api_key},
        json=invoice_data
    )
    
    assert response.status_code == 200
    assert response.json()['success'] is True
```

### Running Tests

```bash
# All tests
pytest

# Specific app
pytest apps/supplier-invoice-loader/tests/

# Unit tests only
pytest apps/*/tests/unit/

# Integration tests
pytest --run-integration

# With coverage
pytest --cov=src --cov-report=html

# Watch mode (requires pytest-watch)
ptw
```

### Test Coverage

Minimum coverage requirements:
- **New code:** 80% coverage
- **Critical paths:** 100% coverage
- **Overall project:** 70%+ coverage

```bash
# Generate coverage report
pytest --cov=src --cov-report=html

# View report
start htmlcov/index.html
```

---

## Pull Request Process

### Before Creating PR

```bash
# 1. Rebase on main
git checkout main
git pull origin main
git checkout feature/my-feature
git rebase main

# 2. Format code
black .
ruff check . --fix

# 3. Run all tests
pytest

# 4. Update manifests if needed
python generate_projects_access.py

# 5. Update documentation if needed
# Edit docs/*.md
```

### PR Title Format

Same as commit messages:

```
feat(loader): add batch processing
fix(api): handle null dates
docs: update installation guide
```

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] All tests passing
- [ ] Code coverage maintained/improved

## Checklist
- [ ] Code formatted with black
- [ ] Linting passed with ruff
- [ ] Documentation updated
- [ ] Manifests regenerated (if structural changes)
- [ ] SESSION_NOTES.md updated (if significant change)

## Screenshots (if applicable)

## Related Issues
Closes #123
Fixes #456
```

### PR Review Process

1. **Automatic Checks** (CI/CD)
   - Tests must pass
   - Code must be formatted
   - Linting must pass

2. **Code Review**
   - At least 1 approval required
   - Address all review comments

3. **Merge**
   - Squash and merge (preferred)
   - Keep commit history clean

---

## Documentation

### When to Update Docs

- ✅ Nová funkcionalita
- ✅ API zmeny
- ✅ Breaking changes
- ✅ Nové dependencies
- ✅ Štruktúrne zmeny

### Documentation Files

- `README.md` - Project overview
- `docs/system/MONOREPO_STRUCTURE.md` - Development guide
- `docs/development/CONTRIBUTING.md` - This file
- `SESSION_NOTES/SESSION_NOTES.md` - Current status
- `SESSION_NOTES/apps/*.json` - App manifests
- Code docstrings

### Docstring Format

```python
def process_invoice(invoice_data: dict, validate: bool = True) -> dict:
    """
    Process invoice and save to database.
    
    This function validates invoice data, extracts relevant fields,
    and saves the invoice to both SQLite and PostgreSQL databases.
    
    Args:
        invoice_data: Dictionary containing invoice information with keys:
            - invoice_number (str): Invoice number
            - total_amount (float): Total amount
            - invoice_date (str): Date in ISO format
        validate: Whether to perform validation before processing
        
    Returns:
        Dictionary with processing result:
            - success (bool): Whether processing succeeded
            - invoice_id (int): Database ID of saved invoice
            - errors (list): List of errors if any
            
    Raises:
        ValueError: If invoice_data is invalid
        DatabaseError: If database save fails
        
    Example:
        >>> data = {
        ...     'invoice_number': 'INV-001',
        ...     'total_amount': 1000.0,
        ...     'invoice_date': '2025-01-15'
        ... }
        >>> result = process_invoice(data)
        >>> print(result['success'])
        True
    """
    pass
```

---

## Release Process

### Versioning

Používame **Semantic Versioning** (MAJOR.MINOR.PATCH):

- **MAJOR** - Breaking changes
- **MINOR** - New features (backward compatible)
- **PATCH** - Bug fixes

### Creating Release

```bash
# 1. Update version in pyproject.toml files
# 2. Update CHANGELOG.md
# 3. Commit version bump
git commit -m "chore: bump version to 2.1.0"

# 4. Create tag
git tag -a v2.1.0 -m "Release v2.1.0"

# 5. Push
git push origin main --tags
```

---

## Getting Help

- **Questions:** Create GitHub Discussion
- **Bug Reports:** Create GitHub Issue
- **Security Issues:** Email rausch@icc.sk
- **Documentation:** See [MONOREPO_STRUCTURE.md](../system/MONOREPO_STRUCTURE.md)

---

## Recognition

Contributors sú uvedení v AUTHORS.md a release notes.

---

**Thank you for contributing!** 🎉

---

**See Also:**
- [GIT_WORKFLOW.md](GIT_WORKFLOW.md) - Git branching a workflow
- [SETUP_GUIDE.md](SETUP_GUIDE.md) - Nastavenie vývojového prostredia
- [TESTING_STRATEGY.md](TESTING_STRATEGY.md) - Testovacia stratégia
- [CODING_STANDARDS.md](../system/CODING_STANDARDS.md) - Štandardy kódu