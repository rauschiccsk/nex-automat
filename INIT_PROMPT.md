# INIT PROMPT - NEX Automat v3.2 Deployment

**Projekt:** nex-automat
**Zákazník:** Mágerstav s.r.o.
**Verzia:** v3.2 - Supplier Invoice Staging Web
**Developer:** Zoltán (40 rokov skúseností)
**Jazyk:** Slovenčina

⚠️ **KRITICKÉ:** Dodržiavať pravidlá z memory_user_edits!

---

## 🎯 CURRENT FOCUS

Deployment v3.2 na server Mágerstav - supplier-invoice-staging-web s reálnym backendom.

---

## ✅ Čo je hotové (Dev PC)

| Komponenta | Status |
|------------|--------|
| staging_routes.py endpointy | ✅ |
| pg8000 named params fix | ✅ |
| Frontend /staging/* endpointy | ✅ |
| Mock data disabled | ✅ |
| NEX Brain na port 8003 | ✅ |

---

## 📋 Next Steps - Deployment

1. Git commit a push
2. Pull na Mágerstav server
3. Reinstall nex-staging package (pg8000 fix)
4. Reštart SupplierInvoiceLoader služby
5. Test /staging/invoices endpoint
6. Build a deploy frontend (ak potrebné)

---

## 🔧 Porty Mágerstav

| Služba | Port |
|--------|------|
| supplier-invoice-loader | 8001 |
| Temporal Server | 7233 |
| Temporal UI | 8233 |
| PostgreSQL | 5432 |

---

## 🔍 RAG Query

```
https://rag-api.icc.sk/search?query=magerstav+deployment+nssm+services&limit=5
```

---

## 📁 Cesty

**Dev:** C:\Development\nex-automat\
**Mágerstav:** C:\Deployment\nex-automat\
