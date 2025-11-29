# Init Prompt - End-to-End Testing & n8n Workflow Setup

**Project:** NEX Automat v2.0 - Supplier Invoice Loader  
**Customer:** Mágerstav s.r.o.  
**Current Progress:** 70% (Server Deployed, n8n Pending)  
**Last Session:** Go-Live Deployment - SUCCESS (2025-11-29)  
**This Session:** n8n Workflow Setup + End-to-End Testing  

---

## Quick Context

Server-side deployment NEX Automat v2.0 na Mágerstav server je **dokončený a funguje**. API beží na porte 8001, je vystavené cez Cloudflare Tunnel na https://magerstav-invoices.icc.sk a odpovedá na health checks. Databáza invoice_staging je vytvorená so všetkými tabuľkami.

**Čo CHÝBA:**
- n8n workflow konfigurácia na ICC serveri
- End-to-end testing celého flow

**Prečo je n8n kritický:**
NEX Automat API sám o sebe len čaká na HTTP POST requesty. Potrebuje n8n workflow, ktorý:
1. Monitoruje IMAP email účet
2. Extrahuje PDF prílohy z emailov
3. Posiela ich na NEX Automat API
4. Spracováva odpovede a posiela alerty

Bez n8n workflow **systém NIE JE FUNKČNÝ** - nie je žiadny zdroj faktúr.

---

## System Architecture

```
┌────────────────────────────────┐
│ ICC Server (Development)      │
│                                │
│ ┌────────────────────────────┐ │
│ │ n8n Instance               │ │
│ │ - Workflow: Supplier...    │ │
│ │ - IMAP Email Monitor       │ │
│ │ - PDF Extraction           │ │
│ └────────────┬───────────────┘ │
└──────────────┼─────────────────┘
               │
               │ HTTPS POST
               │ (Cloudflare Tunnel)
               ▼
┌────────────────────────────────┐
│ Mágerstav Server (Production) │
│                                │
│ ┌────────────────────────────┐ │
│ │ Cloudflare Tunnel          │ │
│ │ magerstav-invoices.icc.sk  │ │
│ └────────────┬───────────────┘ │
│              ▼                 │
│ ┌────────────────────────────┐ │
│ │ NEX Automat API:8001       │ │
│ │ - FastAPI Service          │ │
│ │ - Invoice Processing       │ │
│ └────────────┬───────────────┘ │
│              ▼                 │
│ ┌────────────────────────────┐ │
│ │ PostgreSQL 15              │ │
│ │ - invoice_staging DB       │ │
│ │ - 6 tables                 │ │
│ └────────────────────────────┘ │
└────────────────────────────────┘
```

---

## Current System State

### ✅ Mágerstav Server (Production) - COMPLETE

**Services Running:**
- ✅ postgresql-x64-15 (Running)
- ✅ NEXAutomat (Running - port 8001)
- ✅ CloudflaredMagerstav (Running)

**API Status:**
- ✅ Local: http://localhost:8001/health → 200 OK
- ✅ Public: https://magerstav-invoices.icc.sk/health → 200 OK
- ✅ API Endpoint: https://magerstav-invoices.icc.sk/invoice

**Database:**
- ✅ Database: invoice_staging (created)
- ✅ Tables: 6 (invoices_pending, invoice_items_pending, etc.)
- ✅ Status: Empty, ready for data

**Configuration:**
- ✅ Port: 8001 (changed from 8000 due to conflict)
- ✅ Customer: MAGERSTAV
- ✅ API Key: `magerstav-PWjoMerqzZc-EJZPuT0wN9iBzM8eK_t1Rh-HFZT4IbY`
- ✅ Environment: POSTGRES_PASSWORD = Nex1968 (Machine)
- ✅ Environment: LS_API_KEY = magerstav-PWjoMerqzZc-EJZPuT0wN9iBzM8eK_t1Rh-HFZT4IbY (Machine)

**Cloudflare Tunnel:**
- ✅ Config: `C:\cloudflared-magerstav\config.yml`
- ✅ Tunnel ID: 0fdfffe9-b348-44b5-adcc-969681ac2786
- ✅ Hostname: magerstav-invoices.icc.sk
- ✅ Service: http://localhost:8001 (updated from 8000)

