#!/usr/bin/env python3
"""
Deploy Config Tools - Creates all configuration files and scripts
"""

import os
from pathlib import Path

# Base path
BASE_PATH = Path(r"C:\Development\nex-automat")

# File contents
FILES = {
    "scripts/create_production_config.py": '''#!/usr/bin/env python3
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
    template_path = Path(__file__).parent.parent / "config" / "config.template.yaml"
    if not template_path.exists():
        print(f"❌ Template not found: {template_path}")
        sys.exit(1)

    with open(template_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    # === DATABASE CONFIGURATION ===
    print("\\n" + "=" * 70)
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
    print("\\n" + "=" * 70)
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
    print("\\n" + "=" * 70)
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
    print("\\n" + "=" * 70)
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
    print("\\n" + "=" * 70)
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
    print("\\n" + "=" * 70)
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
    print("\\n" + "=" * 70)
    print("SECURITY SETTINGS")
    print("=" * 70)

    print("Generating encryption key...")
    config['security']['encryption_key'] = secrets.token_hex(32)
    print("✅ Encryption key generated")

    # === CUSTOMER CONFIGURATION ===
    print("\\n" + "=" * 70)
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
    print("\\n" + "=" * 70)
    print("SAVE CONFIGURATION")
    print("=" * 70)

    output_path = Path(__file__).parent.parent / "config" / "config.yaml"

    if output_path.exists():
        if not get_yes_no(f"⚠️  {output_path} already exists. Overwrite?", default=False):
            print("❌ Configuration not saved.")
            sys.exit(1)

    # Save config
    with open(output_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    print(f"\\n✅ Configuration saved to: {output_path}")

    # === SECURITY WARNINGS ===
    print("\\n" + "=" * 70)
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
        print("\\n\\n❌ Configuration cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\\n\\n❌ Error: {e}")
        sys.exit(1)
''',
    "config/config.template.yaml": '''# NEX Automat - Production Configuration Template
# Copy this file to config.yaml and fill in your production values
# WARNING: Never commit config.yaml to Git!

# Database Configuration
database:
  postgres:
    host: "localhost"           # PostgreSQL server hostname or IP
    port: 5432                  # PostgreSQL port (default: 5432)
    database: "invoice_prod"    # Database name
    user: "postgres"            # Database user
    password: "CHANGE_ME"       # Database password (use strong password!)

  # Connection pool settings
  pool:
    min_size: 2
    max_size: 10
    timeout: 30

# NEX Genesis Integration
nex_genesis:
  api_url: "http://localhost:8080/api"  # NEX Genesis API endpoint
  api_key: "CHANGE_ME"                   # API authentication key
  timeout: 30                             # Request timeout in seconds
  retry_attempts: 3                       # Number of retry attempts
  retry_delay: 5                          # Delay between retries (seconds)

# Email Configuration
email:
  # Operator email (receives notifications)
  operator: "operator@magerstav.sk"

  # Alert email (receives critical alerts)
  alert: "alert@icc.sk"

  # SMTP Configuration
  smtp:
    host: "smtp.example.com"    # SMTP server hostname
    port: 587                   # SMTP port (587 for TLS, 465 for SSL)
    user: "CHANGE_ME"           # SMTP username
    password: "CHANGE_ME"       # SMTP password
    use_tls: true               # Use TLS (recommended)
    use_ssl: false              # Use SSL (alternative to TLS)
    from_address: "nex-automat@magerstav.sk"

  # Email notification settings
  notifications:
    send_on_success: false      # Send email on successful processing
    send_on_error: true         # Send email on errors
    send_on_warning: true       # Send email on warnings
    send_daily_summary: true    # Send daily processing summary

# Storage Paths
paths:
  # PDF storage directory
  pdf_storage: "C:/NEX-Automat/storage/pdf"

  # XML storage directory
  xml_storage: "C:/NEX-Automat/storage/xml"

  # Temporary processing directory
  temp_processing: "C:/NEX-Automat/storage/temp"

  # Archive directory (processed files)
  archive: "C:/NEX-Automat/storage/archive"

  # Error directory (failed processing)
  error: "C:/NEX-Automat/storage/error"

# Backup Configuration
backup:
  # Backup storage directory
  backup_dir: "C:/NEX-Automat/backups"

  # Retention policy (days)
  retention:
    daily: 7        # Keep daily backups for 7 days
    weekly: 30      # Keep weekly backups for 30 days
    monthly: 365    # Keep monthly backups for 1 year

  # Compression
  compress: true

  # Encryption (XOR encryption for config files)
  encrypt_config: true

# Logging Configuration
logging:
  level: "INFO"                 # DEBUG, INFO, WARNING, ERROR, CRITICAL
  log_dir: "C:/NEX-Automat/logs"

  # Log rotation
  rotation:
    max_bytes: 10485760         # 10 MB
    backup_count: 10            # Keep 10 old log files

  # Log format
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  date_format: "%Y-%m-%d %H:%M:%S"

# Processing Configuration
processing:
  # Batch size for processing
  batch_size: 10

  # Processing interval (seconds)
  interval: 60

  # Maximum processing time per invoice (seconds)
  max_processing_time: 300

  # Maximum retries for failed invoices
  max_retries: 3

  # Concurrent processing
  concurrent_workers: 2

# Monitoring Configuration
monitoring:
  # Enable monitoring
  enabled: true

  # Metrics collection interval (seconds)
  metrics_interval: 60

  # Health check endpoint
  health_check_enabled: true
  health_check_port: 8000

  # Alert thresholds
  alerts:
    error_rate_threshold: 0.1   # Alert if error rate > 10%
    queue_size_threshold: 100   # Alert if queue size > 100
    processing_time_threshold: 300  # Alert if avg processing time > 5 min

# Customer Configuration
customer:
  id: "MAGERSTAV"
  name: "Mágerstav s.r.o."

  # Customer-specific settings
  settings:
    auto_approve_threshold: 1000    # Auto-approve invoices below this amount
    require_double_approval: true   # Require double approval for large amounts
    double_approval_threshold: 10000  # Threshold for double approval

# Application Settings
application:
  name: "NEX-Automat-Loader"
  version: "2.0.0"
  environment: "production"     # development, staging, production

  # Service settings
  service:
    startup_delay: 10           # Delay before starting processing (seconds)
    shutdown_timeout: 30        # Timeout for graceful shutdown (seconds)
    restart_on_error: true      # Restart service on critical error

# Security Settings
security:
  # API authentication
  api_key_required: true

  # Allowed IP addresses (empty = allow all)
  allowed_ips: []

  # SSL/TLS settings
  ssl_verify: true

  # Password encryption key (generate with: python -c "import secrets; print(secrets.token_hex(32))")
  encryption_key: "CHANGE_ME_GENERATE_NEW_KEY"
''',
    "scripts/validate_config.py": r'''#!/usr/bin/env python3
"""
NEX Automat - Configuration Validator
Validates production configuration for correctness and security
"""

import os
import sys
import yaml
from pathlib import Path


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
            with open(self.config_path, 'r', encoding='utf-8') as f:
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
        db = self.config.get('database', {}).get('postgres', {})

        required = ['host', 'port', 'database', 'user', 'password']
        for field in required:
            if not db.get(field):
                self.errors.append(f"❌ Database: Missing required field '{field}'")

        port = db.get('port')
        if port and not (1 <= port <= 65535):
            self.errors.append(f"❌ Database: Invalid port {port}")

        password = db.get('password', '')
        if password == 'CHANGE_ME':
            self.errors.append("❌ Database: Default password not changed!")
        elif len(password) < 8:
            self.warnings.append("⚠️  Database: Password is weak (< 8 characters)")

        self.info.append(f"✅ Database: {db.get('host')}:{db.get('port')}/{db.get('database')}")

    def validate_nex_genesis(self):
        """Validate NEX Genesis configuration"""
        nex = self.config.get('nex_genesis', {})

        if not nex.get('api_url'):
            self.errors.append("❌ NEX Genesis: Missing API URL")

        api_key = nex.get('api_key', '')
        if not api_key:
            self.errors.append("❌ NEX Genesis: Missing API key")
        elif api_key == 'CHANGE_ME':
            self.errors.append("❌ NEX Genesis: Default API key not changed!")

        self.info.append(f"✅ NEX Genesis: {nex.get('api_url')}")

    def validate_email(self):
        """Validate email configuration"""
        email = self.config.get('email', {})
        smtp = email.get('smtp', {})

        if not email.get('operator'):
            self.warnings.append("⚠️  Email: No operator email configured")
        if not email.get('alert'):
            self.warnings.append("⚠️  Email: No alert email configured")

        if not smtp.get('host'):
            self.warnings.append("⚠️  Email: SMTP host not configured")

        smtp_password = smtp.get('password', '')
        if smtp_password == 'CHANGE_ME':
            self.errors.append("❌ Email: Default SMTP password not changed!")

        port = smtp.get('port')
        if port not in [25, 465, 587]:
            self.warnings.append(f"⚠️  Email: Unusual SMTP port {port}")

        self.info.append(f"✅ Email: {smtp.get('host')}:{port} -> {email.get('operator')}")

    def validate_paths(self):
        """Validate storage paths"""
        paths = self.config.get('paths', {})

        required_paths = ['pdf_storage', 'xml_storage', 'temp_processing', 'archive', 'error']

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
        backup = self.config.get('backup', {})

        backup_dir = backup.get('backup_dir')
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

        retention = backup.get('retention', {})
        if retention.get('daily', 0) < 1:
            self.warnings.append("⚠️  Backup: Daily retention < 1 day")

    def validate_logging(self):
        """Validate logging configuration"""
        logging = self.config.get('logging', {})

        level = logging.get('level', '').upper()
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if level not in valid_levels:
            self.errors.append(f"❌ Logging: Invalid level '{level}'")

        log_dir = logging.get('log_dir')
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
        security = self.config.get('security', {})

        enc_key = security.get('encryption_key', '')
        if not enc_key:
            self.errors.append("❌ Security: No encryption key configured")
        elif enc_key == 'CHANGE_ME_GENERATE_NEW_KEY':
            self.errors.append("❌ Security: Default encryption key not changed!")
        elif len(enc_key) < 32:
            self.warnings.append("⚠️  Security: Encryption key is short (< 32 chars)")

        self.info.append("✅ Security: Encryption key configured")

    def validate_application(self):
        """Validate application settings"""
        app = self.config.get('application', {})

        env = app.get('environment', '').lower()
        if env not in ['development', 'staging', 'production']:
            self.warnings.append(f"⚠️  Application: Unknown environment '{env}'")

        if env == 'production':
            self.info.append("✅ Application: Production environment")
        else:
            self.warnings.append(f"⚠️  Application: Non-production environment '{env}'")

    def check_default_values(self):
        """Check for unchanged default values"""
        config_str = yaml.dump(self.config)

        dangerous_defaults = ['CHANGE_ME', 'example.com', 'password', 'secret']

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
    config_path = Path(__file__).parent.parent / "config" / "config.yaml"

    validator = ConfigValidator(config_path)
    success = validator.validate()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
''',
    "scripts/test_database_connection.py": r'''#!/usr/bin/env python3
"""
NEX Automat - Database Connection Test
Tests PostgreSQL database connectivity and configuration
"""

import sys
import asyncio
import asyncpg
import yaml
from pathlib import Path
from datetime import datetime


async def test_connection(config: dict) -> bool:
    """Test database connection"""
    db_config = config['database']['postgres']

    print("\n" + "=" * 70)
    print("DATABASE CONNECTION TEST")
    print("=" * 70)
    print(f"Host:     {db_config['host']}")
    print(f"Port:     {db_config['port']}")
    print(f"Database: {db_config['database']}")
    print(f"User:     {db_config['user']}")
    print("=" * 70)
    print()

    try:
        print("📡 Connecting to database...")

        conn = await asyncpg.connect(
            host=db_config['host'],
            port=db_config['port'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password'],
            timeout=10
        )

        print("✅ Connected successfully!")

        # Test 1: Get PostgreSQL version
        print("\n" + "-" * 70)
        print("TEST 1: PostgreSQL Version")
        print("-" * 70)

        version = await conn.fetchval('SELECT version()')
        print(f"✅ {version}")

        # Test 2: Check current timestamp
        print("\n" + "-" * 70)
        print("TEST 2: Server Timestamp")
        print("-" * 70)

        timestamp = await conn.fetchval('SELECT NOW()')
        print(f"✅ Server time: {timestamp}")
        local_time = datetime.now()
        print(f"   Local time:  {local_time}")

        # Test 3: List tables
        print("\n" + "-" * 70)
        print("TEST 3: Database Tables")
        print("-" * 70)

        tables = await conn.fetch("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)

        if tables:
            print(f"✅ Found {len(tables)} tables:")
            for table in tables:
                print(f"   - {table['table_name']}")
        else:
            print("⚠️  No tables found (database is empty)")

        # Test 4: Check database size
        print("\n" + "-" * 70)
        print("TEST 4: Database Size")
        print("-" * 70)

        size = await conn.fetchval("""
            SELECT pg_size_pretty(pg_database_size(current_database()))
        """)
        print(f"✅ Database size: {size}")

        # Test 5: Check connection limits
        print("\n" + "-" * 70)
        print("TEST 5: Connection Limits")
        print("-" * 70)

        max_conn = await conn.fetchval('SHOW max_connections')
        current_conn = await conn.fetchval("""
            SELECT count(*) FROM pg_stat_activity 
            WHERE datname = current_database()
        """)
        print(f"✅ Max connections:     {max_conn}")
        print(f"✅ Current connections: {current_conn}")

        # Test 6: Check user privileges
        print("\n" + "-" * 70)
        print("TEST 6: User Privileges")
        print("-" * 70)

        privileges = await conn.fetch("""
            SELECT privilege_type 
            FROM information_schema.table_privileges 
            WHERE grantee = current_user 
            AND table_schema = 'public'
            GROUP BY privilege_type
            ORDER BY privilege_type
        """)

        if privileges:
            print(f"✅ User '{db_config['user']}' has privileges:")
            for priv in privileges:
                print(f"   - {priv['privilege_type']}")
        else:
            print("⚠️  No specific table privileges found")

        # Test 7: Test write capability
        print("\n" + "-" * 70)
        print("TEST 7: Write Capability")
        print("-" * 70)

        await conn.execute("""
            CREATE TEMP TABLE test_write (
                id SERIAL PRIMARY KEY,
                test_data TEXT,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)
        print("✅ Created temporary table")

        await conn.execute("""
            INSERT INTO test_write (test_data) 
            VALUES ('Connection test successful')
        """)
        print("✅ Inserted test data")

        result = await conn.fetchval("""
            SELECT test_data FROM test_write LIMIT 1
        """)
        print(f"✅ Retrieved: {result}")

        await conn.execute("DROP TABLE test_write")
        print("✅ Dropped temporary table")

        await conn.close()
        print("\n✅ Connection closed")

        print("\n" + "=" * 70)
        print("✅ ALL TESTS PASSED")
        print("=" * 70)
        print("Database connection is working correctly!")
        print()

        return True

    except asyncpg.exceptions.InvalidPasswordError:
        print("❌ ERROR: Invalid password")
        return False

    except asyncpg.exceptions.InvalidCatalogNameError:
        print(f"❌ ERROR: Database '{db_config['database']}' does not exist")
        print("\nTo create the database, run:")
        print(f"  createdb -h {db_config['host']} -p {db_config['port']} "
              f"-U {db_config['user']} {db_config['database']}")
        return False

    except asyncpg.exceptions.CannotConnectNowError:
        print("❌ ERROR: Cannot connect to database server")
        print("Check if PostgreSQL service is running")
        return False

    except ConnectionRefusedError:
        print(f"❌ ERROR: Connection refused to {db_config['host']}:{db_config['port']}")
        print("Check if PostgreSQL is running and accepting connections")
        return False

    except asyncio.TimeoutError:
        print("❌ ERROR: Connection timeout")
        print("Check network connectivity and firewall settings")
        return False

    except Exception as e:
        print(f"❌ ERROR: {type(e).__name__}: {e}")
        return False


def main():
    config_path = Path(__file__).parent.parent / "config" / "config.yaml"

    if not config_path.exists():
        print(f"❌ Config file not found: {config_path}")
        print("\nRun this first:")
        print("  python scripts/create_production_config.py")
        sys.exit(1)

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
    except Exception as e:
        print(f"❌ Error loading config: {e}")
        sys.exit(1)

    success = asyncio.run(test_connection(config))

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
''',
}


def create_file(rel_path: str, content: str):
    """Create a file with given content"""
    full_path = BASE_PATH / rel_path
    full_path.parent.mkdir(parents=True, exist_ok=True)

    with open(full_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)

    print(f"✅ Created: {rel_path}")


def main():
    print("=" * 70)
    print("DEPLOYING CONFIG TOOLS")
    print("=" * 70)
    print()

    for rel_path, content in FILES.items():
        create_file(rel_path, content)

    print()
    print("=" * 70)
    print("✅ DEPLOYMENT COMPLETE")
    print("=" * 70)
    print()
    print("Files created:")
    print("  1. config/config.template.yaml")
    print("  2. scripts/create_production_config.py")
    print("  3. scripts/validate_config.py")
    print("  4. scripts/test_database_connection.py")
    print()
    print("Next steps:")
    print("  1. Run: python scripts/create_production_config.py")
    print("  2. Run: python scripts/validate_config.py")
    print("  3. Run: python scripts/test_database_connection.py")
    print()


if __name__ == "__main__":
    main()