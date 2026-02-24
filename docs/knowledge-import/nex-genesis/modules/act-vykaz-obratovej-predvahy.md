# ACT - Výkaz obratovej predvahy (Trial Balance Report)

## Prehľad modulu

- **Súbor**: `NexModules\Act_F.pas`
- **Účel**: Generovanie a archivácia výkazov obratovej predvahy za definované obdobie
- **Kategória**: Účtovníctvo / Výkazy
- **Mark modulu**: ACT

## Rozdiel ACC vs ACT

| Vlastnosť | ACC (ACCTRN) | ACT (ACTnnnnn) |
|-----------|--------------|----------------|
| Účel | Priebežná evidencia | Archívne výkazy |
| Životnosť | Regeneruje sa | Trvalý archív |
| Mesačné obraty | Áno (01-12) | Nie |
| Predchádzajúce obdobie | Nie | Áno (CPrvVal/DPrvVal) |
| Filtrovanie | WriNum | WriNums, CntNum |
| Súbory | Jeden ACCTRN.BTR | Viac ACTnnnnn.BTR |

**ACC** = Operatívna obratová predvaha (regenerovaná)
**ACT** = Archívne výkazy obratovej predvahy (historické)

## Tabuľky modulu

| Tabuľka | Súbor | Popis | Polí | Indexov |
|---------|-------|-------|------|---------|
| ACTLST | ACTLST.BTR | Zoznam výkazov (hlavičky) | 15 | 5 |
| ACT | ACTnnnnn.BTR | Položky výkazu | 20 | 3 |

**Celkom: 2 tabuľky, 35 polí, 8 indexov**

## Sub-moduly (4)

| Súbor | Popis |
|-------|-------|
| Act_F.pas | Hlavný formulár - zoznam výkazov |
| Act_AddAct_F.pas | Vytvorenie nového výkazu |
| Act_DelAct_F.pas | Zmazanie výkazu |
| Act_ItmLst_V.pas | Zobrazenie položiek výkazu |

## Kľúčové funkcie

### Vytvorenie výkazu (Act_AddAct_F)

**Parametre:**
- **BegDate/EndDate** - Obdobie výkazu
- **MthNum** - Číslo mesiaca (automaticky nastaví dátumy)
- **CntNum** - Stredisko (filter)
- **WriNums** - Prevádzkové jednotky (čiarkou oddelený zoznam)
- **Describe** - Popis výkazu

**Zdroje dát:**
- **JrnCollect** - Štandardné účtovníctvo (JOURNAL)
- **FjrCollect** - Jednoduché účtovníctvo (FINJRN)

### Algoritmus JrnCollect

```
1. Otvori JOURNAL indexované SnAn (AccSnt+AccAnl)
2. Pre každý účet:
   a. BegRec=1 → CBegVal, DBegVal (počiatočný stav)
   b. DocDate < BegDate → CPrvVal, DPrvVal (predchádzajúce obdobie)
   c. BegDate <= DocDate <= EndDate → CTrnVal, DTrnVal (aktuálne obdobie)
   d. BegRec=9 sa ignoruje (uzatvorenie)
3. Filter podľa WriNums (prevádzkové jednotky)
4. NulItmDel - odstráni nulové položky
```

### Tlač výkazu (A_PrnAct)

```
Šablóny:
- ACT - Štandardný výkaz
- ACTEAS - Výkaz pre jednoduché účtovníctvo
```

## Štruktúra výkazu (ACT)

### Počiatočné stavy
| Pole | Popis |
|------|-------|
| CBegVal | Počiatočný stav - MD |
| DBegVal | Počiatočný stav - Dal |

### Kumulatív pred obdobím
| Pole | Popis |
|------|-------|
| CPrvVal | Kumulatívny obrat do obdobia - MD |
| DPrvVal | Kumulatívny obrat do obdobia - Dal |

### Obraty za obdobie
| Pole | Popis |
|------|-------|
| CTrnVal | Celkový obrat za obdobie - MD |
| DTrnVal | Celkový obrat za obdobie - Dal |

### Kumulatív ku koncu obdobia
| Pole | Popis |
|------|-------|
| CSumVal | Kumulatívny obrat ku koncu obdobia - MD |
| DSumVal | Kumulatívny obrat ku koncu obdobia - Dal |

