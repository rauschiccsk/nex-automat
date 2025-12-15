# Database Recovery Guide

**Project:** NEX Automat - Supplier Invoice Loader  
**Customer:** Mágerstav s.r.o.  
**Version:** 2.0  
**Last Updated:** 2025-11-21  
**Author:** Zoltán Rausch, ICC Komárno

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [RTO/RPO Definitions](#rtorpo-definitions)
3. [Backup System](#backup-system)
4. [Recovery Procedures](#recovery-procedures)
5. [Disaster Recovery Scenarios](#disaster-recovery-scenarios)
6. [Testing & Validation](#testing--validation)
7. [Emergency Contacts](#emergency-contacts)

---

## 🎯 Overview

This guide provides step-by-step procedures for recovering the NEX Automat database from backups in case of data loss, corruption, or system failure.

### Critical Information

- **Database:** PostgreSQL 14+
- **Database Name:** invoice_staging
- **Backup Location:** `C:\Development\nex-automat\apps\supplier-invoice-loader\backups`
- **Backup Schedule:** Daily (automated via Task Scheduler)
- **Backup Retention:** 7 daily + 4 weekly backups

### Service Objectives

- **RTO (Recovery Time Objective):** < 1 hour
- **RPO (Recovery Point Objective):** < 24 hours
- **Business Impact:** Invoice processing downtime affects supplier payments

---

## 📊 RTO/RPO Definitions

### Recovery Time Objective (RTO)

**Target: < 1 hour**

Maximum acceptable time to restore database operations after failure:

- Database restore: ~15-30 minutes (depending on size)
- Service restart: ~5 minutes
- Verification: ~10 minutes
- **Total: ~30-45 minutes**

### Recovery Point Objective (RPO)

**Target: < 24 hours**

Maximum acceptable data loss in time:

- Daily backups at 02:00 AM
- Maximum data loss: up to 24 hours (last backup point)
- For critical operations: consider increasing backup frequency

---

## 💾 Backup System

### Backup Types

**1. Daily Backups**

- **Schedule:** Every day at 02:00 AM
- **Retention:** 7 days (rolling window)
- **Location:** `backups/daily/`
- **Format:** `backup_YYYYMMDD_HHMMSS_invoice_staging.sql.gz`

**2. Weekly Backups**

- **Schedule:** Every Sunday at 02:00 AM
- **Retention:** 4 weeks (rolling window)
- **Location:** `backups/weekly/`
- **Format:** `backup_YYYYMMDD_HHMMSS_invoice_staging.sql.gz`

### Backup Features

- **Compression:** Gzip level 6 (~70% size reduction)
- **Verification:** SHA256 checksum for each backup
- **Encryption:** XOR encryption for configuration backups
- **Automatic Rotation:** Old backups removed automatically

---

## 🔧 Recovery Procedures

### Procedure 1: List Available Backups

**Purpose:** Identify restore point before recovery

```bash
cd C:\Development\nex-automat\apps\supplier-invoice-loader
python scripts\restore_database.py list
```

**Expected Output:**

```
Available backups (2):

  backup_20251121_020000_invoice_staging.sql.gz
    Type: daily
    Size: 15.43 MB
    Modified: 2025-11-21 02:00:00
    Checksum: Yes

  backup_20251120_020000_invoice_staging.sql.gz
    Type: daily
    Size: 14.87 MB
    Modified: 2025-11-20 02:00:00
    Checksum: Yes
```

---

### Procedure 2: Verify Backup Integrity

**Purpose:** Ensure backup is valid before restore

```bash
python scripts\restore_database.py verify backups\daily\backup_20251121_020000_invoice_staging.sql.gz
```

**Expected Output:**

```
✓ Backup verified successfully (checksum OK)
```

**If verification fails:**

- Try previous backup
- Check disk integrity
- Contact support (see Emergency Contacts)

---

### Procedure 3: Get Restore Point Information

**Purpose:** View detailed backup information

```bash
python scripts\restore_database.py info backups\daily\backup_20251121_020000_invoice_staging.sql.gz
```

**Expected Output:**

```
Restore Point Information:

  Name: backup_20251121_020000_invoice_staging.sql.gz
  Path: C:\Development\nex-automat\apps\supplier-invoice-loader\backups\daily\backup_20251121_020000_invoice_staging.sql.gz
  Timestamp: 2025-11-21 02:00:00
  Size: 15.43 MB (16180224 bytes)
  Verified: Yes
  Message: Backup verified successfully (checksum OK)
```

---

### Procedure 4: Restore Database (Partial Recovery)

**Purpose:** Restore database without dropping existing data (merge mode)

⚠️ **Warning:** This appends data from backup to existing database. Use for partial recovery only.

```bash
python scripts\restore_database.py restore backups\daily\backup_20251121_020000_invoice_staging.sql.gz
```

**Process:**

1. Verifies backup integrity (SHA256 + gzip)
2. Restores SQL commands to existing database
3. Preserves existing data
4. Reports success/failure

---

### Procedure 5: Restore Database (Full Recovery)

**Purpose:** Complete database replacement (disaster recovery)

⚠️ **CRITICAL WARNING:** This will **DELETE ALL EXISTING DATA**!

**Step 1: Stop all services accessing database**

```powershell
# Stop NEX Automat services
Stop-Service "NEX-Automat-Loader"
Stop-Service "NEX-Automat-Editor"

# Verify no active connections
psql -h localhost -p 5432 -U postgres -d postgres -c "SELECT COUNT(*) FROM pg_stat_activity WHERE datname='invoice_staging';"
```

**Step 2: Perform full restore**

```bash
python scripts\restore_database.py restore backups\daily\backup_20251121_020000_invoice_staging.sql.gz --drop
```

**Interactive Confirmation:**

```
⚠ WARNING: Existing database will be dropped!
Continue? (yes/no): yes
```

**Process:**

1. Verifies backup integrity
2. Drops existing database
3. Creates new empty database
4. Restores from backup
5. Verifies data integrity

**Step 3: Restart services**

```powershell
Start-Service "NEX-Automat-Loader"
Start-Service "NEX-Automat-Editor"
```

---

### Procedure 6: Restore Configuration Files

**Purpose:** Restore configuration after system reinstall

**Step 1: List configuration backups**

```bash
python scripts\backup_config.py list
```

**Step 2: Restore configuration**

```bash
python scripts\backup_config.py restore --backup-path backups\config\config_backup_20251121_020000 --restore-dir restored --encryption-key YOUR_KEY
```

**Step 3: Copy restored files**

```powershell
Copy-Item restored\config.yaml config\
Copy-Item restored\.env .
```

---

## 🚨 Disaster Recovery Scenarios

### Scenario 1: Data Corruption (Single Table)

**Symptoms:** Specific invoices or data corrupted

**Recovery:**

1. Identify affected data scope
2. Export clean data from backup
3. Restore only affected tables
4. **RTO:** ~15 minutes
5. **RPO:** Last backup (max 24h)

**Commands:**

```bash
# Extract specific table from backup
gunzip -c backups\daily\backup_20251121_020000_invoice_staging.sql.gz | findstr "invoices" > invoices_restore.sql

# Restore single table
psql -h localhost -U postgres -d invoice_staging -f invoices_restore.sql
```

---

### Scenario 2: Complete Database Loss

**Symptoms:** Database unavailable, corrupted, or deleted

**Recovery:**

1. Stop all services
2. Full database restore with --drop
3. Verify data integrity
4. Restart services
5. **RTO:** ~30-45 minutes
6. **RPO:** Last backup (max 24h)

**Commands:** See Procedure 5: Restore Database (Full Recovery)

---

### Scenario 3: System Crash During Processing

**Symptoms:** Mid-transaction failure, partial data

**Recovery:**

1. Check current database state
2. Identify last successful transaction
3. Partial restore if needed
4. Resume processing
5. **RTO:** ~15 minutes
6. **RPO:** Real-time (transaction log recovery)

**Commands:**

```bash
# Check database status
psql -h localhost -U postgres -d invoice_staging -c "SELECT COUNT(*) FROM invoices WHERE status='processing';"

# If inconsistent, restore from backup
python scripts\restore_database.py restore backups\daily\backup_20251121_020000_invoice_staging.sql.gz
```

---

### Scenario 4: Hardware Failure (Disk/Server)

**Symptoms:** Hardware unavailable, disk corruption

**Recovery:**

1. Install PostgreSQL on new hardware
2. Copy backup files to new server
3. Restore database
4. Update configuration (IP, paths)
5. Restart services
6. **RTO:** ~1 hour (including setup)
7. **RPO:** Last backup (max 24h)

**Commands:**

```bash
# On new server
python scripts\restore_database.py restore \\backup-server\backups\daily\backup_20251121_020000_invoice_staging.sql.gz --drop
```

---

### Scenario 5: Accidental Data Deletion

**Symptoms:** User error, deleted records

**Recovery:**

1. Immediately stop all writes
2. Export deleted data from backup
3. Restore only deleted records
4. **RTO:** ~10 minutes
5. **RPO:** Last backup (max 24h)

**Commands:**

```bash
# Identify deleted records timeframe
# Restore from backup before deletion
python scripts\restore_database.py restore backups\daily\backup_20251120_020000_invoice_staging.sql.gz
```

---

## ✅ Testing & Validation

### Pre-Production Testing Checklist

**Before going live, test all recovery procedures:**

- [ ] **Test 1: List Backups**
  
  - Command: `python scripts\restore_database.py list`
  - Expected: List of daily and weekly backups
  - Status: ______

- [ ] **Test 2: Verify Backup**
  
  - Command: `python scripts\restore_database.py verify [backup]`
  - Expected: Checksum OK
  - Status: ______

- [ ] **Test 3: Get Info**
  
  - Command: `python scripts\restore_database.py info [backup]`
  - Expected: Detailed backup information
  - Status: ______

- [ ] **Test 4: Partial Restore (Test DB)**
  
  - Command: `python scripts\restore_database.py restore [backup]`
  - Expected: Successful restore without drop
  - Status: ______

- [ ] **Test 5: Full Restore (Test DB)**
  
  - Command: `python scripts\restore_database.py restore [backup] --drop`
  - Expected: Complete database replacement
  - Status: ______

- [ ] **Test 6: Configuration Restore**
  
  - Command: `python scripts\backup_config.py restore [...]`
  - Expected: Config files restored
  - Status: ______

- [ ] **Test 7: End-to-End Recovery**
  
  - Simulate complete failure
  - Restore from backup
  - Verify application functionality
  - Status: ______

- [ ] **Test 8: RTO Validation**
  
  - Measure actual recovery time
  - Target: < 1 hour
  - Actual: ______ minutes

- [ ] **Test 9: RPO Validation**
  
  - Verify data loss scope
  - Target: < 24 hours
  - Actual: ______ hours

---

### Monthly Recovery Drills

**Schedule:** First Monday of each month

**Procedure:**

1. Select random backup from previous week
2. Restore to test environment
3. Verify data integrity
4. Document time taken
5. Update procedures if needed

**Documentation Template:**

```
Date: _______________
Backup Used: _______________
Restore Time: _____ minutes
Issues Found: _______________
Actions Taken: _______________
Verified By: _______________
```

---

### Post-Recovery Validation

**After any restore operation, verify:**

1. **Database Connectivity**
   
   ```bash
   psql -h localhost -U postgres -d invoice_staging -c "SELECT 1;"
   ```

2. **Record Counts**
   
   ```sql
   SELECT 
       'invoices' AS table_name, COUNT(*) FROM invoices
   UNION ALL
   SELECT 'suppliers' AS table_name, COUNT(*) FROM suppliers;
   ```

3. **Latest Data**
   
   ```sql
   SELECT MAX(created_at) FROM invoices;
   ```

4. **Application Functionality**
   
   - Start loader service
   - Process test invoice
   - Verify in NEX Genesis

5. **User Notification**
   
   - Inform users of recovery completion
   - Document data loss scope (if any)

---

## 📞 Emergency Contacts

### Primary Contact

**Name:** Zoltán Rausch  
**Role:** Senior Developer  
**Company:** ICC Komárno  
**Phone:** +421 XXX XXX XXX  
**Email:** zoltan.rausch@icc.sk  
**Availability:** 24/7 for critical issues

### Customer Contact

**Company:** Mágerstav s.r.o.  
**Contact:** [Primary Contact Name]  
**Phone:** +421 XXX XXX XXX  
**Email:** contact@magerstav.sk  
**Escalation:** [Manager Name]

### Support Levels

**Level 1: Standard Support**

- Response Time: 4 business hours
- For: Backup verification, partial restores
- Contact: Email to zoltan.rausch@icc.sk

**Level 2: Priority Support**

- Response Time: 1 hour
- For: Full restore needed, data corruption
- Contact: Phone call + Email

**Level 3: Emergency Support**

- Response Time: 15 minutes
- For: Complete system failure, production down
- Contact: Direct phone call

---

## 📝 Recovery Log Template

**Use this template to document all recovery operations:**

```
=== Recovery Log ===

Date/Time: _______________
Initiated By: _______________
Reason: _______________

Backup Used:
  - File: _______________
  - Timestamp: _______________
  - Size: _______________
  - Verified: Yes / No

Procedure Used:
  - Type: Partial / Full / Configuration
  - Drop Existing: Yes / No

Timeline:
  - Start Time: _____
  - Stop Services: _____
  - Restore Begin: _____
  - Restore Complete: _____
  - Verification: _____
  - Services Started: _____
  - End Time: _____
  - Total Duration: _____ minutes

Data Loss:
  - RPO Met: Yes / No
  - Data Lost: _______________
  - Impact: _______________

Issues Encountered:
  - _______________
  - _______________

Resolution:
  - _______________
  - _______________

Verified By: _______________
Approved By: _______________

Post-Recovery Actions:
  - [ ] User notification sent
  - [ ] Documentation updated
  - [ ] Incident report filed
  - [ ] Root cause analysis scheduled
```

---

## 🔗 Related Documentation

- [Deployment Guide](DEPLOYMENT_GUIDE.md)
- [Backup Configuration](../apps/supplier-invoice-loader/config/README.md)
- [Windows Task Scheduler Setup](SCHEDULER_SETUP.md)
- [Monitoring Guide](MONITORING_GUIDE.md)

---

**Document Version:** 1.0  
**Last Review:** 2025-11-21  
**Next Review:** 2025-12-21  
**Status:** Production Ready
