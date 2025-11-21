\# Troubleshooting Guide - NEX Automat



Quick reference for diagnosing and fixing common issues.



---



\## Quick Diagnostics



\### Run Full Diagnostic



```powershell

cd C:\\Deployment\\nex-automat

venv32\\Scripts\\activate



\# 1. Service status

python scripts\\manage\_service.py status



\# 2. Database connection

python scripts\\test\_database\_connection.py



\# 3. Configuration validation

python scripts\\validate\_config.py



\# 4. Check logs

python scripts\\manage\_service.py logs



\# 5. API health

Invoke-WebRequest -Uri http://localhost:8000/health

```



---



\## Common Issues



\### 1. Service Won't Start



\#### Symptom

```

❌ Failed to start service

Error: NEX-Automat-Loader: START: ...

```



\#### Possible Causes \& Solutions



\*\*A. PostgreSQL Not Running\*\*

```powershell

\# Check PostgreSQL status

Get-Service postgresql\*



\# If stopped, start it

Start-Service postgresql-x64-15

```



\*\*B. Port 8000 Already in Use\*\*

```powershell

\# Check what's using port 8000

netstat -ano | findstr :8000



\# Kill the process

taskkill /F /PID <PID>



\# Start service again

python scripts\\manage\_service.py start

```



\*\*C. POSTGRES\_PASSWORD Not Set\*\*

```powershell

\# Check environment variable

$env:POSTGRES\_PASSWORD



\# If empty, set it

$env:POSTGRES\_PASSWORD = "your\_password"

setx POSTGRES\_PASSWORD "your\_password"

```



\*\*D. Configuration Invalid\*\*

```powershell

\# Validate config

python scripts\\validate\_config.py



\# Fix errors in config.yaml

notepad apps\\supplier-invoice-loader\\config\\config.yaml

```



\*\*E. Storage Directories Missing\*\*

```powershell

\# Check directories exist

Test-Path C:\\NEX\\IMPORT\\pdf

Test-Path C:\\NEX\\IMPORT\\xml



\# Create if missing

New-Item -ItemType Directory -Path C:\\NEX\\IMPORT\\pdf -Force

New-Item -ItemType Directory -Path C:\\NEX\\IMPORT\\xml -Force

```



---



\### 2. Unicode Encoding Errors



\#### Symptom

```

UnicodeEncodeError: 'charmap' codec can't encode character '\\U0001f680'

```



\#### Solution

```powershell

\# Stop service

python scripts\\manage\_service.py stop



\# Fix all Unicode issues

python scripts\\fix\_all\_print\_statements.py



\# Start service

python scripts\\manage\_service.py start

```



\*\*Prevention:\*\*

\- Never use emoji in print() statements

\- Use only ASCII characters in console output

\- Test code before deploying to Windows Service



---



\### 3. Service Stuck in PAUSED State



\#### Symptom

```

Status: ⚠️  SERVICE\_PAUSED

```



\#### Solution

```powershell

\# Force stop

C:\\Deployment\\nex-automat\\tools\\nssm\\win32\\nssm.exe stop NEX-Automat-Loader



\# Kill any remaining processes

Get-Process python\* | Where-Object {$\_.Path -like "\*nex-automat\*"} | Stop-Process -Force



\# Wait

Start-Sleep -Seconds 3



\# Start again

C:\\Deployment\\nex-automat\\tools\\nssm\\win32\\nssm.exe start NEX-Automat-Loader

```



---



\### 4. Database Connection Failed



\#### Symptom

```

ERROR: Database connection failed

psycopg2.OperationalError: could not connect to server

```



\#### Diagnosis

```powershell

\# Test PostgreSQL connection

python scripts\\test\_database\_connection.py

```



\#### Solutions



\*\*A. PostgreSQL Not Running\*\*

```powershell

Get-Service postgresql\*

Start-Service postgresql-x64-15

```



\*\*B. Wrong Password\*\*

```powershell

\# Check password environment variable

$env:POSTGRES\_PASSWORD



\# Update if wrong

setx POSTGRES\_PASSWORD "correct\_password"



\# Restart service

python scripts\\manage\_service.py restart

```



\*\*C. Database Doesn't Exist\*\*

```powershell

\# Create database

psql -U postgres -c "CREATE DATABASE invoice\_staging;"



\# Run migrations

cd apps\\supplier-invoice-loader

python -m database.migrations

```



\*\*D. Connection Refused\*\*

```powershell

\# Check PostgreSQL listening on port 5432

netstat -ano | findstr :5432



\# Check pg\_hba.conf allows local connections

\# Edit: C:\\Program Files\\PostgreSQL\\15\\data\\pg\_hba.conf

```



---



\### 5. API Not Responding



\#### Symptom

```

Invoke-WebRequest : Unable to connect to the remote server

```



\#### Diagnosis

```powershell

\# 1. Check service status

python scripts\\manage\_service.py status



\# 2. Check if port is listening

netstat -ano | findstr :8000



\# 3. Check logs

python scripts\\manage\_service.py logs

```



