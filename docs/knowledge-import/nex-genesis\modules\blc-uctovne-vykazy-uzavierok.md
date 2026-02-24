# BLC - Účtovné výkazy uzávierok (Financial Statements)

## Prehľad modulu

- **Súbor**: `NexModules\Blc_F.pas`
- **Účel**: Výpočet a archivácia účtovných výkazov - Súvaha a Výsledovka (Výkaz ziskov a strát)
- **Kategória**: Účtovníctvo / Uzávierkové výkazy
- **Mark modulu**: BLC

## Tabuľky modulu

| Tabuľka | Súbor | Popis | Polí | Indexov |
|---------|-------|-------|------|---------|
| BLCLST | BLCLST.BTR | Zoznam uložených výkazov | 12 | 3 |
| SUVDEF | SUVDEF.BTR | Definícia riadkov súvahy | 5 | 1 |
| SUV | SUVnnnnn.BTR | Výkaz súvahy (archívny) | 11 | 1 |
| SUVCALC | SUVCALC.BTR | Kalkulačné vzorce súvahy | 10 | 1 |
| VYSDEF | VYSDEF.BTR | Definícia riadkov výsledovky | 7 | 1 |
| VYS | VYSnnnnn.BTR | Výkaz ziskov a strát (archívny) | 8 | 1 |
| VYSCALC | VYSCALC.BTR | Kalkulačné vzorce výsledovky | 9 | 1 |

**Celkom: 7 tabuliek, 62 polí, 10 indexov**

## Sub-moduly (15)

### Hlavný formulár
| Súbor | Popis |
|-------|-------|
| Blc_F.pas | Hlavný formulár - zoznam výkazov, zobrazenie, tlač |

### Výpočet výkazov
| Súbor | Popis |
|-------|-------|
| Blc_Calc_F.pas | Kompletný výpočet súvahy a výsledovky |

### Definícia súvahy
| Súbor | Popis |
|-------|-------|
| Blc_SuvDef_F.pas | Editor definície riadku súvahy |
| Blc_SuvCalc_F.pas | Editor kalkulačného vzorca súvahy |
| Blc_SuvCalc_V.pas | Výber kalkulačného vzorca súvahy |
| Blc_SuvCalcForm_F.pas | Formulár kalkulačných vzorcov |
| Blc_SuvCalcForm_V.pas | Výber kalkulačných vzorcov |
| Blc_SuvPrev_F.pas | Editácia hodnôt minulého obdobia súvahy |

### Definícia výsledovky
| Súbor | Popis |
|-------|-------|
| Blc_VysDef_F.pas | Editor definície riadku výsledovky |
| Blc_VysCalc_F.pas | Editor kalkulačného vzorca výsledovky |
| Blc_VysCalc_V.pas | Výber kalkulačného vzorca výsledovky |
| Blc_VysCalcForm_F.pas | Formulár kalkulačných vzorcov |
| Blc_VysCalcForm_V.pas | Výber kalkulačných vzorcov |
| Blc_VysPrev_F.pas | Editácia hodnôt minulého obdobia výsledovky |

### Pomocné
| Súbor | Popis |
|-------|-------|
| Blc_Upgrade_F.pas | Migrácia starých štruktúr (BLCDOC → SUVDEF/VYSDEF) |

## Typy výkazov

### Súvaha (Balance Sheet)
Štruktúra podľa slovenskej legislatívy:

| Časť | Riadky | Popis |
|------|--------|-------|
| AKTÍVA | 1-64 | Majetok spoločnosti |
| PASÍVA | 65-118 | Zdroje krytia majetku |
| Kontrolné | 888/999 | Kontrolné súčty |

**Stĺpce súvahy:**
- **Brutto** (ExBrutVal/RdBrutVal) - Hrubá hodnota aktív
- **Korekcia** (ExCorrVal/RdCorrVal) - Oprávky a opravné položky
- **Netto** (ExNettVal/RdNettVal) - Čistá hodnota (Brutto - Korekcia)
- **Minulé obdobie** (ExPrevVal/RdPrevVal) - Hodnota predchádzajúceho roka

**Bilančná rovnica:** AKTÍVA = PASÍVA

### Výsledovka (Profit & Loss Statement)
Štruktúra podľa slovenskej legislatívy:

