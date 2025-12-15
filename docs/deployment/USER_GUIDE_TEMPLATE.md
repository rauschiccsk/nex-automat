# NEX Automat - User Guide Template
## Automated Supplier Invoice Processing

**Customer:** [CUSTOMER_NAME]  
**System:** NEX Automat [VERSION]  
**Version:** [VERSION]  
**Date:** [DATE]  
**Status:** [STATUS]

---

## How It Works

NEX Automat automatically processes supplier invoices received via email. The system:

1. ✅ Receives email with invoice (PDF attachment)
2. ✅ Extracts invoice data (supplier, invoice number, amount...)
3. ✅ Saves invoice to database
4. ✅ Creates ISDOC XML file for NEX Genesis
5. ✅ Prepares invoice for NEX Genesis import
6. ✅ Displays invoice in desktop application for manual review

**Everything runs automatically without human intervention.**

---

## Desktop Application - NEX Invoice Manager

### What is it?

**NEX Invoice Manager** is a desktop application for viewing and manually reviewing processed invoices.

### How to launch?

Double-click the desktop icon:

```
🖥️ NEX Invoice Manager
```

### Features

- 📋 **View all invoices** - overview of all processed invoices
- 🔍 **Invoice detail** - display all extracted data
- 📄 **PDF preview** - open original invoice directly
- 📊 **Statistics** - overview of invoice counts, amounts, suppliers
- 🔄 **Export to NEX Genesis** - manual export of selected invoices (planned)

### How to use

1. **Launch application** - double-click desktop icon
2. **Invoice list** - left panel shows all invoices
3. **Click invoice** - right panel shows details
4. **Buttons:**
   - **Open PDF** - displays original invoice
   - **Open XML** - displays ISDOC XML file
   - **Export** - (planned) export to NEX Genesis

---

## How to Send Invoice for Processing

### Method 1: Forward Email (Recommended)

When you receive an invoice from a supplier:

1. Open email with invoice
2. Click **"Forward"**
3. In **"To"** field enter: **[INVOICE_EMAIL]**
4. Click **"Send"**

**Done!** System automatically processes it within 1-2 minutes.

### Method 2: Direct Email (For manual invoices)

If you have invoice as PDF file on computer:

1. Create new email
2. In **"To"** field enter: **[INVOICE_EMAIL]**
3. In **"Subject"** field enter anything (e.g., "Invoice from supplier")
4. Attach PDF file
5. Click **"Send"**

---

## Invoice Requirements

### ✅ Supported formats:
- PDF files (`.pdf`)
- Size: up to 10 MB (average invoice ~0.5 MB)
- Structure: Slovak invoices with IČO, DIČ, invoice number

### ⚠️ Not supported:
- Invoice images (JPG, PNG) - please convert to PDF
- Word documents (DOC, DOCX)
- Excel files (XLS, XLSX)
- Zipped files

---

## How to Check Invoice Was Processed

### Method 1: Desktop Application (Recommended)

1. Launch **"NEX Invoice Manager"** from desktop icon
2. Invoice appears in list (automatic refresh)
3. Click invoice for details

### Method 2: Automatic Confirmation (Planned)

In future you will receive automatic email confirmation that invoice was successfully processed.

### Method 3: Contact Support

If you need to verify invoice was processed, contact:

**Support:**  
📧 Email: [SUPPORT_EMAIL]  
📞 Tel: [SUPPORT_PHONE]

---

## What Happens to Invoice

After successful processing:

1. **PDF invoice** - saved on server
2. **ISDOC XML** - generated for NEX Genesis
3. **SQLite database** - record created for history
4. **PostgreSQL staging** - prepared for NEX Genesis import
5. **Desktop application** - displayed in invoice list

**Invoice is ready for import into NEX Genesis system.**

---

## Frequently Asked Questions (FAQ)

### Can I send same invoice multiple times?

Yes, system automatically detects duplicate invoices. If you send same invoice twice, system processes it only once and informs you about duplicate.

### How long does processing take?

Typically **30-60 seconds** after sending email. For large invoices (5+ MB) it may take up to 2 minutes.

### What if wrong email arrives?

System only processes PDF attachments. If email has no PDF attachment or PDF is not an invoice, system ignores it.

### Can I send multiple invoices at once?

Yes, you can attach multiple PDF files to one email. Each invoice will be processed separately.

### Does it work on weekends?

Yes, system runs 24/7 and processes invoices whenever they arrive.

### Can I edit invoice in desktop application?

Currently no - application is view-only. Editing and export to NEX Genesis is planned for future versions.

### Where are invoices stored?

All invoices are securely stored on server in [CUSTOMER] office. Automatically backed up.

---

## What to Do If Problem Occurs

### Problem symptoms:

- Invoice not processed after 5 minutes
- Received error email from system
- Invoice has incorrect data
- Desktop application won't launch
- Invoice not showing in application

### Problem procedure:

1. **Wait 5 minutes** - system may be temporarily busy
2. **Refresh desktop application** - close and relaunch
3. **Try sending again** - problem may be temporary
4. **Contact support:**
   - 📧 Email: **[SUPPORT_EMAIL]**
   - 📞 Phone: **[SUPPORT_PHONE]**
   - Send:
     - Original invoice (PDF)
     - Time when you sent it
     - Screenshot of error (if any)
     - Problem description

**Support responds within 24 hours on business days.**

---

## Security and Data Protection