\#### Solutions



\*\*A. Service Not Running\*\*

```powershell

python scripts\\manage\_service.py start

```



\*\*B. Port Blocked by Firewall\*\*

```powershell

\# Add firewall rule

New-NetFirewallRule -DisplayName "NEX Automat API" -Direction Inbound -LocalPort 8000 -Protocol TCP -Action Allow

```



\*\*C. Application Crashed\*\*

```powershell

\# Check stderr log

type logs\\service-stderr.log



\# Look for Python tracebacks

\# Fix the underlying issue

\# Restart service

```



---



\### 6. High Memory Usage



\#### Symptom

Service consuming excessive memory (>500 MB)



\#### Diagnosis

```powershell

\# Check memory usage

Get-Process python\* | Where-Object {$\_.Path -like "\*nex-automat\*"} | Select-Object Name,PM,WS

```



\#### Solutions



\*\*A. Memory Leak in Application\*\*

```powershell

\# Schedule regular restarts (temporary fix)

\# Add to Task Scheduler - restart service daily at 3 AM



\# Long-term: Review code for memory leaks

\# - Database connections not closed

\# - Large objects not released

\# - Circular references

```



\*\*B. Database Connection Pool Exhaustion\*\*

```powershell

\# Check configuration

type apps\\supplier-invoice-loader\\config\\config.yaml



\# Reduce pool size if too high

\# Update: max\_pool\_size in config

```



---



\### 7. Log Files Growing Too Large



\#### Symptom

Disk space running out due to large log files



\#### Solutions



\*\*A. Enable Log Rotation\*\*

```powershell

\# Already configured via NSSM:

\# - Rotation: Daily

\# - Max size: 10 MB

\# - Should rotate automatically

```



\*\*B. Manually Clean Old Logs\*\*

```powershell

\# Delete logs older than 30 days

Get-ChildItem logs\\\*.log | Where-Object {$\_.LastWriteTime -lt (Get-Date).AddDays(-30)} | Remove-Item



\# Archive old logs

Compress-Archive -Path logs\\\*.log -DestinationPath "backups\\logs-$(Get-Date -Format 'yyyy-MM-dd').zip"

```



\*\*C. Reduce Log Verbosity\*\*

```powershell

\# Edit config.yaml

\# Change log level from DEBUG to INFO or WARNING

notepad apps\\supplier-invoice-loader\\config\\config.yaml

```



---



\### 8. Slow API Response



\#### Symptom

API requests taking >1 second to respond



\#### Diagnosis

```powershell

\# Test response time

Measure-Command { Invoke-WebRequest -Uri http://localhost:8000/health }

```



\#### Solutions



\*\*A. Database Query Optimization\*\*

```sql

-- Check slow queries in PostgreSQL

SELECT query, mean\_exec\_time 

FROM pg\_stat\_statements 

ORDER BY mean\_exec\_time DESC 

LIMIT 10;

```



\*\*B. Add Database Indexes\*\*

```sql

-- Add indexes to frequently queried columns

CREATE INDEX idx\_invoices\_date ON invoices(invoice\_date);

CREATE INDEX idx\_invoices\_supplier ON invoices(supplier\_id);

```



\*\*C. Increase Worker Processes\*\*

```yaml

\# Edit config.yaml

\# Increase uvicorn workers (if multi-core CPU)

workers: 2

```



---



\### 9. File Processing Errors



\#### Symptom

Invoices not being processed, files stuck in temp directory



\#### Diagnosis

```powershell

\# Check error directory

dir C:\\NEX\\IMPORT\\error\\



\# Check logs for file processing errors

Select-String -Path logs\\service-stdout.log -Pattern "ERROR"

```



\#### Solutions



\*\*A. Permission Issues\*\*

```powershell

\# Check directory permissions

icacls C:\\NEX\\IMPORT\\



\# Grant full control

icacls C:\\NEX\\IMPORT\\ /grant "NT AUTHORITY\\SYSTEM:(OI)(CI)F"

```



\*\*B. Invalid File Format\*\*

```powershell

\# Check error directory for details

type C:\\NEX\\IMPORT\\error\\error-YYYYMMDD.log



\# Move invalid files

Move-Item C:\\NEX\\IMPORT\\temp\\\*.\* C:\\NEX\\IMPORT\\error\\

```



\*\*C. Disk Space Full\*\*

```powershell

\# Check free space

Get-PSDrive C | Select-Object Used,Free



\# Clean up old files

Remove-Item C:\\NEX\\IMPORT\\archive\\\* -Recurse -Force -Confirm:$false

```



---



\### 10. NEX Genesis Integration Failed



\#### Symptom

```

ERROR: Failed to connect to NEX Genesis API

```



\#### Diagnosis

```powershell

\# Test NEX Genesis Server

curl http://localhost:8080/api/health



\# or

Invoke-WebRequest -Uri http://localhost:8080/api/health

```



