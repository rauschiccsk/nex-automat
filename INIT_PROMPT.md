INIT PROMPT - nex-staging Package Migration

Projekt: nex-automat
Current Status: Package vytvorený, loader inštalácia zlyháva
Developer: Zoltán (40 rokov skúseností)
Jazyk: Slovenčina

⚠️ KRITICKÉ: Dodržiavať pravidlá z memory_user_edits!

🎯 CURRENT FOCUS: Vyriešiť pg8000/psycopg2 kompatibilitu pre venv32

## Čo je hotové ✅

| Komponenta | Status |
|------------|--------|
| nex-staging package | ✅ DONE |
| supplier-invoice-staging migrácia | ✅ DONE |
| supplier-invoice-loader import update | ✅ DONE |
| nex-shared cleanup | ✅ DONE |
| Loader test vo venv32 | ❌ FAIL - psycopg2 |

## Problém

supplier-invoice-loader používa venv32 (32-bit Python pre Btrieve DLL).
psycopg2-binary nefunguje v 32-bit Python.
Loader pôvodne používal pg8000.

## Riešenie

Upraviť nex-staging aby podporoval pg8000 (už v connection.py je základ).

## Pending Tasks

1. [ ] Upraviť nex-staging pre pg8000 kompatibilitu
2. [ ] Test loader vo venv32
3. [ ] Git commit všetkých zmien
4. [ ] Deploy na Mágerstav

## RAG Query

```
https://rag-api.icc.sk/search?query=nex-staging+supplier_invoice_heads+StagingClient&limit=5
```
