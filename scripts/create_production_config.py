#!/usr/bin/env python3
"""
NEX Automat - Production Config Generator
Interactive script to create production configuration
"""

import os
import sys
import yaml
import secrets
from pathlib import Path
from getpass import getpass


def get_input(prompt: str, default: str = None, required: bool = True) -> str:
    """Get user input with optional default value"""
    if default:
        prompt_text = f"{prompt} [{default}]: "
    else:
        prompt_text = f"{prompt}: "

    while True:
        value = input(prompt_text).strip()

        if not value and default:
            return default

        if not value and required:
            print("❌ This field is required!")
            continue

        return value


def get_password(prompt: str) -> str:
    """Get password input (hidden)"""
    while True:
        password = getpass(f"{prompt}: ")
        if not password:
            print("❌ Password is required!")
            continue

        confirm = getpass(f"{prompt} (confirm): ")
        if password != confirm:
            print("❌ Passwords do not match!")
            continue

        return password


def get_yes_no(prompt: str, default: bool = True) -> bool:
    """Get yes/no input"""
    default_str = "Y/n" if default else "y/N"
    while True:
        value = input(f"{prompt} [{default_str}]: ").strip().lower()

        if not value:
            return default

        if value in ['y', 'yes']:
            return True
        if value in ['n', 'no']:
            return False

        print("❌ Please enter 'y' or 'n'")


def create_directory(path: str):
    """Create directory if it doesn't exist"""
    Path(path).mkdir(parents=True, exist_ok=True)
    print(f"✅ Created directory: {path}")


