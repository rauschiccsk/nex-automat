# STK - Skladové karty zásob (Stock Management)

## Prehľad

Modul STK slúži na komplexnú správu skladov, skladových kariet, pohybov (príjemky, výdajky), FIFO oceňovania a inventúr. Je to jeden z najrozsiahlejších modulov NEX Genesis.

## Základné údaje

| Položka | Hodnota |
|---------|---------|
| **Názov modulu** | Skladové karty zásob |
| **Prefix** | Stk_ |
| **Hlavný súbor** | NexModules/Stk_F.pas (1317 riadkov) |
| **Hlavná trieda** | TF_Stk (extends TLangForm) |
| **Data modul** | DM_STKDAT (dmSTK), DM_DLSDAT (dmDLS) |

## Funkcionalita

- Evidencia skladových kariet (zásoby, ceny, normatívy)
- FIFO oceňovanie skladových zásob
- Evidencia skladových pohybov (príjem, výdaj, presun)
- Správa viacerých skladov (multi-warehouse)
- Sledovanie výrobných čísel a šarží
- Pozičné skladovanie (bin locations)
- Finančné vyhodnotenie a reporty
- Kontroly konzistencie (FIFO, pohyby, počiatočné stavy)

## Hlavné tabuľky

| Tabuľka | BDF súbor | Polí | Indexov | Popis |
|---------|-----------|------|---------|-------|
| STK | STKxxxxx.BTR | 64 | 18 | Skladové karty (x=číslo skladu) |
| STKLST | STKLST.BTR | 14 | 2 | Zoznam skladov |
| STM | STMxxxxx.BTR | 26 | 10 | Skladové pohyby |
| FIF | FIFxxxxx.BTR | 20 | 11 | FIFO karty |
| STB | STBxxxxx.BTR | 27 | 3 | Počiatočné stavy |
| STS | STSxxxxx.BTR | 11 | 5 | Rezervácie predaja |
| STKPDN | STKPDN.BTR | 16 | 5 | Výrobné čísla |
| STKPOS | STKPOS.BTR | 9 | 4 | Pozičné miesta |
| STKOFR | STKOFR.BTR | 10 | 5 | Ponuky od dodávateľov |

## Číselníky

| Tabuľka | BDF súbor | Popis |
|---------|-----------|-------|
| SMLST | STMLST.BTR | Zoznam skladových operácií |
| SMGDEF | SMGDEF.BTR | Definícia skupín pre vyhodnotenie |

## Sub-moduly (99+)

### Zobrazenie a informácie
| Súbor | Popis |
|-------|-------|
| Stk_StcInf_F.pas | Skladová karta - detail |
| Stk_ActFif_V.pas | Nevydané FIFO karty |
| Stk_AllFif_V.pas | Všetky FIFO karty položky |
| Stk_StmLst_F.pas | História skladových pohybov |
| Stk_StmHst_F.pas | História pohybov za roky |
| Stk_StcLst_V.pas | Zásoba v jednotlivých skladoch |
| Stk_CpaLst_V.pas | Odberatelia vybranej položky |
| Stk_SpaLst_V.pas | Dodávatelia vybranej položky |
| Stk_SapLst_V.pas | Ceny z predajných cenníkov |
| Stk_MinLst_V.pas | Skladové nad normatívy |
| Stk_MaxLst_V.pas | Skladové pod normatívy |
| Stk_StsLst_V.pas | Rezervácie na predaj |
| Stk_SpcLst_V.pas | Zásoba na pozičných miestach |
| Stk_StbLst.pas | Počiatočné stavy tovaru |

### Vyhľadávanie
| Súbor | Popis |
|-------|-------|
| Stk_BcSrch_F.pas | Hľadať podľa čiarového kódu |
| Stk_NaSrch_F.pas | Hľadať podľa časti názvu |
| Stk_StcFilt_F.pas | Filtrovať skladové karty |
| Stk_MgcFlt_F.pas | Filter podľa tovarovej skupiny |

### Finančné vyhodnotenia
| Súbor | Popis |
|-------|-------|
| Stk_StEval_F.pas | Finančné vyhodnotenie skladov |
| Stk_SmEval_F.pas | Finančné vyhodnotenie ku dňu |
| Stk_SmgEvl_F.pas | Zásoba podľa skupín |
| Stk_StmSum_F.pas | Finančné vyhodnotenie pohybov |
| Stk_StmAcc_F.pas | Finančné vyhodnotenie účtov |
| Stk_StvTrn_F.pas | Vyhodnotenie obrátkovosti |
| Stk_RndDif_F.pas | Výkaz cenových rozdielov |

### Výkazy
| Súbor | Popis |
|-------|-------|
| Stk_DayStm_F.pas | Denný výkaz príjmov a výdajov |
| Stk_DayStc_F.pas | Zásoba k zadanému dátumu |
| Stk_SapStc_F.pas | Zásoba podľa dodávateľov |
| Stk_StmItm_F.pas | Výkaz skladových pohybov |
| Stk_NusStc_F.pas | Nepoužité skladové karty |
| Stk_DrbLst_F.pas | Trvanlivosť položiek |
| Stk_NtrStc_F.pas | Neobrátkový tovar |
| Stk_StmRep_F.pas | Výkaz spotreby |
| Stk_SalMov.pas | Výkaz pohybov predaja |

