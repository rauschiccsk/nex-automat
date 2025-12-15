# NEX Automat v2.0 - Školiaci materiál

**Zákazník:** Mágerstav s.r.o.  
**Systém:** Supplier Invoice Loader  
**Verzia:** 2.0.0  
**Dátum školenia:** 2025-11-27  

---

## Obsah školenia

| #   | Téma               | Trvanie | Cieľová skupina |
| --- | ------------------ | ------- | --------------- |
| 1   | Úvod do systému    | 15 min  | Všetci          |
| 2   | Základné operácie  | 20 min  | Používatelia    |
| 3   | Administrácia      | 30 min  | IT Admin        |
| 4   | Riešenie problémov | 20 min  | IT Admin        |
| 5   | Praktické cvičenia | 25 min  | Všetci          |

**Celkové trvanie:** 2 hodiny

---

## 1. Úvod do systému

### 1.1 Čo je NEX Automat?

NEX Automat je automatizovaný systém na spracovanie dodávateľských faktúr:

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐    ┌─────────────┐
│  PDF        │ →  │  NEX Automat │ →  │  Databáza   │ →  │ NEX Genesis │
│  Faktúra    │    │  (OCR + AI)  │    │  PostgreSQL │    │    ERP      │
└─────────────┘    └──────────────┘    └─────────────┘    └─────────────┘
```

### 1.2 Výhody systému

| Pred                      | Po                      |
| ------------------------- | ----------------------- |
| Manuálne zadávanie faktúr | Automatické spracovanie |
| Chyby pri prepise         | Presná extrakcia dát    |
| Hodiny práce              | Sekundy na faktúru      |
| Nekonzistentné dáta       | Štandardizovaný formát  |

### 1.3 Čo systém spracováva

- ✅ PDF faktúry od dodávateľov
- ✅ Faktúry v slovenčine a češtine
- ✅ Štandardné formáty faktúr
- ❌ Skenované nekvalitné dokumenty
- ❌ Ručne písané faktúry

---

## 2. Základné operácie (Používatelia)

### 2.1 Ako nahrať faktúru

**Krok 1:** Uložte PDF faktúru do vstupného priečinka

```
Vstupný priečinok: [bude nakonfigurovaný]
```

**Krok 2:** Systém automaticky detekuje a spracuje faktúru

**Krok 3:** Skontrolujte výsledok v NEX Genesis

> 💡 **Tip:** Systém spracováva faktúry automaticky každých niekoľko sekúnd. Nemusíte robiť nič špeciálne.

### 2.2 Kontrola stavu spracovania

**V NEX Genesis:**

1. Otvorte modul Dodávateľské faktúry
2. Vyhľadajte faktúru podľa čísla
3. Skontrolujte správnosť dát

**Ak faktúra chýba:**

1. Počkajte 5 minút (systém môže byť zaneprázdnený)
2. Skontrolujte či PDF je v správnom priečinku
3. Kontaktujte IT ak problém pretrváva

### 2.3 Formát PDF faktúry

**Správny formát:**

- PDF súbor (nie obrázok)
- Čitateľný text (nie sken)
- Štandardná štruktúra faktúry
- Názov súboru bez špeciálnych znakov

**Príklad správneho názvu:**

```
faktura_2024_001234.pdf
FA-2024-001234.pdf
dodavatel_november_2024.pdf
```

**Nevhodné názvy:**

```
faktúra číslo 123 (1).pdf  ❌ (medzery, zátvorky)
nová&faktúra.pdf           ❌ (špeciálne znaky)
```

---

## 3. Administrácia (IT Admin)

### 3.1 Prístup k serveru

**Pripojenie:**

1. Spustite Remote Desktop (mstsc)
2. Zadajte adresu servera
3. Prihláste sa s admin účtom

### 3.2 Správa služby

**Otvorte PowerShell ako Administrátor:**

```powershell
cd C:\Deployment\nex-automat
```

**Základné príkazy:**

| Akcia       | Príkaz                                     |
| ----------- | ------------------------------------------ |
| Stav služby | `python scripts\manage_service.py status`  |
| Spustiť     | `python scripts\manage_service.py start`   |
| Zastaviť    | `python scripts\manage_service.py stop`    |
| Reštartovať | `python scripts\manage_service.py restart` |
| Logy        | `python scripts\manage_service.py logs`    |

### 3.3 Denná kontrola

**Každé ráno (5 minút):**

```powershell
# 1. Skontrolujte stav
python scripts\manage_service.py status
# Očakávané: SERVICE_RUNNING

# 2. Skontrolujte logy
python scripts\manage_service.py logs
# Hľadajte: ERROR alebo CRITICAL

# 3. Spustite diagnostiku
python scripts\day5_preflight_check.py
# Očakávané: 6/6 PASS
```

### 3.4 Monitoring diskov

```powershell
# Skontrolujte voľné miesto
Get-PSDrive C | Select-Object Used, Free

