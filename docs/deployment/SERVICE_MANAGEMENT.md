# Service Management Guide - NEX Automat

Complete guide for managing the NEX Automat Windows Service.

**Service Name:** NEX-Automat-Loader  
**Display Name:** NEX Automat - Supplier Invoice Loader  
**Version:** 2.0.0

---

## Quick Reference

### Common Commands

```powershell
# Status
python scripts\manage_service.py status

# Start
python scripts\manage_service.py start

# Stop
python scripts\manage_service.py stop

# Restart
python scripts\manage_service.py restart

# View logs
python scripts\manage_service.py logs

# Tail logs (follow)
python scripts\manage_service.py tail
```

---

## Service Management

### Starting the Service

**Using management script:**

```powershell
cd C:\Deployment\nex-automat
venv32\Scripts\activate
python scripts\manage_service.py start
```

**Using NSSM directly:**

```powershell
C:\Deployment\nex-automat\tools\nssm\win32\nssm.exe start NEX-Automat-Loader
```

**Using Windows Services:**

1. Open Services (services.msc)
2. Find "NEX Automat - Supplier Invoice Loader"
3. Right-click → Start

**Expected Result:**

- Service status: RUNNING
- API accessible at http://localhost:8000/health
- Logs being written to logs\service-stdout.log

---

### Stopping the Service

**Using management script:**

```powershell
python scripts\manage_service.py stop
```

**Using NSSM directly:**

```powershell
C:\Deployment\nex-automat\tools\nssm\win32\nssm.exe stop NEX-Automat-Loader
```

**Using Windows Services:**

1. Open Services (services.msc)
2. Find "NEX Automat - Supplier Invoice Loader"
3. Right-click → Stop

**Wait Time:** Service may take 5-10 seconds to stop gracefully.

---

### Restarting the Service

**Using management script:**

```powershell
python scripts\manage_service.py restart
```

**Manual restart:**

```powershell
python scripts\manage_service.py stop
Start-Sleep -Seconds 5
python scripts\manage_service.py start
```

**When to Restart:**

- After configuration changes
- After code updates
- When service is unresponsive
- During troubleshooting

---

### Checking Service Status

**Detailed status:**

```powershell
python scripts\manage_service.py status
```

**Output includes:**

- Service state (RUNNING, STOPPED, etc.)
- Process ID (PID)
- Uptime
- Memory usage
- API health check result

**Quick check:**

```powershell
# Check if running
Get-Service "NEX-Automat-Loader" | Select-Object Status

# Test API
Invoke-WebRequest -Uri http://localhost:8000/health
```

---

## Log Management

### Viewing Logs

**Recent logs (last 50 lines):**

```powershell
python scripts\manage_service.py logs
```

**Specific number of lines:**

```powershell
python scripts\manage_service.py logs --lines 100
```

**Follow logs (tail -f):**

```powershell
python scripts\manage_service.py tail
```

**Direct log access:**

```powershell
# Service output
Get-Content logs\service-stdout.log -Tail 50

# Service errors
Get-Content logs\service-stderr.log -Tail 50

# Follow live
Get-Content logs\service-stdout.log -Wait
```

### Log Files

| File                    | Purpose                 | Rotation    |
| ----------------------- | ----------------------- | ----------- |
| logs\service-stdout.log | Service standard output | 10MB, daily |
| logs\service-stderr.log | Service errors          | 10MB, daily |
| logs\app-*.log          | Application logs        | Daily       |

### Log Rotation

Logs are automatically rotated:

- **Size-based:** When file reaches 10MB
- **Time-based:** Daily at midnight
- **Retention:** 30 days of logs kept

**Manual cleanup:**

```powershell
# Remove old logs (older than 30 days)
Get-ChildItem logs\* -Include *.log | Where-Object {$_.LastWriteTime -lt (Get-Date).AddDays(-30)} | Remove-Item
```

---

## Troubleshooting

### Service Won't Start

**Check logs first:**

```powershell
python scripts\manage_service.py logs
Get-Content logs\service-stderr.log -Tail 20
```

