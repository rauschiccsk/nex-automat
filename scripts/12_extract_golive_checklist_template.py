"""
Script 12: Extract Go-Live Checklist Template
Creates generic template + archives Mágerstav-specific version
"""

import os
import shutil
from pathlib import Path


def create_generic_template():
    """Create generic Go-Live checklist template"""
    template = """# NEX Automat - Go-Live Checklist

**Customer:** [CUSTOMER_NAME]  
**System:** Supplier Invoice Loader  
**Target Go-Live:** [YYYY-MM-DD]  
**Responsible:** [TEAM/PERSON]

---

## Readiness Overview

| Area | Status | Notes |
|------|--------|-------|
| Infrastructure | ⏳ | Server preparation |
| Application | ⏳ | Deployment pending |
| Database | ⏳ | Configuration pending |
| Testing | ⏳ | Test execution pending |
| Documentation | ⏳ | Documentation review |
| Training | ⏳ | User training pending |
| Monitoring | ⏳ | Monitoring setup |

---

## 1. Infrastructure (T-3 days)

### 1.1 Server

- [ ] Windows Server available
- [ ] Python 3.13 32-bit installed
- [ ] PostgreSQL 15+ installed and running
- [ ] NSSM installed
- [ ] Deployment directory created (C:\\Deployment\\nex-automat)
- [ ] Sufficient disk space (>100GB free)

### 1.2 Network

- [ ] Server accessible on network
- [ ] Firewall rules configured (port 8000 if needed)
- [ ] Access to NEX Genesis server verified

### 1.3 Backup

- [ ] Backup strategy defined
- [ ] Automated backups configured
- [ ] Recovery test performed
- [ ] Pre-Go-Live backup created

---

## 2. Application (T-2 days)

### 2.1 Deployment

- [ ] Code deployed to C:\\Deployment\\nex-automat
- [ ] Virtual environment created (venv32)
- [ ] All dependencies installed
- [ ] config.yaml properly configured

### 2.2 Windows Service

- [ ] NEX-Automat-Loader service created
- [ ] Service running (SERVICE_RUNNING)
- [ ] Auto-start on system boot
- [ ] Recovery settings configured (restart on failure)

### 2.3 Environment Variables

- [ ] POSTGRES_PASSWORD set
- [ ] LS_API_KEY set (if needed)
- [ ] Verified after server restart

---

## 3. Database (T-2 days)

### 3.1 PostgreSQL

- [ ] Database invoice_staging created
- [ ] Schema migrated
- [ ] User postgres with password
- [ ] Connection pooling configured

### 3.2 Data

- [ ] Production data imported (if exists)
- [ ] Test data removed
- [ ] Indexes created

### 3.3 Performance

- [ ] Query performance verified (<1ms)
- [ ] Connection time verified (<200ms)

---

## 4. Testing (T-1 day)

### 4.1 Automated Tests

- [ ] Error handling tests: PASS
- [ ] Performance tests: PASS
- [ ] Preflight checks: PASS

### 4.2 Manual Tests

- [ ] End-to-end invoice processing
- [ ] Output verification in NEX Genesis
- [ ] Test with real customer invoice

### 4.3 Load Tests

- [ ] Concurrent processing tested
- [ ] Memory leak check passed
- [ ] Throughput validated (0.5+ files/sec)

---

## 5. Documentation (T-1 day)

### 5.1 Technical Documentation

- [ ] SESSION_NOTES.md current
- [ ] PROJECT_MANIFEST.json generated
- [ ] KNOWN_ISSUES.md updated

### 5.2 Operations Documentation

- [ ] RECOVERY_PROCEDURES.md created
- [ ] OPERATIONS_GUIDE.md created
- [ ] TROUBLESHOOTING.md completed

### 5.3 Customer Documentation

- [ ] User manual
- [ ] Quick Reference Card
- [ ] FAQ document

---

## 6. Training (T-1 day)

### 6.1 Administrator Training

- [ ] Service management (start/stop/restart)
- [ ] Log reading
- [ ] Basic troubleshooting
- [ ] Backup and recovery

### 6.2 User Training

- [ ] How to upload invoices
- [ ] Processing status check
- [ ] Error handling

### 6.3 Training Documents

- [ ] Training materials prepared
- [ ] Contact information provided
- [ ] SLA conditions explained

---

## 7. Monitoring (T-1 day)

### 7.1 Health Checks

- [ ] Service status monitoring
- [ ] Database connectivity check
- [ ] Disk space monitoring

### 7.2 Alerting

- [ ] Email notifications on failure
- [ ] Escalation defined
- [ ] On-call contacts

### 7.3 Logging

- [ ] Application logs configured
- [ ] Log rotation set up
- [ ] Central log collection (if needed)

---

## 8. Go-Live Day (D-Day)

### 8.1 Before Launch (morning)

- [ ] Final backup created
- [ ] All services verified
- [ ] Preflight check: PASS
- [ ] Customer informed

### 8.2 Launch

- [ ] Service start verified
- [ ] First invoice processed
- [ ] Output in NEX Genesis verified
- [ ] Customer confirmed functionality

### 8.3 Post Launch (1h)

- [ ] Monitoring active
- [ ] No errors in logs
- [ ] Performance normal
- [ ] Customer satisfied

### 8.4 Post Launch (24h)

- [ ] Stability verified
- [ ] All invoices processed
- [ ] Customer reported OK
- [ ] Documentation delivered

---

## 9. Post Go-Live (D+1 to D+7)

### 9.1 Monitoring

- [ ] Daily log review
- [ ] Performance trending
- [ ] Incident tracking

### 9.2 Support

- [ ] Helpdesk ready
- [ ] Escalation working
- [ ] SLA met

### 9.3 Optimization

- [ ] Customer feedback
- [ ] Performance tuning if needed
- [ ] Documentation updated

---

## Critical Contacts

| Role | Name | Phone | Email |
|------|------|-------|-------|
| Project Lead | [NAME] | [PHONE] | [EMAIL] |
| Technician | [NAME] | [PHONE] | [EMAIL] |
| Customer IT | [NAME] | [PHONE] | [EMAIL] |
| Customer PM | [NAME] | [PHONE] | [EMAIL] |

---

## Rollback Plan

**If Go-Live fails:**

1. Stop service: `python scripts\\manage_service.py stop`
2. Restore DB from backup
3. Inform customer
4. Analyze root cause
5. Schedule new date

**Rollback Criteria:**

- Service doesn't start within 15 min
- Critical errors in processing
- Customer requests stop

---

## Sign-off

| Item | Signature | Date |
|------|-----------|------|
| Infrastructure OK | ________ | ________ |
| Application OK | ________ | ________ |
| Testing OK | ________ | ________ |
| Documentation OK | ________ | ________ |
| Training OK | ________ | ________ |
| Go-Live Approved | ________ | ________ |

---

**Template Version:** 1.0  
**Last Updated:** 2025-12-15
"""
    return template


