#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Patch PostgresClient to accept dict config"""

from pathlib import Path

FILE = Path(__file__).parent.parent / 'src' / 'database' / 'postgres_client.py'

with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace _get_connection_params method
old_method = '''    def _get_connection_params(self) -> dict:
        """Get connection parameters from config"""
        # Try to get config from 'database.postgres' or 'postgresql'
        db_config = self.config.get('database.postgres', {})
        if not db_config:
            db_config = self.config.get('postgresql', {})

        params = {
            'host': db_config.get('host', 'localhost'),
            'port': db_config.get('port', 5432),
            'database': db_config.get('database', 'supplier_invoice_editor'),
            'user': db_config.get('user', 'postgres'),
            'password': db_config.get('password', '')
        }

        self.logger.info(f"Connection params: host={params['host']} port={params['port']} database={params['database']} user={params['user']}")

        return params'''

new_method = '''    def _get_connection_params(self) -> dict:
        """Get connection parameters from config"""
        # Check if config is already a connection dict (has 'host' key)
        if isinstance(self.config, dict) and 'host' in self.config:
            # Direct connection params
            params = {
                'host': self.config.get('host', 'localhost'),
                'port': self.config.get('port', 5432),
                'database': self.config.get('database', 'supplier_invoice_editor'),
                'user': self.config.get('user', 'postgres'),
                'password': self.config.get('password', '')
            }
        else:
            # Config object - try to get nested config
            db_config = self.config.get('database.postgres', {})
            if not db_config:
                db_config = self.config.get('postgresql', {})

            params = {
                'host': db_config.get('host', 'localhost'),
                'port': db_config.get('port', 5432),
                'database': db_config.get('database', 'supplier_invoice_editor'),
                'user': db_config.get('user', 'postgres'),
                'password': db_config.get('password', '')
            }

        self.logger.info(f"Connection params: host={params['host']} port={params['port']} database={params['database']} user={params['user']}")

        return params'''

content = content.replace(old_method, new_method)

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"OK Patched: {FILE}")
print("PostgresClient now accepts both Config object and direct dict")
print("\nTest again:")
print("  python scripts/test_pg8000_direct.py")
print("  python scripts/import_xml_to_staging.py C:\\NEX\\IMPORT\\32501215.xml")