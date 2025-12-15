# PostgreSQL Setup Guide

## 📋 Prerekvizity

1. **PostgreSQL Server** nainštalovaný a bežiaci
2. **psycopg2-binary** Python package (zatiaľ nie je nainštalovaný)

---

## 🐘 PostgreSQL Server Setup

### Windows Installation

1. **Download PostgreSQL**
   - https://www.postgresql.org/download/windows/
   - Odporúčaná verzia: PostgreSQL 15 alebo 16

2. **Install**
   - Spusti installer
   - Zapamätaj si **password** pre postgres user
   - Default port: **5432**

3. **Verify Installation**
   ```bash
   # Check if PostgreSQL is running
   pg_isready
   
   # Should output: accepting connections
   ```

---

## 🗄️ Database Setup

### 1. Create Database

Otvor **pgAdmin4** alebo **psql**:

```sql
-- Create database
CREATE DATABASE invoice_staging;

-- Create user (optional)
CREATE USER invoice_user WITH PASSWORD 'your_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE invoice_staging TO invoice_user;
```

### 2. Run Schema

```bash
cd C:\Development\supplier-invoice-editor

# Using psql
psql -U postgres -d invoice_staging -f database\schemas\001_initial_schema.sql

# Or use pgAdmin4 Query Tool and paste content from 001_initial_schema.sql
```

### 3. Verify Tables

```sql
-- Check tables
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public';

-- Expected: 6 tables
-- invoices_pending, invoice_items_pending, invoice_log,
-- categories_cache, products_staging, barcodes_staging
```

---

## 🐍 Python Package Installation

### Problem: psycopg2-binary Requires C++ Build Tools

**Current Status:** ❌ Not installed (requires Microsoft Visual C++ 14.0+)

### Solutions:

#### **Option A: Install Build Tools** (Recommended for Production)

1. Download: https://visualstudio.microsoft.com/visual-cpp-build-tools/
2. Install **"Desktop development with C++"**
3. Install package:
   ```bash
   pip install psycopg2-binary
   ```

#### **Option B: Use psycopg3** (Modern Alternative)

```bash
pip install psycopg[binary]
```

**Note:** psycopg3 has different API, requires code changes.

#### **Option C: Pre-compiled Wheel** (Unofficial)

Search for unofficial Windows wheels:
- https://www.lfd.uci.edu/~gohlke/pythonlibs/
- Download appropriate `.whl` file
- Install: `pip install downloaded_file.whl`

#### **Option D: Skip for Now** (Current Approach)

- ✅ PostgreSQL client interface is ready
- ✅ Will install psycopg2 when actually needed
- ✅ Can develop UI and Btrieve integration first

---

## ⚙️ Configuration

### Update config.yaml

```yaml
database:
  postgres:
    host: localhost
    port: 5432
    database: invoice_staging
    user: postgres
    password: ${ENV:POSTGRES_PASSWORD}
    
    # Connection Pool
    pool_size: 5
    max_overflow: 10
    connection_timeout: 10
```

### Set Environment Variable

```bash
# Windows CMD:
set POSTGRES_PASSWORD=your_password

# Windows PowerShell:
$env:POSTGRES_PASSWORD="your_password"

# Add to Windows Environment Variables permanently:
# System Properties → Advanced → Environment Variables → New
```

---

## ✅ Test Connection

### Test Script

Create `tests/test_postgres_connection.py`:

```python
# tests/test_postgres_connection.py
"""Test PostgreSQL connection"""

from src.utils import load_config
from src.database import create_postgres_client

def test_connection():
    """Test PostgreSQL connection"""
    try:
        # Load config
        config = load_config()
        pg_config = config.get_postgres_config()
        
        # Connect
        client = create_postgres_client(pg_config)
        
        # Test query
        result = client.fetch_one("SELECT version()")
        print(f"✅ Connected to PostgreSQL!")
        print(f"   Version: {result[0]}")
        
        # Test tables
        tables = client.fetch_all("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        
        print(f"\n✅ Found {len(tables)} tables:")
        for (table_name,) in tables:
            print(f"   - {table_name}")
        
        # Close
        client.close()
        print("\n✅ Connection test passed!")
        
    except ImportError as e:
        print(f"⚠️  psycopg2 not installed: {e}")
        print("   Install: pip install psycopg2-binary")
        print("   Or follow POSTGRESQL_SETUP.md")
        
    except Exception as e:
        print(f"❌ Connection test failed: {e}")

if __name__ == "__main__":
    test_connection()
```

