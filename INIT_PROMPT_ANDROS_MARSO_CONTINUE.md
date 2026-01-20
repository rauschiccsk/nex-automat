# INIT PROMPT - ANDROS MARSO Extractor Continuation

**Projekt:** nex-automat v3.0
**Úloha:** Dokončiť MARSO extractor testovanie pre ANDROS
**Developer:** Zoltán Rausch
**Dátum:** 2026-01-20

---

## 🎯 CIEĽ SESSION

Dokončiť end-to-end testovanie MARSO faktúr na ANDROS Windows VM.

---

## ✅ DOKONČENÉ (predchádzajúca session)

### MARSO Extractor
- [x] `marso_extractor.py` vytvorený (472 riadkov)
- [x] Detekcia a routing v `main.py`
- [x] Lokálny test: 69 položiek, 26295.71 EUR
- [x] ISDOC XML generovanie OK

### Config Opravy
- [x] `STAGING_DIR`, `NEX_DATA_PATH` pridané do template
- [x] Unicode emoji → ASCII text (cp1250)
- [x] Git commits pushed (3231d34, be5cfd2, f00835d)

### ANDROS Setup
- [x] `config_customer.py` vytvorený
- [x] Všetky 3 Windows Services bežia
- [x] API health OK (port 8001)

### E2E Test - Čiastočný
- [x] Email polling funguje (mail.webglobe.sk)
- [x] 2 MARSO faktúry detekované a spracované
- [x] POST /invoice vrátil 200 OK
- [ ] **PENDING:** Overiť PostgreSQL záznamy
- [ ] **PENDING:** Overiť súbory v adresároch

---

## ⏳ ZOSTÁVA DOKONČIŤ

### Fáza 1: Overenie E2E testu
- [ ] Skontrolovať PostgreSQL (supplier_invoice_heads)
- [ ] Skontrolovať súbory v C:\ANDROS\NEX\IMPORT\
- [ ] Ak faktúry chýbajú, poslať nový test email

### Fáza 2: Nový E2E test (ak treba)
- [ ] Poslať MARSO PDF na andros.invoices@icc.sk
- [ ] Sledovať logy
- [ ] Overiť vytvorené PDF/XML súbory
- [ ] Overiť PostgreSQL záznamy

### Fáza 3: (Voliteľné) ICC Deployment
- [ ] Git clone C:\ICC\nex-automat\
- [ ] Setup venv + config
- [ ] Windows Services
- [ ] Testovanie

---

## 🖥️ PRÍSTUPY

### Windows VM (ANDROS + ICC)
```
RDP: 100.107.134.104 (Tailscale)
User: Administrator
```

### Ubuntu Host
```bash
ssh andros@192.168.100.23
# Password: Andros-2026
```

### PostgreSQL
```bash
docker exec -it andros-postgres psql -U nex_admin -d nex_automat
```

---

## 📊 PORT MAPPING

| Service | ANDROS | ICC |
|---------|--------|-----|
| PostgreSQL | 5432 | 5433 |
| Temporal | 7233 | 7234 |
| Temporal UI | 8080 | 8082 |
| FastAPI Loader | 8001 | 8002 |

---

## 🚀 ZAČAŤ S

### 1. Overiť PostgreSQL záznamy

Na Ubuntu host:
```bash
docker exec -it andros-postgres psql -U nex_admin -d nex_automat -c "SELECT id, xml_invoice_number, file_status, created_at FROM supplier_invoice_heads ORDER BY id DESC LIMIT 5;"
```

### 2. Overiť súbory na Windows VM

```powershell
Get-ChildItem "C:\ANDROS\NEX\IMPORT\SUPPLIER-INVOICES" -Recurse
Get-ChildItem "C:\ANDROS\NEX\IMPORT\SUPPLIER-STAGING" -Recurse
```

---

## 📋 KNOWLEDGE DOKUMENTY

- `KNOWLEDGE_2026-01-20_marso-extractor-andros.md` - Táto session
- `KNOWLEDGE_2025-12-22_project-structure.md` - Projektová štruktúra
- `N8N_TO_TEMPORAL_MIGRATION.md` - Temporal architektúra

---

## ⚠️ ZNÁME PROBLÉMY

1. **Prvý E2E test** - 2 faktúry boli spracované pred opravou config, súbory môžu byť na nesprávnom mieste alebo chýbať
2. **Položky** - MARSO extraktor extrahuje 69/80 položiek (niektoré cez viac strán)
3. **config_customer.py** - nie je v Git (obsahuje heslá), treba vytvoriť manuálne