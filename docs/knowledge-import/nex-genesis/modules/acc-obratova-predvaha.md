# ACC - Obratová predvaha účtov (Trial Balance)

## Prehľad modulu

- **Súbor**: `NexModules\Acc_F.pas`
- **Účel**: Zobrazenie a tlač obratovej predvahy analytických účtov s mesačnými obratmi
- **Kategória**: Účtovníctvo / Výkazy
- **Mark modulu**: ACC

## Tabuľky modulu

| Tabuľka | Súbor | Popis | Polí | Indexov | Stav dok. |
|---------|-------|-------|------|---------|-----------|
| ACCTRN | ACCTRN.BTR | Obratová predvaha analytických účtov | 43 | 3 | Nová |
| ACCSNT | ACCSNT.BTR | Syntetické účty (účtová osnova) | 12 | 2 | Existuje |
| ACCANL | ACCANL.BTR | Analytické účty s obratmi | 49 | 7 | Existuje |
| ACCANLC | ACCANLC.BTR | Analytické účty podľa stredísk | 45 | 3 | Existuje |
| JOURNAL | JOURNAL.BTR | Denník účtovných zápisov | 29 | 9 | Existuje |

**Nová tabuľka: 1 (ACCTRN), 43 polí, 3 indexy**

## Sub-moduly (13)

### Hlavné zobrazenie
| Súbor | Popis |
|-------|-------|
| Acc_F.pas | Hlavný formulár obratovej predvahy |

### Prepočet
| Súbor | Popis |
|-------|-------|
| Acc_ReCalc_F.pas | Prepočet obratovej predvahy z JOURNAL |

### Tlač a export
| Súbor | Popis |
|-------|-------|
| Acc_TrnPrn_F.pas | Tlač obratovej predvahy (QuickReport + Excel) |

### Účtová osnova
| Súbor | Popis |
|-------|-------|
| Acc_AccSnt_F.pas | Editor syntetického účtu |
| Acc_AccSnt_V.pas | Výber syntetického účtu |
| Acc_AccAnl_F.pas | Editor analytického účtu |
| Acc_AccAnl_V.pas | Výber analytického účtu |

### Pohyby na účte
| Súbor | Popis |
|-------|-------|
| Jrn_AccMov_F.pas | Zobrazenie pohybov na vybranom účte |

### Porovnanie
| Súbor | Popis |
|-------|-------|
| Acc_JrnCmp_F.pas | Porovnanie s denníkom |
| Acc_JrnLst.pas | Zoznam zápisov denníka |

### Profily
| Súbor | Popis |
|-------|-------|
| Acc_ProLst.pas | Zoznam profilov |
| Acc_ProEdi.pas | Editor profilov |

### Pomocné
| Súbor | Popis |
|-------|-------|
| Acc_PmbLst_F.pas | Zoznam položiek |
| Acc_PmbLst_V.pas | Výber položiek |

## Kľúčové funkcie

### A_ReCalc - Prepočet predvahy

Prepočítava obratovú predvahu z denníka účtovných zápisov (JOURNAL).

**Algoritmus:**
```
1. Vymaž ACCTRN
2. Pre každý účet (AccSnt + AccAnl) v JOURNAL:
   a. Rozlíš počiatočné stavy (BegRec=1)
   b. Rozdeľ obraty podľa mesiacov (MthNum)
   c. Počítaj súčty MD a D
   d. Vytvor záznam v ACCTRN
3. Výpočet konečných stavov:
   CEndVal = CBegVal + CTrnVal
   DEndVal = DBegVal + DTrnVal
   DifVal = CEndVal - DEndVal
```

### A_AccMov - Pohyby na účte

Zobrazuje všetky zápisy z denníka pre vybraný účet v zadanom období.

### A_Delete - Mazanie záznamu

Umožňuje mazanie len účtov s nulovými hodnotami:
```
CBegVal = 0 AND DBegVal = 0 AND CTrnVal = 0 AND DTrnVal = 0
```

## Štruktúra obratovej predvahy (ACCTRN)

### Počiatočné stavy
| Pole | Popis |
|------|-------|
| CBegVal | Počiatočný stav - MD (Má dať) |
| DBegVal | Počiatočný stav - Dal |

### Mesačné obraty (01-12)
| Pole | Popis |
|------|-------|
| CTrnVal01-12 | Obrat za mesiac - MD |
| DTrnVal01-12 | Obrat za mesiac - Dal |

### Celkové obraty
| Pole | Popis |
|------|-------|
| CTrnVal | Celkový obrat - MD |
| DTrnVal | Celkový obrat - Dal |

