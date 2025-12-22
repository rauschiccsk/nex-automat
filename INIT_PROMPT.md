INIT PROMPT - File Mover Service Implementation

Projekt: nex-automat
Current Status: Phase 6 Complete, File Organization Fázy A-C Done
Developer: Zoltán (40 rokov skúseností)
Jazyk: Slovenčina
Previous Session: 2025-12-22

⚠️ KRITICKÉ: Dodržiavať pravidlá z memory_user_edits!

🎯 CURRENT FOCUS: Fáza D - File Mover Service

## Čo je hotové ✅

| Komponenta | Status |
|------------|--------|
| Temporal validácia (14/14 XML) | ✅ PASSED |
| n8n zastavený | ✅ DONE |
| Temporal produkcia | ✅ Running |
| Fáza A - DB zmeny | ✅ DONE |
| Fáza B - Adresáre | ✅ DONE |
| Fáza C - Kód loader | ✅ DONE |

## Nová adresárová štruktúra

```
C:\NEX\IMPORT\SUPPLIER-INVOICES\  <- received
C:\NEX\IMPORT\SUPPLIER-STAGING\   <- staged
C:\NEX\YEARACT\ARCHIV\SUPPLIER-INVOICES\PDF|XML\  <- archived
```

## Fáza D Tasks

1. [ ] Vytvoriť File Mover Service
2. [ ] Presun received → staged (po PostgreSQL uložení)
3. [ ] Presun staged → archived (po NEX Genesis importe)
4. [ ] Premenovanie na finálny názov pri archivácii

## Fáza E Tasks

1. [ ] Migračný skript pre existujúce súbory z LS/PDF a LS/XML

## RAG Query

```
https://rag-api.icc.sk/search?query=file+mover+service+staging+archive&limit=5
```

Session Priority: File Mover Service → Migrácia → Testovanie