### Údržba a kontroly
| Súbor | Popis |
|-------|-------|
| Stk_ReCalc_F.pas | Prepočet skladovej karty |
| Stk_StkCalc_F.pas | Prepočet všetkých kariet |
| Stk_Synchr_F.pas | Synchronizácia základných údajov |
| Stk_StcVer_F.pas | Kontrola skladových kariet |
| Stk_FifVer_F.pas | Kontrola FIFO kariet |
| Stk_FifDup.pas | Kontrola duplicity FIFO |
| Stk_StmDup_F.pas | Kontrola duplicity pohybov |
| Stk_DocVer_F.pas | Kontrola pohybov podľa dokladov |
| Stk_LosStm_F.pas | Chýbajúce skladové pohyby |
| Stk_LosStc_F.pas | Chýbajúce skladové karty |
| Stk_BegVer_F.pas | Kontrola počiatočného stavu |
| Stk_CpcVer_F.pas | Kontrola nákupných cien |
| Stk_StpVer.pas | Kontrola pozičnej zásoby |

### FIFO operácie
| Súbor | Popis |
|-------|-------|
| Stk_FifClc_F.pas | Prepočet FIFO a pohybov |
| Stk_FifCor_F.pas | Prepočet nulových FIFO |
| Stk_FifGen_F.pas | Generovanie FIFO |
| Stk_FifEdit_F.pas | Editácia FIFO karty |
| Stk_FifLst_F.pas | Zoznam FIFO kariet |
| Stk_FifoPrn_F.pas | Tlač FIFO kariet |

### Servisné funkcie
| Súbor | Popis |
|-------|-------|
| Stk_AvgRef_F.pas | Aktualizácia priemernej NC |
| Stk_LastRef_F.pas | Aktualizácia poslednej NC |
| Stk_StmDir_V.pas | Denník skladových pohybov |
| Stk_SalClc_F.pas | Prepočet rezervácií ERP |
| Stk_NrmClc_F.pas | Výpočet normatívov |
| Stk_MinMax_F.pas | Správa normatívov |

## UI komponenty

- **TV_Stk**: TTableView - hlavná tabuľka skladových kariet
- **BL_StkLst**: TBookList - výber skladu
- **AL_Tcb**: TActionList - 80+ akcií

## Multi-warehouse architektúra

```
STKLST.BTR           → Zoznam skladov
├── StkNum=1         → STK00001.BTR, STM00001.BTR, FIF00001.BTR
├── StkNum=2         → STK00002.BTR, STM00002.BTR, FIF00002.BTR
└── StkNum=3         → STK00003.BTR, STM00003.BTR, FIF00003.BTR
```

## FIFO oceňovanie

```
Príjem tovaru → Vytvorenie FIFO karty (Status=A)
                     ↓
Výdaj tovaru  → Čerpanie z FIFO kariet (FIFO princíp)
                     ↓
Spotrebovanie → FIFO karta (Status=X)

Stavy FIFO karty:
- A = Aktívna (obsahuje zásobu)
- W = Čakajúca
- X = Spotrebovaná (ActQnt=0)
```

## Skladové pohyby (SmCode)

| SmSign | Typ | Príklad |
|--------|-----|---------|
| + | Príjem | Príjemka od dodávateľa |
| - | Výdaj | Výdajka na predaj |
| + | Prevod príjem | Presun medzi skladmi |
| - | Prevod výdaj | Presun medzi skladmi |

## Vzťahy s inými modulmi

```
┌─────────────────────────────────────────────────────┐
│                    STK Modul                         │
├─────────────────────────────────────────────────────┤
│                                                      │
│  GSC (Produkty) ────────► STK.GsCode                │
│                                                      │
│  PAB (Partneri) ────────► STM.PaCode, STM.SpaCode   │
│                                                      │
│  ISC (Príjemky) ────────► STM.DocNum                │
│                                                      │
│  OSC (Výdajky)  ────────► STM.DocNum                │
│                                                      │
│  ORC (Objednávky) ──────► STM.OcdNum, STS           │
│                                                      │
│  POS (Pokladňa) ────────► STS (rezervácie)          │
│                                                      │
└─────────────────────────────────────────────────────┘
```

## Kľúčové koncepty

### Množstvové polia v STK

| Pole | Popis |
|------|-------|
| BegQnt | Počiatočný stav |
| InQnt | Celkový príjem |
| OutQnt | Celkový výdaj |
| ActQnt | Aktuálna zásoba (BegQnt + InQnt - OutQnt) |
| FreQnt | Voľné množstvo (ActQnt - SalQnt - OcdQnt) |
| SalQnt | Predané, neodpočítané |
| OcdQnt | Rezervované pre objednávky |
| OsdQnt | Objednané u dodávateľa |

### Cenové polia

| Pole | Popis |
|------|-------|
| AvgPrice | Priemerná NC (vážený priemer) |
| LastPrice | Posledná NC |
| ActPrice | Aktuálna NC (podľa aktívnej FIFO) |
| BPrice | Predajná cena s DPH |

## Prístupové práva

Modul využíva gAfc.Stk.* štruktúru, ale konkrétna implementácia je prázdna v AccesControl.

## Stav migrácie

- [ ] Btrieve modely (packages/nexdata/)
- [ ] PostgreSQL modely (packages/nex-staging/)
- [ ] API endpoints
- [ ] Desktop UI (PySide6)
- [ ] Web UI (React)
- [ ] Testy
- [ ] Dokumentácia

## Poznámky

- Najkomplexnejší modul NEX Genesis (99+ sub-modulov)
- Kritický pre správne účtovanie zásob
- FIFO princíp je povinný pre účtovníctvo SR/CZ
- Prepojený so všetkými dokladovými modulmi
- Kódovanie: KEYBCS2 (Kamenický) pre SK/CZ znaky
