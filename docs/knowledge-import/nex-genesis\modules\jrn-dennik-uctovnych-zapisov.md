# JRN - Denník účtovných zápisov

## Popis modulu

Centrálny modul pre správu účtovného denníka (hlavná kniha). Prijíma účtovné zápisy zo všetkých modulov systému NEX Genesis - faktúr, pokladní, bankových výpisov, interných dokladov a skladových pohybov. Poskytuje kompletné podvojné účtovníctvo s analytickými účtami.

## Hlavný súbor

`NexModules\Jrn_F.pas`

## Tabuľky modulu

| Tabuľka | Súbor | Popis | Polí | Indexov |
|---------|-------|-------|------|---------|
| JOURNAL | JOURNAL.BTR | Denník účtovných zápisov | 29 | 9 |
| ACCSNT | ACCSNT.BTR | Účtová osnova (syntetické účty) | 12 | 2 |
| ACCANL | ACCANL.BTR | Obratová predvaha analytických účtov | 49 | 7 |
| ACCANLC | ACCANLC.BTR | Obratová predvaha podľa stredísk | 45 | 3 |

**Celkom: 4 tabuľky, 135 polí, 21 indexov**

## Sub-moduly

### Zobrazenie denníka
| Súbor | Popis |
|-------|-------|
| Jrn_F.pas | Hlavný formulár denníka |
| Jrn_AccLst_V.pas | Zápisy vybraného dokladu |
| Jrn_JrnDir_V.pas | Všetky zápisy denníka |
| Jrn_JrnFilt_F.pas | Filtrovanie zápisov |
| Jrn_JrnFilt_V.pas | Filtrovaný pohľad |

### Účtová osnova
| Súbor | Popis |
|-------|-------|
| Jrn_AccLst_F.pas | Zoznam syntetických účtov |
| Jrn_AccEdit_F.pas | Editor syntetického účtu |
| Jrn_AnlLst_F.pas | Zoznam analytických účtov |
| Jrn_AnlEdit_F.pas | Editor analytického účtu |

### Výkazy a prehľady
| Súbor | Popis |
|-------|-------|
| Jrn_AccBal_F.pas | Obraty a zostatky účtov |
| Jrn_AccStt_F.pas | Stav účtov k dátumu |
| Jrn_AccTrn_F.pas | Obraty účtov za obdobie |
| Jrn_MonBal_F.pas | Mesačné obraty |
| Jrn_YerBal_F.pas | Ročné obraty |

### Tlač
| Súbor | Popis |
|-------|-------|
| Jrn_JrnPrn_F.pas | Tlač denníka |
| Jrn_AccPrn_F.pas | Tlač účtovnej osnovy |
| Jrn_BalPrn_F.pas | Tlač obratov a zostatkov |

### Údržba
| Súbor | Popis |
|-------|-------|
| Jrn_JrnVer_F.pas | Kontrola integrity zápisov |
| Jrn_JrnDel_F.pas | Mazanie zápisov |
| Jrn_AccMrg_F.pas | Zlúčenie účtov |
| Jrn_YerCls_F.pas | Uzatvorenie účtovného roka |

## Prístupové práva (gAfc.Jrn.*)

### Zobrazenie
| Právo | Popis |
|-------|-------|
| JrnLst | Zobrazenie denníka |
| AccLst | Zobrazenie účtovnej osnovy |
| AnlLst | Zobrazenie analytických účtov |
| BalLst | Zobrazenie obratov a zostatkov |

### Účtová osnova
| Právo | Popis |
|-------|-------|
| AccAdd | Pridanie syntetického účtu |
| AccDel | Zmazanie syntetického účtu |
| AccMod | Úprava syntetického účtu |
| AnlAdd | Pridanie analytického účtu |
| AnlDel | Zmazanie analytického účtu |
| AnlMod | Úprava analytického účtu |

### Tlač
| Právo | Popis |
|-------|-------|
| PrnJrn | Tlač denníka |
| PrnAcc | Tlač účtovnej osnovy |
| PrnBal | Tlač obratov |
| TxtExp | Export do textu |
| XlsExp | Export do Excelu |

