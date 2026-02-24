# Session: RAG Cleanup & Telegram Tokens

**Dátum:** 2025-12-25
**Status:** ✅ DONE

---

## Dokončené úlohy

### 1. Telegram Bot Tokeny ✅
- Všetky 3 boty mali neplatné tokeny (401 Unauthorized)
- Revokované a vygenerované nové tokeny cez @BotFather
- Aktualizovaný `.env` súbor v `apps/nex-brain/telegram/`
- Aktualizovaný `CREDENTIALS.md` v RAG

**Nové tokeny:**
| Bot | Username |
|-----|----------|
| Admin | @ai_dev_automatin_bot |
| ICC | @NexBrainIcc_bot |
| ANDROS | @NexBrainAndros_bot |

### 2. RAG Cleanup ✅
- Problém: RAG indexoval celý `docs/` vrátane `archive/` a `deployment/`
- Staré dokumenty s `invoice_staging` spôsobovali zmätok
- Opravený `tools/rag/rag_update.py` - `--all` teraz indexuje len `docs/knowledge/`
- RAG vyčistený a reindexovaný (34 dokumentov, 66 chunks)

### 3. Dokumentácia ✅
- Vytvorené popisy pre supplier-invoice-loader a supplier-invoice-worker
- Opravené File Storage cesty v dokumentácii

## Dôležité zmeny

### rag_update.py
```python
# PRED (zlé)
directory=self.docs_path  # indexovalo celý docs/

# PO (správne)  
directory=self.knowledge_path  # indexuje len docs/knowledge/
```

### Databázy (aktuálny stav)
- **SQLite:** `invoices.db` - duplicate detection (stále používané)
- **PostgreSQL:** `supplier_invoice_staging` - hlavná staging DB
- **VYMAZANÉ z RAG:** `invoice_staging`, `invoices_pending`, `invoice_items_pending`

## Dôležité príkazy

```powershell
# RAG full reindex (len docs/knowledge/)
python tools/rag/rag_update.py --all

# RAG incremental (nové súbory dnes)
python tools/rag/rag_update.py --new

# RAG stats
python tools/rag/rag_update.py --stats

# Telegram boty
cd apps/nex-brain/telegram
python multi_bot.py
```

## Next Steps

1. Cleanup script pre testovanie na Mágerstav (SQLite + PostgreSQL)
2. ANDROS deployment planning
3. Fáza 5: Btrieve Models (TSH/TSI/PLS/RPC)