def main():
    print("=" * 70)
    print("NEX AUTOMAT - PRODUCTION CONFIGURATION GENERATOR")
    print("=" * 70)
    print()
    print("This wizard will guide you through creating production configuration.")
    print("Press Ctrl+C at any time to cancel.")
    print()

    # Load template
    template_path = Path(__file__).parent.parent / "apps" / "supplier-invoice-loader" / "config" / "config.template.yaml"
    if not template_path.exists():
        print(f"❌ Template not found: {template_path}")
        sys.exit(1)

    with open(template_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    # === DATABASE CONFIGURATION ===
    print("\n" + "=" * 70)
    print("DATABASE CONFIGURATION")
    print("=" * 70)

    config['database']['postgres']['host'] = get_input(
        "PostgreSQL Host", 
        default="localhost"
    )

    config['database']['postgres']['port'] = int(get_input(
        "PostgreSQL Port", 
        default="5432"
    ))

    config['database']['postgres']['database'] = get_input(
        "Database Name", 
        default="invoice_prod"
    )

    config['database']['postgres']['user'] = get_input(
        "Database User", 
        default="postgres"
    )

    config['database']['postgres']['password'] = get_password(
        "Database Password"
    )

    # === NEX GENESIS INTEGRATION ===
    print("\n" + "=" * 70)
    print("NEX GENESIS INTEGRATION")
    print("=" * 70)

    config['nex_genesis']['api_url'] = get_input(
        "NEX Genesis API URL",
        default="http://localhost:8080/api"
    )

    config['nex_genesis']['api_key'] = get_password(
        "NEX Genesis API Key"
    )

    # === EMAIL CONFIGURATION ===
    print("\n" + "=" * 70)
    print("EMAIL CONFIGURATION")
    print("=" * 70)

    config['email']['operator'] = get_input(
        "Operator Email",
        default="operator@magerstav.sk"
    )

    config['email']['alert'] = get_input(
        "Alert Email",
        default="alert@icc.sk"
    )

    if get_yes_no("Configure SMTP?", default=True):
        config['email']['smtp']['host'] = get_input(
            "SMTP Host",
            default="smtp.example.com"
        )

        config['email']['smtp']['port'] = int(get_input(
            "SMTP Port (587 for TLS, 465 for SSL)",
            default="587"
        ))

        config['email']['smtp']['user'] = get_input(
            "SMTP User"
        )

        config['email']['smtp']['password'] = get_password(
            "SMTP Password"
        )

        config['email']['smtp']['use_tls'] = get_yes_no(
            "Use TLS?", 
            default=True
        )

        config['email']['smtp']['from_address'] = get_input(
            "From Address",
            default="nex-automat@magerstav.sk"
        )

    # === STORAGE PATHS ===
    print("\n" + "=" * 70)
    print("STORAGE PATHS")
    print("=" * 70)

    base_path = get_input(
        "Base Storage Path",
        default="C:/NEX-Automat/storage"
    )

    config['paths']['pdf_storage'] = f"{base_path}/pdf"
    config['paths']['xml_storage'] = f"{base_path}/xml"
    config['paths']['temp_processing'] = f"{base_path}/temp"
    config['paths']['archive'] = f"{base_path}/archive"
    config['paths']['error'] = f"{base_path}/error"

    if get_yes_no("Create storage directories?", default=True):
        for path in config['paths'].values():
            create_directory(path)

    # === BACKUP CONFIGURATION ===
    print("\n" + "=" * 70)
    print("BACKUP CONFIGURATION")
    print("=" * 70)

    backup_dir = get_input(
        "Backup Directory",
        default="C:/NEX-Automat/backups"
    )
    config['backup']['backup_dir'] = backup_dir

    if get_yes_no("Create backup directory?", default=True):
        create_directory(backup_dir)

    # === LOGGING CONFIGURATION ===
    print("\n" + "=" * 70)
    print("LOGGING CONFIGURATION")
    print("=" * 70)

    log_dir = get_input(
        "Log Directory",
        default="C:/NEX-Automat/logs"
    )
    config['logging']['log_dir'] = log_dir

    if get_yes_no("Create log directory?", default=True):
        create_directory(log_dir)

    log_level = get_input(
        "Log Level (DEBUG/INFO/WARNING/ERROR)",
        default="INFO"
    ).upper()
    config['logging']['level'] = log_level

    # === SECURITY SETTINGS ===
    print("\n" + "=" * 70)
    print("SECURITY SETTINGS")
    print("=" * 70)

    print("Generating encryption key...")
    config['security']['encryption_key'] = secrets.token_hex(32)
    print("✅ Encryption key generated")

    # === CUSTOMER CONFIGURATION ===
    print("\n" + "=" * 70)
    print("CUSTOMER CONFIGURATION")
    print("=" * 70)

    config['customer']['id'] = get_input(
        "Customer ID",
        default="MAGERSTAV"
    ).upper()

    config['customer']['name'] = get_input(
        "Customer Name",
        default="Mágerstav s.r.o."
    )

    # === SAVE CONFIGURATION ===
    print("\n" + "=" * 70)
    print("SAVE CONFIGURATION")
    print("=" * 70)

    output_path = Path(__file__).parent.parent / "apps" / "supplier-invoice-loader" / "config" / "config.yaml"

    if output_path.exists():
        if not get_yes_no(f"⚠️  {output_path} already exists. Overwrite?", default=False):
            print("❌ Configuration not saved.")
            sys.exit(1)

    # Save config
    with open(output_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    print(f"\n✅ Configuration saved to: {output_path}")

    # === SECURITY WARNINGS ===
    print("\n" + "=" * 70)
    print("⚠️  SECURITY WARNINGS")
    print("=" * 70)
    print("1. Never commit config.yaml to Git!")
    print("2. Protect config.yaml with appropriate file permissions")
    print("3. Backup config.yaml securely")
    print("4. Store encryption key separately")
    print("5. Use strong passwords for all services")
    print()

    # === NEXT STEPS ===
    print("=" * 70)
    print("NEXT STEPS")
    print("=" * 70)
    print("1. Review config.yaml for correctness")
    print("2. Test database connection: python scripts/test_database_connection.py")
    print("3. Validate configuration: python scripts/validate_config.py")
    print("4. Initialize database schema")
    print("5. Install Windows Service")
    print()
    print("✅ Configuration setup complete!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Configuration cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        sys.exit(1)
