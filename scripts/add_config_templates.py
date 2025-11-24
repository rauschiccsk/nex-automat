#!/usr/bin/env python
"""Add config templates and update deploy_fresh.py for clean installation support."""

from pathlib import Path

CONFIG_YAML_TEMPLATE = '''# NEX Automat v2.0 - Configuration Template
# Copy to config.yaml and update values for your customer

customer:
  name: CUSTOMER_CODE           # Short customer code (e.g., MAGERSTAV)
  full_name: Customer Name s.r.o.  # Full company name
  ico: '00000000'               # Company registration number (IČO)

database:
  postgres:
    host: localhost
    port: 5432
    database: invoice_staging
    user: postgres
    password: ${ENV:POSTGRES_PASSWORD}  # Set POSTGRES_PASSWORD environment variable

paths:
  pdf_storage: C:/NEX/IMPORT/pdf
  xml_storage: C:/NEX/IMPORT/xml
  temp_processing: C:/NEX/IMPORT/temp
  archive: C:/NEX/IMPORT/archive
  error: C:/NEX/IMPORT/error

nex_genesis:
  api_url: http://localhost:8080/api
  api_key: ''
  timeout: 30
  retry_attempts: 3
  retry_delay: 5
  root_path: C:/NEX
  yearact_path: C:/NEX/YEARACT
  stores_path: C:/NEX/YEARACT/STORES
  dials_path: C:/NEX/YEARACT/DIALS

email:
  operator: operator@customer.sk
  alert: alert@icc.sk
  smtp_host: ''
  smtp_port: 587
  smtp_user: ''
  smtp_password: ''
  enabled: false

features:
  send_daily_summary: false
  heartbeat_enabled: true
  auto_approve_threshold: 1000
  require_double_approval: true
  double_approval_threshold: 10000

logging:
  level: INFO
  log_dir: C:/Deployment/nex-automat/logs
  max_bytes: 10485760
  backup_count: 10

backup:
  backup_dir: C:/Deployment/nex-automat/backups
  retention:
    daily: 7
    weekly: 30
    monthly: 365
  compress: true
  encrypt_config: true

processing:
  batch_size: 10
  interval: 60
  max_processing_time: 300
  max_retries: 3
  concurrent_workers: 2

monitoring:
  enabled: true
  metrics_interval: 60
  health_check_enabled: true
  health_check_port: 8000

application:
  name: NEX-Automat-Loader
  version: 2.0.0
  environment: production

security:
  # Generate new key: python -c "import secrets; print(secrets.token_hex(32))"
  encryption_key: GENERATE_NEW_KEY_FOR_PRODUCTION
'''

CONFIG_CUSTOMER_TEMPLATE = '''# -*- coding: utf-8 -*-
"""
Supplier Invoice Loader - Customer Configuration Template
Copy to config_customer.py and update values for your customer
"""

import os
from pathlib import Path

# ============================================================================
# CUSTOMER SPECIFIC CONFIGURATION
# ============================================================================

CUSTOMER_NAME = "CUSTOMER_CODE"
CUSTOMER_FULL_NAME = "Customer Name s.r.o."

NEX_GENESIS_API_URL = "http://localhost:8080/api"
NEX_GENESIS_API_KEY = "customer-api-key"

OPERATOR_EMAIL = "operator@customer.sk"
AUTOMATION_EMAIL = "automation@customer.sk"

ALERT_EMAIL = "rausch@icc.sk"
SEND_DAILY_SUMMARY = True
HEARTBEAT_ENABLED = True

# ============================================================================
# GENERIC CONFIGURATION
# ============================================================================

API_KEY = os.getenv("LS_API_KEY", "ls-dev-key-change-in-production-2025")

BASE_DIR = Path(__file__).resolve().parent
STORAGE_BASE = Path(r"C:\\NEX\\IMPORT\\LS")
PDF_DIR = STORAGE_BASE / "PDF"
XML_DIR = STORAGE_BASE / "XML"

PDF_DIR.mkdir(parents=True, exist_ok=True)
XML_DIR.mkdir(parents=True, exist_ok=True)

DB_FILE = BASE_DIR / "invoices.db"
LOG_FILE = BASE_DIR / "invoice_loader.log"
LOG_LEVEL = "INFO"

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SMTP_FROM = "noreply@icc.sk"

# ==============================================================================
# POSTGRESQL STAGING CONFIGURATION
# ==============================================================================

POSTGRES_STAGING_ENABLED = True
POSTGRES_HOST = "localhost"
POSTGRES_PORT = 5432
POSTGRES_DATABASE = "invoice_staging"
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "")
'''

