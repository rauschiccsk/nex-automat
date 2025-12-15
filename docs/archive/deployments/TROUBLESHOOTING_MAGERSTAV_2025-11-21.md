# Troubleshooting Guide - NEX Automat

Common issues and their solutions for NEX Automat v2.0.

---

## Service Issues

### Service Won't Start

**Symptoms:**

- Service status shows STOPPED
- Cannot access API at localhost:8000
- Error in service-stderr.log

**Diagnostic Steps:**

1. **Check service status:**
   
   ```powershell
   python scripts\manage_service.py status
   ```

2. **Review error logs:**
   
   ```powershell
   Get-Content logs\service-stderr.log -Tail 50
   ```

3. **Check for port conflicts:**
   
   ```powershell
   netstat -ano | findstr :8000
   ```

**Solutions:**

**Port 8000 already in use:**

```powershell
# Find process using port 8000
$pid = (netstat -ano | findstr :8000 | Select-Object -First 1) -replace '\s+', ' ' | ForEach-Object { ($_ -split ' ')[-1] }

# Kill the process
taskkill /F /PID $pid

# Start service
python scripts\manage_service.py start
```

**Configuration error:**

```powershell
# Validate configuration
python scripts\validate_config.py

# Fix any errors reported
# Then restart
python scripts\manage_service.py start
```

**Missing dependencies:**

```powershell
cd C:\Deployment\nex-automat
venv32\Scripts\activate
pip install -r apps\supplier-invoice-loader\requirements.txt
python scripts\manage_service.py start
```

---

### Service Crashes Repeatedly

**Symptoms:**

- Service starts then stops immediately
- Multiple crash entries in logs
- Auto-restart not working

**Diagnostic Steps:**

1. **Check crash logs:**
   
   ```powershell
   Get-Content logs\service-stderr.log -Tail 100
   ```

2. **Look for Python errors:**
   
   ```powershell
   Get-Content logs\service-stderr.log | Select-String "Traceback"
   ```

3. **Test manual start:**
   
   ```powershell
   cd C:\Deployment\nex-automat
   venv32\Scripts\activate
   python apps\supplier-invoice-loader\main.py
   ```

**Common Causes:**

**Unicode errors in code:**

```powershell
# Fix Unicode issues
python scripts\fix_all_print_statements.py

# Verify
Get-Content apps\supplier-invoice-loader\main.py | Select-String -Pattern "\\U[0-9a-fA-F]{8}"

# Should return nothing
python scripts\manage_service.py restart
```

**Import errors:**

```powershell
# Reinstall packages
cd C:\Deployment\nex-automat
venv32\Scripts\activate
pip install -e packages\invoice-shared
pip install -e packages\nex-shared
python scripts\manage_service.py restart
```

---

## Database Issues

### Cannot Connect to PostgreSQL

**Symptoms:**

- Error: "could not connect to server"
- Service fails to start
- Database tests fail

**Diagnostic Steps:**

1. **Check PostgreSQL service:**
   
   ```powershell
   Get-Service postgresql*
   ```

2. **Test connection:**
   
   ```powershell
   python scripts\test_database_connection.py
   ```

3. **Check password:**
   
   ```powershell
   $env:POSTGRES_PASSWORD
   # Should display password
   ```

**Solutions:**

**PostgreSQL not running:**

```powershell
Start-Service postgresql-x64-15
Get-Service postgresql* | Select-Object Status
```

**Wrong password:**

```powershell
# Set correct password
setx POSTGRES_PASSWORD "correct_password"

# Restart PowerShell
# Then restart service
python scripts\manage_service.py restart
```

**Database doesn't exist:**

```powershell
psql -U postgres -c "CREATE DATABASE invoice_staging;"
cd C:\Deployment\nex-automat\apps\supplier-invoice-loader
..\..\venv32\Scripts\python.exe -m database.migrations
```

---

### Slow Database Queries

**Symptoms:**

- API response time > 1 second
- High CPU usage by PostgreSQL
- Timeout errors

**Diagnostic Steps:**

1. **Test query performance:**
   
   ```powershell
   python scripts\performance_tests.py
   ```

2. **Check database size:**
   
   ```powershell
   psql -U postgres -d invoice_staging -c "SELECT pg_size_pretty(pg_database_size('invoice_staging'));"
   ```

**Solutions:**

**Missing indexes:**

```sql
psql -U postgres -d invoice_staging

-- Check indexes
\di

-- Create missing indexes if needed
CREATE INDEX IF NOT EXISTS idx_invoices_supplier ON invoices(supplier_id);
CREATE INDEX IF NOT EXISTS idx_invoice_lines_invoice ON invoice_lines(invoice_id);
```

**Too much data:**

```powershell
# Archive old data
python scripts\archive_old_data.py --days 90
```

---

## API Issues

### API Not Responding

**Symptoms:**

- Cannot access http://localhost:8000
- Timeout errors
- Connection refused