# Očakávané: Minimum 10 GB voľné
```

### 3.5 Zálohovanie

**Manuálna záloha (pred zmenami):**

```powershell
$d = Get-Date -Format "yyyyMMdd_HHmmss"
pg_dump -h localhost -U postgres -d invoice_staging -f "backups\manual_$d.sql"
```

**Kontrola záloh:**

```powershell
dir backups\*.sql
```

---

## 4. Riešenie problémov

### 4.1 Služba nebeží

**Príznaky:** Faktúry sa nespracovávajú

**Riešenie:**

```powershell
# 1. Skontrolujte stav
python scripts\manage_service.py status

# 2. Ak nie je RUNNING, spustite
python scripts\manage_service.py start

# 3. Overte
python scripts\manage_service.py status
```

### 4.2 Chyby v logoch

**Ako nájsť chyby:**

```powershell
python scripts\manage_service.py logs
```

**Časté chyby a riešenia:**

| Chyba                | Príčina       | Riešenie               |
| -------------------- | ------------- | ---------------------- |
| `Connection refused` | DB nebeží     | Reštartujte PostgreSQL |
| `Permission denied`  | Práva         | Spustite ako Admin     |
| `File not found`     | Chýba súbor   | Skontrolujte cestu     |
| `Invalid PDF`        | Poškodený PDF | Skontrolujte súbor     |

### 4.3 Faktúra sa nespracovala

**Checklist:**

1. [ ] Je PDF v správnom priečinku?
2. [ ] Je to platný PDF súbor?
3. [ ] Služba beží?
4. [ ] Nie sú chyby v logoch?

**Ak nič nepomáha:**

1. Reštartujte službu
2. Počkajte 5 minút
3. Skontrolujte znova
4. Kontaktujte ICC podporu

### 4.4 Pomalé spracovanie

**Možné príčiny:**

- Veľa faktúr naraz
- Málo miesta na disku
- Vysoké využitie pamäte

**Riešenie:**

```powershell
# Skontrolujte performance
python scripts\day5_performance_tests.py

# Reštartujte službu
python scripts\manage_service.py restart
```

---

## 5. Praktické cvičenia

### Cvičenie 1: Kontrola stavu (5 min)

**Úloha:** Skontrolujte či systém beží správne

```powershell
cd C:\Deployment\nex-automat
python scripts\manage_service.py status
python scripts\day5_preflight_check.py
```

**Očakávaný výsledok:**

- Status: SERVICE_RUNNING
- Preflight: 6/6 PASS

### Cvičenie 2: Čítanie logov (5 min)

**Úloha:** Nájdite posledné spracované faktúry

```powershell
python scripts\manage_service.py logs
```

**Hľadajte:** Riadky obsahujúce "processed" alebo "SUCCESS"

### Cvičenie 3: Reštart služby (5 min)

**Úloha:** Bezpečne reštartujte službu

```powershell
# 1. Zastavte
python scripts\manage_service.py stop

# 2. Počkajte 5 sekúnd

# 3. Spustite
python scripts\manage_service.py start

# 4. Overte
python scripts\manage_service.py status
```

### Cvičenie 4: Spracovanie testovacej faktúry (10 min)

**Úloha:** Spracujte testovaciu faktúru

1. Nájdite testovacie PDF:
   
   ```powershell
   dir apps\supplier-invoice-loader\tests\samples\*.pdf
   ```

2. Skopírujte do vstupného priečinka

3. Sledujte logy:
   
   ```powershell
   python scripts\manage_service.py tail
   ```

4. Overte spracovanie v NEX Genesis

---

## Záverečný test

### Otázky pre používateľov

1. Kam nahráte PDF faktúru na spracovanie?
2. Ako dlho trvá spracovanie faktúry?
3. Kde skontrolujete výsledok?
4. Koho kontaktujete pri probléme?

### Otázky pre IT Adminov

1. Ako zistíte stav služby?
2. Ako reštartujete službu?
3. Kde nájdete logy?
4. Ako vytvoríte zálohu databázy?
5. Čo urobíte ak služba nebeží?

---

## Kontakty a podpora

### Interná podpora (Mágerstav IT)

- Prvý kontakt pre používateľov
- Základné troubleshooting
- Reštart služby

### Externá podpora (ICC Komárno)

- Komplexné problémy
- Aktualizácie systému
- Zmeny konfigurácie

**ICC Komárno:**

- Email: podpora@icc-komarno.sk
- Telefón: +421 XXX XXX XXX
- Pracovná doba: Po-Pi 8:00-16:00

---

## Materiály na stiahnutie

| Dokument               | Účel                  |
| ---------------------- | --------------------- |
| OPERATIONS_GUIDE.md    | Denná prevádzka       |
| RECOVERY_PROCEDURES.md | Obnova pri problémoch |
| GO_LIVE_CHECKLIST.md   | Kontrolný zoznam      |

**Umiestnenie:** `C:\Deployment\nex-automat\docs\deployment\`

---

## Poznámky zo školenia

```
Dátum: ________________

Účastníci:
1. ________________________________
2. ________________________________
3. ________________________________

Otázky a odpovede:
_________________________________________________
_________________________________________________
_________________________________________________

Dohodnuté akcie:
_________________________________________________
_________________________________________________
```

---

**Školenie pripravil:** ICC Komárno  
**Verzia:** 1.0  
**Dátum:** 2025-11-24