**Validation Tests:**
- ✅ Preflight: 4/6 PASS (67%) - 2 non-blocking issues
- ✅ Error Handling: 10/12 PASS (83%)
- ✅ Performance: PASS (34.5 MB peak, 0.16 ms DB queries)

### ❌ ICC Server (n8n) - NOT CONFIGURED YET

**Status:**
- ❌ n8n workflow NOT imported
- ❌ IMAP credentials NOT configured
- ❌ HTTP node NOT configured
- ❌ Alert email NOT configured
- ❌ No testing performed

**Available Resources:**
- ✅ Workflow template: `n8n-SupplierInvoiceEmailLoader.json`
- ✅ Configuration guide: See previous session artifacts
- ✅ API connection details documented

---

## Session Goals

### Priority 1: n8n Workflow Setup (MUST DO)

**Location:** ICC Development Server

#### Task 1.1: Import Workflow Template

**File Location:**
```
Repository: nex-automat
Path: apps/supplier-invoice-loader/n8n-workflows/n8n-SupplierInvoiceEmailLoader.json
GitHub: https://raw.githubusercontent.com/rauschiccsk/nex-automat/main/apps/supplier-invoice-loader/n8n-workflows/n8n-SupplierInvoiceEmailLoader.json
```

**Steps:**
1. Open n8n UI (ICC server)
2. Create New Workflow
3. Import from File → select JSON
4. Rename to: "SupplierInvoiceEmailLoader - MAGERSTAV"

#### Task 1.2: Configure IMAP Email Trigger

**Node:** "Email Trigger (IMAP)"

**Information Needed:**
- Email provider (Gmail / Outlook / Custom IMAP)
- Operator email address
- Email password / App Password

**Gmail Setup (if using Gmail):**
1. Enable 2-Step Verification: https://myaccount.google.com/security
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Use App Password in n8n (NOT regular password)

**IMAP Credential:**
```
Host: imap.gmail.com (or outlook.office365.com)
Port: 993
User: [operator_email]
Password: [app_password]
SSL/TLS: Enabled
```

**Node Settings:**
- Mailbox: INBOX
- Action: Mark as read (prevents reprocessing!)
- Download Attachments: ✅ Enabled
- Execute Once: ❌ Disabled (continuous monitoring)

**Email Filters (Optional):**
- Subject Contains: "Faktúra" or specific keywords
- From Contains: Supplier email domains

#### Task 1.3: Configure HTTP POST Node

**Node:** "HTTP Request" (POST to NEX Automat API)

**URL:**
```
https://magerstav-invoices.icc.sk/invoice
```

**Method:** POST

**Headers:**
```
X-API-Key: magerstav-PWjoMerqzZc-EJZPuT0wN9iBzM8eK_t1Rh-HFZT4IbY
Content-Type: application/json
```

**Body:** (keep from template)
```json
{
  "file_b64": "{{ $json.file_b64 }}",
  "filename": "{{ $json.filename }}",
  "from_email": "{{ $json.from }}",
  "subject": "{{ $json.subject }}",
  "message_id": "{{ $json.message_id }}"
}
```

**Timeout:** 120000 ms (2 minutes)

**Retry Settings (Recommended):**
- Retry On Fail: ✅ Enabled
- Maximum Retries: 3
- Wait Between Tries: 5000 ms

#### Task 1.4: Configure Alert Email Node

**Node:** "Send Alert Email"

**Purpose:** Send notification when email has no PDF attachment

**Option A: Gmail OAuth2**
- Requires Google Cloud Console setup
- More reliable but complex

**Option B: SMTP (Simpler)**
- Host: smtp.gmail.com
- Port: 587
- User: [sender_email]
- Password: [app_password]
- Use TLS: Yes

**Email Settings:**
- Send To: `it@magerstav.sk` (or customer preference)
- Subject: `⚠️ Nerozpoznaná faktúra - {{ $json.subject }}`
- Message: Keep default template

#### Task 1.5: Activate Workflow

1. Save workflow
2. Toggle "Active" switch to ON
3. Workflow will now monitor email continuously

---

### Priority 2: End-to-End Testing

#### Test 2.1: Happy Path - Invoice Processing

**Objective:** Verify complete flow from email to database

**Steps:**
1. Send test email to configured IMAP account
   - Subject: "Test Faktúra - Mágerstav"
   - Attach: Sample PDF invoice (any invoice PDF)
   - From: Any email address