### Konečné stavy
| Pole | Popis |
|------|-------|
| CEndVal | Konečný stav - MD |
| DEndVal | Konečný stav - Dal |
| DifVal | Rozdiel (CEndVal - DEndVal) |

## Výpočtové pravidlá

### Bilančná rovnováha
```
Suma(CBegVal) = Suma(DBegVal)  // Počiatočné stavy
Suma(CTrnVal) = Suma(DTrnVal)  // Obraty
Suma(CEndVal) = Suma(DEndVal)  // Konečné stavy
```

### Výpočet konečného stavu
```
CEndVal = CBegVal + CTrnVal
DEndVal = DBegVal + DTrnVal
DifVal = CEndVal - DEndVal
```

### Interpretácia DifVal
| DifVal | Typ účtu | Význam |
|--------|----------|--------|
| > 0 | Aktívny | Zostatok na strane MD |
| < 0 | Pasívny | Zostatok na strane D |
| = 0 | - | Vyrovnaný účet |

## Filtrovanie

### Podľa prevádzkové jednotky (WriNum)
- E_WriEdit umožňuje výber prevádzkovej jednotky
- WriNum=0 znamená všetky jednotky
- Prepočet filtruje zápisy podľa WriNum v JOURNAL

### Podľa účtovného roka (AccAcYear)
- E_AcYear nastavuje rok pre prepočet
- Zápisy pred FirstYearDate sa sčítajú do počiatočného stavu
- Zápisy po LastYearDate sa ignorujú

## Tlačové zostavy

| Report | Popis | Obdobie |
|--------|-------|---------|
| ACCTRNM | Obratová predvaha | Mesačne |
| ACCTRND | Obratová predvaha | K dátumu |
| ACCLDGM | Hlavná kniha | Mesačne |
| ACCLDGD | Hlavná kniha | K dátumu |

### Export do Excel
- Podpora OLE Automation
- Šablóna pre formátovaný export
- Uloženie ako PDF (voliteľné)

## Integrácie

### Väzby na moduly

| Modul | Väzba | Popis |
|-------|-------|-------|
| JRN | JOURNAL → ACCTRN | Zdrojové dáta pre prepočet |
| - | ACCSNT, ACCANL | Názvy účtov |
| WRI | WriNum | Prevádzkové jednotky |

### Dátové toky

```
JOURNAL (účtovné zápisy)
    ↓
Acc_ReCalc_F (prepočet)
    ↓
ACCTRN (obratová predvaha)
    ↓
├→ Acc_TrnPrn_F (tlač)
├→ Export Excel
└→ Jrn_AccMov_F (detail účtu)
```

## UI komponenty

| Komponent | Popis |
|-----------|-------|
| TV_AccTrn | TableView pre ACCTRN |
| E_WriEdit | Výber prevádzkovej jednotky |
| E_AcYear | Účtovný rok |
| B_ReCalc | Prepočet predvahy |
| B_PrnTrn | Tlač predvahy |

### Menu štruktúra
- **Program** - Ukončenie, O programe
- **Zobrazit** - Pohyby na účte
- **Tlač** - Tlač predvahy
- **Nástroje** - (voľné)
- **Údržba** - Prepočet, Mazanie

## Business pravidlá

### Prepočet
- Vymaže existujúce ACCTRN záznamy
- Sumarizuje z JOURNAL podľa AccSnt + AccAnl
- Rozlíši BegRec=1 (počiatočný stav) od bežných zápisov
- BegRec=9 (uzatvorenie) sa ignoruje

### Mazanie
- Možné len pri nulových hodnotách
- Ochrana pred stratou dát

### Rok
- Zápisy pred rokom sa pripočítajú k počiatočnému stavu
- Zápisy po roku sa ignorujú

## Migračné poznámky

### Pre PostgreSQL migráciu

1. **ACCTRN** môže byť materializovaný pohľad:
   ```sql
   CREATE MATERIALIZED VIEW acctrn AS
   SELECT acc_snt, acc_anl,
          SUM(CASE WHEN beg_rec = 1 THEN cred_val END) as c_beg_val,
          SUM(CASE WHEN beg_rec = 1 THEN deb_val END) as d_beg_val,
          SUM(CASE WHEN MONTH(doc_date) = 1 THEN cred_val END) as c_trn_val01,
          ...
   FROM journal
   GROUP BY acc_snt, acc_anl;
   ```

2. **Refresh** namiesto prepočtu:
   ```sql
   REFRESH MATERIALIZED VIEW acctrn;
   ```

3. **Filtrovanie** cez WHERE klauzulu v pohľade

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
