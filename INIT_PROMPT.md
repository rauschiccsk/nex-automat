INIT PROMPT - Supplier Invoice Staging Verification

Projekt: nex-automat
Current Status: Fáza D Complete, Documentation Updated
Developer: Zoltán (40 rokov skúseností)
Jazyk: Slovenčina
Previous Session: 2025-12-22

⚠️ KRITICKÉ: Dodržiavať pravidlá z memory_user_edits!

🎯 CURRENT FOCUS: Verify GUI compatibility with DB changes

## Čo je hotové ✅

| Komponenta | Status |
|------------|--------|
| Temporal validácia (14/14 XML) | ✅ PASSED |
| n8n zastavený | ✅ DONE |
| Fáza A - DB zmeny | ✅ DONE |
| Fáza B - Adresáre | ✅ DONE |
| Fáza C - Kód loader | ✅ DONE |
| Fáza D - File Mover | ✅ DONE |
| RAG dokumentácia | ✅ DONE |

## Pending Tasks

1. [ ] Overiť invoice_repository.py kompatibilitu s novými DB stĺpcami
2. [ ] Deploy na Mágerstav
3. [ ] E2E test - poslať faktúru cez email

## RAG Query

```
https://rag-api.icc.sk/search?query=invoice_repository+supplier_invoice_heads+file_status&limit=5
```

Session Priority: GUI verification → Deploy → E2E Test
