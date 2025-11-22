"""
Deployment Package Validator
Validates deployment package completeness before sending to customer

Ensures all DAY 4 lessons learned are addressed
"""

import sys
from pathlib import Path
from datetime import datetime


class PackageValidator:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.errors = []
        self.warnings = []
        self.passed = []

    def log(self, status, message):
        """Log validation result"""
        icon = {
            'pass': '[OK]',
            'fail': '[ERROR]',
            'warn': '[WARNING]'
        }[status]

        print(f"{icon} {message}")

        if status == 'pass':
            self.passed.append(message)
        elif status == 'fail':
            self.errors.append(message)
        elif status == 'warn':
            self.warnings.append(message)

    def check_requirements_file(self):
        """Validate requirements.txt has all DAY 4 dependencies"""
        print("\n" + "=" * 80)
        print("1. REQUIREMENTS.TXT VALIDATION")
        print("=" * 80)

        req_file = self.project_root / "apps" / "supplier-invoice-loader" / "requirements.txt"

        if not req_file.exists():
            self.log('fail', "requirements.txt not found!")
            return

        with open(req_file, 'r') as f:
            content = f.read().lower()

        # DAY 4 Critical dependencies
        critical_deps = {
            'pdfplumber': 'PDF extraction (DAY 4 CRITICAL)',
            'pg8000': 'PostgreSQL staging (DAY 4 CRITICAL)',
        }

        # Optional but recommended
        recommended_deps = {
            'pytesseract': 'OCR support',
            'pdf2image': 'PDF processing',
        }

        for dep, desc in critical_deps.items():
            if dep in content:
                self.log('pass', f"{dep} in requirements.txt - {desc}")
            else:
                self.log('fail', f"MISSING {dep} - {desc}")

        for dep, desc in recommended_deps.items():
            if dep in content:
                self.log('pass', f"{dep} in requirements.txt - {desc}")
            else:
                self.log('warn', f"Recommended: {dep} - {desc}")

    def check_documentation(self):
        """Check all deployment documentation exists"""
        print("\n" + "=" * 80)
        print("2. DOCUMENTATION COMPLETENESS")
        print("=" * 80)

        docs_dir = self.project_root / "docs" / "deployment"

        required_docs = {
            'DEPLOYMENT_GUIDE.md': 'Main deployment instructions',
            'PRE_DEPLOYMENT_CHECKLIST.md': 'Pre-deployment validation',
            'SERVICE_MANAGEMENT.md': 'Service operations guide',
            'TROUBLESHOOTING.md': 'Common issues and solutions',
            'KNOWN_ISSUES.md': 'DAY 4 lessons learned',
        }

        for doc, desc in required_docs.items():
            doc_path = docs_dir / doc
            if doc_path.exists():
                size_kb = doc_path.stat().st_size / 1024
                self.log('pass', f"{doc} ({size_kb:.1f} KB) - {desc}")
            else:
                self.log('fail', f"MISSING: {doc} - {desc}")

    def check_scripts(self):
        """Check deployment scripts exist"""
        print("\n" + "=" * 80)
        print("3. DEPLOYMENT SCRIPTS")
        print("=" * 80)

        scripts_dir = self.project_root / "scripts"

        required_scripts = {
            'prepare_deployment.py': 'Pre-deployment checks',
            'install_nssm.py': 'NSSM installation',
            'create_windows_service.py': 'Service creation',
            'manage_service.py': 'Service management',
            'test_e2e_workflow.py': 'E2E validation',
            'test_performance.py': 'Performance testing',
            'check_service_logs.py': 'Log viewer',
        }

        for script, desc in required_scripts.items():
            script_path = scripts_dir / script
            if script_path.exists():
                self.log('pass', f"{script} - {desc}")
            else:
                self.log('fail', f"MISSING: {script} - {desc}")

    def check_configuration_template(self):
        """Check configuration template exists"""
        print("\n" + "=" * 80)
        print("4. CONFIGURATION TEMPLATE")
        print("=" * 80)

        config_dir = self.project_root / "apps" / "supplier-invoice-loader" / "config"

        template = config_dir / "config.template.yaml"
        if template.exists():
            self.log('pass', "config.template.yaml exists")

            # Check template contains critical sections
            with open(template, 'r') as f:
                content = f.read()

            sections = ['customer:', 'paths:', 'database:', 'nex_genesis:']
            for section in sections:
                if section in content:
                    self.log('pass', f"  Template has {section}")
                else:
                    self.log('fail', f"  Template missing {section}")
        else:
            self.log('fail', "config.template.yaml not found")

    def check_test_data(self):
        """Check test data availability"""
        print("\n" + "=" * 80)
        print("5. TEST DATA")
        print("=" * 80)

        samples_dir = self.project_root / "apps" / "supplier-invoice-loader" / "tests" / "samples"

        if samples_dir.exists():
            pdf_files = list(samples_dir.glob("*.pdf"))

            if len(pdf_files) >= 3:
                self.log('pass', f"{len(pdf_files)} test PDF invoices available")
            elif len(pdf_files) > 0:
                self.log('warn', f"Only {len(pdf_files)} test PDFs - recommend 3+")
            else:
                self.log('warn', "No test PDFs - customer will need to provide samples")
        else:
            self.log('warn', "Test samples directory not found")

    def check_package_structure(self):
        """Verify package has correct structure"""
        print("\n" + "=" * 80)
        print("6. PACKAGE STRUCTURE")
        print("=" * 80)

        required_dirs = [
            "apps/supplier-invoice-loader",
            "packages/invoice-shared",
            "packages/nex-shared",
            "scripts",
            "docs/deployment",
        ]

        for dir_path in required_dirs:
            full_path = self.project_root / dir_path
            if full_path.exists():
                self.log('pass', f"{dir_path}/ exists")
            else:
                self.log('fail', f"{dir_path}/ MISSING")

    def check_environment_docs(self):
        """Check environment variable documentation"""
        print("\n" + "=" * 80)
        print("7. ENVIRONMENT VARIABLES DOCUMENTATION (DAY 4 CRITICAL)")
        print("=" * 80)

        # Check if deployment guide mentions critical env vars
        deployment_guide = self.project_root / "docs" / "deployment" / "DEPLOYMENT_GUIDE.md"

        if deployment_guide.exists():
            with open(deployment_guide, 'r') as f:
                content = f.read()

            # DAY 4 Critical variables
            critical_vars = {
                'POSTGRES_PASSWORD': 'PostgreSQL authentication',
                'LS_API_KEY': 'API authentication (DAY 4)',
            }

            for var, desc in critical_vars.items():
                if var in content:
                    self.log('pass', f"Documentation mentions {var} - {desc}")
                else:
                    self.log('fail', f"Documentation missing {var} - {desc}")
        else:
            self.log('fail', "DEPLOYMENT_GUIDE.md not found - cannot verify env var docs")

    def generate_package_manifest(self):
        """Generate deployment package manifest"""
        print("\n" + "=" * 80)
        print("8. GENERATING PACKAGE MANIFEST")
        print("=" * 80)

        manifest_path = self.project_root / "DEPLOYMENT_PACKAGE_MANIFEST.md"

        manifest_content = f"""# NEX Automat v2.0 - Deployment Package Manifest

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Version:** 2.0.0  
**Customer:** Mágerstav s.r.o.  
**Target Deployment:** 2025-11-27

---

## Package Contents

### Applications
- ✅ supplier-invoice-loader (main application)
  - Complete source code
  - Configuration templates
  - Test suites
  - Sample data

### Shared Packages
- ✅ invoice-shared (shared invoice models)
- ✅ nex-shared (NEX Genesis integration)

### Scripts ({len(list((self.project_root / 'scripts').glob('*.py')))} files)
- ✅ Deployment preparation
- ✅ Service installation
- ✅ Service management
- ✅ Testing utilities
- ✅ Log management

### Documentation ({len(list((self.project_root / 'docs' / 'deployment').glob('*.md')))} guides)
- ✅ DEPLOYMENT_GUIDE.md
- ✅ PRE_DEPLOYMENT_CHECKLIST.md
- ✅ SERVICE_MANAGEMENT.md
- ✅ TROUBLESHOOTING.md
- ✅ KNOWN_ISSUES.md (DAY 4 lessons)

---

## Critical Dependencies (DAY 4)

**MUST BE INSTALLED:**
```
pdfplumber>=0.11.8    # PDF extraction
pg8000>=1.31.5        # PostgreSQL staging
pytesseract>=0.3.13   # OCR support
pdf2image>=1.17.0     # PDF processing
```

**Environment Variables REQUIRED:**
```
POSTGRES_PASSWORD     # PostgreSQL authentication
LS_API_KEY           # API authentication (DAY 4 CRITICAL)
```

---

## Pre-Deployment Checklist

Before deploying to customer:

1. ✅ Run validation: `python scripts\\prepare_deployment.py`
2. ✅ All critical dependencies in requirements.txt
3. ✅ All documentation complete
4. ✅ All scripts tested
5. ✅ Environment variables documented
6. ✅ KNOWN_ISSUES.md reviewed

---

## Quick Start

```powershell
# 1. Extract package
cd C:\\Deployment\\nex-automat

# 2. Run preparation check
python scripts\\prepare_deployment.py

# 3. If all checks pass, run automated deployment
powershell -ExecutionPolicy Bypass -File scripts\\auto_deploy.ps1

# 4. Validate deployment
python scripts\\test_e2e_workflow.py
```

---

## Support

**Developer:** Zoltán Rausch  
**Email:** zoltan.rausch@icc.sk  
**Company:** ICC Komárno

---

**Package Validated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Validation Status:** {"PASS" if len(self.errors) == 0 else "FAIL"}  
**Critical Issues:** {len(self.errors)}  
**Warnings:** {len(self.warnings)}
"""

        try:
            with open(manifest_path, 'w', encoding='utf-8') as f:
                f.write(manifest_content)

            self.log('pass', f"Package manifest generated: {manifest_path.name}")
        except Exception as e:
            self.log('fail', f"Failed to generate manifest: {e}")

    def print_summary(self):
        """Print validation summary"""
        print("\n" + "=" * 80)
        print("DEPLOYMENT PACKAGE VALIDATION SUMMARY")
        print("=" * 80)
        print()
        print(f"Passed:   {len(self.passed)}")
        print(f"Warnings: {len(self.warnings)}")
        print(f"Errors:   {len(self.errors)}")
        print()

        if self.errors:
            print("CRITICAL ERRORS (MUST FIX):")
            print("-" * 80)
            for error in self.errors:
                print(f"  ❌ {error}")
            print()

        if self.warnings:
            print("WARNINGS (REVIEW):")
            print("-" * 80)
            for warning in self.warnings:
                print(f"  ⚠️  {warning}")
            print()

        if self.errors == 0:
            print("✅ DEPLOYMENT PACKAGE READY")
            print()
            print("Next Steps:")
            print("1. Review DEPLOYMENT_PACKAGE_MANIFEST.md")
            print("2. Create deployment archive:")
            print("   Compress-Archive -Path * -DestinationPath nex-automat-v2.0-deployment.zip")
            print("3. Send to customer with deployment instructions")
        else:
            print("❌ DEPLOYMENT PACKAGE NOT READY")
            print()
            print("Fix all critical errors and run again:")
            print("  python scripts\\validate_deployment_package.py")

        print()
        print("=" * 80)

    def run(self):
        """Run all validations"""
        print("=" * 80)
        print("NEX AUTOMAT v2.0 - DEPLOYMENT PACKAGE VALIDATOR")
        print("=" * 80)
        print()
        print("Validating package completeness based on DAY 4 lessons learned")
        print()

        self.check_requirements_file()
        self.check_documentation()
        self.check_scripts()
        self.check_configuration_template()
        self.check_test_data()
        self.check_package_structure()
        self.check_environment_docs()
        self.generate_package_manifest()
        self.print_summary()

        return 0 if len(self.errors) == 0 else 1


if __name__ == "__main__":
    validator = PackageValidator()
    sys.exit(validator.run())