### Konečné stavy
| Pole | Popis |
|------|-------|
| CEndVal | Konečný stav - MD |
| DEndVal | Konečný stav - Dal |
| DifVal | Zostatok na účte |

## Výpočtové pravidlá

```
CSumVal = CPrvVal + CTrnVal
DSumVal = DPrvVal + DTrnVal
CEndVal = CBegVal + CSumVal
DEndVal = DBegVal + DSumVal
DifVal = CEndVal - DEndVal
```

## Filtrovanie

### Podľa strediska (CntNum)
- Výber strediska automaticky načíta jeho prevádzkové jednotky
- Z CNTLST.WriNums alebo z WRILST.CntNum

### Podľa prevádzkových jednotiek (WriNums)
- Čiarkou oddelený zoznam čísel
- Funkcia LongInInt kontroluje príslušnosť zápisu
- Príklad: "1,2,5,8" = prevádzkové jednotky 1, 2, 5 a 8

### Podľa mesiaca (MthNum)
- Automaticky nastaví BegDate = FirstMthDate
- Automaticky nastaví EndDate = LastMthDate

## Integrácie

### Zdrojové tabuľky

| Tabuľka | Použitie |
|---------|----------|
| JOURNAL | Zdroj účtovných zápisov (štandardné) |
| FINJRN | Zdroj účtovných zápisov (jednoduché) |
| ACCANL | Názvy analytických účtov |
| CNTLST | Strediská |
| WRILST | Prevádzkové jednotky |

### Dátové toky

```
JOURNAL/FINJRN
       ↓
Act_AddAct_F (generovanie)
       ↓
├→ ACTLST (hlavička výkazu)
└→ ACTnnnnn (položky výkazu)
       ↓
├→ Act_ItmLst_V (zobrazenie)
└→ A_PrnAct (tlač)
```

## Tlačové zostavy

| Report | Popis |
|--------|-------|
| ACT | Štandardný výkaz obratovej predvahy |
| ACTEAS | Výkaz pre jednoduché účtovníctvo |

## Business pravidlá

### Archivácia
- Každý výkaz má unikátne SerNum
- Súbor ACTnnnnn.BTR kde nnnnn = SerNum
- Výkazy sa neprepisujú - vytvárajú sa nové

### Mazanie nulových položiek
- Po generovaní sa automaticky vymažú položky kde:
  ```
  Abs(CBegVal) + Abs(DBegVal) + Abs(CSumVal) + Abs(DSumVal) = 0
  ```

### Jednoduché účtovníctvo (EasLdg)
- Používa FINJRN namiesto JOURNAL
- Iná šablóna tlače (ACTEAS)
- Zjednodušená štruktúra (len AcValue namiesto CredVal/DebVal)

## UI komponenty

| Komponent | Popis |
|-----------|-------|
| TV_ActLst | TableView so zoznamom výkazov |
| E_BegDate/E_EndDate | Výber obdobia |
| E_MthNum | Výber mesiaca |
| E_CntNum | Výber strediska |
| E_WriNums | Prevádzkové jednotky (interval) |
| E_Describe | Popis výkazu |
| PB_Indicator | Progress bar pri generovaní |

### Menu štruktúra
- **Úpravy** - Pridať/Zmazať výkaz
- **Zobrazit** - Zoznam položiek výkazu
- **Tlač** - Výkaz obratovej predvahy

## Migračné poznámky

### Pre PostgreSQL migráciu

1. **ACTLST** - jednoduchá tabuľka s metadátami výkazu

2. **ACT** - položky výkazu:
   - V PostgreSQL môže byť jedna tabuľka s FK na ACTLST.SerNum
   - Namiesto ACTnnnnn.BTR súborov

3. **Generovanie** - SQL verzia:
   ```sql
   INSERT INTO act (act_lst_id, acc_snt, acc_anl, ...)
   SELECT :report_id, acc_snt, acc_anl,
          SUM(CASE WHEN beg_rec = 1 THEN cred_val END),
          SUM(CASE WHEN beg_rec = 1 THEN deb_val END),
          SUM(CASE WHEN doc_date < :beg_date THEN cred_val END),
          ...
   FROM journal
   WHERE wri_num IN (:wri_nums)
   GROUP BY acc_snt, acc_anl;
   ```

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