2. Wait 30-60 seconds (IMAP polling interval)

3. Check n8n Executions tab
   - Should see new execution
   - Status: SUCCESS
   - All nodes green

4. Verify n8n node outputs:
   - Email Trigger: Shows email data
   - Split PDF: Shows extracted PDF (file_b64)
   - Check PDF Present: Routes to HTTP node (Output 1)
   - HTTP POST: Response 200, status "success"

5. Check Mágerstav database:
```sql
-- On Mágerstav server, in PostgreSQL
SELECT * FROM invoices_pending ORDER BY created_at DESC LIMIT 1;
```

**Expected Database Record:**
- supplier_name: extracted from PDF
- invoice_number: extracted from PDF
- status: 'pending'
- file_hash: unique hash
- created_at: recent timestamp

6. Check NEX Automat logs:
```powershell
# On Mágerstav server
Get-Content C:\Deployment\nex-automat\logs\service-stdout.log -Tail 50
```

**Expected Log:**
```
[INFO] Processing invoice from email: [sender]
[INFO] Invoice processed successfully: [invoice_number]
```

#### Test 2.2: Error Path - No PDF Attachment

**Objective:** Verify alert email is sent when no PDF attached

**Steps:**
1. Send email WITHOUT attachment
   - Subject: "Test bez PDF"
   - Body: Plain text only
   - NO attachment

2. Wait 30-60 seconds

3. Check n8n Executions:
   - Email Trigger: Shows email
   - Split PDF: No PDF found
   - Check PDF Present: Routes to Alert Email (Output 2)
   - Send Alert Email: SUCCESS

4. Check alert email recipient inbox
   - Should receive notification
   - Subject: "⚠️ Nerozpoznaná faktúra - Test bez PDF"

5. Verify NO database record created:
```sql
SELECT COUNT(*) FROM invoices_pending WHERE subject LIKE '%Test bez PDF%';
-- Expected: 0
```

#### Test 2.3: Duplicate Detection

**Objective:** Verify same invoice is rejected on second attempt

**Steps:**
1. Send same PDF invoice twice (exact same file)

2. Check first execution:
   - HTTP Response: `{"status": "success", "duplicate": false}`
   - Database: Record created

3. Check second execution:
   - HTTP Response: `{"status": "success", "duplicate": true}`
   - Database: Only 1 record (not 2)

**Verification:**
```sql
SELECT file_hash, COUNT(*) 
FROM invoices_pending 
GROUP BY file_hash 
HAVING COUNT(*) > 1;
-- Expected: Empty result (no duplicates)
```

#### Test 2.4: Large PDF Handling

**Objective:** Verify system handles larger PDFs (5-10 MB)

**Steps:**
1. Find large invoice PDF (5-10 MB)
2. Send via email
3. Monitor execution time in n8n
4. Verify processing completes within timeout (120s)

**If timeout occurs:**
- Increase timeout in HTTP node
- Check NEX Automat logs for processing time
- May need to optimize PDF processing

#### Test 2.5: Multiple Invoices Batch

**Objective:** Verify sequential processing works

**Steps:**
1. Send 5 different invoice PDFs (separate emails)
2. Wait for all to process
3. Check all 5 executions are SUCCESS
4. Verify 5 database records:
```sql
SELECT COUNT(*) FROM invoices_pending 
WHERE created_at > NOW() - INTERVAL '10 minutes';
-- Expected: 5
```

---

### Priority 3: Validation & Monitoring

#### Validation 3.1: Health Check Availability

**From ICC Server (where n8n runs):**
```bash
curl https://magerstav-invoices.icc.sk/health
```

**Expected:**
```json
{"status":"healthy","timestamp":"2025-11-29T..."}
```

**If fails:**
- Check Cloudflare Tunnel on Mágerstav server
- Check firewall rules
- Verify DNS resolution

#### Validation 3.2: API Documentation Access

**URL:** https://magerstav-invoices.icc.sk/docs

**Should show:**
- Swagger UI
- POST /invoice endpoint
- Request/response models

**If 404:**
- FastAPI docs might be disabled in production
- Access via local: http://localhost:8001/docs

#### Validation 3.3: Database Integrity

