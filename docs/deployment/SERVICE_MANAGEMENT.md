\# Service Management Guide - NEX Automat



\*\*Service Name:\*\* NEX-Automat-Loader  

\*\*Display Name:\*\* NEX Automat - Supplier Invoice Loader  

\*\*Location:\*\* C:\\Deployment\\nex-automat



---



\## Quick Reference



\### Basic Commands



```powershell

\# Navigate to deployment directory

cd C:\\Deployment\\nex-automat

venv32\\Scripts\\activate



\# Check status

python scripts\\manage\_service.py status



\# Start service (requires Administrator)

python scripts\\manage\_service.py start



\# Stop service (requires Administrator)

python scripts\\manage\_service.py stop



\# Restart service (requires Administrator)

python scripts\\manage\_service.py restart



\# View logs

python scripts\\manage\_service.py logs



\# Monitor logs in real-time

python scripts\\manage\_service.py tail

```



\### Direct NSSM Commands



```powershell

\# Using NSSM directly (requires Administrator)

C:\\Deployment\\nex-automat\\tools\\nssm\\win32\\nssm.exe status NEX-Automat-Loader

C:\\Deployment\\nex-automat\\tools\\nssm\\win32\\nssm.exe start NEX-Automat-Loader

C:\\Deployment\\nex-automat\\tools\\nssm\\win32\\nssm.exe stop NEX-Automat-Loader

C:\\Deployment\\nex-automat\\tools\\nssm\\win32\\nssm.exe restart NEX-Automat-Loader

```



---



\## Service Operations



\### Starting the Service



\*\*Prerequisites:\*\*

\- PostgreSQL must be running

\- POSTGRES\_PASSWORD environment variable set

\- All storage directories exist



\*\*Method 1: Using manage\_service.py\*\*

```powershell

cd C:\\Deployment\\nex-automat

venv32\\Scripts\\activate

python scripts\\manage\_service.py start

```



\*\*Method 2: Using NSSM directly\*\*

```powershell

C:\\Deployment\\nex-automat\\tools\\nssm\\win32\\nssm.exe start NEX-Automat-Loader

```



\*\*Method 3: Using Windows Services\*\*

1\. Open Services (services.msc)

2\. Find "NEX Automat - Supplier Invoice Loader"

3\. Right-click → Start



\*\*Expected Output:\*\*

```

Starting service 'NEX-Automat-Loader'...

✅ Service started successfully

&nbsp;  Status: SERVICE\_RUNNING

```



\*\*Verification:\*\*

```powershell

\# Check API is responding

Invoke-WebRequest -Uri http://localhost:8000/health



\# Should return: {"status":"healthy","timestamp":"..."}

```



---



\### Stopping the Service



\*\*⚠️ IMPORTANT:\*\* Stop the service gracefully before:

\- Updating the application

\- Modifying configuration

\- Database maintenance

\- Server maintenance



\*\*Method 1: Using manage\_service.py\*\*

```powershell

python scripts\\manage\_service.py stop

```



\*\*Method 2: Using NSSM directly\*\*

```powershell

C:\\Deployment\\nex-automat\\tools\\nssm\\win32\\nssm.exe stop NEX-Automat-Loader

```



\*\*Expected Output:\*\*

```

Stopping service 'NEX-Automat-Loader'...

✅ Service stopped successfully

&nbsp;  Status: SERVICE\_STOPPED

```



---



\### Restarting the Service



\*\*When to restart:\*\*

\- After configuration changes

\- After code updates

\- To clear memory/connections

\- As part of troubleshooting



\*\*Command:\*\*

```powershell

python scripts\\manage\_service.py restart

```



\*\*What happens:\*\*

1\. Service stops gracefully

2\. Wait 2 seconds

3\. Service starts

4\. Status verification



---



\### Checking Service Status



\*\*Quick status check:\*\*

```powershell

python scripts\\manage\_service.py status

```



\*\*Possible statuses:\*\*

\- 🟢 \*\*SERVICE\_RUNNING\*\* - Service is running normally

\- 🔴 \*\*SERVICE\_STOPPED\*\* - Service is stopped

\- 🟡 \*\*SERVICE\_PAUSED\*\* - Service is paused (unusual)

\- ⚠️ \*\*ERROR\*\* - Service error occurred



\*\*Detailed status:\*\*