**Diagnostic Steps:**

1. **Check if service running:**
   
   ```powershell
   python scripts\manage_service.py status
   ```

2. **Test API:**
   
   ```powershell
   Invoke-WebRequest -Uri http://localhost:8000/health
   ```

3. **Check port:**
   
   ```powershell
   netstat -ano | findstr :8000
   ```

**Solutions:**

**Service not running:**

```powershell
python scripts\manage_service.py start
Start-Sleep -Seconds 5
Invoke-WebRequest -Uri http://localhost:8000/health
```

**Firewall blocking:**

```powershell
# Add firewall rule
New-NetFirewallRule -DisplayName "NEX Automat API" -Direction Inbound -LocalPort 8000 -Protocol TCP -Action Allow
```

---

### API Returns Errors

**Symptoms:**

- HTTP 500 errors
- "Internal Server Error"
- Unexpected responses

**Diagnostic Steps:**

1. **Check application logs:**
   
   ```powershell
   python scripts\manage_service.py logs | Select-String "ERROR"
   ```

2. **Test specific endpoint:**
   
   ```powershell
   Invoke-WebRequest -Uri http://localhost:8000/api/invoices
   ```

**Solutions:**

**Database connection error:**

```powershell
python scripts\test_database_connection.py
# Fix database issues
python scripts\manage_service.py restart
```

**Configuration error:**

```powershell
python scripts\validate_config.py
# Fix config
python scripts\manage_service.py restart
```

---

## File Processing Issues

### Files Not Being Processed

**Symptoms:**

- Files remain in C:\NEX\IMPORT\xml\
- No entries in database
- No errors in logs

**Diagnostic Steps:**

1. **Check file permissions:**
   
   ```powershell
   icacls C:\NEX\IMPORT\xml\
   ```

2. **Check file format:**
   
   ```powershell
   Get-Content C:\NEX\IMPORT\xml\test-file.xml -Head 10
   ```

3. **Check logs:**
   
   ```powershell
   python scripts\manage_service.py logs | Select-String "Processing"
   ```

**Solutions:**

**File watcher not running:**

```powershell
python scripts\manage_service.py restart
python scripts\manage_service.py logs | Select-String "Watching"
```

**Invalid XML:**

```powershell
# Move invalid files to error folder
Move-Item C:\NEX\IMPORT\xml\*.xml C:\NEX\IMPORT\error\
```

---

### Files Stuck in Error Folder

**Symptoms:**

- Files in C:\NEX\IMPORT\error\
- Error entries in logs
- Processing failed

**Diagnostic Steps:**

1. **Check error reason:**
   
   ```powershell
   python scripts\manage_service.py logs | Select-String "error" -Context 2
   ```

2. **Examine error file:**
   
   ```powershell
   Get-Content C:\NEX\IMPORT\error\*.xml
   ```

**Solutions:**

**Fix file and retry:**

```powershell
# Fix the file
# Move back to xml folder
Move-Item C:\NEX\IMPORT\error\fixed-file.xml C:\NEX\IMPORT\xml\
```

---

## Performance Issues

### High Memory Usage

**Symptoms:**

- Service using >500 MB RAM
- System slowdown
- Out of memory errors

**Diagnostic Steps:**

1. **Check memory:**
   
   ```powershell
   python scripts\manage_service.py status
   ```

2. **Review logs for leaks:**
   
   ```powershell
   python scripts\manage_service.py logs | Select-String "memory"
   ```

**Solutions:**

**Memory leak:**

```powershell
# Restart service
python scripts\manage_service.py restart
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

**Diagnostic Steps:**

1. **Check CPU:**
   
   ```powershell
   Get-Process | Where-Object {$_.ProcessName -like "*python*"} | Select-Object Name,CPU,WorkingSet
   ```

2. **Review active operations:**
   
   ```powershell
   python scripts\manage_service.py logs | Select-String "Processing"
   ```

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
python scripts\fix_all_print_statements.py
python scripts\manage_service.py restart
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
# Find and kill process
$pid = (netstat -ano | findstr :8000) -replace '\s+', ' ' | ForEach-Object { ($_ -split ' ')[-1] }
taskkill /F /PID $pid
python scripts\manage_service.py start
```

---

## Getting Help

### Collect Diagnostic Information

```powershell
# Service status
python scripts\manage_service.py status > diagnostic.txt

# Recent logs
python scripts\manage_service.py logs >> diagnostic.txt

# Configuration
Get-Content apps\supplier-invoice-loader\config\config.yaml >> diagnostic.txt

# System info
Get-ComputerInfo >> diagnostic.txt
```

### Contact Support

**Email:** zoltan.rausch@icc.sk  
**Include:**

- diagnostic.txt
- Description of issue
- Steps to reproduce
- Recent changes

---

**Document Version:** 1.0  
**Last Updated:** 2025-11-21  
**Next Review:** 2025-12-21
