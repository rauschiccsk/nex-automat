# NEX Automat - Prevádzková príručka

**Zákazník:** [ZÁKAZNÍK]  
**Systém:** Supplier Invoice Loader  
**Verzia:** [VERZIA]  
**Dátum:** [YYYY-MM-DD]

---

## Obsah

1. [Prehľad systému](#1-prehľad-systému)
2. [Denné operácie](#2-denné-operácie)
3. [Správa služby](#3-správa-služby)
4. [Monitoring](#4-monitoring)
5. [Zálohovanie](#5-zálohovanie)
6. [Údržba](#6-údržba)
7. [Bezpečnosť](#7-bezpečnosť)

---

## 1. Prehľad systému

### 1.1 Čo systém robí

NEX Automat automaticky spracováva dodávateľské faktúry:

```
PDF faktúra → OCR spracovanie → Extrakcia dát → Uloženie do DB → Export do NEX Genesis
```

### 1.2 Komponenty

| Komponent       | Popis              | Umiestnenie                    |
| --------------- | ------------------ | ------------------------------ |
| Windows Service | NEX-Automat-Loader | Windows Services               |
| Databáza        | PostgreSQL 15+     | localhost:5432                 |
| Aplikácia       | Python FastAPI     | C:\Deployment\nex-automat      |
| Logy            | Aplikačné logy     | C:\Deployment\nex-automat\logs |

### 1.3 Priečinky

```
C:\Deployment\nex-automat\
├── apps\supplier-invoice-loader\    # Hlavná aplikácia
│   ├── config\config.yaml           # Konfigurácia
│   └── tests\samples\               # Testovacie PDF
├── logs\                            # Aplikačné logy
├── backups\                         # Zálohy databázy
├── scripts\                         # Správcovské skripty
└── test_results\                    # Výsledky testov
```

---

## 2. Denné operácie

### 2.1 Ranná kontrola (5 minút)

**Každý pracovný deň ráno vykonajte:**

1. **Skontrolujte stav služby:**

   ```powershell
   cd C:\Deployment\nex-automat
   python scripts\manage_service.py status
   ```

   Očakávaný výstup: `SERVICE_RUNNING`

2. **Skontrolujte posledné logy:**

   ```powershell
   python scripts\manage_service.py logs
   ```

   Hľadajte: Žiadne ERROR alebo CRITICAL správy

3. **Skontrolujte disk:**

   ```powershell
   Get-PSDrive C | Select-Object Used, Free
   ```

   Požadované: Minimálne 10 GB voľné

### 2.2 Spracovanie faktúr

**Systém automaticky:**

- Monitoruje vstupný priečinok
- Spracováva nové PDF faktúry
- Ukladá dáta do databázy
- Exportuje do NEX Genesis

**Manuálne nie je potrebné nič robiť** - systém beží automaticky.

### 2.3 Kontrola spracovania

**Overenie že faktúry boli spracované:**

1. Skontrolujte logy pre úspešné spracovanie
2. Overte dáta v NEX Genesis
3. Pri problémoch pozrite sekciu Troubleshooting

---

## 3. Správa služby

### 3.1 Základné príkazy

Všetky príkazy spúšťajte v **PowerShell ako Administrátor**:

```powershell
cd C:\Deployment\nex-automat

# Zistiť stav
python scripts\manage_service.py status

# Spustiť službu
python scripts\manage_service.py start

# Zastaviť službu
python scripts\manage_service.py stop

# Reštartovať službu
python scripts\manage_service.py restart

# Zobraziť logy (posledných 50 riadkov)
python scripts\manage_service.py logs

# Sledovať logy naživo
python scripts\manage_service.py tail
```

### 3.2 Kedy reštartovať službu

Reštartujte službu ak:

- Služba nereaguje dlhšie ako 5 minút
- Vysoké využitie pamäte (>500 MB)
- Po zmene konfigurácie
- Po aktualizácii systému

### 3.3 Automatický reštart

Služba je nakonfigurovaná na automatický reštart pri:

- Zlyhaní služby
- Reštarte servera

Nie je potrebná manuálna intervencia.

---

## 4. Monitoring

### 4.1 Čo sledovať

| Metrika         | Normálna hodnota | Kritická hodnota |
| --------------- | ---------------- | ---------------- |
| Service status  | RUNNING          | STOPPED          |
| Memory usage    | <200 MB          | >500 MB          |
| Disk space      | >50 GB           | <10 GB           |
| Error rate      | 0%               | >5%              |
| Processing time | <3s/faktúra      | >10s/faktúra     |

### 4.2 Kontrolné príkazy

**Kompletná diagnostika:**

```powershell
python scripts\preflight_check.py
```

**Performance test:**

```powershell
python scripts\performance_tests.py
```

**Error handling test:**

```powershell
python scripts\error_handling_tests.py
```

### 4.3 Kde hľadať problémy

1. **Aplikačné logy:** `logs\service-*.log`
2. **Windows Event Viewer:** Application → NEX-Automat
3. **Test results:** `test_results\*.json`

---

## 5. Zálohovanie

### 5.1 Automatické zálohy

- **Frekvencia:** Denne o 02:00
- **Umiestnenie:** `C:\Deployment\nex-automat\backups\`
- **Retencia:** 7 dní

### 5.2 Manuálna záloha

**Pred dôležitými zmenami vytvorte zálohu:**

```powershell
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupFile = "C:\Deployment\nex-automat\backups\manual_$timestamp.sql"

pg_dump -h localhost -U postgres -d invoice_staging -f $backupFile
```

### 5.3 Kontrola záloh

**Týždenne skontrolujte:**

```powershell
dir C:\Deployment\nex-automat\backups\*.sql
```

Overte že:

- Zálohy existujú za posledných 7 dní
- Veľkosť záloh je rozumná (nie 0 KB)

---

## 6. Údržba

### 6.1 Týždenná údržba

**Každý piatok:**

1. **Vymazať staré logy:**

   ```powershell
   # Ponechať len posledných 7 dní
   Get-ChildItem logs\*.log | 
   Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-7) } | 
   Remove-Item
   ```

2. **Skontrolovať veľkosť databázy:**

   ```powershell
   psql -h localhost -U postgres -d invoice_staging -c "
   SELECT pg_size_pretty(pg_database_size('invoice_staging'));"
   ```

3. **Spustiť diagnostiku:**

   ```powershell
   python scripts\preflight_check.py
   ```

### 6.2 Mesačná údržba

**Prvý pondelok v mesiaci:**

1. **Test obnovy zo zálohy** (na testovacom prostredí)
2. **Kontrola diskového priestoru**
3. **Review logov za posledný mesiac**
4. **Aktualizácia dokumentácie ak potrebné**

### 6.3 Aktualizácie systému

**Aktualizácie vykonáva ICC Komárno:**

1. Kontaktujte podporu pre aktualizáciu
2. Dohodnite termín (mimo pracovnej doby)
3. ICC vykoná aktualizáciu vzdialene
4. Overíte funkčnosť po aktualizácii

---

## 7. Bezpečnosť

### 7.1 Prístupové údaje

| Systém     | Používateľ | Kde je heslo         |
| ---------- | ---------- | -------------------- |
| Windows    | Admin      | IT správa            |
| PostgreSQL | postgres   | Environment variable |
| Aplikácia  | -          | Bez autentifikácie   |

### 7.2 Bezpečnostné pravidlá

- **Nezdieľajte** prístupové údaje
- **Nemeňte** konfiguráciu bez konzultácie s dodávateľom
- **Hlášte** podozrivé aktivity
- **Zálohy** uchovávajte bezpečne

### 7.3 Prístup k serveru

- Len autorizovaní pracovníci
- Len cez zabezpečené pripojenie (RDP cez VPN)
- Logujte prístupy

---

## Quick Reference Card

### Najčastejšie príkazy

```powershell
# Prejsť do adresára
cd C:\Deployment\nex-automat

# Stav služby
python scripts\manage_service.py status

# Reštart služby
python scripts\manage_service.py restart

# Logy
python scripts\manage_service.py logs

# Diagnostika
python scripts\preflight_check.py
```

### Kedy volať podporu

| Situácia              | Urgencia | Kontakt |
| --------------------- | -------- | ------- |
| Služba nebeží >30 min | Vysoká   | Telefón |
| Chyby v spracovaní    | Stredná  | Email   |
| Otázky                | Nízka    | Email   |

### Kontakt na podporu

**[DODÁVATEĽ]**

- Email: [EMAIL]
- Telefón: [TELEFÓN]
- Pracovná doba: Po-Pi 8:00-16:00

---

## Prílohy

### A. Checklist denná kontrola

```
[ ] Service status = RUNNING
[ ] Žiadne ERROR v logoch
[ ] Disk space > 10 GB
[ ] Faktúry spracované
```

### B. Checklist týždenná údržba

```
[ ] Staré logy vymazané
[ ] Zálohy existujú (7 dní)
[ ] Diagnostika OK
[ ] Veľkosť DB skontrolovaná
```

---

**Dokument vytvorený:** [YYYY-MM-DD]  
**Posledná aktualizácia:** [YYYY-MM-DD]  
**Verzia:** 1.0