```powershell

\# Using NSSM

C:\\Deployment\\nex-automat\\tools\\nssm\\win32\\nssm.exe status NEX-Automat-Loader



\# Check process

Get-Process python\* | Where-Object {$\_.Path -like "\*nex-automat\*"}



\# Check port binding

netstat -ano | findstr :8000

```



---



\## Log Management



\### Viewing Logs



\*\*Recent logs (last 50 lines):\*\*

```powershell

python scripts\\manage\_service.py logs

```



\*\*Real-time monitoring:\*\*

```powershell

python scripts\\manage\_service.py tail

\# Press Ctrl+C to exit

```



\*\*View specific log file:\*\*

```powershell

\# Standard output

type logs\\service-stdout.log



\# Standard error

type logs\\service-stderr.log



\# Last 100 lines

Get-Content logs\\service-stdout.log -Tail 100

```



\### Log Files



\*\*Location:\*\* `C:\\Deployment\\nex-automat\\logs\\`



\*\*Files:\*\*

\- `service-stdout.log` - Application output

\- `service-stderr.log` - Errors and warnings

\- `app-YYYY-MM-DD.log` - Daily application logs (if configured)



\### Log Rotation



\*\*Configuration:\*\*

\- \*\*Rotation:\*\* Daily

\- \*\*Max size:\*\* 10 MB per file

\- \*\*Retention:\*\* Automatic (NSSM manages)



\*\*Manual rotation:\*\*

```powershell

\# Trigger log rotation

C:\\Deployment\\nex-automat\\tools\\nssm\\win32\\nssm.exe rotate NEX-Automat-Loader

```



---



\## Configuration Management



\### Viewing Current Configuration



```powershell

\# Application config

type apps\\supplier-invoice-loader\\config\\config.yaml



\# Service config (all parameters)

C:\\Deployment\\nex-automat\\tools\\nssm\\win32\\nssm.exe dump NEX-Automat-Loader

```



\### Modifying Configuration



\*\*⚠️ IMPORTANT:\*\* Always stop service before config changes!



```powershell

\# 1. Stop service

python scripts\\manage\_service.py stop



\# 2. Edit configuration

notepad apps\\supplier-invoice-loader\\config\\config.yaml



\# 3. Validate configuration

python scripts\\validate\_config.py



\# 4. Start service

python scripts\\manage\_service.py start

```



\### Service Parameters



\*\*View parameter:\*\*

```powershell

C:\\Deployment\\nex-automat\\tools\\nssm\\win32\\nssm.exe get NEX-Automat-Loader <parameter>

```



\*\*Set parameter:\*\*

```powershell

C:\\Deployment\\nex-automat\\tools\\nssm\\win32\\nssm.exe set NEX-Automat-Loader <parameter> <value>

```



\*\*Common parameters:\*\*

\- `AppDirectory` - Working directory

\- `AppRestartDelay` - Restart delay (milliseconds)

\- `AppStdout` - stdout log path

\- `AppStderr` - stderr log path

\- `Start` - Startup type



---



\## Auto-Restart Configuration



\*\*Current settings:\*\*

\- \*\*Restart on failure:\*\* YES

\- \*\*Restart delay:\*\* 0 seconds (immediate)

\- \*\*Exit code:\*\* Any (Default)



\*\*Verify auto-restart:\*\*

```powershell

C:\\Deployment\\nex-automat\\tools\\nssm\\win32\\nssm.exe get NEX-Automat-Loader AppExit Default

\# Should return: Restart



C:\\Deployment\\nex-automat\\tools\\nssm\\win32\\nssm.exe get NEX-Automat-Loader AppRestartDelay

\# Should return: 0

```



\*\*Test auto-restart:\*\*

```powershell

\# 1. Get current PID

netstat -ano | findstr :8000



\# 2. Kill process

taskkill /F /PID <PID>



\# 3. Wait 5 seconds

Start-Sleep -Seconds 5



\# 4. Verify service restarted

python scripts\\manage\_service.py status

Invoke-WebRequest -Uri http://localhost:8000/health

```



---



\## Troubleshooting



\### Service Won't Start



\*\*Check:\*\*

1\. PostgreSQL is running

2\. POSTGRES\_PASSWORD environment variable set

3\. Port 8000 is not in use

4\. All storage directories exist

5\. Config file is valid



\*\*Commands:\*\*

