# Init Prompt - Mágerstav Go-Live Testing

**Project:** NEX Automat v2.0 - Supplier Invoice Loader  
**Customer:** Mágerstav s.r.o.  
**Current Progress:** 85% (Server + n8n Ready, Testing Pending)  
**Last Session:** n8n Recovery & Workflow Setup - SUCCESS (2025-12-02)  
**This Session:** End-to-End Testing & Production Validation  

---

## Quick Context

**Server-side deployment** na Mágerstav server je **dokončený a funguje**:
- ✅ API beží na porte 8001
- ✅ Cloudflare Tunnel: https://magerstav-invoices.icc.sk
- ✅ Databáza invoice_staging vytvorená
- ✅ Health check odpovedá

**n8n workflow** na ICC serveri je **nakonfigurovaný a aktívny**:
- ✅ Workflow: n8n-SupplierInvoiceEmailLoader (ACTIVE)
- ✅ Email monitoring: magerstavinvoice@gmail.com
- ✅ IMAP credential: nastavený a funkčný
- ✅ Gmail credential: nastavený a funkčný
- ✅ API integration: správna URL a API key
- ✅ Environment variable: LS_API_KEY nastavená

**Čo CHÝBA:**
- End-to-end testing celého flow
- Production validation
- Customer handoff

---

## System Architecture

```
┌────────────────────────────────┐
│ ICC Server (n8n)               │
│                                │
│ ┌────────────────────────────┐ │
│ │ n8n Instance (LocalSystem) │ │
│ │ - Workflow: ACTIVE         │ │
│ │ - Email: magerstav...      │ │
│ │ - IMAP Monitor: Running    │ │
│ └─────────────┬──────────────┘ │
└───────────────┼────────────────┘
                │
                │ HTTPS POST
                │ (Cloudflare Tunnel)
                ▼
┌────────────────────────────────┐
│ Mágerstav Server (Production)  │
│                                │
│ ┌────────────────────────────┐ │
│ │ Cloudflare Tunnel          │ │
│ │ magerstav-invoices.icc.sk  │ │
│ └─────────────┬──────────────┘ │
│               ▼                │
│ ┌────────────────────────────┐ │
│ │ NEX Automat API:8001       │ │
│ │ - FastAPI Service          │ │
│ │ - Invoice Processing       │ │
│ └─────────────┬──────────────┘ │
│               ▼                │
│ ┌────────────────────────────┐ │
│ │ PostgreSQL 15              │ │
│ │ - invoice_staging DB       │ │
│ │ - 6 tables                 │ │
│ └────────────────────────────┘ │
└────────────────────────────────┘
```

---

## Current System State

### ✅ Mágerstav Server (Production) - DEPLOYED

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
- ✅ Port: 8001
- ✅ Customer: MAGERSTAV
- ✅ API Key: `magerstav-PWjoMerqzZc-EJZPuT0wN9iBzM8eK_t1Rh-HFZT4IbY`
- ✅ Environment: POSTGRES_PASSWORD = Nex1968
- ✅ Environment: LS_API_KEY = magerstav-PWjoMerqzZc-EJZPuT0wN9iBzM8eK_t1Rh-HFZT4IbY

**Cloudflare Tunnel:**
- ✅ Config: `C:\cloudflared-magerstav\config.yml`
- ✅ Tunnel ID: 0fdfffe9-b348-44b5-adcc-969681ac2786
- ✅ Hostname: magerstav-invoices.icc.sk
- ✅ Service: http://localhost:8001

### ✅ ICC Server (n8n) - CONFIGURED

**n8n Service:**
- ✅ Service Name: n8n-service
- ✅ Manager: NSSM
- ✅ Account: LocalSystem
- ✅ Status: Running
- ✅ Port: 5678
- ✅ Web UI: http://localhost:5678

**Database:**
- ✅ Location: `C:\Windows\SysWOW64\config\systemprofile\.n8n\database.sqlite`
- ✅ Size: 53.98 MB
- ✅ Workflows: 24 total
- ✅ Credentials: 8 total (all decrypted)
- ✅ Encryption Key: `OpvW9Fyd3Wi0x3lJJtpPW0ULcyHeDdK7`

