"""
Script 19: Extract Troubleshooting Guide Template
Creates generic template + archives Mágerstav-specific version
"""

import os
import shutil
from pathlib import Path


def create_generic_template():
    """Create generic Troubleshooting Guide template"""
    template = """# Troubleshooting Guide - NEX Automat

Common issues and their solutions for NEX Automat.

---

## Service Issues

### Service Won't Start

**Symptoms:**
- Service status shows STOPPED
- Cannot access API at localhost:8000
- Error in service-stderr.log

**Diagnostic Steps:**

1. Check service status: `python scripts\\manage_service.py status`
2. Review error logs: `Get-Content logs\\service-stderr.log -Tail 50`
3. Check for port conflicts: `netstat -ano | findstr :8000`

**Solutions:**

**Port 8000 already in use:**
```powershell
# Find and kill process using port 8000
$pid = (netstat -ano | findstr :8000 | Select-Object -First 1) -replace '\\s+', ' ' | ForEach-Object { ($_ -split ' ')[-1] }
taskkill /F /PID $pid
python scripts\\manage_service.py start
```

**Configuration error:**
```powershell
python scripts\\validate_config.py
# Fix any errors reported
python scripts\\manage_service.py start
```

**Missing dependencies:**
```powershell
cd C:\\Deployment\\nex-automat
venv32\\Scripts\\activate
pip install -r apps\\supplier-invoice-loader\\requirements.txt
python scripts\\manage_service.py start
```

---

### Service Crashes Repeatedly

**Symptoms:**
- Service starts then stops immediately
- Multiple crash entries in logs
- Auto-restart not working

**Diagnostic Steps:**

1. Check crash logs: `Get-Content logs\\service-stderr.log -Tail 100`
2. Look for Python errors: `Get-Content logs\\service-stderr.log | Select-String "Traceback"`
3. Test manual start

**Common Causes:**

**Unicode errors in code:**
```powershell
python scripts\\fix_all_print_statements.py
python scripts\\manage_service.py restart
```

**Import errors:**
```powershell
cd C:\\Deployment\\nex-automat
venv32\\Scripts\\activate
pip install -e packages\\nex-shared
pip install -e packages\\nexdata
python scripts\\manage_service.py restart
```

---

## Database Issues

### Cannot Connect to PostgreSQL

**Symptoms:**
- Error: "could not connect to server"
- Service fails to start
- Database tests fail

**Diagnostic Steps:**

1. Check PostgreSQL service: `Get-Service postgresql*`
2. Test connection: `python scripts\\test_database_connection.py`
3. Check password: `$env:POSTGRES_PASSWORD`

**Solutions:**

**PostgreSQL not running:**
```powershell
Start-Service postgresql-x64-15
Get-Service postgresql* | Select-Object Status
```

**Wrong password:**
```powershell
setx POSTGRES_PASSWORD "correct_password"
# Restart PowerShell
python scripts\\manage_service.py restart
```

**Database doesn't exist:**
```powershell
psql -U postgres -c "CREATE DATABASE invoice_staging;"
cd C:\\Deployment\\nex-automat\\apps\\supplier-invoice-loader
..\\..\\venv32\\Scripts\\python.exe -m database.migrations
```

---

### Slow Database Queries

**Symptoms:**
- API response time > 1 second
- High CPU usage by PostgreSQL
- Timeout errors

**Solutions:**

**Missing indexes:**
```sql
psql -U postgres -d invoice_staging

-- Check indexes
\\di

-- Create missing indexes if needed
CREATE INDEX IF NOT EXISTS idx_invoices_supplier ON invoices(supplier_id);
CREATE INDEX IF NOT EXISTS idx_invoice_lines_invoice ON invoice_lines(invoice_id);
```

---

## API Issues

### API Not Responding

**Symptoms:**
- Cannot access http://localhost:8000
- Timeout errors
- Connection refused

**Solutions:**

**Service not running:**
```powershell
python scripts\\manage_service.py start
Start-Sleep -Seconds 5
Invoke-WebRequest -Uri http://localhost:8000/health
```

**Firewall blocking:**
```powershell
New-NetFirewallRule -DisplayName "NEX Automat API" -Direction Inbound -LocalPort 8000 -Protocol TCP -Action Allow
```

---

### API Returns Errors

**Symptoms:**
- HTTP 500 errors
- "Internal Server Error"
- Unexpected responses

**Solutions:**

**Database connection error:**
```powershell
python scripts\\test_database_connection.py
# Fix database issues
python scripts\\manage_service.py restart
```

**Configuration error:**
```powershell
python scripts\\validate_config.py
# Fix config
python scripts\\manage_service.py restart
```

---

## File Processing Issues

### Files Not Being Processed

**Symptoms:**
- Files remain in C:\\NEX\\IMPORT\\xml\\
- No entries in database
- No errors in logs

**Solutions:**

**File watcher not running:**
```powershell
python scripts\\manage_service.py restart
python scripts\\manage_service.py logs | Select-String "Watching"
```

**Invalid XML:**
```powershell
Move-Item C:\\NEX\\IMPORT\\xml\\*.xml C:\\NEX\\IMPORT\\error\\
```

---

### Files Stuck in Error Folder

**Symptoms:**
- Files in C:\\NEX\\IMPORT\\error\\
- Error entries in logs
- Processing failed

**Solutions:**

**Fix file and retry:**
```powershell
# Fix the file
# Move back to xml folder
Move-Item C:\\NEX\\IMPORT\\error\\fixed-file.xml C:\\NEX\\IMPORT\\xml\\
```

---

## Performance Issues

### High Memory Usage

**Symptoms:**
- Service using >500 MB RAM
- System slowdown
- Out of memory errors

**Solutions:**

**Memory leak:**
```powershell
python scripts\\manage_service.py restart
```

**Too many concurrent operations:**
```yaml
# Edit config.yaml
processing:
  max_workers: 2  # Reduce from 4
```

---

### High CPU Usage

**Symptoms:**
- CPU usage constantly >50%
- System slowdown
- Service unresponsive

**Solutions:**

**Reduce processing load:**
```yaml
# Edit config.yaml
processing:
  batch_size: 5  # Reduce from 10
  interval_seconds: 10  # Increase from 5
```

---

## Common Error Messages

### "Unicode error in output"

**Cause:** Emoji or special characters in console output

**Solution:**
```powershell
python scripts\\fix_all_print_statements.py
python scripts\\manage_service.py restart
```

---

### "Database connection pool exhausted"

**Cause:** Too many concurrent database connections

**Solution:**
```yaml
# Edit config.yaml
database:
  postgres:
    pool_size: 20  # Increase from 10
```

---

### "Port 8000 already in use"

**Cause:** Another process using port 8000

**Solution:**
```powershell
$pid = (netstat -ano | findstr :8000) -replace '\\s+', ' ' | ForEach-Object { ($_ -split ' ')[-1] }
taskkill /F /PID $pid
python scripts\\manage_service.py start
```

---

## Getting Help

### Collect Diagnostic Information

```powershell
# Service status
python scripts\\manage_service.py status > diagnostic.txt

# Recent logs
python scripts\\manage_service.py logs >> diagnostic.txt

# Configuration
Get-Content apps\\supplier-invoice-loader\\config\\config.yaml >> diagnostic.txt

# System info
Get-ComputerInfo >> diagnostic.txt
```

### Contact Support

**Email:** [SUPPORT_EMAIL]  
**Include:**
- diagnostic.txt
- Description of issue
- Steps to reproduce
- Recent changes

---

**Document Version:** 1.0  
**Last Updated:** [YYYY-MM-DD]
"""
    return template


