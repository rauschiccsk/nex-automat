#!/usr/bin/env python3
"""
Script 21: Extract Training Guide Template + Archive Mágerstav Version

Migrates TRAINING_GUIDE.md-old:
1. Creates generic TRAINING_GUIDE_TEMPLATE.md in docs/deployment/
2. Archives customer-specific version in docs/archive/deployments/
3. Deletes original .md-old file
"""

import shutil
from pathlib import Path

# Paths
REPO_ROOT = Path(r"C:\Development\nex-automat")
SOURCE = REPO_ROOT / "docs/deployment/TRAINING_GUIDE.md-old"
TEMPLATE_NEW = REPO_ROOT / "docs/deployment/TRAINING_GUIDE_TEMPLATE.md"
ARCHIVE = REPO_ROOT / "docs/archive/deployments/TRAINING_GUIDE_MAGERSTAV_2025-11-27.md"

# Generic template content
TEMPLATE = r"""# NEX Automat - Training Guide Template

**Customer:** [CUSTOMER_NAME]  
**System:** Supplier Invoice Loader  
**Version:** [VERSION]  
**Training Date:** [DATE]  

---

## Training Content

| Topic               | Duration | Target Audience |
| ------------------- | -------- | --------------- |
| System Introduction | 15 min   | All             |
| Basic Operations    | 20 min   | Users           |
| Administration      | 30 min   | IT Admin        |
| Troubleshooting     | 20 min   | IT Admin        |
| Practical Exercises | 25 min   | All             |

**Total Duration:** 2 hours

---

## 1. System Introduction

### What is NEX Automat?

NEX Automat is an automated system for processing supplier invoices.

### System Benefits

- Automatic processing instead of manual entry
- Accurate data extraction
- Seconds per invoice instead of hours
- Standardized format

### What System Processes

- ✅ PDF invoices from suppliers
- ✅ Invoices in [LANGUAGES]
- ✅ Standard invoice formats
- ❌ Low quality scanned documents

---

## 2. Basic Operations (Users)

### How to Upload Invoice

1. Save PDF invoice to input folder
2. System automatically processes
3. Check result in NEX Genesis

### Check Processing Status

- Search invoice by number in NEX Genesis
- Verify data accuracy
- Contact IT if missing after 5 minutes

---

## 3. Administration (IT Admin)

### Service Management Commands

```powershell
cd [DEPLOYMENT_PATH]
python scripts\manage_service.py status
python scripts\manage_service.py start
python scripts\manage_service.py stop
python scripts\manage_service.py restart
python scripts\manage_service.py logs
```

### Daily Check

1. Check service status
2. Review logs for errors
3. Run diagnostics
4. Monitor disk space

---

## 4. Troubleshooting

### Service Not Running

```powershell
python scripts\manage_service.py status
python scripts\manage_service.py start
```

### Common Errors

- Connection refused → Restart PostgreSQL
- Permission denied → Run as Admin
- File not found → Check path
- Invalid PDF → Check file

---

## 5. Practical Exercises

### Exercise 1: Check Status (5 min)
### Exercise 2: Read Logs (5 min)
### Exercise 3: Service Restart (5 min)
### Exercise 4: Process Test Invoice (10 min)

---

## Final Test Questions

**For Users:**
1. Where to upload invoices?
2. How long does processing take?
3. Where to check results?

**For IT Admins:**
1. How to check service status?
2. How to restart service?
3. Where to find logs?

---

## Support Contacts

**[SUPPORT_COMPANY]:**
- Email: [SUPPORT_EMAIL]
- Phone: [SUPPORT_PHONE]
- Hours: [BUSINESS_HOURS]

---

**Training prepared by:** [SUPPORT_COMPANY]  
**Version:** [VERSION]
"""


def main():
    print("=" * 80)
    print("Script 21: Extract Training Guide Template + Archive")
    print("=" * 80)

    if not SOURCE.exists():
        print(f"\n❌ ERROR: Source not found: {SOURCE}")
        return False

    print(f"\n✅ Source: {SOURCE.name} ({SOURCE.stat().st_size:,} bytes)")

    # Create template
    print("\n" + "=" * 80)
    print("Step 1: Creating generic template")
    print("=" * 80)

    TEMPLATE_NEW.parent.mkdir(parents=True, exist_ok=True)
    with open(TEMPLATE_NEW, 'w', encoding='utf-8') as f:
        f.write(TEMPLATE)

    print(f"✅ Created: {TEMPLATE_NEW}")

    # Archive
    print("\n" + "=" * 80)
    print("Step 2: Archiving customer version")
    print("=" * 80)

    ARCHIVE.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(SOURCE, ARCHIVE)
    print(f"✅ Archived: {ARCHIVE}")

    # Delete
    print("\n" + "=" * 80)
    print("Step 3: Deleting .md-old")
    print("=" * 80)

    SOURCE.unlink()
    print(f"✅ Deleted: {SOURCE.name}")

    # Summary
    print("\n" + "=" * 80)
    print("Summary")
    print("=" * 80)
    print("\n✅ Created: TRAINING_GUIDE_TEMPLATE.md")
    print("✅ Archived: TRAINING_GUIDE_MAGERSTAV_2025-11-27.md")
    print("✅ Deleted: TRAINING_GUIDE.md-old")
    print("\n📋 Update: docs/archive/00_ARCHIVE_INDEX.md")
    print("\n✅ Script completed")
    print("=" * 80)

    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)