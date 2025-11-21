#!/usr/bin/env python3
"""
Update Config for Production Deployment
Changes paths from C:\Development to C:\Deployment
"""

import yaml
from pathlib import Path

# Paths
DEV_PATH = Path(r"C:\Development\nex-automat")
PROD_PATH = Path(r"C:\Deployment\nex-automat")

# Production configuration
PROD_CONFIG = {
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
        "api_key": "",
        "timeout": 30,
        "retry_attempts": 3,
        "retry_delay": 5,
        # NEX data paths
        "root_path": "C:/NEX",
        "yearact_path": "C:/NEX/YEARACT",
        "stores_path": "C:/NEX/YEARACT/STORES",
        "dials_path": "C:/NEX/YEARACT/DIALS"
    },

    "email": {
        "operator": "operator@magerstav.sk",
        "alert": "alert@icc.sk",
        "smtp_host": "smtp.example.com",
        "smtp_port": 587,
        "smtp_user": "",
        "smtp_password": "",
        "enabled": False
    },

    "features": {
        "send_daily_summary": False,
        "heartbeat_enabled": True,
        "auto_approve_threshold": 1000,
        "require_double_approval": True,
        "double_approval_threshold": 10000
    },

    "logging": {
        "level": "INFO",
        "log_dir": "C:/Deployment/nex-automat/logs",  # Production path
        "max_bytes": 10485760,
        "backup_count": 10
    },

    "backup": {
        "backup_dir": "C:/Deployment/nex-automat/backups",  # Production path
        "retention": {
            "daily": 7,
            "weekly": 30,
            "monthly": 365
        },
        "compress": True,
        "encrypt_config": True
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
        "environment": "production"
    }
}


def create_prod_directories():
    """Create production directories"""
    dirs = [
        "C:/Deployment/nex-automat/logs",
        "C:/Deployment/nex-automat/backups",
        "C:/NEX/IMPORT/pdf",
        "C:/NEX/IMPORT/xml",
        "C:/NEX/IMPORT/temp",
        "C:/NEX/IMPORT/archive",
        "C:/NEX/IMPORT/error"
    ]

    print("Creating production directories...")
    for dir_path in dirs:
        path = Path(dir_path)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            print(f"  ✅ Created: {dir_path}")
        else:
            print(f"  ✅ Exists: {dir_path}")


def save_config(base_path: Path):
    """Save configuration"""
    config_path = base_path / "apps" / "supplier-invoice-loader" / "config" / "config.yaml"

    # Backup if exists
    if config_path.exists():
        backup_path = config_path.with_suffix('.yaml.backup')
        import shutil
        shutil.copy2(config_path, backup_path)
        print(f"✅ Backed up: {backup_path}")

    # Save config
    config_path.parent.mkdir(parents=True, exist_ok=True)
    with open(config_path, 'w', encoding='utf-8') as f:
        yaml.dump(PROD_CONFIG, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    print(f"✅ Saved config: {config_path}")


def main():
    print("=" * 70)
    print("UPDATE CONFIG FOR PRODUCTION DEPLOYMENT")
    print("=" * 70)
    print()

    # Create directories
    print("1. Creating directories...")
    create_prod_directories()
    print()

    # Update development config (for testing deployment from dev)
    print("2. Updating development config...")
    save_config(DEV_PATH)
    print()

    # Show summary
    print("=" * 70)
    print("✅ PRODUCTION PATHS CONFIGURED")
    print("=" * 70)
    print()
    print("Deployment structure:")
    print("  Production:  C:/Deployment/nex-automat/")
    print("  Logs:        C:/Deployment/nex-automat/logs/")
    print("  Backups:     C:/Deployment/nex-automat/backups/")
    print("  Storage:     C:/NEX/IMPORT/")
    print("  NEX Data:    C:/NEX/YEARACT/")
    print()
    print("Next steps:")
    print("  1. Validate: python scripts/validate_config.py")
    print("  2. Test DB:  python scripts/test_database_connection.py")
    print("  3. Deploy:   python scripts/deploy_to_production.py")
    print()


if __name__ == "__main__":
    main()