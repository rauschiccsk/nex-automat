#!/usr/bin/env python3
"""
Create Test/Production Config for NEX Automat
Based on existing config structure
"""

import os
import yaml
from pathlib import Path

BASE_PATH = Path(r"C:\Development\nex-automat")

# Test configuration for supplier-invoice-loader
TEST_CONFIG = {
    "customer": {
        "name": "MAGERSTAV",
        "full_name": "Mágerstav s.r.o.",
        "ico": "12345678"
    },

    "database": {
        "postgres": {
            "host": "localhost",
            "port": 5432,
            "database": "invoice_staging",
            "user": "postgres",
            "password": "${ENV:POSTGRES_PASSWORD}"
        }
    },

    "paths": {
        "pdf_storage": "C:/NEX/IMPORT/pdf",
        "xml_storage": "C:/NEX/IMPORT/xml",
        "temp_processing": "C:/NEX/IMPORT/temp",
        "archive": "C:/NEX/IMPORT/archive",
        "error": "C:/NEX/IMPORT/error"
    },

    "nex_genesis": {
        "api_url": "http://localhost:8080/api",
        "api_key": "",  # Not required for local testing
        "timeout": 30,
        "retry_attempts": 3,
        "retry_delay": 5
    },

    "email": {
        "operator": "operator@magerstav.sk",
        "alert": "alert@icc.sk",
        "smtp_host": "smtp.example.com",
        "smtp_port": 587,
        "smtp_user": "",
        "smtp_password": "",
        "enabled": False  # Disabled for testing
    },

    "features": {
        "send_daily_summary": False,  # Disabled for testing
        "heartbeat_enabled": True,
        "auto_approve_threshold": 1000,
        "require_double_approval": True,
        "double_approval_threshold": 10000
    },

    "logging": {
        "level": "INFO",
        "log_dir": "C:/NEX-Automat/logs",
        "max_bytes": 10485760,  # 10 MB
        "backup_count": 10
    },

    "processing": {
        "batch_size": 10,
        "interval": 60,
        "max_processing_time": 300,
        "max_retries": 3,
        "concurrent_workers": 2
    },

    "monitoring": {
        "enabled": True,
        "metrics_interval": 60,
        "health_check_enabled": True,
        "health_check_port": 8000
    },

    "application": {
        "name": "NEX-Automat-Loader",
        "version": "2.0.0",
        "environment": "development"
    }
}


def create_directories():
    """Create required directories"""
    dirs = [
        "C:/NEX/IMPORT/pdf",
        "C:/NEX/IMPORT/xml",
        "C:/NEX/IMPORT/temp",
        "C:/NEX/IMPORT/archive",
        "C:/NEX/IMPORT/error",
        "C:/NEX-Automat/logs",
        "C:/NEX-Automat/backups"
    ]

    print("Creating directories...")
    for dir_path in dirs:
        path = Path(dir_path)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            print(f"  ✅ Created: {dir_path}")
        else:
            print(f"  ✅ Exists: {dir_path}")


def check_postgres_password():
    """Check if POSTGRES_PASSWORD environment variable exists"""
    password = os.environ.get('POSTGRES_PASSWORD')
    if password:
        print(f"✅ POSTGRES_PASSWORD found in environment")
        return True
    else:
        print("⚠️  POSTGRES_PASSWORD not found in environment variables")
        print("\nTo set it:")
        print('  setx POSTGRES_PASSWORD "your-password"')
        print("  (requires new terminal session)")
        return False


def save_config():
    """Save configuration to file"""
    config_path = BASE_PATH / "apps" / "supplier-invoice-loader" / "config" / "config.yaml"

    # Backup existing config if exists
    if config_path.exists():
        backup_path = config_path.with_suffix('.yaml.backup')
        import shutil
        shutil.copy2(config_path, backup_path)
        print(f"✅ Backed up existing config to: {backup_path}")

    # Save new config
    with open(config_path, 'w', encoding='utf-8') as f:
        yaml.dump(TEST_CONFIG, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    print(f"✅ Saved config to: {config_path}")


def main():
    print("=" * 70)
    print("NEX AUTOMAT - TEST/DEVELOPMENT CONFIG GENERATOR")
    print("=" * 70)
    print()

    # Check environment
    print("1. Checking environment...")
    has_password = check_postgres_password()
    print()

    # Create directories
    print("2. Creating directories...")
    create_directories()
    print()

    # Save config
    print("3. Saving configuration...")
    save_config()
    print()

    # Summary
    print("=" * 70)
    print("✅ TEST CONFIG CREATED")
    print("=" * 70)
    print()
    print("Configuration:")
    print("  Database: invoice_staging @ localhost:5432")
    print("  NEX Genesis: http://localhost:8080/api")
    print("  Storage: C:/NEX/IMPORT/")
    print("  Logs: C:/NEX-Automat/logs/")
    print()

    if not has_password:
        print("⚠️  WARNING: POSTGRES_PASSWORD not set!")
        print("   Set it before running tests")
        print()

    print("Next steps:")
    print("  1. Verify config: python scripts/validate_config.py")
    print("  2. Test database: python scripts/test_database_connection.py")
    print("  3. Run tests: pytest apps/supplier-invoice-loader/tests/")
    print()


if __name__ == "__main__":
    main()