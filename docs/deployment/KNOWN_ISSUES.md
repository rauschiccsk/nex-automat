# Known Issues & Solutions - NEX Automat v2.0

**Generated:** 2025-11-22 12:28:38  
**Based on:** DAY 4 Testing (2025-11-22)

---

## Critical Issues Fixed During DAY 4

### 1. Missing pdfplumber (CRITICAL)

- **Symptom:** ModuleNotFoundError: No module named 'pdfplumber'
- **Fix:** pip install pdfplumber
- **Status:** Added to requirements.txt

### 2. Missing pg8000 (CRITICAL)

- **Symptom:** PostgreSQL staging error: pg8000 package not installed
- **Fix:** pip install pg8000
- **Status:** Added to requirements.txt

### 3. Missing LS_API_KEY (CRITICAL)

- **Symptom:** 422 - Missing X-API-Key header
- **Fix:** setx LS_API_KEY "your_key"
- **Status:** Documented in DEPLOYMENT_GUIDE.md

### 4. POSTGRES_PASSWORD not set (CRITICAL)

- **Symptom:** password authentication failed for user "postgres"
- **Fix:** setx POSTGRES_PASSWORD "your_password"
- **Status:** Documented in DEPLOYMENT_GUIDE.md

---

## Pre-Deployment Checklist

Before deploying to customer, verify:

- [ ] All dependencies in requirements.txt installed
- [ ] POSTGRES_PASSWORD environment variable set
- [ ] LS_API_KEY environment variable set  
- [ ] PostgreSQL 15+ running
- [ ] Run: python scripts/prepare_deployment.py

---

## Performance Notes

- Sequential processing only (SQLite limitation)
- ~5 seconds per invoice (acceptable)
- Health endpoint: 6ms average (excellent)

---

**Document Version:** 1.0  
**Last Updated:** 2025-11-22
