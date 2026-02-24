# TSB - Dodávateľské dodacie listy (Supplier Delivery Notes)

## Prehľad

Modul TSB slúži na evidenciu a spracovanie dodávateľských dodacích listov - príjem tovaru od dodávateľov. Umožňuje evidenciu dokladov, párovanie s faktúrami, príjem na sklad a účtovanie.

## Základné údaje

| Položka | Hodnota |
|---------|---------|
| **Názov modulu** | Dodávateľské dodacie listy |
| **Prefix** | Tsb_, Tsh_, Tsi_ |
| **Hlavný súbor** | NexModules/Tsb_F.pas (1247 riadkov) |
| **Hlavná trieda** | TF_Tsb (extends TLangForm) |
| **Data modul** | DM_STKDAT (dmSTK), DM_DLSDAT (dmDLS) |
| **Kniha definícií** | gBok, gKey.Tsb* |

## Funkcionalita

- Evidencia dodacích listov od dodávateľov
- Príjem tovaru na sklad (skladové pohyby)
- Párovanie s dodávateľskými faktúrami
- Párovanie s objednávkami
- Rozpočet obstarávacích nákladov (CLO, doprava, ostatné)
- Elektronický príjem dokladov (EDI)
- Účtovanie do hlavnej knihy
- Multi-mena (účtovná mena, vyúčtovacia mena)

## Hlavné tabuľky

| Tabuľka | BDF súbor | Polí | Indexov | Popis |
|---------|-----------|------|---------|-------|
| TSH | TSHyynnn.BTR | 128 | 20 | Hlavičky dodacích listov |
| TSI | TSIyynnn.BTR | 64 | 9 | Položky dodacích listov |
| TSN | TSNyynnn.BTR | 6 | 2 | Poznámky k dokladom |
| TSP | TSPyynnn.BTR | 12 | 6 | Výrobné čísla položiek |
| TSBLST | TSBLST.BTR | 41 | 2 | Zoznam kníh DDL |
| TSHOLE | TSHOLE.BTR | 7 | 1 | Voľné poradové čísla |

## Pomenovanie súborov

Formát: `TSx`**yy**`nnn`.BTR
- **yy** = rok (napr. 24 pre 2024)
- **nnn** = číslo knihy (napr. 001)

Príklad: `TSH24001.BTR` = Hlavičky DDL, rok 2024, kniha 001

## Sub-moduly (49)

### Editácia
| Súbor | Popis |
|-------|-------|
| Tsb_TshEdit_F.pas | Editor hlavičky DDL |
| Tsb_TsiEdit_F.pas | Editor položky DDL |
| Tsb_TsiLst_F.pas | Zoznam položiek DDL |
| Tsb_DocDsc_F.pas | Zľava na doklad |

### Príjem na sklad
| Súbor | Popis |
|-------|-------|
| Tsb_IncDoc_F.pas | Príjem všetkých položiek |
| Tsb_IncBook_F.pas | Príjem položiek viacerých dokladov |
| Tsb_StmTsi_F.pas | Porovnanie s pohybmi |
| Tsb_StmTsd_F.pas | Porovnanie dokladu s pohybmi |
| Tsb_StmTsa_F.pas | Porovnanie dokladov s pohybmi |

### Párovanie
| Súbor | Popis |
|-------|-------|
| Tsb_TsiIsi_F.pas | Párovanie DDL s faktúrami |
| Tsb_NoPair_F.pas | Nevypárované doklady |
| Tsb_TsdMpr_F.pas | Spojenie DDL s faktúrou |

### Elektronický prenos
| Súbor | Popis |
|-------|-------|
| Tsb_EdiRcv_F.pas | EDI príjem dokladov |
| Tsb_TsdRcv_F.pas | Elektronický prenos |
| Tsb_TrmRcv_F.pas | Načítanie zo záznamníka |
| Tsb_TrmRcv_V.pas | Zobrazenie dát zo záznamníka |
| Tsb_ImpDoc_F.pas | Import elektronického dokladu |

### Tlač
| Súbor | Popis |
|-------|-------|
| Tsb_DocPrn_F.pas | Tlač dokladu |
| Tsb_TsdPrn_F.pas | Tlač dokladov za obdobie |

### Kontroly a údržba
| Súbor | Popis |
|-------|-------|
| Tsb_TsdVer_F.pas | Hodnotová kontrola |
| Tsb_TsnVer_F.pas | Kontrola interného čísla |
| Tsb_TsiVer_F.pas | Kontrola položiek |
| Tsb_TsdMis_F.pas | Chýbajúce doklady |
| Tsb_DocClc_F.pas | Prepočet dokladov |

### Špeciálne funkcie
| Súbor | Popis |
|-------|-------|
| Tsb_AddAcq_F.pas | Rozpočet obstarávacích nákladov |
| Tsb_DocCopy_F.pas | Kopírovanie dokladu |
| Tsb_TshRen_F.pas | Premenovanie dokladu |
| Tsb_TsiRep_F.pas | Výkaz príjmu tovaru |
| Tsb_DlvSur_V.pas | Zoznam dodávok naviac |
| Tsb_PckRep.pas | Výkaz obalov |

