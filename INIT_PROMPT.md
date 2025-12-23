INIT PROMPT - Fix pg8000 list index out of range

Projekt: nex-automat
Current Status: pg8000 INSERT RETURNING zlyhá
Developer: Zoltán (40 rokov skúseností)
Jazyk: Slovenčina

⚠️ KRITICKÉ: Dodržiavať pravidlá z memory_user_edits!

🎯 CURRENT FOCUS: Opraviť "list index out of range" chybu v pg8000 kóde

## Čo je hotové ✅

| Komponenta | Status |
|------------|--------|
| nex-staging pg8000 migrácia | ✅ DONE |
| Deployment Mágerstav | ✅ DONE |
| config_customer.py cesty | ✅ DONE |
| DB supplier_invoice_staging | ✅ DONE |
| E2E test | ❌ FAIL - list index out of range |

## Problém

```
[WARN] PostgreSQL staging error: list index out of range
```

Chyba nastáva pri INSERT RETURNING v StagingClient.insert_invoice_with_items()

## Pravdepodobná príčina

V `connection.py` Pg8000Cursor.fetchone():
```python
def fetchone(self):
    if self._row_index >= len(self._rows):
        return None
    row = self._rows[self._row_index]  # <- možno prázdne self._rows
```

## Next Steps

1. [ ] Pozrieť stderr log na serveri pre full traceback
2. [ ] Analyzovať Pg8000Cursor implementáciu
3. [ ] Opraviť fetchone() pre RETURNING queries
4. [ ] Test na Development
5. [ ] Deploy a E2E test

## RAG Query

```
https://rag-api.icc.sk/search?query=nex-staging+connection+Pg8000Cursor+fetchone&limit=5
```
