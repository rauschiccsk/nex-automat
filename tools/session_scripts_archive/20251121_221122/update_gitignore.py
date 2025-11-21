#!/usr/bin/env python3
"""
Update .gitignore to exclude production configuration
"""

from pathlib import Path

BASE_PATH = Path(r"C:\Development\nex-automat")
GITIGNORE_PATH = BASE_PATH / ".gitignore"

GITIGNORE_ENTRIES = """
# Production Configuration (NEVER commit these files!)
config/config.yaml
config/.env
config/*.key
config/*.secret

# Backup files
backups/
*.backup
*.bak

# Log files
logs/
*.log

# Temporary files
temp/
*.tmp

# Storage directories (contain sensitive data)
storage/

# IDE and editor files
.vscode/
.idea/
*.swp
*.swo
*~

# Python cache
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.so
*.egg
*.egg-info/
dist/
build/

# Virtual environments
venv/
venv32/
env/
ENV/

# OS files
.DS_Store
Thumbs.db
desktop.ini

# Database files
*.db
*.sqlite
*.sqlite3

# Certificates and keys
*.pem
*.key
*.crt
*.cer
*.p12
*.pfx
"""


def update_gitignore():
    """Update .gitignore with production config exclusions"""
    print("=" * 70)
    print("UPDATING .gitignore")
    print("=" * 70)
    print()

    # Read existing .gitignore if it exists
    existing_content = ""
    if GITIGNORE_PATH.exists():
        with open(GITIGNORE_PATH, 'r', encoding='utf-8') as f:
            existing_content = f.read()
        print(f"✅ Found existing .gitignore")
    else:
        print("⚠️  No existing .gitignore found, creating new one")

    # Check if entries already exist
    if "config/config.yaml" in existing_content:
        print("âœ… Production config entries already in .gitignore")
        return

    # Append new entries
    with open(GITIGNORE_PATH, 'a', encoding='utf-8', newline='\n') as f:
        if existing_content and not existing_content.endswith('\n'):
            f.write('\n')
        f.write(GITIGNORE_ENTRIES)

    print("✅ Updated .gitignore with production config exclusions")
    print()
    print("=" * 70)
    print("âœ… GITIGNORE UPDATE COMPLETE")
    print("=" * 70)
    print()
    print("Next step: Verify with 'git status' that config.yaml is ignored")
    print()


if __name__ == "__main__":
    update_gitignore()