**On Mágerstav Server:**
```sql
-- Check all tables exist
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public' 
ORDER BY table_name;

-- Expected: 6 tables + 2 views

-- Check indexes
SELECT indexname FROM pg_indexes 
WHERE schemaname = 'public';

-- Check for any data corruption
SELECT COUNT(*) as total_invoices,
       COUNT(DISTINCT file_hash) as unique_hashes
FROM invoices_pending;
-- Both should match (no hash collisions)
```

#### Validation 3.4: Service Auto-Start

**Verify services start on boot:**
```powershell
# On Mágerstav server
Get-Service NEXAutomat | Select-Object Name, Status, StartType
Get-Service CloudflaredMagerstav | Select-Object Name, Status, StartType
Get-Service postgresql-x64-15 | Select-Object Name, Status, StartType
```

**Expected StartType:** Automatic for all

**Test:**
1. Restart Mágerstav server
2. Wait 2 minutes
3. Check all services are Running
4. Check health endpoint responds

---

## Critical Information

### Connection Details

**NEX Automat API:**
- Public URL: https://magerstav-invoices.icc.sk
- Endpoint: /invoice (POST)
- Health: /health (GET)
- Docs: /docs (GET)

**API Authentication:**
- Header: X-API-Key
- Value: `magerstav-PWjoMerqzZc-EJZPuT0wN9iBzM8eK_t1Rh-HFZT4IbY`

**Database:**
- Host: localhost (on Mágerstav server)
- Port: 5432
- Database: invoice_staging
- User: postgres
- Password: Nex1968

**Cloudflare Tunnel:**
- Tunnel ID: 0fdfffe9-b348-44b5-adcc-969681ac2786
- Hostname: magerstav-invoices.icc.sk
- Config: C:\cloudflared-magerstav\config.yml

### File Locations

