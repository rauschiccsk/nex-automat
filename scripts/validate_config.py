#!/usr/bin/env python3
"""
NEX Automat - Configuration Validator
Validates production configuration for correctness and security
"""

import os
import sys
from pathlib import Path

import yaml


class ConfigValidator:
    def __init__(self, config_path: Path):
        self.config_path = config_path
        self.config = None
        self.errors = []
        self.warnings = []
        self.info = []

    def load_config(self) -> bool:
        """Load configuration file"""
        try:
            with open(self.config_path, encoding="utf-8") as f:
                self.config = yaml.safe_load(f)
            self.info.append(f"✅ Loaded config from: {self.config_path}")
            return True
        except FileNotFoundError:
            self.errors.append(f"❌ Config file not found: {self.config_path}")
            return False
        except yaml.YAMLError as e:
            self.errors.append(f"❌ Invalid YAML: {e}")
            return False
        except Exception as e:
            self.errors.append(f"❌ Error loading config: {e}")
            return False

    def validate_database(self):
        """Validate database configuration"""
        db = self.config.get("database", {}).get("postgres", {})

        required = ["host", "port", "database", "user", "password"]
        for field in required:
            if not db.get(field):
                self.errors.append(f"❌ Database: Missing required field '{field}'")

        port = db.get("port")
        if port and not (1 <= port <= 65535):
            self.errors.append(f"❌ Database: Invalid port {port}")

        password = db.get("password", "")
        if password == "CHANGE_ME":
            self.errors.append("❌ Database: Default password not changed!")
        elif len(password) < 8:
            self.warnings.append("⚠️  Database: Password is weak (< 8 characters)")

        self.info.append(f"✅ Database: {db.get('host')}:{db.get('port')}/{db.get('database')}")

    def validate_nex_genesis(self):
        """Validate NEX Genesis configuration"""
        nex = self.config.get("nex_genesis", {})

        if not nex.get("api_url"):
            self.errors.append("❌ NEX Genesis: Missing API URL")

        api_key = nex.get("api_key", "")
        if api_key == "CHANGE_ME":
            self.errors.append("❌ NEX Genesis: Default API key not changed!")
        elif not api_key:
            self.info.append("✅ NEX Genesis: API key empty (OK for local testing)")

        self.info.append(f"✅ NEX Genesis: {nex.get('api_url')}")

    def validate_email(self):
        """Validate email configuration"""
        email = self.config.get("email", {})
        smtp = email.get("smtp", {})

        if not email.get("operator"):
            self.warnings.append("⚠️  Email: No operator email configured")
        if not email.get("alert"):
            self.warnings.append("⚠️  Email: No alert email configured")

        if not smtp.get("host"):
            self.warnings.append("⚠️  Email: SMTP host not configured")

        smtp_password = smtp.get("password", "")
        if smtp_password == "CHANGE_ME":
            self.errors.append("❌ Email: Default SMTP password not changed!")

        port = smtp.get("port")
        if port not in [25, 465, 587]:
            self.warnings.append(f"⚠️  Email: Unusual SMTP port {port}")

        self.info.append(f"✅ Email: {smtp.get('host')}:{port} -> {email.get('operator')}")

    def validate_paths(self):
        """Validate storage paths"""
        paths = self.config.get("paths", {})

        required_paths = ["pdf_storage", "xml_storage", "temp_processing", "archive", "error"]

        for path_name in required_paths:
            path = paths.get(path_name)

            if not path:
                self.errors.append(f"❌ Paths: Missing '{path_name}'")
                continue

            path_obj = Path(path)

            if not path_obj.exists():
                self.warnings.append(f"⚠️  Path does not exist: {path} (will be created)")
            else:
                if not os.access(path, os.W_OK):
                    self.errors.append(f"❌ Path not writable: {path}")
                else:
                    self.info.append(f"✅ Path OK: {path}")

    def validate_backup(self):
        """Validate backup configuration"""
        backup = self.config.get("backup", {})

        backup_dir = backup.get("backup_dir")
        if not backup_dir:
            self.errors.append("❌ Backup: No backup directory configured")
        else:
            path_obj = Path(backup_dir)
            if not path_obj.exists():
                self.warnings.append(f"⚠️  Backup directory does not exist: {backup_dir}")
            elif not os.access(backup_dir, os.W_OK):
                self.errors.append(f"❌ Backup directory not writable: {backup_dir}")
            else:
                self.info.append(f"✅ Backup: {backup_dir}")

        retention = backup.get("retention", {})
        if retention.get("daily", 0) < 1:
            self.warnings.append("⚠️  Backup: Daily retention < 1 day")

    def validate_logging(self):
        """Validate logging configuration"""
        logging = self.config.get("logging", {})

        level = logging.get("level", "").upper()
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if level not in valid_levels:
            self.errors.append(f"❌ Logging: Invalid level '{level}'")

        log_dir = logging.get("log_dir")
        if not log_dir:
            self.errors.append("❌ Logging: No log directory configured")
        else:
            path_obj = Path(log_dir)
            if not path_obj.exists():
                self.warnings.append(f"⚠️  Log directory does not exist: {log_dir}")
            elif not os.access(log_dir, os.W_OK):
                self.errors.append(f"❌ Log directory not writable: {log_dir}")
            else:
                self.info.append(f"✅ Logging: {level} -> {log_dir}")

    def validate_security(self):
        """Validate security settings"""
        security = self.config.get("security", {})

        enc_key = security.get("encryption_key", "")
        if not enc_key:
            self.errors.append("❌ Security: No encryption key configured")
        elif enc_key == "CHANGE_ME_GENERATE_NEW_KEY":
            self.errors.append("❌ Security: Default encryption key not changed!")
        elif len(enc_key) < 32:
            self.warnings.append("⚠️  Security: Encryption key is short (< 32 chars)")

        self.info.append("✅ Security: Encryption key configured")

    def validate_application(self):
        """Validate application settings"""
        app = self.config.get("application", {})

        env = app.get("environment", "").lower()
        if env not in ["development", "staging", "production"]:
            self.warnings.append(f"⚠️  Application: Unknown environment '{env}'")

        if env == "production":
            self.info.append("✅ Application: Production environment")
        else:
            self.warnings.append(f"⚠️  Application: Non-production environment '{env}'")

    def check_default_values(self):
        """Check for unchanged default values"""
        import re

        config_str = yaml.dump(self.config)

        # Remove environment variable references (e.g., ${ENV:POSTGRES_PASSWORD})
        config_str = re.sub(r"\$\{ENV:[^}]+\}", "", config_str)

        dangerous_defaults = ["CHANGE_ME", "example.com"]

        for default in dangerous_defaults:
            if default in config_str:
                self.errors.append(f"❌ Found unchanged default value: '{default}'")

    def validate(self) -> bool:
        """Run all validations"""
        print("=" * 70)
        print("NEX AUTOMAT - CONFIGURATION VALIDATION")
        print("=" * 70)
        print()

        if not self.load_config():
            return False

        self.validate_database()
        self.validate_nex_genesis()
        self.validate_email()
        self.validate_paths()
        self.validate_backup()
        self.validate_logging()
        self.validate_security()
        self.validate_application()
        self.check_default_values()

        print("\n" + "=" * 70)
        print("VALIDATION RESULTS")
        print("=" * 70)

        if self.info:
            print("\n📋 INFORMATION:")
            for msg in self.info:
                print(f"  {msg}")

        if self.warnings:
            print("\n⚠️  WARNINGS:")
            for msg in self.warnings:
                print(f"  {msg}")

        if self.errors:
            print("\n❌ ERRORS:")
            for msg in self.errors:
                print(f"  {msg}")

        print("\n" + "=" * 70)
        print("SUMMARY")
        print("=" * 70)
        print(f"Information: {len(self.info)}")
        print(f"Warnings:    {len(self.warnings)}")
        print(f"Errors:      {len(self.errors)}")
        print()

        if self.errors:
            print("❌ VALIDATION FAILED - Fix errors before proceeding")
            return False
        elif self.warnings:
            print("⚠️  VALIDATION PASSED WITH WARNINGS - Review warnings")
            return True
        else:
            print("✅ VALIDATION PASSED - Configuration is valid")
            return True


def main():
    config_path = Path(__file__).parent.parent / "apps" / "supplier-invoice-loader" / "config" / "config.yaml"

    validator = ConfigValidator(config_path)
    success = validator.validate()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