```powershell

\# Check PostgreSQL

Get-Service postgresql\*



\# Check port

netstat -ano | findstr :8000



\# Validate config

python scripts\\validate\_config.py



\# Check logs

type logs\\service-stderr.log

```



\### Service Crashes Repeatedly



\*\*Steps:\*\*

1\. Check stderr log for errors

2\. Test application manually

3\. Verify database connection

4\. Check disk space

5\. Review recent changes



```powershell

\# Test manual run

cd C:\\Deployment\\nex-automat\\apps\\supplier-invoice-loader

..\\..\\venv32\\Scripts\\python.exe main.py

```



\### High Memory Usage



\*\*Monitor:\*\*

```powershell

\# Check process memory

Get-Process python\* | Where-Object {$\_.Path -like "\*nex-automat\*"} | Select-Object Name,Id,PM,WS



\# Monitor over time

while ($true) {

&nbsp;   Get-Process python\* | Where-Object {$\_.Path -like "\*nex-automat\*"} | Select-Object Name,Id,PM,WS

&nbsp;   Start-Sleep -Seconds 5

}

```



\*\*If memory leak suspected:\*\*

1\. Schedule regular service restarts

2\. Review code for memory leaks

3\. Monitor database connection pool



---



\## Maintenance Procedures



\### Regular Maintenance



\*\*Daily:\*\*

\- Check service status

\- Review error logs

\- Verify API health



\*\*Weekly:\*\*

\- Review all logs

\- Check disk space

\- Verify backup processes



\*\*Monthly:\*\*

\- Clean old log files

\- Review configuration

\- Test recovery procedures



\### Service Updates



\*\*Update procedure:\*\*

```powershell

\# 1. Stop service

python scripts\\manage\_service.py stop



\# 2. Backup current version

Copy-Item -Recurse apps\\supplier-invoice-loader apps\\supplier-invoice-loader.backup



\# 3. Deploy new version

\# (copy new files)



\# 4. Test configuration

python scripts\\validate\_config.py



\# 5. Start service

python scripts\\manage\_service.py start



\# 6. Verify

python scripts\\manage\_service.py logs

Invoke-WebRequest -Uri http://localhost:8000/health

```



---



\## Emergency Procedures



\### Complete Service Reset



```powershell

\# 1. Stop and remove service

C:\\Deployment\\nex-automat\\tools\\nssm\\win32\\nssm.exe stop NEX-Automat-Loader

C:\\Deployment\\nex-automat\\tools\\nssm\\win32\\nssm.exe remove NEX-Automat-Loader confirm



\# 2. Recreate service

python scripts\\create\_windows\_service.py



\# 3. Start service

python scripts\\manage\_service.py start

```



\### Service Won't Stop



```powershell

\# Force stop via NSSM

C:\\Deployment\\nex-automat\\tools\\nssm\\win32\\nssm.exe stop NEX-Automat-Loader



\# If still running, force kill process

Get-Process python\* | Where-Object {$\_.Path -like "\*nex-automat\*"} | Stop-Process -Force

```



---



\## Monitoring \& Alerts



\### Health Check Endpoint



```powershell

\# Manual check

Invoke-WebRequest -Uri http://localhost:8000/health



\# Automated monitoring script

while ($true) {

&nbsp;   try {

&nbsp;       $response = Invoke-WebRequest -Uri http://localhost:8000/health -TimeoutSec 5

&nbsp;       Write-Host "\[OK] Service healthy - $($response.Content)"

&nbsp;   } catch {

&nbsp;       Write-Host "\[ERROR] Service not responding - $\_"

&nbsp;   }

&nbsp;   Start-Sleep -Seconds 60

}

```



\### Performance Metrics



```powershell

\# CPU and Memory

Get-Process python\* | Where-Object {$\_.Path -like "\*nex-automat\*"} | Select-Object Name,Id,CPU,PM,WS



\# Database connections

\# (check via PostgreSQL admin tools)



\# Port status

netstat -ano | findstr :8000

```



---



\## Contact \& Support



\*\*Developer:\*\* Zoltán Rausch  

\*\*Company:\*\* ICC Komárno  

\*\*Email:\*\* zoltan.rausch@icc.sk  

\*\*Customer:\*\* Mágerstav s.r.o.



\*\*For urgent issues:\*\*

1\. Check TROUBLESHOOTING.md

2\. Review service logs

3\. Contact developer



---



\*\*Last Updated:\*\* 2025-11-21  

\*\*Version:\*\* 1.0