## UI komponenty

- **TV_Tsh**: TTableView - hlavná tabuľka dokladov
- **Nb_BokLst**: TNxbLst - výber knihy
- **AL_Tsb**: TActionList - 70+ akcií

## Prístupové práva (gAfc.Tsb.*)

| Právo | Popis |
|-------|-------|
| DocAdd | Pridanie dokladu |
| DocDel | Zmazanie dokladu |
| DocDsc | Zľava na doklad |
| DocRnd | Zaokrúhlenie |
| DocLck | Uzamknutie dokladu |
| DocUnl | Odomknutie dokladu |
| VatChg | Zmena DPH |
| SitLst | Zobrazenie položiek |
| AccLst | Zobrazenie účtovania |
| NpaDoc | Nevypárované doklady |
| DlvSur | Dodávky naviac |
| PrnDoc | Tlač dokladu |
| PrnMas | Hromadná tlač |
| PrnLst | Tlač zoznamu |
| PrnLab | Tlač etikiet |
| DocFlt | Filtrovanie |
| DocStp | Príjem na sklad |
| DocCpy | Kopírovanie |
| AccDoc | Účtovanie dokladu |
| AccDel | Zrušenie účtovania |
| AccMas | Hromadné účtovanie |
| DocEtr | Elektronický prenos |
| TsdMpr | Spojenie s faktúrou |
| AddAcq | Obstarávacie náklady |
| TrmRcv | Príjem zo záznamníka |
| TsiRep | Výkaz príjmu |
| MntFnc | Údržbové funkcie |
| SerFnc | Servisné funkcie |

## Multi-mena štruktúra

### Účtovná mena (Ac*)
Hodnoty v účtovnej mene (EUR):
- AcCValue - NC bez DPH
- AcEValue - NC s DPH
- AcDscVal - Zľava
- AcZValue - Clo
- AcTValue - Doprava
- AcOValue - Ostatné náklady

### Vyúčtovacia mena (Fg*)
Hodnoty v mene faktúry:
- FgCValue - NC bez DPH
- FgEValue - NC s DPH
- FgCourse - Kurz

## Workflow

```
┌──────────────────────────────────────────────────────────┐
│                   TSB Workflow                           │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  1. Vytvorenie DDL                                       │
│     ├── Manuálne (Tsb_TshEdit_F)                        │
│     └── EDI import (Tsb_EdiRcv_F)                       │
│                                                          │
│  2. Zadanie položiek (TSI)                              │
│     ├── Manuálne (Tsb_TsiEdit_F)                        │
│     └── Import z faktúry                                │
│                                                          │
│  3. Príjem na sklad (DstStk = 'S')                      │
│     └── Vytvorenie STM pohybov                          │
│                                                          │
│  4. Párovanie s faktúrou (ISB)                          │
│     └── DstPair = 'Q'                                   │
│                                                          │
│  5. Účtovanie (DstAcc = 'A')                            │
│     └── Zápisy do JRN                                   │
│                                                          │
│  6. Uzamknutie (DstLck = 1)                             │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

## Príznaky stavu dokladu

| Pole | Hodnota | Popis |
|------|---------|-------|
| DstStk | N | Položky nie sú prijaté na sklad |
| DstStk | S | Všetky položky sú prijaté |
| DstPair | N | Nevypárované s faktúrou |
| DstPair | Q | Vypárované s faktúrou |
| DstPair | C | Uhradené v hotovosti |
| DstLck | 0 | Odomknutý doklad |
| DstLck | 1 | Uzamknutý doklad |
| DstAcc | A | Zaúčtovaný doklad |

## Závislosti na iných moduloch

```
┌─────────────────────────────────────────────────────┐
│                    TSB Modul                         │
├─────────────────────────────────────────────────────┤
│                                                      │
│  PAB (Partneri) ────────► TSH.PaCode (dodávateľ)    │
│                                                      │
│  GSC (Produkty) ────────► TSI.GsCode                │
│                                                      │
│  STK (Sklady)   ────────► príjem na sklad (STM)     │
│                                                      │
│  ISB (Faktúry)  ◄────────► párovanie s TSH.IsdNum   │
│                                                      │
│  OSD (Objednávky) ◄──────► párovanie s TSI.OsdNum   │
│                                                      │
│  JRN (Účtovníctvo) ◄──────► účtovanie dokladov     │
│                                                      │
│  PLS (Cenníky)  ────────► TSH.PlsNum                │
│                                                      │
└─────────────────────────────────────────────────────┘
```

## Stav migrácie

- [x] Btrieve modely TSH, TSI (packages/nexdata/)
- [ ] PostgreSQL modely (packages/nex-staging/)
- [ ] API endpoints
- [ ] Desktop UI (PySide6)
- [ ] Web UI (React)
- [ ] Testy
- [ ] Dokumentácia

## Poznámky

- Modul je prepojený so skladovým hospodárstvom (STK)
- Podporuje viacnásobné DPH sadzby (VatPrc1-5)
- Obstarávacie náklady sa rozpočítavajú na položky
- Kódovanie: KEYBCS2 (Kamenický) pre SK/CZ znaky