def extract_and_archive():
    """Extract template and archive Mágerstav version"""

    repo_root = Path(r"C:\Development\nex-automat")
    old_file = repo_root / "docs" / "deployment" / "GO_LIVE_CHECKLIST.md-old"
    template_file = repo_root / "docs" / "deployment" / "GO_LIVE_CHECKLIST.md"
    archive_dir = repo_root / "docs" / "archive" / "deployments"
    archive_file = archive_dir / "CHECKLIST_MAGERSTAV_2025-11-27.md"
    archive_index = repo_root / "docs" / "archive" / "00_ARCHIVE_INDEX.md"

    print("🔄 Extracting Go-Live Checklist Template...")
    print()

    # 1. Create generic template
    template = create_generic_template()
    with open(template_file, 'w', encoding='utf-8') as f:
        f.write(template)
    print(f"✅ Created: {template_file.relative_to(repo_root)}")
    print("   Generic Go-Live checklist template")
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

        # Find Deployment Records section
        if "## Deployment Records" in content:
            lines = content.split('\n')
            # Find the section and add new entry after first entry
            insert_idx = None
            for i, line in enumerate(lines):
                if "2025-11-29" in line and "Mágerstav Production Deployment" in line:
                    # Insert after this line
                    insert_idx = i + 1
                    break

            if insert_idx:
                new_entry = "- **2025-11-27** - [Mágerstav Go-Live Checklist](deployments/CHECKLIST_MAGERSTAV_2025-11-27.md) - Pre-deployment preparation checklist"
                lines.insert(insert_idx, new_entry)
                content = '\n'.join(lines)

        with open(archive_index, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✅ Updated: {archive_index.relative_to(repo_root)}")
        print("   Added checklist entry to deployment records")

    print()
    print("=" * 60)
    print("✅ MIGRATION COMPLETE")
    print("=" * 60)
    print()
    print("Summary:")
    print(f"  • Created: docs/deployment/GO_LIVE_CHECKLIST.md (template)")
    print(f"  • Archived: CHECKLIST_MAGERSTAV_2025-11-27.md")
    print(f"  • Updated: Archive index")
    print()


if __name__ == "__main__":
    extract_and_archive()