**Environment Variables:**
```
N8N_PORT=5678
N8N_HOST=0.0.0.0
LS_API_KEY=magerstav-PWjoMerqzZc-EJZPuT0wN9iBzM8eK_t1Rh-HFZT4IbY
```

**Mágerstav Workflow:**
- ✅ Name: n8n-SupplierInvoiceEmailLoader
- ✅ ID: yBsDIpw6oMs96hi6
- ✅ Status: ACTIVE 🟢
- ✅ Email: magerstavinvoice@gmail.com
- ✅ IMAP: Configured and connected
- ✅ Gmail: Configured and connected
- ✅ HTTP: magerstav-invoices.icc.sk/invoice
- ✅ API Key: From $env.LS_API_KEY

**Workflow Nodes:**
1. Email Trigger (IMAP) - monitors magerstavinvoice@gmail.com
2. Split PDF (Code) - extracts PDF from attachments
3. Has PDF? (Switch) - routes based on PDF presence
   - Output 1 (Has PDF) → HTTP Request → Mágerstav API
   - Output 2 (No PDF) → Send Error Notification → it@magerstav.sk

---

## Session Goals

### Priority 1: End-to-End Testing (MUST DO)

#### Test 1.1: Happy Path - Invoice Processing

**Objective:** Verify complete flow from email to database

**Prerequisites:**
- Sample PDF invoice ready (any invoice PDF, 1-5 MB)
- Access to magerstavinvoice@gmail.com for sending
- Access to n8n UI for monitoring
- Access to Mágerstav server for database check

**Steps:**
1. **Send test email:**
   - To: magerstavinvoice@gmail.com
   - Subject: "Test Faktúra - Mágerstav"
   - Body: "Testovacia faktúra pre NEX Automat"
   - Attachment: PDF invoice file

2. **Wait 30-60 seconds** (IMAP polling interval)

3. **Check n8n Executions:**
   - Open: http://localhost:5678
   - Go to: Executions tab
   - Find latest execution
   - Status should be: SUCCESS (all nodes green)

4. **Verify n8n node outputs:**
   - Email Trigger: Shows email metadata
   - Split PDF: Shows file_b64 (base64 PDF)
   - Has PDF?: Routes to Output 1 (Has PDF)
   - HTTP Request: Response 200, status "success"

5. **Check Mágerstav database:**
   ```sql
   -- On Mágerstav server
   SELECT * FROM invoices_pending ORDER BY created_at DESC LIMIT 1;
   ```
   
   **Expected Fields:**
   - supplier_name: extracted from PDF
   - invoice_number: extracted or generated
   - status: 'pending'
   - file_hash: unique hash
   - from_email: sender email
   - created_at: recent timestamp

6. **Check NEX Automat logs:**
   ```powershell
   Get-Content C:\Deployment\nex-automat\logs\service-stdout.log -Tail 50
   ```
   
   **Expected Log:**
   ```
   [INFO] Processing invoice from email: [sender]
   [INFO] Invoice processed successfully
   ```

**Success Criteria:**
- ✅ n8n execution: SUCCESS
- ✅ HTTP response: 200 with {"status": "success"}
- ✅ Database record created
- ✅ No errors in logs

#### Test 1.2: Error Path - No PDF Attachment

**Objective:** Verify alert email is sent when no PDF attached

**Steps:**
1. **Send email WITHOUT attachment:**
   - To: magerstavinvoice@gmail.com
   - Subject: "Test bez PDF"
   - Body: Plain text only
   - NO attachment

2. **Wait 30-60 seconds**

3. **Check n8n Executions:**
   - Email Trigger: Shows email
   - Split PDF: No PDF found (error in json)
   - Has PDF?: Routes to Output 2 (No PDF)
   - Send Error Notification: SUCCESS

4. **Check alert email recipient inbox:**
   - Recipient: it@magerstav.sk (needs to be updated to correct email)
   - Subject: "⚠️ Nerozpoznaná faktúra - Test bez PDF"
   - Body: Contains email details

5. **Verify NO database record:**
   ```sql
   SELECT COUNT(*) FROM invoices_pending 
   WHERE from_email LIKE '%test%' OR subject LIKE '%Test bez PDF%';
   -- Expected: 0
   ```