| Časť | Riadky | Popis |
|------|--------|-------|
| Výnosy | 1-30 | Triedy 6 účtovej osnovy |
| Náklady | 31-60 | Triedy 5 účtovej osnovy |
| Výsledok | 61 | Hospodársky výsledok |
| Kontrolné | 99 | Kontrolný súčet |

**Stĺpce výsledovky:**
- **Aktuálne obdobie** (ExActVal/RdActVal) - Bežný rok
- **Minulé obdobie** (ExPrevVal/RdPrevVal) - Predchádzajúci rok

**Výpočet:** Výsledok = Výnosy - Náklady

## Algoritmus výpočtu

### Hlavný postup (Blc_Calc_F)

```
1. NewDocToBlcLst      - Vytvorenie záznamu v BLCLST
2. CollectPrevYear     - Zber počiatočných stavov (ak nie je otvorenie roku)

=== SÚVAHA ===
3. CreateNewSuv        - Kopírovanie SUVDEF → SUVnnnnn
4. ClearSuvCalc        - Vynulovanie SUVCALC
5. CalcSuvCalc         - Výpočet hodnôt z JOURNAL
6. CalcSuvVal          - Výpočet riadkov súvahy
7. SumSuvVal           - Sumarizácia súčtových riadkov
8. RoundSuvVal         - Zaokrúhlenie na celé EUR
9. SuvCheckSum         - Výpočet kontrolných čísel (888, 999)

=== VÝSLEDOVKA ===
10. CreateNewVys       - Kopírovanie VYSDEF → VYSnnnnn
11. ClearVysCalc       - Vynulovanie VYSCALC
12. CalcVysCalc        - Výpočet hodnôt z JOURNAL
13. CalcVysVal         - Výpočet riadkov výsledovky
14. SumVysVal          - Sumarizácia súčtových riadkov
15. RoundVysVal        - Zaokrúhlenie na celé EUR
16. VysCheckSum        - Výpočet kontrolného čísla (99)

17. SaveToBlcLst       - Uloženie hospodárskeho výsledku
18. AccAbsentVer       - Kontrola nepožitých účtov
```

### Kalkulačné vzorce (Formula)

| Formula | Výpočet | Použitie |
|---------|---------|----------|
| C-D | MD - Dal | Aktívne účty |
| D-C | Dal - MD | Pasívne účty |
| C | MD | Len strana MD |
| D | Dal | Len strana Dal |

### Znamienko účtu (SignSpc)

| Hodnota | Význam |
|---------|--------|
| (prázdne) | Všetky hodnoty |
| + | Len kladné hodnoty |
| - | Len záporné hodnoty |

### Stĺpec pre súvahu (Collum)

| Hodnota | Stĺpec |
|---------|--------|
| 0 | Brutto |
| 1 | Korekcia |

## Štruktúra definícií

### Typy riadkov (RowSum)

| Hodnota | Typ | CalcRows |
|---------|-----|----------|
| 0 | Kalkulačný | Prázdne (vzorce v SUVCALC/VYSCALC) |
| 1 | Súčtový | Vzorec sumarizácie riadkov |

### Formát CalcRows

```
Príklady:
"SUM(1..10)"           - Súčet riadkov 1 až 10
"1+2+3"                - Súčet riadkov 1, 2 a 3
"10-5"                 - Riadok 10 mínus riadok 5
"SUM(1..5)+SUM(10..15)" - Kombinovaný súčet
```

## Varianty výkazov

### Podľa veľkosti

| Varianta | Počet riadkov | Šablóny |
|----------|---------------|---------|
| Štandardná | > 45 | SUV_A, SUV_P, VYS |
| Mikro | ≤ 45 | SUV_A_M, SUV_P_M, VYS_M |

Mikro varianty majú zjednodušenú štruktúru pre malé podniky.

### Podľa roku

| Rok | Konverzia |
|-----|-----------|
| 2009 | SKK → EUR (kurz 30.126) |
| 2010+ | Len EUR |

## Integrácie

### Zdrojové tabuľky

| Tabuľka | Použitie |
|---------|----------|
| JOURNAL | Účtovné zápisy - aktuálny rok |
| JOURNAL (predch.) | Účtovné zápisy - minulý rok |
| ACCANL | Analytické účty (názvy, salda) |