### Nástroje
| Právo | Popis |
|-------|-------|
| JrnFlt | Filtrovanie denníka |
| AccStt | Stav účtov |
| AccTrn | Obraty účtov |
| MonBal | Mesačné zostatky |
| YerBal | Ročné zostatky |

### Administrácia
| Právo | Popis |
|-------|-------|
| JrnDel | Mazanie zápisov |
| AccMrg | Zlúčenie účtov |
| YerCls | Uzatvorenie roka |
| MntFnc | Údržbové funkcie |
| SerFnc | Servisné funkcie |

## Kľúčové vlastnosti

### Štruktúra účtu
- **AccSnt** = Syntetický účet (3-miestny kód, napr. 321)
- **AccAnl** = Analytický účet (do 6 znakov, napr. 001)
- Plný účet = AccSnt + AccAnl (napr. 321001 = Dodávatelia tuzemskí)

### Typy účtov (SntType/AccType)
| Hodnota | Popis |
|---------|-------|
| A | Aktívny (súvahový - aktíva) |
| P | Pasívny (súvahový - pasíva) |
| N | Nákladový (výsledkový) |
| V | Výnosový (výsledkový) |

### Strany účtovania
- **CredVal** = Má dať (MD / Debit)
- **DebVal** = Dal (D / Credit)
- Suma CredVal musí rovnať sume DebVal (bilančná rovnováha)

### Zdroje zápisov (podľa DocNum prefixu)
| Prefix | Modul | Popis |
|--------|-------|-------|
| IS* | ISB | Dodávateľské faktúry |
| IC* | ICB | Odberateľské faktúry |
| CS* | CSB | Hotovostná pokladňa |
| BS* | BSM | Bankové výpisy |
| ID* | IDB | Interné účtovné doklady |
| IM* | IMB | Interné príjemky |
| OM* | OMB | Interné výdajky |

## Workflow účtovania

```
Zdrojový modul (ISB, ICB, CSB, BSM, IDB...)
         ↓
    A_AccDoc (Zaúčtovanie)
         ↓
    JOURNAL zápisy (MD a Dal)
         ↓
    Aktualizácia obratov (ACCANL, ACCANLC)
         ↓
    DstAcc = 'A' v zdrojovom doklade
```

## Integrácie

### Moduly ktoré účtujú do JOURNAL

| Modul | Typ zápisov |
|-------|-------------|
| ISB | Záväzky voči dodávateľom (321) |
| ICB | Pohľadávky od odberateľov (311) |
| CSB | Pokladňa (211), DPH, tržby |
| BSM | Bankové účty (221), úhrady |
| IDB | Interné zápisy, kurzové rozdiely |
| IMB | Príjem na sklad (účet 131/132) |
| OMB | Výdaj zo skladu (účet 504/542) |

### Číselníky

| Tabuľka | Popis |
|---------|-------|
| ACCSNT | Syntetické účty (účtová osnova) |
| ACCANL | Analytické účty s obratmi |
| ACCANLC | Obraty po strediskách |
| WRILST | Prevádzkové jednotky |
| ECUNIT | Hospodárske strediská |

## Business pravidlá

- Každý zápis musí mať párový zápis (MD = Dal)
- DocNum prepája zápis na zdrojový doklad
- Po zaúčtovaní zdrojový doklad nastaví DstAcc='A'
- Zrušenie účtovania vymaže zápisy z JOURNAL
- Obraty v ACCANL sa aktualizujú automaticky
- BegRec=1 označuje počiatočný stav účtu

## Výkazy

### Obraty a zostatky (z ACCANL)
- Počiatočný stav (CBegVal/DBegVal)
- Mesačné obraty (CTurn01-12/DTurn01-12)
- Konečný stav (CEndVal/DEndVal)
- Zostatok (DiffVal)

### Hlavná kniha (z JOURNAL)
- Chronologický zoznam zápisov
- Filtrovanie podľa účtu, obdobia, partnera

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
