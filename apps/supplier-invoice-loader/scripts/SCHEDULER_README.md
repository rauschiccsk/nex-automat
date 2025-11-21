# Windows Task Scheduler Setup

Automated database backups using Windows Task Scheduler.

## Installation

**Run as Administrator:**

```powershell
cd C:\Development\nex-automat\apps\supplier-invoice-loader\scripts
.\setup_task_scheduler.ps1
```

## Scheduled Tasks

**Daily Backup:**
- Task Name: `NEX-Automat-Backup-Daily`
- Schedule: Every day at 02:00 AM
- Retention: 7 backups
- Location: `backups/daily/`

**Weekly Backup:**
- Task Name: `NEX-Automat-Backup-Weekly`
- Schedule: Every Sunday at 02:00 AM
- Retention: 4 backups
- Location: `backups/weekly/`

## Management Commands

**List tasks:**
```powershell
Get-ScheduledTask -TaskName "NEX-Automat-Backup-*"
```

**Run manually:**
```powershell
Start-ScheduledTask -TaskName "NEX-Automat-Backup-Daily"
Start-ScheduledTask -TaskName "NEX-Automat-Backup-Weekly"
```

**Disable/Enable:**
```powershell
Disable-ScheduledTask -TaskName "NEX-Automat-Backup-Daily"
Enable-ScheduledTask -TaskName "NEX-Automat-Backup-Daily"
```

**Remove tasks:**
```powershell
Unregister-ScheduledTask -TaskName "NEX-Automat-Backup-Daily" -Confirm:$false
Unregister-ScheduledTask -TaskName "NEX-Automat-Backup-Weekly" -Confirm:$false
```

## Logs

Backup logs are stored in `logs/` directory:
- `backup_daily_YYYYMMDD.log`
- `backup_weekly_YYYYMMDD.log`

**View latest log:**
```powershell
Get-Content logs\backup_daily_$(Get-Date -Format "yyyyMMdd").log -Tail 50
```

## Troubleshooting

**Task not running:**
1. Check task status: `Get-ScheduledTask -TaskName "NEX-Automat-Backup-Daily"`
2. View task history: Task Scheduler GUI → History tab
3. Check logs in `logs/` directory

**Permission errors:**
- Tasks run as SYSTEM user
- Ensure SYSTEM has access to project directory
- Check PostgreSQL authentication (PGPASSWORD)

**Backup failures:**
- Check database connectivity
- Verify config.yaml settings
- Check disk space
- Review logs for detailed errors

## Email Notifications

Email notifications are sent on backup failures to:
- Operator email (configured in config.yaml)
- Alert email (alert@icc.sk)

**Configure SMTP settings in config.yaml:**
```yaml
email:
  operator: "operator@customer.com"
  alert: "alert@icc.sk"
  smtp_host: "smtp.gmail.com"
  smtp_port: 587
  smtp_user: "your-email@gmail.com"
  smtp_password: "your-password"
```

## Testing

**Test daily backup:**
```powershell
Start-ScheduledTask -TaskName "NEX-Automat-Backup-Daily"
Get-Content logs\backup_daily_$(Get-Date -Format "yyyyMMdd").log
```

**Verify backup created:**
```powershell
dir backups\daily | Sort-Object LastWriteTime -Descending | Select-Object -First 1
```

---

**Last Updated:** 2025-11-21  
**Author:** Zoltán Rausch, ICC Komárno