### Where is my data?

- All invoices stored **locally on your server** in office
- No data sent to cloud (except Gmail email)
- Server access only for authorized employees

### Who has access to invoices?

- Only [CUSTOMER] employees with server access
- [SUPPORT_COMPANY] (technical support) - only on request for troubleshooting

### How are passwords protected?

- All passwords encrypted
- API keys randomly generated
- Database access password-protected

---

## Technical Details (For IT Department)

### System Architecture:

- **Email endpoint:** [INVOICE_EMAIL]
- **n8n Workflow:** n8n-SupplierInvoiceEmailLoader ([SERVER_LOCATION])
- **API endpoint:** [API_URL]
- **Service:** NEXAutomat (Windows Service on [CUSTOMER] server)
- **Database:** SQLite + PostgreSQL staging
- **Desktop App:** PyQt5 GUI (Python 3.13)
- **Monitoring:** Health check - [API_URL]/health

### File Locations ([CUSTOMER] Server):

```
C:\Deployment\nex-automat\
├── apps\
│   ├── supplier-invoice-loader\        # Backend service
│   │   ├── config\invoices.db          # SQLite database
│   │   ├── data\pdf\                   # PDF invoices
│   │   └── data\xml\                   # ISDOC XML files
│   │
│   └── supplier-invoice-editor\        # Desktop application
│       ├── config\config.yaml          # Configuration
│       └── logs\                       # Application logs
│
└── logs\                               # Service logs
```

### Backup:

- **PDF invoices:** `C:\Deployment\nex-automat\apps\supplier-invoice-loader\data\pdf\`
- **XML files:** `C:\Deployment\nex-automat\apps\supplier-invoice-loader\data\xml\`
- **SQLite DB:** `C:\Deployment\nex-automat\apps\supplier-invoice-loader\config\invoices.db`
- **PostgreSQL:** Automatic PostgreSQL backup
- **Recommendation:** Daily backup of entire `C:\Deployment\nex-automat\`

### Error Notifications:

Email notifications about errors sent to: **[SUPPORT_EMAIL]**

### API Key:

For API access, n8n workflow uses API key: [API_KEY] (not needed to know)

### Windows Services:

```
NEXAutomat           - Invoice processing service
postgresql-x64-15    - Database server
Cloudflared[CUSTOMER] - Tunnel service (public access)
```

All services set to **Automatic** start.

### Monitoring:

```bash
# Health check (curl or browser)
[API_URL]/health

# Expected response:
{"status":"healthy","timestamp":"YYYY-MM-DDTHH:MM:SS"}
```

### Service Restart (if needed):

```powershell
# PowerShell (Run as Administrator)
Restart-Service NEXAutomat
Get-Service NEXAutomat  # Verify Running
```

---

## Version History

### Version [VERSION] ([DATE]) - [STATUS]
- ✅ List of changes and improvements

---

## Planned Improvements (Roadmap)

### Version [NEXT_VERSION]
- List of planned features and improvements

---

## Contact

**[SUPPORT_COMPANY] - NEX Automat Support**

📧 Email: [SUPPORT_EMAIL]  
📞 Tel: [SUPPORT_PHONE]  
🌐 Web: [SUPPORT_WEB]  
📍 Address: [SUPPORT_ADDRESS]

**Business hours:**
- Monday - Friday: 8:00 - 16:00
- Weekend: Email support (response on business day)

**Emergency contact:** [SUPPORT_EMAIL] (24/7 for critical issues)

---

## Appendices

### Appendix A: Sample Email for Sending Invoice

```
To: [INVOICE_EMAIL]
Subject: Invoice from supplier XY
Attachments: invoice_12345.pdf

Email text (optional):
Invoice No. 12345 from supplier XY.
```

### Appendix B: Desktop Application Screenshot

(Available in desktop application - Help → Documentation)

### Appendix C: Supported PDF Formats

- PDF/A (recommended for archival)
- PDF 1.4 - 1.7
- Text PDF (not scanned images)

---

## Conclusion

**NEX Automat** is a fully functional system for automatic processing of supplier invoices.

**For regular use:**
1. Send invoices to **[INVOICE_EMAIL]**
2. Monitor processed invoices in **"NEX Invoice Manager"** desktop application
3. Contact **[SUPPORT_EMAIL]** for problems

**System runs 24/7 and is fully automatic.**

---

**Thank you for using NEX Automat!** 🚀

**Document version:** [VERSION]  
**Last update:** [DATE]  
**Status:** [STATUS]  
**Author:** [SUPPORT_COMPANY] Development Team

---

## Placeholders to Replace

Replace these placeholders when creating customer-specific guide:

- `[CUSTOMER_NAME]` - Customer company name
- `[VERSION]` - System version (e.g., 2.1)
- `[DATE]` - Current date
- `[STATUS]` - Status (e.g., Production, Testing)
- `[INVOICE_EMAIL]` - Invoice receiving email address
- `[SUPPORT_EMAIL]` - Support email address
- `[SUPPORT_PHONE]` - Support phone number
- `[SUPPORT_COMPANY]` - Support company name
- `[SUPPORT_WEB]` - Support website
- `[SUPPORT_ADDRESS]` - Support address
- `[SERVER_LOCATION]` - Server location description
- `[API_URL]` - API endpoint URL
- `[API_KEY]` - API key (partial, for reference)
- `[NEXT_VERSION]` - Next planned version number
