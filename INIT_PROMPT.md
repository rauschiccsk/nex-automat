# INIT PROMPT - NEX Automat v3.2

**Projekt:** nex-automat
**Zákazník:** Mágerstav s.r.o.
**Verzia:** v3.2 - Supplier Invoice Staging Web
**Developer:** Zoltán (40 rokov skúseností)
**Jazyk:** Slovenčina

⚠️ **KRITICKÉ:** Dodržiavať pravidlá z memory_user_edits!

---

## 🎯 CURRENT STATUS

✅ Deployment v3.2 kompletný - Web UI funguje na http://localhost:8001/app

---

## ✅ Čo je hotové

| Komponenta | Status |
|------------|--------|
| Backend API (8001) | ✅ |
| Temporal workflows | ✅ |
| Web UI frontend | ✅ |
| Windows služby | ✅ |
| PostgreSQL staging | ✅ |

---

## 📋 Možné next steps

1. Doladiť UI (chýbajúce polia v hlavičke faktúry)
2. Implementovať schvaľovací workflow
3. Import do NEX Genesis
4. Deploy na ANDROS

---

## 🔧 Porty Mágerstav

| Služba | Port |
|--------|------|
| NEX-SupplierInvoiceLoader | 8001 |
| Temporal Server | 7233 |
| Temporal UI | 8233 |
| PostgreSQL | 5432 |

---

## 🔍 RAG Query

```
https://rag-api.icc.sk/search?query=staging+web+deployment+magerstav&limit=5
```

---

## 📁 Cesty

**Dev:** C:\Development\nex-automat\
**Mágerstav:** C:\Deployment\nex-automat\
**Web UI:** http://localhost:8001/app
