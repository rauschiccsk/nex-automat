# IMB - Interné skladové príjemky

## Popis modulu

Modul pre evidenciu a spracovanie interných skladových príjemok. Používa sa pre príjem tovaru bez dodávateľa - inventúrne prebytky, vrátenia z výroby, vlastná výroba, medziskladové presuny a iné interné príjmy.

## Hlavný formulár

**Súbor:** `NexModules\Imb_F.pas`
**Trieda:** `TF_Imb`
**Mark modulu:** `IMB`

## Funkcie modulu

### Správa dokladov
- Nový doklad (A_DocAdd) - vytvorenie novej príjemky
- Vymazanie dokladu (A_DocDel) - zrušenie príjemky s reverziou pohybov
- Uzamknutie dokladu (A_DocLck)
- Odomknutie dokladu (A_DocUnl)
- Prepočet dokladu (A_ImhCalc)
- Zmena sadzieb DPH (A_VatChg)

### Položky
- Zoznam položiek (A_SitLst) - Imb_ImiLst_F
- Editor položky (Imb_ItmEdi_F)
- Položky všetkých príjemok (A_ImiDir) - Imb_ImiDir_V

### Príjem na sklad
- Príjem vybraného dokladu (A_IncDoc) - Imb_IncDoc_F
- Hromadný príjem za knihu (A_IncBook) - Imb_IncBook_F

### Účtovanie
- Zaúčtovanie dokladu (A_AccDoc) - Imb_DocAcc
- Hromadné zaúčtovanie (A_AccBok) - Imb_BokAcc
- Zrušenie zaúčtovania (A_AccDel)
- Účtovné zápisy dokladu (A_AccLst) - Jrn_AccLst_V

### Tlač
- Tlač dokladu (A_DocPrn) - Imb_DocPrn_F
- Hromadná tlač (A_DocsPrn) - Imb_DocPrn_F
- Zoznam dokladov (A_ImhPrn)
- Zoznam dokladov za obdobie (A_ImdPrn) - Imb_ImdPrn_F

### Import
- Import elektronického dokladu (A_ImpDoc) - Imb_ImpDoc_F
- Import z CSV (A_ImpCSV) - Imb_ImpCSV_F
- Import váhového dokladu (A_ImpWgd) - WgdImp_F
- Načítanie z elektronickej váhy (A_WghRcv) - Imb_WghRcv_F
- Načítanie záznamníkových príjemok (A_TrdInc) - Doc_TrdInc_F

### Nástroje
- Filtrovanie dokladov (A_ImdFilt) - Imb_ImdFilt_F
- Evidencia skladových pohybov (A_SmLst) - Stk_SmLst_V
- Výkaz prijatého majetku (A_ImiFxa) - Imb_ImiFxa_F
- Dodatočne pridané položky (A_CrdDif) - Imb_CrdDif_F

### Údržba
- Porovnávanie dokladu s pohybmi (A_StmImd) - Imb_StmImd_F
- Porovnávanie dokladov s pohybmi (A_StmIma) - Imb_StmIma_F
- Obnova položiek podľa hlavičky (A_ImiRef) - Imb_ImiRef_F

### Servis
- Zmena položiek na neodpočítané (A_ImiToN) - Imb_ImiToN_F

## Prístupové práva (gAfc.Imb.*)

### Úpravy
| Právo | Popis |
|-------|-------|
| DocAdd | Pridanie dokladu |
| DocDel | Vymazanie dokladu |
| DocMod | Úprava dokladu |
| DocLck | Uzamknutie dokladu |
| DocUnl | Odomknutie dokladu |
| VatChg | Zmena DPH sadzieb |

### Zobrazenie
| Právo | Popis |
|-------|-------|
| SitLst | Zoznam položiek |
| AccLst | Účtovné zápisy |

### Tlač
| Právo | Popis |
|-------|-------|
| PrnDoc | Tlač dokladu |
| PrnMas | Hromadná tlač |
| PrnLst | Tlač zoznamu |
| PrnLab | Tlač štítkov |

### Nástroje
| Právo | Popis |
|-------|-------|
| DocFlt | Filter dokladov |
| DocStp | Príjem na sklad |
| AccDoc | Zaúčtovanie dokladu |
| AccDel | Zrušenie zaúčtovania |
| AccMas | Hromadné zaúčtovanie |
| MovLst | Evidencia pohybov |
| WghRcv | Príjem z váhy |
| OitSnd | Interný prenos |
| TrmInc | Záznamníkové príjemky |
| EdoImp | Import elektronického dokladu |
| ImiFxa | Výkaz prijatého majetku |

### Položky
| Právo | Popis |
|-------|-------|
| ItmAdd | Pridanie položky |
| ItmDel | Vymazanie položky |
| ItmMod | Úprava položky |

### Administrácia
| Právo | Popis |
|-------|-------|
| MntFnc | Údržbové funkcie |
| SerFnc | Servisné funkcie |

## Tabuľky modulu

### Hlavné dátové tabuľky
| Tabuľka | Súbor | Popis | Polí | Indexov |
|---------|-------|-------|------|---------|
| IMH | IMHyynnn.BTR | Hlavičky príjemok | 76 | 15 |
| IMI | IMIyynnn.BTR | Položky príjemok | 52 | 15 |
| IMN | IMNyynnn.BTR | Poznámky | 4 | 2 |
| IMP | IMPyynnn.BTR | Výrobné čísla | 12 | 6 |
| IMW | IMWnnnnn.BTR | Váhové balíčky | 14 | 3 |

