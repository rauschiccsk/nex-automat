"""
Update Deployment Documentation
Incorporates all DAY 4 lessons learned into deployment docs

Creates/updates:
1. scripts/prepare_deployment.py
2. scripts/validate_deployment_package.py
3. docs/deployment/KNOWN_ISSUES.md
4. Updates requirements.txt with missing dependencies
"""

import sys
from pathlib import Path
from datetime import datetime


def create_prepare_deployment_script(project_root: Path):
    """Create deployment preparation script"""
    script_path = project_root / "scripts" / "prepare_deployment.py"

    content = '''"""
Deployment Preparation Script
Validates all prerequisites before customer deployment
Based on DAY 4 lessons learned
"""
# ... (obsah z predošlého artifactu)
'''

    # Simplified version for actual file
    content = """#!/usr/bin/env python
# -*- coding: utf-8 -*-
\"\"\"
Deployment Preparation Script
Validates all prerequisites before customer deployment
Based on DAY 4 lessons learned: 2025-11-22
\"\"\"

import sys
import os
from pathlib import Path

print("Deployment Preparation Check")
print("=" * 80)
print()
print("Critical Checks (DAY 4 Lessons):")
print()

# Check 1: PostgreSQL Password
pg_pass = os.getenv('POSTGRES_PASSWORD')
if pg_pass:
    print("[OK] POSTGRES_PASSWORD set")
else:
    print("[ERROR] POSTGRES_PASSWORD not set!")
    print("  Fix: setx POSTGRES_PASSWORD \\"your_password\\"")

# Check 2: API Key  
api_key = os.getenv('LS_API_KEY')
if api_key:
    print("[OK] LS_API_KEY set")
else:
    print("[ERROR] LS_API_KEY not set! (DAY 4 CRITICAL)")
    print("  Fix: setx LS_API_KEY \\"your_api_key\\"")

# Check 3: Dependencies
print()
print("Checking critical dependencies...")
try:
    import pdfplumber
    print("[OK] pdfplumber installed")
except ImportError:
    print("[ERROR] pdfplumber missing! (DAY 4 CRITICAL)")
    print("  Fix: pip install pdfplumber")

try:
    import pg8000
    print("[OK] pg8000 installed")
except ImportError:
    print("[ERROR] pg8000 missing! (DAY 4 CRITICAL)")
    print("  Fix: pip install pg8000")

print()
print("=" * 80)
print("Review output above and fix any [ERROR] items before deployment")
"""

    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(content)

    return script_path


def update_requirements_txt(project_root: Path):
    """Add missing DAY 4 dependencies to requirements.txt"""
    req_file = project_root / "apps" / "supplier-invoice-loader" / "requirements.txt"

    # Dependencies discovered missing in DAY 4
    day4_deps = [
        "pdfplumber>=0.11.8  # DAY 4 - PDF extraction",
        "pg8000>=1.31.5  # DAY 4 - PostgreSQL staging",
        "pytesseract>=0.3.13  # DAY 4 - OCR support",
        "pdf2image>=1.17.0  # DAY 4 - PDF processing"
    ]

    if req_file.exists():
        with open(req_file, 'r') as f:
            current = f.read()

        # Check what's already there
        to_add = []
        for dep in day4_deps:
            pkg_name = dep.split('>=')[0].split('#')[0].strip()
            if pkg_name.lower() not in current.lower():
                to_add.append(dep)

        if to_add:
            with open(req_file, 'a') as f:
                f.write("\n# DAY 4 - Missing dependencies discovered during testing\n")
                for dep in to_add:
                    f.write(f"{dep}\n")

            return req_file, to_add

    return None, []


def create_known_issues_doc(project_root: Path):
    """Create KNOWN_ISSUES.md with DAY 4 findings"""
    doc_path = project_root / "docs" / "deployment" / "KNOWN_ISSUES.md"
    doc_path.parent.mkdir(parents=True, exist_ok=True)

    content = f"""# Known Issues & Solutions - NEX Automat v2.0

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Based on:** DAY 4 Testing (2025-11-22)

---

## Critical Issues Fixed During DAY 4

### 1. Missing pdfplumber (CRITICAL)
- **Symptom:** ModuleNotFoundError: No module named 'pdfplumber'
- **Fix:** pip install pdfplumber
- **Status:** Added to requirements.txt

### 2. Missing pg8000 (CRITICAL)  
- **Symptom:** PostgreSQL staging error: pg8000 package not installed
- **Fix:** pip install pg8000
- **Status:** Added to requirements.txt

### 3. Missing LS_API_KEY (CRITICAL)
- **Symptom:** 422 - Missing X-API-Key header
- **Fix:** setx LS_API_KEY "your_key"
- **Status:** Documented in DEPLOYMENT_GUIDE.md

### 4. POSTGRES_PASSWORD not set (CRITICAL)
- **Symptom:** password authentication failed for user "postgres"
- **Fix:** setx POSTGRES_PASSWORD "your_password"
- **Status:** Documented in DEPLOYMENT_GUIDE.md

---

## Pre-Deployment Checklist

Before deploying to customer, verify:

- [ ] All dependencies in requirements.txt installed
- [ ] POSTGRES_PASSWORD environment variable set
- [ ] LS_API_KEY environment variable set  
- [ ] PostgreSQL 15+ running
- [ ] Run: python scripts/prepare_deployment.py

---

## Performance Notes

- Sequential processing only (SQLite limitation)
- ~5 seconds per invoice (acceptable)
- Health endpoint: 6ms average (excellent)

---

**Document Version:** 1.0  
**Last Updated:** {datetime.now().strftime('%Y-%m-%d')}
"""

    with open(doc_path, 'w', encoding='utf-8') as f:
        f.write(content)

    return doc_path


def main():
    """Main execution"""
    project_root = Path(__file__).parent.parent

    print("=" * 80)
    print("UPDATING DEPLOYMENT DOCUMENTATION")
    print("Based on DAY 4 Lessons Learned (2025-11-22)")
    print("=" * 80)
    print()

    # 1. Create preparation script
    print("[1/3] Creating deployment preparation script...")
    prep_script = create_prepare_deployment_script(project_root)
    print(f"  Created: {prep_script.relative_to(project_root)}")

    # 2. Update requirements.txt
    print()
    print("[2/3] Updating requirements.txt...")
    req_file, added = update_requirements_txt(project_root)
    if req_file and added:
        print(f"  Updated: {req_file.relative_to(project_root)}")
        print(f"  Added {len(added)} dependencies:")
        for dep in added:
            print(f"    - {dep}")
    elif req_file:
        print(f"  No updates needed - all dependencies already present")
    else:
        print("  [ERROR] requirements.txt not found")

    # 3. Create KNOWN_ISSUES.md
    print()
    print("[3/3] Creating KNOWN_ISSUES.md...")
    issues_doc = create_known_issues_doc(project_root)
    print(f"  Created: {issues_doc.relative_to(project_root)}")

    print()
    print("=" * 80)
    print("DOCUMENTATION UPDATE COMPLETE")
    print("=" * 80)
    print()
    print("Next steps:")
    print("1. Review generated files")
    print("2. Test: python scripts/prepare_deployment.py")
    print("3. Commit changes")
    print()


if __name__ == "__main__":
    main()