**Success Criteria:**
- ✅ n8n execution: SUCCESS
- ✅ Alert email sent
- ✅ No database record created
- ✅ No API call made

#### Test 1.3: Duplicate Detection

**Objective:** Verify same invoice is rejected on second attempt

**Steps:**
1. **Send same PDF twice** (exact same file)

2. **First execution:**
   - Check HTTP response: `{"status": "success", "duplicate": false}`
   - Verify database: 1 record created

3. **Second execution:**
   - Check HTTP response: `{"status": "success", "duplicate": true}`
   - Verify database: Still only 1 record (not 2)

**Verification:**
```sql
SELECT file_hash, COUNT(*) 
FROM invoices_pending 
GROUP BY file_hash 
HAVING COUNT(*) > 1;
-- Expected: Empty result (no duplicates)
```

**Success Criteria:**
- ✅ First attempt: creates record
- ✅ Second attempt: duplicate=true
- ✅ Only 1 database record exists

#### Test 1.4: Large PDF Handling

**Objective:** Verify system handles larger PDFs (5-10 MB)

**Steps:**
1. Find large invoice PDF (5-10 MB)
2. Send via email to magerstavinvoice@gmail.com
3. Monitor n8n execution time
4. Verify processing completes within timeout (120s)

**If timeout occurs:**
- Increase timeout in HTTP node settings
- Check NEX Automat processing time in logs
- May need to optimize PDF processing

**Success Criteria:**
- ✅ Execution completes within 120s
- ✅ Database record created
- ✅ No timeout errors

---

### Priority 2: Production Validation

#### Validation 2.1: Health Check Availability

**From ICC Server:**
```bash
curl https://magerstav-invoices.icc.sk/health
```

**Expected:**
```json
{"status":"healthy","timestamp":"2025-12-02T..."}
```

**If fails:**
- Check Cloudflare Tunnel on Mágerstav
- Check firewall rules
- Verify DNS resolution

#### Validation 2.2: Database Integrity

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

-- Check for data corruption
SELECT COUNT(*) as total_invoices,
       COUNT(DISTINCT file_hash) as unique_hashes
FROM invoices_pending;
-- Both should match (no hash collisions)
```

#### Validation 2.3: Service Auto-Start

**Test service resilience:**
```powershell
# On Mágerstav server
Get-Service NEXAutomat | Select-Object Name, Status, StartType
Get-Service CloudflaredMagerstav | Select-Object Name, Status, StartType
Get-Service postgresql-x64-15 | Select-Object Name, Status, StartType