### Dátové toky

```
JOURNAL (účtovné zápisy)
    ↓
Blc_Calc_F (výpočet)
    ↓
├→ SUVCALC (medzivýpočty súvahy)
│      ↓
│  SUVnnnnn (výkaz súvahy)
│
└→ VYSCALC (medzivýpočty výsledovky)
       ↓
   VYSnnnnn (výkaz výsledovky)
       ↓
   BLCLST (zoznam výkazov)
       ↓
   ├→ Tlač (SUV_A, SUV_P, VYS)
   └→ Export
```

## Tlačové zostavy

| Report | Popis |
|--------|-------|
| SUV_A | Súvaha - Aktíva |
| SUV_P | Súvaha - Pasíva |
| SUV_A_M | Súvaha Mikro - Aktíva |
| SUV_P_M | Súvaha Mikro - Pasíva |
| VYS | Výkaz ziskov a strát |
| VYS_M | Výkaz ziskov a strát - Mikro |
| FBSTIT | Titulná strana súvahy |
| FBPTIT | Titulná strana výsledovky |
| BLCCLV | Kontrolný zoznam vzorcov |
| BLCCLVS | Kontrolný zoznam vzorcov s hodnotami |

## UI komponenty

| Komponent | Popis |
|-----------|-------|
| TV_BlcLst | TableView - zoznam výkazov |
| TV_Suv | TableView - súvaha |
| TV_Vys | TableView - výsledovka |
| TV_SuvDef | TableView - definícia súvahy |
| TV_VysDef | TableView - definícia výsledovky |
| TV_SuvPrev | TableView - minulé obdobie súvahy |
| TV_VysPrev | TableView - minulé obdobie výsledovky |

### Menu štruktúra

- **Program** - Ukončenie, O programe
- **Úpravy** - Nový výkaz, Zmazať výkaz
- **Zobrazit** - Súvaha, Výsledovka, Definície
- **Tlač** - Všetky výkazy, Súvaha, Výsledovka, Kontrolný zoznam

## Business pravidlá

### Archivácia

- Každý výkaz má unikátne SerNum
- Súbor SUVnnnnn.BTR kde nnnnn = SerNum (súvaha)
- Súbor VYSnnnnn.BTR kde nnnnn = SerNum (výsledovka)
- Výkazy sa neprepisujú - vytvárajú sa nové

### Kontroly

- **Bilančná rovnováha**: Aktíva = Pasíva
- **Hospodársky výsledok**: Súvaha r.100 = Výsledovka r.61
- **Kontrolné čísla**: r.888 (súčet aktív), r.999 (súčet pasív)
- **Nepoužité účty**: Zoznam účtov bez priradenia k výkazu

### Slovenská legislatíva

- Formát výkazov podľa Opatrenia MF SR
- Štruktúra riadkov podľa účtovej osnovy
- Zaokrúhľovanie na celé EUR
- Podpora mikro účtovných jednotiek

## Migračné poznámky

### Pre PostgreSQL migráciu

1. **BLCLST** - jednoduchá tabuľka metadát

2. **SUV/VYS** - v PostgreSQL jedna tabuľka s FK:
   ```sql
   CREATE TABLE financial_statements (
     id SERIAL PRIMARY KEY,
     blc_lst_id INTEGER REFERENCES blc_lst(ser_num),
     statement_type CHAR(3),  -- 'SUV' alebo 'VYS'
     row_num INTEGER,
     marking VARCHAR(10),
     text VARCHAR(160),
     ex_brut_val DECIMAL(15,2),
     ex_corr_val DECIMAL(15,2),
     ex_nett_val DECIMAL(15,2),
     ex_prev_val DECIMAL(15,2),
     rd_brut_val INTEGER,
     rd_corr_val INTEGER,
     rd_nett_val INTEGER,
     rd_prev_val INTEGER
   );
   ```

3. **Definície** - konfiguračné tabuľky:
   - SUVDEF, VYSDEF môžu byť seeds alebo konfigurácia
   - SUVCALC, VYSCALC definujú kalkulačné pravidlá

4. **Výpočet** - materialized view alebo stored procedure

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