### Run Test

```bash
# After installing psycopg2:
python tests\test_postgres_connection.py
```

---

## 📚 Usage Examples

### Basic Queries

```python
from src.database import create_postgres_client
from src.utils import load_config

# Load config
config = load_config()
pg_config = config.get_postgres_config()

# Connect
client = create_postgres_client(pg_config)

# Fetch all pending invoices
invoices = client.fetch_all(
    "SELECT * FROM invoices_pending WHERE status = %s",
    ("pending",)
)

# Fetch as dictionaries
invoices = client.fetch_dict(
    "SELECT id, invoice_number, total_amount FROM invoices_pending"
)

# Close
client.close()
```

### Insert Data

```python
# Insert invoice
invoice_id = client.insert('invoices_pending', {
    'supplier_ico': '12345678',
    'supplier_name': 'Test Supplier s.r.o.',
    'invoice_number': 'FAV-2025-001',
    'invoice_date': '2025-11-12',
    'currency': 'EUR',
    'total_amount': 1200.00,
    'status': 'pending'
})

print(f"Inserted invoice ID: {invoice_id}")
```

### Update Data

```python
# Approve invoice
affected = client.update(
    'invoices_pending',
    {
        'status': 'approved',
        'approved_by': 'operator1',
        'approved_at': datetime.now()
    },
    'id = %s',
    (invoice_id,)
)

print(f"Updated {affected} rows")
```

### Transactions

```python
# Using context manager (recommended)
with client.transaction():
    # Update invoice
    client.update('invoices_pending', {...}, 'id = %s', (1,))
    
    # Log action
    client.insert('invoice_log', {
        'invoice_id': 1,
        'action': 'APPROVED',
        'user_name': 'operator1'
    })
    # Auto-commit on exit

# Manual transaction
client.begin_transaction()
try:
    client.execute_query("UPDATE ...")
    client.execute_query("INSERT ...")
    client.commit()
except Exception as e:
    client.rollback()
    raise
```

### Context Manager

```python
# Automatic connection/close
with PostgresClient(pg_config) as client:
    invoices = client.fetch_all("SELECT * FROM invoices_pending")
    # Auto-close on exit
```

---

## 🔒 Security Best Practices

1. **Never commit passwords** to Git
   - Use environment variables: `${ENV:POSTGRES_PASSWORD}`
   - Or use `.env` file (add to `.gitignore`)

2. **Use connection pooling**
   - Already configured in PostgresClient
   - Default: 5 connections, max 15

3. **Always use parameterized queries**
   - ✅ `client.fetch_all("SELECT * WHERE id = %s", (123,))`
   - ❌ `client.fetch_all(f"SELECT * WHERE id = {user_input}")`  # SQL injection!

4. **Close connections**
   - Use `with` statement or `try/finally`
   - Pool handles cleanup automatically

---

## 🐛 Troubleshooting

### Error: "psycopg2 is not installed"

```
ImportError: psycopg2-binary is not installed
```

**Solution:** Install psycopg2 (see Options A-D above)

### Error: "could not connect to server"

```
psycopg2.OperationalError: could not connect to server
```

**Check:**
1. PostgreSQL server is running: `pg_isready`
2. Correct host/port in config.yaml
3. Firewall allows connection
4. Password is correct

### Error: "password authentication failed"

```
psycopg2.OperationalError: password authentication failed for user "postgres"
```

**Solution:**
1. Check password in config.yaml
2. Verify POSTGRES_PASSWORD environment variable
3. Test with psql: `psql -U postgres -d invoice_staging`

### Error: "database does not exist"

```
psycopg2.OperationalError: database "invoice_staging" does not exist
```

**Solution:** Create database (see Database Setup section)

---

## 📊 Next Steps

1. ✅ PostgreSQL client interface created
2. ⏳ Install psycopg2 when needed
3. ⏳ Create database
4. ⏳ Run schema
5. ⏳ Test connection
6. ⏳ Integrate with UI

**Current Status:** Ready to use, pending psycopg2 installation