### Konfiguračné tabuľky
| Tabuľka | Súbor | Popis | Polí | Indexov |
|---------|-------|-------|------|---------|
| IMBLST | IMBLST.BTR | Zoznam kníh | 36 | 2 |
| IMHOLE | IMHOLE.BTR | Voľné poradové čísla | 5 | 1 |
| IMPLST | IMPLST.BTR | Zoznam importov | 5 | 3 |
| IMPDEF | IMPDEF.BTR | Definície importu | 11 | 2 |

## Sub-moduly (27 formulárov)

### Editačné formuláre
- `Imb_F.pas` - Hlavný formulár modulu
- `Imb_ImhEdit_F.pas` - Editor hlavičky príjemky
- `Imb_ImiLst_F.pas` - Zoznam položiek
- `Imb_ItmEdi_F.pas` - Editor položky

### Príjem a spracovanie
- `Imb_IncDoc_F.pas` - Príjem dokladu na sklad
- `Imb_IncBook_F.pas` - Hromadný príjem za knihu

### Účtovanie
- `Imb_DocAcc.pas` - Zaúčtovanie dokladu
- `Imb_BokAcc.pas` - Hromadné zaúčtovanie

### Tlač
- `Imb_DocPrn_F.pas` - Tlač dokladu
- `Imb_ImdPrn_F.pas` - Zoznam dokladov za obdobie

### Filtrovanie
- `Imb_ImdFilt_F.pas` - Filter dokladov
- `Imb_ImdFilt_V.pas` - Prehľad filtrovaných
- `Imb_DocFilt_F.pas` - Filter dokladov (starší)

### Import
- `Imb_ImpDoc_F.pas` - Import elektronického dokladu
- `Imb_ImpCSV_F.pas` - Import z CSV
- `Imb_WghRcv_F.pas` - Príjem z elektronickej váhy

### Prehľady
- `Imb_ImiDir_V.pas` - Položky všetkých príjemok
- `Imb_DocLst_V.pas` - Zoznam dokladov
- `Imb_ImiFxa_F.pas` - Výkaz prijatého majetku
- `Imb_CrdDif_F.pas` - Dodatočne pridané položky

### Údržba a servis
- `Imb_StmImd_F.pas` - Porovnanie dokladu s pohybmi
- `Imb_StmIma_F.pas` - Porovnanie dokladov s pohybmi
- `Imb_StmImi_F.pas` - Porovnanie položiek
- `Imb_ImiRef_F.pas` - Obnova položiek
- `Imb_ImiToN_F.pas` - Zmena na neodpočítané

### Šarže
- `Imb_RbaHis.pas` - História šarží
- `Imb_RbaCum.pas` - Kumulácia šarží

## Workflow

```
1. Vytvorenie novej príjemky (IMH)
   ↓
2. Zadanie položiek (IMI)
   ├→ Ručné zadanie
   ├→ Import z CSV/elektronického dokladu
   └→ Príjem z elektronickej váhy
   ↓
3. Kontrola a prepočet
   ↓
4. Príjem na sklad (A_IncDoc)
   ├→ Aktualizácia STK (skladové karty)
   ├→ Aktualizácia STM (skladové pohyby)
   └→ IMI.StkStat = 'S'
   ↓
5. Zaúčtovanie (voliteľné)
   ↓
6. Tlač dokladu
   ↓
7. Uzatvorenie (DstLck = 1)
```

## Farebné kódovanie riadkov

| Farba | Stav |
|-------|------|
| Čierna | Štandardný doklad |
| Červená | Doklad nie je prijatý na sklad (DstStk='N') |

## Väzby na iné moduly

| Modul | Väzba | Popis |
|-------|-------|-------|
| STK | IMH.StkNum → STKLST.StkNum | Cieľový sklad |
| GSC | IMI.GsCode → GSCAT.GsCode | Tovar |
| STM | Skladové pohyby | Evidencia pohybov |
| OCB | IMH.OcdNum → OCH.DocNum | Zdrojová zákazka |
| RMB | IMH.OmdNum | Zdrojová výdajka (medziskladový presun) |
| JRN | Účtovný denník | Zaúčtované doklady |

## Stavy dokladu

### DstStk (Stav skladu)
| Hodnota | Popis |
|---------|-------|
| N | Nezaevidovaný na sklade |
| S | Zaevidovaný na sklade |

### DstLck (Uzamknutie)
| Hodnota | Popis |
|---------|-------|
| 0 | Odomknutý |
| 1 | Uzamknutý |

### DstAcc (Účtovanie)
| Hodnota | Popis |
|---------|-------|
| (prázdne) | Nezaúčtovaný |
| A | Zaúčtovaný |

### StkStat položky (IMI)
| Hodnota | Popis |
|---------|-------|
| N | Zaevidovaná (nezaskladnená) |
| S | Naskladnená |

## Typy interných príjemok

- Inventúrne prebytky
- Vrátenia z výroby
- Vlastná výroba
- Medziskladové presuny (príjem z iného skladu)
- Vrátenia od zákazníkov
- Opravy chybných výdajov

## Stav migrácie

- [x] Analýza modulu
- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