# Expected StartType: Automatic for all
```

**Test reboot:**
1. Restart Mágerstav server (if possible)
2. Wait 2 minutes
3. Check all services are Running
4. Check health endpoint responds
5. Check n8n can connect

---

### Priority 3: Production Handoff

#### Task 3.1: Update Error Notification Email

**Current recipient:** it@magerstav.sk (needs confirmation)

**In n8n:**
1. Open workflow: n8n-SupplierInvoiceEmailLoader
2. Edit node: "Send Error Notification"
3. Update "Send To" field with correct email
4. Save workflow

#### Task 3.2: Customer Onboarding Guide

**Create guide for Mágerstav:**
- How to forward supplier invoices to magerstavinvoice@gmail.com
- Expected email format
- How to check if invoice was processed
- What to do if error occurs
- Contact for support

#### Task 3.3: Monitoring Setup

**Setup ongoing monitoring:**
- Daily check of n8n executions
- Weekly database review
- Monthly log analysis
- Error alerting configuration

---

## Critical Information

### Connection Details

**NEX Automat API:**
- Public URL: https://magerstav-invoices.icc.sk
- Endpoint: /invoice (POST)
- Health: /health (GET)
- API Key: magerstav-PWjoMerqzZc-EJZPuT0wN9iBzM8eK_t1Rh-HFZT4IbY

**n8n Workflow:**
- Service: n8n-service (LocalSystem)
- Web UI: http://localhost:5678
- User: automation@isnex.ai
- Workflow: n8n-SupplierInvoiceEmailLoader (yBsDIpw6oMs96hi6)
- Email: magerstavinvoice@gmail.com

**Database:**
- Host: localhost (Mágerstav server)
- Port: 5432
- Database: invoice_staging
- User: postgres
- Password: Nex1968

### File Locations

**Mágerstav Server:**
- NEX Automat: `C:\Deployment\nex-automat`
- Logs: `C:\Deployment\nex-automat\logs\`
- Cloudflare: `C:\cloudflared-magerstav\`

**ICC Server (n8n):**
- Database: `C:\Windows\SysWOW64\config\systemprofile\.n8n\database.sqlite`
- Config: `C:\Windows\SysWOW64\config\systemprofile\.n8n\config`
- Logs: `C:\n8n-data\logs\`

---

## Known Issues (Non-Blocking)

1. **Error notification recipient needs update**
   - Current: it@magerstav.sk
   - Action: Confirm correct email with customer

2. **n8n encryption key backup**
   - Critical: OpvW9Fyd3Wi0x3lJJtpPW0ULcyHeDdK7
   - Action: Store in secure location

3. **n8n database backup strategy**
   - Current: No automated backup
   - Action: Setup weekly backup to safe location

---

## Success Criteria

### Must Have (Blocking)

- [ ] Test 1.1: Email with PDF creates database record
- [ ] Test 1.2: Email without PDF sends alert
- [ ] Test 1.3: Duplicate detection works
- [ ] n8n executions show no errors
- [ ] NEX Automat logs show no errors
- [ ] Database integrity verified

### Should Have (Important)

- [ ] Test 1.4: Large PDF handling (5+ MB)
- [ ] Health check responds from internet
- [ ] Services auto-start on reboot
- [ ] Error notification email updated
- [ ] Customer onboarding guide created

### Nice to Have (Optional)

- [ ] Monitoring/alerting configured
- [ ] Workflow backup exported
- [ ] Performance baseline established
- [ ] Documentation complete

---

## Troubleshooting Guide

### n8n Execution Fails

**Check:**
1. n8n service status: `Get-Service n8n-service`
2. n8n logs: `Get-Content C:\n8n-data\logs\n8n-error.log -Tail 50`
3. Workflow active status in UI
4. IMAP credential still valid

### HTTP Request Fails

**Check:**
1. Cloudflare Tunnel: `Get-Service CloudflaredMagerstav`
2. NEXAutomat service: `Get-Service NEXAutomat`
3. Health endpoint: `curl https://magerstav-invoices.icc.sk/health`
4. API key in environment: `$env:LS_API_KEY`
5. Firewall rules

### Database Record Not Created

**Check:**
1. Database connection: `psql -U postgres -d invoice_staging -c "SELECT 1;"`
2. NEX Automat logs: `Get-Content C:\Deployment\nex-automat\logs\service-stderr.log -Tail 50`
3. POSTGRES_PASSWORD environment variable
4. PostgreSQL service running

---

## Reference Documents

**Previous Sessions:**
- SESSION_NOTES.md (last session achievements)
- Go-Live Deployment Summary (server setup)
- n8n Recovery Documentation (database migration)

**Configuration:**
- n8n Workflow: n8n-SupplierInvoiceEmailLoader (in n8n UI)
- NSSM Service: HKLM:\SYSTEM\CurrentControlSet\Services\n8n-service\Parameters

**API Documentation:**
- Swagger: https://magerstav-invoices.icc.sk/docs
- Local: http://localhost:8001/docs (on Mágerstav server)

---

## Next Steps After This Session

1. **Monitor First 48 Hours:**
   - Check n8n executions daily
   - Review NEX Automat logs
   - Verify database growth
   - Watch for errors

2. **Customer Training:**
   - Email forwarding setup
   - Error handling procedure
   - Support contact information

3. **Schedule 1-Week Review:**
   - Review processing statistics
   - Check for any issues
   - Optimize if needed
   - Collect customer feedback

4. **Documentation Handoff:**
   - Export workflow backup
   - Create operations guide
   - Provide credentials (secure storage)
   - Transfer to support team

---

**Session Type:** End-to-End Testing & Production Validation  
**Expected Duration:** 2-3 hours  
**Blocking Issues:** None - ready to proceed  
**Status:** 🟢 READY TO TEST

---

**Last Updated:** 2025-12-02  
**Previous Session:** n8n Recovery (Complete)  
**This Session:** Go-Live Testing (Ready to Start)