**Mágerstav Server:**
- NEX Automat: `C:\Deployment\nex-automat`
- Logs: `C:\Deployment\nex-automat\logs\`
- Config: `C:\Deployment\nex-automat\apps\supplier-invoice-loader\config\`
- Cloudflare: `C:\cloudflared-magerstav\`

**Development (Git changes pending):**
- Repository: `C:\Development\nex-automat`
- Modified: scripts/init_database.py (new)
- Modified: scripts/deploy_fresh.py (updated)

**n8n Workflow:**
- Template: `nex-automat/apps/supplier-invoice-loader/n8n-workflows/n8n-SupplierInvoiceEmailLoader.json`
- GitHub: https://raw.githubusercontent.com/rauschiccsk/nex-automat/main/apps/supplier-invoice-loader/n8n-workflows/n8n-SupplierInvoiceEmailLoader.json

### Email Configuration

**IMAP Account (TBD in this session):**
- Provider: Gmail / Outlook / Custom
- Email: [operator_email]
- Password: [app_password]

**Alert Recipient:**
- Email: it@magerstav.sk (or customer preference)

---

## Known Issues (Non-Blocking)

1. **Preflight Service Name Mismatch**
   - Script looks for "NEX-Automat-Loader"
   - Actual service: "NEXAutomat"
   - Impact: Cosmetic false negative in test
   - Status: Service runs fine

2. **Port Changed from 8000 to 8001**
   - Original: 8000
   - Updated: 8001 (due to conflict)
   - Impact: None (documented everywhere)
   - Status: Resolved

3. **No PDF Test Files**
   - Performance tests skip PDF-based tests
   - Impact: Can't test concurrent processing
   - Status: Will use real invoices for testing

---

## Success Criteria

### Must Have (Blocking)

- [ ] n8n workflow imported and configured
- [ ] IMAP credentials working
- [ ] HTTP POST to API working (with correct API key)
- [ ] Test email with PDF → creates database record
- [ ] Test email without PDF → sends alert
- [ ] No errors in n8n executions
- [ ] No errors in NEX Automat logs

### Should Have (Important)

- [ ] Duplicate detection working
- [ ] Large PDF handling (5+ MB)
- [ ] Multiple invoices processed
- [ ] Alert email received and formatted correctly
- [ ] Database integrity verified
- [ ] Services auto-start on reboot

### Nice to Have (Optional)

- [ ] Email filters configured (subject/sender)
- [ ] Monitoring/alerting configured
- [ ] Workflow backup exported
- [ ] Customer onboarding guide created

---

## Troubleshooting Guide

### n8n Workflow Not Triggering

**Symptoms:**
- No executions appearing
- Email sent but nothing happens

**Check:**
1. Workflow Active toggle is ON
2. IMAP credentials valid (test connection)
3. Email account has new unread messages
4. Email matches filters (if configured)
5. n8n server can reach IMAP server

**Solution:**
- Click "Test Step" on Email Trigger node
- Check n8n logs for IMAP errors
- Verify email credentials (try manual login)

### HTTP Request Fails

**Symptoms:**
- Error: ECONNREFUSED or ETIMEDOUT
- 401 Unauthorized

**Check:**
1. Cloudflare Tunnel running on Mágerstav:
   ```powershell
   Get-Service CloudflaredMagerstav
   ```

2. NEXAutomat service running:
   ```powershell
   Get-Service NEXAutomat
   ```

3. Health endpoint responds:
   ```bash
   curl https://magerstav-invoices.icc.sk/health
   ```

4. API key matches exactly (case-sensitive):
   ```
   magerstav-PWjoMerqzZc-EJZPuT0wN9iBzM8eK_t1Rh-HFZT4IbY
   ```

5. No extra spaces in header value

**Solution:**
- Restart Cloudflare Tunnel if stopped
- Restart NEXAutomat service if stopped
- Verify API key character-by-character
- Check firewall rules (ICC → Internet → Mágerstav)

### PDF Not Extracted

**Symptoms:**
- "No PDF attachment found" even when PDF attached

**Check:**
1. "Download Attachments" enabled in IMAP node
2. Email actually contains PDF (not link to PDF)
3. PDF size < 25 MB (IMAP limitation)
4. Check node execution data: does $binary have attachment_0?

**Solution:**
- Enable "Download Attachments" option
- Send smaller PDF if > 25 MB
- Try different PDF (some are corrupted)
- Check email provider allows attachments

### Database Record Not Created

**Symptoms:**
- HTTP returns success but no database entry

**Check:**
1. Database connection on Mágerstav server:
   ```powershell
   & "C:\Program Files\PostgreSQL\15\bin\psql.exe" -U postgres -d invoice_staging -c "SELECT COUNT(*) FROM invoices_pending;"
   ```

2. NEX Automat logs:
   ```powershell
   Get-Content C:\Deployment\nex-automat\logs\service-stderr.log -Tail 50
   ```

3. Database errors in logs

**Solution:**
- Check POSTGRES_PASSWORD environment variable
- Restart NEXAutomat service
- Check PostgreSQL service running
- Verify database permissions

---

## Reference Documents

**Previous Session:**
- SESSION_NOTES.md (this session's achievements)
- Go-Live Deployment Summary (artifacts)

**Configuration Guides:**
- n8n Workflow Configuration - Mágerstav (artifacts)
- N8N_WORKFLOW_SETUP.md (repository)

**API Documentation:**
- FastAPI Swagger: https://magerstav-invoices.icc.sk/docs
- Local docs: http://localhost:8001/docs (on Mágerstav server)

---

## Next Steps After This Session

1. **Monitor First 48 Hours**
   - Check n8n executions daily
   - Review NEX Automat logs
   - Verify database growth
   - Watch for errors

2. **Customer Onboarding**
   - Send operator email for forwarding invoices
   - Document email format requirements
   - Provide contact for support

3. **Schedule 1-Week Review**
   - Review processing statistics
   - Check for any issues
   - Optimize if needed
   - Collect customer feedback

4. **Documentation Handoff**
   - Export workflow backup
   - Create operations guide
   - Provide credentials (secure storage)
   - Transfer to support team

---

## Contact Information

**Technical Support:** rausch@icc.sk  
**Customer:** Mágerstav s.r.o.  
**Server Location:** Mágerstav Production Server  
**n8n Location:** ICC Development Server

---

**Session Type:** End-to-End Testing & n8n Workflow Setup  
**Expected Duration:** 2-3 hours  
**Blocking Issues:** None - ready to proceed  
**Status:** 🟢 READY TO START

---

**Last Updated:** 2025-11-29  
**Previous Session:** Go-Live Deployment (Complete)  
**This Session:** n8n + Testing (Ready to Start)