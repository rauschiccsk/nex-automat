# NEX Automat v2.0 - Obnovovacie postupy

**Zákazník:** Mágerstav s.r.o.  
**Systém:** Supplier Invoice Loader  
**Verzia:** 2.0.0  
**Dátum:** 2025-11-24  

---

## Obsah

1. [Rýchly prehľad](#1-rýchly-prehľad)
2. [Reštart služby](#2-reštart-služby)
3. [Zálohovanie a obnova databázy](#3-zálohovanie-a-obnova-databázy)
4. [Rollback postupy](#4-rollback-postupy)
5. [Núdzové postupy](#5-núdzové-postupy)
6. [Riešenie problémov](#6-riešenie-problémov)
7. [Kontakty](#7-kontakty)

---

## 1. Rýchly prehľad

### Kritické príkazy (Admin PowerShell)

```powershell
# Umiestnenie
cd C:\Deployment\nex-automat

# Stav služby
python scripts\manage_service.py status

# Reštart služby
python scripts\manage_service.py restart

# Posledné logy
python scripts\manage_service.py logs

# Kontrola systému
python scripts\day5_preflight_check.py
```

### Dôležité súbory

| Súbor | Účel |
|-------|------|
| `config/config.yaml` | Hlavná konfigurácia |
| `logs/service-*.log` | Aplikačné logy |
| `backups/` | Zálohy databázy |
| `scripts/manage_service.py` | Správa služby |

---

## 2. Reštart služby

### 2.1 Štandardný reštart

**Kedy použiť:** Služba nereaguje, pomalé spracovanie, po zmene konfigurácie

**Postup:**
1. Otvorte PowerShell ako Administrátor
2. Spustite príkazy:

```powershell
cd C:\Deployment\nex-automat
python scripts\manage_service.py restart
```

3. Overte stav:
```powershell
python scripts\manage_service.py status
```

**Očakávaný výstup:** `SERVICE_RUNNING`

### 2.2 Núdzové zastavenie

**Kedy použiť:** Kritická chyba, potreba okamžitého zastavenia

```powershell
python scripts\manage_service.py stop
```

### 2.3 Manuálny reštart cez NSSM

**Kedy použiť:** Ak manage_service.py nefunguje

```powershell
# Zastavenie
C:\Tools\nssm\win64\nssm.exe stop NEX-Automat-Loader

# Počkajte 10 sekúnd

# Spustenie
C:\Tools\nssm\win64\nssm.exe start NEX-Automat-Loader
```

### 2.4 Reštart cez Windows Services

1. Stlačte `Win + R`
2. Napíšte `services.msc` a stlačte Enter
3. Nájdite `NEX-Automat-Loader`
4. Pravý klik → Reštartovať

---

## 3. Zálohovanie a obnova databázy

### 3.1 Automatické zálohy

Systém vytvára automatické zálohy:
- **Umiestnenie:** `C:\Deployment\nex-automat\backups\`
- **Frekvencia:** Denne o 02:00
- **Retencia:** 7 dní

### 3.2 Manuálna záloha

**Kedy použiť:** Pred zmenami, pred aktualizáciou

```powershell
# PowerShell ako Admin
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupFile = "C:\Deployment\nex-automat\backups\invoice_staging_$timestamp.sql"

pg_dump -h localhost -U postgres -d invoice_staging -f $backupFile

Write-Host "Záloha vytvorená: $backupFile"
```

### 3.3 Obnova databázy zo zálohy

**⚠️ POZOR: Toto vymaže všetky aktuálne dáta!**

**Postup:**

1. **Zastavte službu:**
```powershell
cd C:\Deployment\nex-automat
python scripts\manage_service.py stop
```

2. **Vyberte zálohu:**
```powershell
dir backups\*.sql
```

3. **Obnovte databázu:**
```powershell
# Nahraďte FILENAME názvom zálohy
psql -h localhost -U postgres -d invoice_staging -f backups\FILENAME.sql
```

4. **Spustite službu:**
```powershell
python scripts\manage_service.py start
```

5. **Overte funkčnosť:**
```powershell
python scripts\day5_preflight_check.py
```

### 3.4 Obnova jednej tabuľky

```powershell
# Export jednej tabuľky
pg_dump -h localhost -U postgres -d invoice_staging -t invoices -f invoices_backup.sql

# Import jednej tabuľky
psql -h localhost -U postgres -d invoice_staging -f invoices_backup.sql
```

---

## 4. Rollback postupy

### 4.1 Rollback konfigurácie

**Kedy použiť:** Po neúspešnej zmene konfigurácie

1. Zálohy konfigurácie sú v: `config/backups/`
2. Obnovte predchádzajúcu verziu:

```powershell
cd C:\Deployment\nex-automat

# Zoznam záloh
dir apps\supplier-invoice-loader\config\backups\

# Obnova (nahraďte TIMESTAMP)
copy apps\supplier-invoice-loader\config\backups\config_TIMESTAMP.yaml `
     apps\supplier-invoice-loader\config\config.yaml

# Reštart služby
python scripts\manage_service.py restart
```

### 4.2 Rollback aplikácie

**Kedy použiť:** Po neúspešnej aktualizácii

1. Kontaktujte ICC Komárno pre rollback
2. Záloha predchádzajúcej verzie je v Git histórii
3. Rollback vykoná technik

### 4.3 Rollback databázovej schémy

**Kedy použiť:** Po neúspešnej migrácii

```powershell
# Zoznam migrácií
dir migrations\

# Rollback poslednej migrácie (kontaktujte ICC)
# Tento postup vyžaduje technickú podporu
```

---

## 5. Núdzové postupy

### 5.1 Služba spadla a nereštartuje sa

**Diagnostika:**
```powershell
cd C:\Deployment\nex-automat

# Skontrolujte logy
python scripts\manage_service.py logs

# Skontrolujte systém
python scripts\day5_preflight_check.py
```

**Možné príčiny a riešenia:**

| Príčina | Riešenie |
|---------|----------|
| Chýba POSTGRES_PASSWORD | Nastavte environment variable |
| Databáza nedostupná | Reštartujte PostgreSQL |
| Port obsadený | Nájdite a ukončite konfliktný proces |
| Poškodená konfigurácia | Rollback konfigurácie |

### 5.2 Databáza nedostupná

**Diagnostika:**
```powershell
# Test pripojenia
psql -h localhost -U postgres -d invoice_staging -c "SELECT 1"
```

**Riešenie:**
```powershell
# Reštart PostgreSQL služby
net stop postgresql-x64-16
net start postgresql-x64-16
```

### 5.3 Disk plný

**Diagnostika:**
```powershell
Get-PSDrive C | Select-Object Used, Free
```

**Riešenie:**
1. Vymažte staré logy: `del logs\service-*.log` (okrem posledného)
2. Vymažte staré zálohy: `del backups\*.sql` (okrem posledných 3)
3. Vyprázdnite Temp: `del $env:TEMP\* -Recurse`

### 5.4 Vysoké využitie pamäte

**Diagnostika:**
```powershell
Get-Process python | Select-Object Name, WorkingSet64
```

**Riešenie:**
```powershell
python scripts\manage_service.py restart
```

### 5.5 Kompletný reset systému

**⚠️ POSLEDNÁ MOŽNOSŤ - použite len ak nič iné nefunguje!**

```powershell
# 1. Zastavte všetko
python scripts\manage_service.py stop
net stop postgresql-x64-16

# 2. Počkajte 30 sekúnd

# 3. Spustite PostgreSQL
net start postgresql-x64-16

# 4. Počkajte 10 sekúnd

# 5. Spustite službu
python scripts\manage_service.py start

# 6. Overte
python scripts\day5_preflight_check.py
```

---

## 6. Riešenie problémov

### 6.1 Chybové hlásenia a riešenia

| Chyba | Príčina | Riešenie |
|-------|---------|----------|
| `Connection refused` | DB nebeží | Reštart PostgreSQL |
| `Authentication failed` | Zlé heslo | Overte POSTGRES_PASSWORD |
| `Service not found` | NSSM problém | Preinštalujte službu |
| `Permission denied` | Práva | Spustite ako Admin |
| `Port in use` | Konflikt | Nájdite proces na porte |
| `Out of memory` | RAM | Reštart služby |
| `PDF processing error` | Poškodený PDF | Skontrolujte vstupný súbor |

### 6.2 Kontrola logov

**Aplikačné logy:**
```powershell
# Posledných 50 riadkov
python scripts\manage_service.py logs

# Živý výstup
python scripts\manage_service.py tail
```

**Windows Event Log:**
1. Otvorte Event Viewer (`eventvwr.msc`)
2. Windows Logs → Application
3. Filtrujte podľa "NEX-Automat"

### 6.3 Diagnostický skript

```powershell
cd C:\Deployment\nex-automat

# Kompletná diagnostika
python scripts\day5_preflight_check.py
python scripts\day5_error_handling_tests.py
```

### 6.4 Časté problémy

**Problém: Faktúry sa nespracovávajú**
1. Skontrolujte či služba beží
2. Skontrolujte vstupný priečinok
3. Pozrite logy pre chyby
4. Overte formát PDF súborov

**Problém: Pomalé spracovanie**
1. Skontrolujte využitie CPU/RAM
2. Skontrolujte dostupný disk
3. Reštartujte službu
4. Kontaktujte podporu ak pretrváva

**Problém: Chýbajúce dáta v databáze**
1. Skontrolujte logy pre chyby
2. Overte že PDF bolo správne spracované
3. Obnovte zo zálohy ak potrebné

---

## 7. Kontakty

### Technická podpora

**ICC Komárno - Innovation & Consulting Center**

| Kontakt | Informácie |
|---------|------------|
| Email | podpora@icc-komarno.sk |
| Telefón | +421 XXX XXX XXX |
| Pracovná doba | Po-Pi 8:00-16:00 |

### Eskalácia

| Úroveň | Situácia | Kontakt |
|--------|----------|---------|
| L1 | Bežné problémy | Email |
| L2 | Služba nefunguje | Telefón |
| L3 | Strata dát | Telefón + Email |

### Pred kontaktovaním podpory pripravte:

1. Popis problému
2. Kedy problém vznikol
3. Čo ste skúsili
4. Výstup z `day5_preflight_check.py`
5. Posledné riadky z logov

---

## Prílohy

### A. Checklist pre denný monitoring

- [ ] Služba beží (`python scripts\manage_service.py status`)
- [ ] Databáza dostupná
- [ ] Dostatok miesta na disku (>10GB)
- [ ] Žiadne ERROR v logoch
- [ ] Záloha vytvorená

### B. Checklist pre týždenný monitoring

- [ ] Všetky denné kontroly
- [ ] Vymazanie starých logov
- [ ] Kontrola veľkosti databázy
- [ ] Test obnovy zo zálohy
- [ ] Aktualizácia dokumentácie

---

**Dokument vytvorený:** 2025-11-24  
**Posledná aktualizácia:** 2025-11-24  
**Verzia dokumentu:** 1.0