def extract_and_archive():
    """Extract template and archive Mágerstav version"""

    repo_root = Path(r"C:\Development\nex-automat")
    old_file = repo_root / "docs" / "deployment" / "TROUBLESHOOTING.md-old"
    template_file = repo_root / "docs" / "deployment" / "TROUBLESHOOTING.md"
    archive_dir = repo_root / "docs" / "archive" / "deployments"
    archive_file = archive_dir / "TROUBLESHOOTING_MAGERSTAV_2025-11-21.md"
    archive_index = repo_root / "docs" / "archive" / "00_ARCHIVE_INDEX.md"
    doc_index = repo_root / "docs" / "00_DOCUMENTATION_INDEX.md"

    print("🔄 Extracting Troubleshooting Guide Template...")
    print()

    # 1. Create generic template
    template = create_generic_template()
    with open(template_file, 'w', encoding='utf-8') as f:
        f.write(template)
    print(f"✅ Created: {template_file.relative_to(repo_root)}")
    print("   Generic Troubleshooting Guide template")
    print()

    # 2. Archive Mágerstav-specific version
    if old_file.exists():
        shutil.move(str(old_file), str(archive_file))
        print(f"✅ Archived: {old_file.name}")
        print(f"   → {archive_file.relative_to(repo_root)}")
    else:
        print(f"❌ Not found: {old_file}")
        return

    print()

    # 3. Update archive index
    if archive_index.exists():
        with open(archive_index, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find Deployment Records section and add entry
        if "## Deployment Records" in content:
            lines = content.split('\n')
            # Find recovery procedures entry and add after it
            insert_idx = None
            for i, line in enumerate(lines):
                if "Recovery Procedures" in line and "2025-11-24" in line:
                    insert_idx = i + 1
                    break

            if insert_idx:
                new_entry = "- **2025-11-21** - [Mágerstav Troubleshooting Guide](deployments/TROUBLESHOOTING_MAGERSTAV_2025-11-21.md) - Common issues and solutions"
                lines.insert(insert_idx, new_entry)
                content = '\n'.join(lines)

        with open(archive_index, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✅ Updated: {archive_index.relative_to(repo_root)}")
        print("   Added troubleshooting guide entry")

    # 4. Update documentation index
    if doc_index.exists():
        with open(doc_index, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find Deployment section and add entry
        deployment_section = "## 📦 Deployment"

        if deployment_section in content:
            lines = content.split('\n')
            insert_idx = None

            # Find RECOVERY_GUIDE entry and add after it
            for i, line in enumerate(lines):
                if "Recovery Guide" in line:
                    insert_idx = i + 1
                    break

            if insert_idx:
                new_entry = "- [Troubleshooting Guide](deployment/TROUBLESHOOTING.md) - Common issues and solutions"
                lines.insert(insert_idx, new_entry)
                content = '\n'.join(lines)

        with open(doc_index, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✅ Updated: {doc_index.relative_to(repo_root)}")
        print("   Added TROUBLESHOOTING.md to deployment section")

    print()
    print("=" * 60)
    print("✅ MIGRATION COMPLETE")
    print("=" * 60)
    print()
    print("Summary:")
    print(f"  • Created: docs/deployment/TROUBLESHOOTING.md (template)")
    print(f"  • Archived: TROUBLESHOOTING_MAGERSTAV_2025-11-21.md")
    print(f"  • Updated: Archive index + Documentation index")
    print()


if __name__ == "__main__":
    extract_and_archive()