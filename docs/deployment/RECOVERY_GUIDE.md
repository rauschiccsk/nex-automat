# Database Recovery Guide

**Project:** NEX Automat - Supplier Invoice Loader  
**Customer:** [CUSTOMER_NAME]  
**Version:** [VERSION]  
**Last Updated:** [YYYY-MM-DD]

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

- **Database:** PostgreSQL 15+
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

---

### Procedure 2: Verify Backup Integrity

**Purpose:** Ensure backup is valid before restore

```bash
python scripts\restore_database.py verify backups\daily\backup_YYYYMMDD_HHMMSS_invoice_staging.sql.gz
```

**If verification fails:**

- Try previous backup
- Check disk integrity
- Contact support

---

### Procedure 3: Get Restore Point Information

**Purpose:** View detailed backup information

```bash
python scripts\restore_database.py info backups\daily\backup_YYYYMMDD_HHMMSS_invoice_staging.sql.gz
```

---

### Procedure 4: Restore Database (Partial Recovery)

**Purpose:** Restore database without dropping existing data (merge mode)

⚠️ **Warning:** This appends data from backup to existing database. Use for partial recovery only.

```bash
python scripts\restore_database.py restore backups\daily\backup_YYYYMMDD_HHMMSS_invoice_staging.sql.gz
```

---

### Procedure 5: Restore Database (Full Recovery)

**Purpose:** Complete database replacement (disaster recovery)

⚠️ **CRITICAL WARNING:** This will **DELETE ALL EXISTING DATA**!

**Step 1: Stop all services accessing database**

```powershell
# Stop NEX Automat services
Stop-Service "NEX-Automat-Loader"

# Verify no active connections
psql -h localhost -p 5432 -U postgres -d postgres -c "SELECT COUNT(*) FROM pg_stat_activity WHERE datname='invoice_staging';"
```

**Step 2: Perform full restore**

```bash
python scripts\restore_database.py restore backups\daily\backup_YYYYMMDD_HHMMSS_invoice_staging.sql.gz --drop
```

**Step 3: Restart services**

```powershell
Start-Service "NEX-Automat-Loader"
```

---

### Procedure 6: Restore Configuration Files

**Purpose:** Restore configuration after system reinstall

```bash
python scripts\backup_config.py list
python scripts\backup_config.py restore --backup-path backups\config\config_backup_YYYYMMDD_HHMMSS --restore-dir restored --encryption-key YOUR_KEY
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

---

### Scenario 5: Accidental Data Deletion

**Symptoms:** User error, deleted records

**Recovery:**

1. Immediately stop all writes
2. Export deleted data from backup
3. Restore only deleted records
4. **RTO:** ~10 minutes
5. **RPO:** Last backup (max 24h)

---

## ✅ Testing & Validation

### Pre-Production Testing Checklist

**Before going live, test all recovery procedures:**

- [ ] Test 1: List Backups
- [ ] Test 2: Verify Backup
- [ ] Test 3: Get Info
- [ ] Test 4: Partial Restore (Test DB)
- [ ] Test 5: Full Restore (Test DB)
- [ ] Test 6: Configuration Restore
- [ ] Test 7: End-to-End Recovery
- [ ] Test 8: RTO Validation (< 1 hour)
- [ ] Test 9: RPO Validation (< 24 hours)

---

### Monthly Recovery Drills

**Schedule:** First Monday of each month

**Procedure:**

1. Select random backup from previous week
2. Restore to test environment
3. Verify data integrity
4. Document time taken
5. Update procedures if needed

---

### Post-Recovery Validation

**After any restore operation, verify:**

1. **Database Connectivity**
2. **Record Counts**
3. **Latest Data**
4. **Application Functionality**
5. **User Notification**

---

## 📞 Emergency Contacts

### Primary Contact

**Name:** [DEVELOPER_NAME]  
**Role:** [ROLE]  
**Company:** [COMPANY]  
**Phone:** [PHONE]  
**Email:** [EMAIL]  
**Availability:** [AVAILABILITY]

### Customer Contact

**Company:** [CUSTOMER_NAME]  
**Contact:** [CONTACT_NAME]  
**Phone:** [PHONE]  
**Email:** [EMAIL]

### Support Levels

**Level 1: Standard Support**
- Response Time: 4 business hours
- For: Backup verification, partial restores

**Level 2: Priority Support**
- Response Time: 1 hour
- For: Full restore needed, data corruption

**Level 3: Emergency Support**
- Response Time: 15 minutes
- For: Complete system failure, production down

---

## 📝 Recovery Log Template

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

Verified By: _______________
```

---

**Document Version:** 1.0  
**Last Review:** [YYYY-MM-DD]  
**Next Review:** [YYYY-MM-DD]