\#### Solutions



\*\*A. NEX Genesis Not Running\*\*

```powershell

\# Start NEX Genesis Server

\# (method depends on your NEX setup)



\# Check if it's running

netstat -ano | findstr :8080

```



\*\*B. API Key Invalid\*\*

```powershell

\# Check config

type apps\\supplier-invoice-loader\\config\\config.yaml



\# Update API key if needed

notepad apps\\supplier-invoice-loader\\config\\config.yaml

```



\*\*C. Network/Firewall Issue\*\*

```powershell

\# Test connection

Test-NetConnection -ComputerName localhost -Port 8080



\# Add firewall rule if needed

New-NetFirewallRule -DisplayName "NEX Genesis" -Direction Inbound -LocalPort 8080 -Protocol TCP -Action Allow

```



---



\## Emergency Procedures



\### Complete System Reset



\*\*⚠️ Use only as last resort\*\*



```powershell

\# 1. Stop everything

python scripts\\manage\_service.py stop

Get-Process python\* | Stop-Process -Force



\# 2. Backup current state

Copy-Item -Recurse apps\\supplier-invoice-loader backups\\loader-$(Get-Date -Format 'yyyyMMdd')



\# 3. Remove and recreate service

C:\\Deployment\\nex-automat\\tools\\nssm\\win32\\nssm.exe remove NEX-Automat-Loader confirm

python scripts\\create\_windows\_service.py



\# 4. Validate everything

python scripts\\validate\_config.py

python scripts\\test\_database\_connection.py



\# 5. Start fresh

python scripts\\manage\_service.py start

python scripts\\manage\_service.py logs

```



---



\## Diagnostic Scripts



\### Create System Diagnostic Report



```powershell

\# Create diagnostic report

$report = @"

=== NEX Automat Diagnostic Report ===

Date: $(Get-Date)



=== Service Status ===

$(C:\\Deployment\\nex-automat\\tools\\nssm\\win32\\nssm.exe status NEX-Automat-Loader)



=== PostgreSQL Status ===

$(Get-Service postgresql\*)



=== Port 8000 Status ===

$(netstat -ano | findstr :8000)



=== Process Status ===

$(Get-Process python\* | Where-Object {$\_.Path -like "\*nex-automat\*"} | Format-Table)



=== Disk Space ===

$(Get-PSDrive C | Select-Object Used,Free | Format-Table)



=== Recent Errors ===

$(Get-Content logs\\service-stderr.log -Tail 20)



=== Configuration ===

$(type apps\\supplier-invoice-loader\\config\\config.yaml)

"@



$report | Out-File "diagnostic-report-$(Get-Date -Format 'yyyyMMdd-HHmmss').txt"

Write-Host "Diagnostic report saved"

```



---



\## Getting Help



\### Information to Provide



When contacting support, include:



1\. \*\*Diagnostic report\*\* (see above)

2\. \*\*Recent logs\*\* (last 100 lines)

3\. \*\*Steps to reproduce\*\* the issue

4\. \*\*Error messages\*\* (exact text)

5\. \*\*When it started\*\* (date/time)

6\. \*\*Recent changes\*\* (config, updates, etc.)



\### Collect Debug Information



```powershell

\# Create debug package

$debugPath = "debug-$(Get-Date -Format 'yyyyMMdd-HHmmss')"

New-Item -ItemType Directory -Path $debugPath



\# Copy logs

Copy-Item logs\\\*.log $debugPath\\



\# Copy config (redact passwords!)

Copy-Item apps\\supplier-invoice-loader\\config\\config.yaml $debugPath\\



\# Save diagnostic info

C:\\Deployment\\nex-automat\\tools\\nssm\\win32\\nssm.exe dump NEX-Automat-Loader > $debugPath\\service-config.txt



\# Create archive

Compress-Archive -Path $debugPath\\\* -DestinationPath "$debugPath.zip"



Write-Host "Debug package created: $debugPath.zip"

```



---



\## Preventive Maintenance



\### Daily Checks

```powershell

\# Automated daily check

python scripts\\manage\_service.py status

Invoke-WebRequest -Uri http://localhost:8000/health

```



\### Weekly Maintenance

```powershell

\# Review logs

python scripts\\manage\_service.py logs | Select-String -Pattern "ERROR|WARNING"



\# Check disk space

Get-PSDrive C | Select-Object Used,Free

```



\### Monthly Tasks

```powershell

\# Clean old logs

Get-ChildItem logs\\\*.log | Where-Object {$\_.LastWriteTime -lt (Get-Date).AddDays(-30)} | Remove-Item



\# Test backup/restore

\# (follow DEPLOYMENT\_GUIDE.md procedures)

```



---



\## Contact



\*\*Developer:\*\* Zoltán Rausch  

\*\*Company:\*\* ICC Komárno  

\*\*Email:\*\* zoltan.rausch@icc.sk



---



\*\*Last Updated:\*\* 2025-11-21  

\*\*Version:\*\* 1.0