**Common causes:**

1. **Port 8000 already in use**
   
   ```powershell
   netstat -ano | findstr :8000
   ```

2. **Database connection failed**
   
   ```powershell
   python scripts\test_database_connection.py
   ```

3. **Configuration error**
   
   ```powershell
   python scripts\validate_config.py
   ```

4. **Missing dependencies**
   
   ```powershell
   venv32\Scripts\pip list
   ```

**Resolution:**

```powershell
# Fix the issue, then restart
python scripts\manage_service.py start
```

---

### Service Crashes/Stops Unexpectedly

**Check crash logs:**

```powershell
Get-Content logs\service-stderr.log -Tail 100
```

**Auto-restart configuration:**
Service is configured to restart automatically on failure with 0-second delay.

**Verify auto-restart:**

```powershell
C:\Deployment\nex-automat\tools\nssm\win32\nssm.exe get NEX-Automat-Loader AppRestartDelay
# Should show: 0
```

**If auto-restart not working:**

```powershell
C:\Deployment\nex-automat\tools\nssm\win32\nssm.exe set NEX-Automat-Loader AppRestartDelay 0
```

---

### High Memory Usage

**Check memory:**

```powershell
python scripts\manage_service.py status
```

**Normal memory usage:** 100-200 MB

**If memory usage high (>500 MB):**

1. Review recent logs for errors
2. Check for memory leaks
3. Restart service:
   
   ```powershell
   python scripts\manage_service.py restart
   ```

---

### API Not Responding

**Test API:**

```powershell
Invoke-WebRequest -Uri http://localhost:8000/health
```

**If no response:**

1. Check if service running:
   
   ```powershell
   python scripts\manage_service.py status
   ```

2. Check if port 8000 listening:
   
   ```powershell
   netstat -ano | findstr :8000
   ```

3. Check firewall rules (if applicable)

4. Restart service:
   
   ```powershell
   python scripts\manage_service.py restart
   ```

---

## Maintenance Tasks

### Weekly

- [ ] Review logs for errors
- [ ] Check service uptime
- [ ] Verify API health
- [ ] Check disk space

**Commands:**

```powershell
python scripts\manage_service.py status
python scripts\manage_service.py logs | Select-String "ERROR"
Get-PSDrive C | Select-Object Used,Free
```

### Monthly

- [ ] Review performance metrics
- [ ] Check log rotation
- [ ] Verify backups
- [ ] Update documentation if needed

---

## Performance Monitoring

### Key Metrics

**Service Status:**

```powershell
python scripts\manage_service.py status
```

**API Response Time:**

```powershell
Measure-Command { Invoke-WebRequest -Uri http://localhost:8000/health }
```

**Database Performance:**

```powershell
python scripts\test_database_connection.py
```

**Disk Space:**

```powershell
Get-PSDrive C | Select-Object Used,Free
```

---

## Emergency Procedures

### Complete Service Failure

1. **Stop service:**
   
   ```powershell
   python scripts\manage_service.py stop
   ```

2. **Check logs:**
   
   ```powershell
   Get-Content logs\service-stderr.log -Tail 100
   ```

3. **Verify database:**
   
   ```powershell
   python scripts\test_database_connection.py
   ```

4. **Restart service:**
   
   ```powershell
   python scripts\manage_service.py start
   ```

5. **If still failing, contact support**

### Database Connection Lost

1. **Check PostgreSQL service:**
   
   ```powershell
   Get-Service postgresql*
   ```

2. **Test connection:**
   
   ```powershell
   python scripts\test_database_connection.py
   ```

3. **Restart PostgreSQL if needed:**
   
   ```powershell
   Restart-Service postgresql-x64-15
   ```

4. **Restart application service:**
   
   ```powershell
   python scripts\manage_service.py restart
   ```

---

## Contact Information

**Support:** zoltan.rausch@icc.sk  
**Company:** ICC Komárno  
**Emergency:** [phone number]

---

**Document Version:** 1.0  
**Last Updated:** 2025-11-21  
**Next Review:** 2025-12-21
