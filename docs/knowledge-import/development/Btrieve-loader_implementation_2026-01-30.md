# Btrieve-Loader Session Knowledge

## Dokončené dnes

### Fázy implementácie
| Fáza | Commit | Popis |
|------|--------|-------|
| 1 | eaf2edb | Core + Schemas |
| 2 | e02e11b | REST API Routes |
| 3 | 4761247 | main.py refaktor + Legacy |
| 4 | f04a960 | Unit testy (67 testov) |

### Bugfixy
| Commit | Popis |
|--------|-------|
| 4f9cfb6 | MGLST 134-byte support |
| 6c5eda9 | stores schema level >= 0 |
| 2ecaf75 | TSH Pascal ShortString parser |
| 8a88b31 | TSH hybrid fixed pascal fields |
| 6d64264 | TSH amounts hardcoded offsets |
| 964b071 | TSH fixed-width DocNum/ExtNum pre správny doc_date offset |

### Integration test - KOMPLETNÝ
| Endpoint | Status | Záznamov |
|----------|--------|----------|
| Products | ✅ | 10,000 |
| Partners | ✅ | 226 |
| Barcodes | ✅ | OK |
| Stores | ✅ | 28 |
| Documents | ✅ | 7, doc_date OK |

## Zostávajúce issues (nízka priorita)

| Issue | Priorita | Popis |
|-------|----------|-------|
| pab_address prefix | 🔵 Nízka | \u000e prefix v adrese |
| Encoding UTF-8 | 🔵 Nízka | CP852 → UTF-8 konverzia |
| TSI (položky) test | 🔵 Nízka | /documents/{id}/items |
| CI/CD nezávislé deploy | ⚠️ Stredná | Ak jeden runner offline, blokuje všetko |

## Kľúčové technické zistenia

### NEX Genesis Btrieve formáty
1. **Pascal ShortString**: [1-byte length][N-bytes data]
2. **Hybrid fixed pascal**: [1-byte length][fixed-width buffer] - ignorovať length, čítať celý buffer
3. **DateType**: INT16 (nie INT32) - dni od 1899-12-30
4. **Amounts**: Na neštandardných offsetoch (0x0215, 0x023d, 0x0245), nie 4-byte aligned

### TSH štruktúra (opravená)
```
Offset | Veľkosť | Pole
-------|---------|------
0x0000 | 4       | doc_id
0x0004 | 13      | doc_number (fixed)
0x0011 | 13      | reference (fixed)
0x001e | 2       | doc_date (INT16)
0x0020 | 2       | warehouse_code
0x0022 | 4       | pab_code
0x0026 | 30      | pab_name (hybrid)
```

### CI/CD poznámky
- ANDROS runner beží v Docker kontajneri: `myoung34/github-runner:latest`
- Config: `/opt/nex-automat-src/docker-compose.runner.yml`
- Po reštarte servera treba spustiť runner kontajner manuálne

## Súbory

### Deployment
- MAGER: `C:\Deployment\nex-automat`
- Windows Service: `NEX-BtrieveLoader` (port 8001)
- Python venv: `C:\Deployment\nex-automat\venv32` (32-bit)

### Kód
- Btrieve-Loader: `apps/btrieve-loader/`
- nexdata models: `packages/nexdata/nexdata/models/`
- TSH parser: `packages/nexdata/nexdata/models/tsh.py`

### Dokumentácia
- RAG: `docs/knowledge/btrieve-loader-api.md`