COPY_FROM_TEMPLATES_FUNC = '''
def copy_from_templates(deploy_path: Path):
    """Copy configuration templates when no backup exists."""
    log("Copying from templates (clean installation)...", "STEP")

    config_dir = deploy_path / "apps" / "supplier-invoice-loader" / "config"

    templates = [
        ("config.yaml.template", "config.yaml"),
        ("config_customer.py.template", "config_customer.py"),
    ]

    for template_name, target_name in templates:
        template = config_dir / template_name
        target = config_dir / target_name

        if template.exists() and not target.exists():
            shutil.copy2(template, target)
            log(f"Created from template: {target_name}", "OK")
        elif target.exists():
            log(f"Already exists: {target_name}", "INFO")
        else:
            log(f"Template not found: {template_name}", "WARN")

    # Try to find NSSM
    nssm_dst = deploy_path / "tools" / "nssm"
    if not nssm_dst.exists():
        alt_nssm = Path(r"C:\\Tools\\nssm")
        if alt_nssm.exists():
            shutil.copytree(alt_nssm, nssm_dst)
            log(f"Copied NSSM from {alt_nssm}", "OK")
        else:
            log("NSSM not found - install manually to tools/nssm/", "WARN")

    log("", "WARN")
    log("IMPORTANT: Edit config files before starting service!", "WARN")
    log(f"  1. Edit: {config_dir / 'config.yaml'}", "WARN")
    log(f"  2. Edit: {config_dir / 'config_customer.py'}", "WARN")
    log("  3. Generate new security.encryption_key", "WARN")


'''


def main():
    # 1. Create template files
    config_dir = Path("apps/supplier-invoice-loader/config")

    yaml_template = config_dir / "config.yaml.template"
    yaml_template.write_text(CONFIG_YAML_TEMPLATE, encoding="utf-8")
    print(f"[OK] Created: {yaml_template}")

    py_template = config_dir / "config_customer.py.template"
    py_template.write_text(CONFIG_CUSTOMER_TEMPLATE, encoding="utf-8")
    print(f"[OK] Created: {py_template}")

    # 2. Update deploy_fresh.py
    deploy_script = Path("scripts/deploy_fresh.py")
    content = deploy_script.read_text(encoding="utf-8")

    # 2a. Add copy_from_templates function
    insert_marker = "def copy_from_backup(deploy_path: Path, backup_path: Path):"
    if "def copy_from_templates" not in content:
        content = content.replace(insert_marker, COPY_FROM_TEMPLATES_FUNC + insert_marker)
        print("[OK] Added copy_from_templates function")

    # 2b. Update else branch to use templates
    old_else = '''else:
            log(f"No backup found at {backup_path}", "WARN")
            log("You will need to manually copy config.yaml and config_customer.py", "WARN")'''

    new_else = '''else:
            log(f"No backup found at {backup_path}", "WARN")
            copy_from_templates(deploy_path)'''

    if old_else in content:
        content = content.replace(old_else, new_else)
        print("[OK] Updated else branch to use templates")

    deploy_script.write_text(content, encoding="utf-8")
    print(f"[OK] Updated: {deploy_script}")

    return 0


if __name__ == "__main__":
    exit(main())