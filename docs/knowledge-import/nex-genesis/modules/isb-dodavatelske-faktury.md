# ISB - Dodávateľské faktúry

## Popis modulu

Modul pre evidenciu a spracovanie dodávateľských faktúr (záväzky). Poskytuje kompletnú funkcionalitu pre príjem, párovanie s dodacími listami, sledovanie úhrad a účtovanie faktúr.

## Hlavný formulár

**Súbor:** `NexModules\Isb_F.pas`
**Trieda:** `TF_Isb`
**Data modul:** `DM_LDGDAT` (účtovné doklady)

## Funkcie modulu

### Správa dokladov
- Nový doklad (A_DocNew) - vytvorenie novej faktúry
- Vymazanie dokladu (A_DocDel) - zrušenie faktúry
- Úprava dokladu (A_DocRev) - zmena hodnôt faktúry
- Kopírovanie dokladu (A_DocCopy)
- Uzamknutie/Odomknutie (A_DocLck, A_UnLock)
- Zaokrúhlenie (A_DocRnd)
- Zľava na doklad (A_DocDsc)
- Vystavenie dobropisu (A_CorGen)

### Párovanie a likvidácia
- Párovanie s DDL (A_TsdPair) - pripojenie dodacích listov
- Likvidácia faktúry (A_IsdLiq) - kompletné spracovanie

### Úhrady
- História úhrad (A_PayLst)
- Denník úhrad (A_PmiLst)
- Prepočet úhrady (A_PayCalc)
- Záväzky k dátumu (A_IsdPay)
- Záväzky podľa splatnosti (A_IspEvl)
- Neuhradené faktúry (A_NpyIsd)
- História prevodných príkazov (A_PmqLst)

### Účtovanie
- Zaúčtovanie dokladu (A_AccDoc)
- Zrušenie účtovania (A_AccDel)
- Hromadné účtovanie (A_AccPer)
- Účtovné zápisy (A_AccLst)

### Tlač a reporty
- Tlač dokladu (A_PrnDoc)
- Hromadná tlač (A_PrnMas)
- Zoznam dokladov (A_PrnLst)

### Údržba
- Správa kníh (A_AddBook, A_ModBook, A_DelBook)
- Prepočet hlavičky (A_IshCalc)
- Kontrola dokladov (A_IsdVer)
- Kontrola poznámok (A_IsnVer)
- Chýbajúce čísla (A_MisNum)
- Obnova položiek (A_ItmRef)
- Zmena DPH sadzieb (A_VatChg)
- Kurzové prepočty (A_DvzCalc, A_AcvClc)

## Prístupové práva (gAfc.Isb.*)

### Úpravy
| Právo | Popis |
|-------|-------|
| DocAdd | Pridanie dokladu |
| DocDel | Vymazanie dokladu |
| DocDsc | Zľava na doklad |
| DocLck | Uzamknutie dokladu |
| DocUnl | Odomknutie dokladu |
| DocRnd | Zaokrúhlenie dokladu |
| DocEdi | Úprava dokladu |
| DocSpc | Špecifikácia dokladu |
| VatChg | Zmena DPH sadzieb |
| ItmRnd | Zaokrúhlenie položiek |

### Zobrazenie
| Právo | Popis |
|-------|-------|
| SitLst | Zoznam položiek |
| AccLst | Účtovné zápisy |
| PayLst | História úhrad |
| PmiLst | Denník úhrad |
| PqbLst | Prevodné príkazy |
| NpyIsd | Neuhradené faktúry |
| IswLst | Evidencia upomienok |

### Tlač
| Právo | Popis |
|-------|-------|
| PrnDoc | Tlač dokladu |
| PrnMas | Hromadná tlač |
| PrnLst | Zoznam dokladov |

### Nástroje
| Právo | Popis |
|-------|-------|
| DocFlt | Filtrovanie dokladov |
| AccDoc | Zaúčtovanie |
| AccDel | Zrušenie účtovania |
| AccMas | Hromadné účtovanie |
| TsdPar | Párovanie s DDL |
| IsdPay | Záväzky k dátumu |
| IspEvl | Záväzky podľa splatnosti |
| DocCpy | Kopírovanie dokladu |
| IsdLiq | Likvidácia faktúry |

### Administrácia
| Právo | Popis |
|-------|-------|
| MntFnc | Údržbové funkcie |
| SerFnc | Servisné funkcie |
| ItmAdd | Pridanie položky |
| ItmDel | Vymazanie položky |
| ItmMod | Úprava položky |

## Tabuľky modulu

### Hlavné dátové tabuľky
| Tabuľka | Súbor | Popis | Polí | Indexov |
|---------|-------|-------|------|---------|
| ISH | ISHyynnn.BTR | Hlavičky faktúr | 124 | 15 |
| ISI | ISIyynnn.BTR | Položky faktúr | 47 | 6 |
| ISN | ISNyynnn.BTR | Poznámky | 5 | 2 |
| ISW | ISWbbbbb.BTR | Upomienky | 13 | 2 |

### Číselníky a konfigurácia
| Tabuľka | Súbor | Popis | Polí | Indexov |
|---------|-------|-------|------|---------|
| ISBLST | ISBLST.BTR | Zoznam kníh | 41 | 1 |
| ISDSPC | ISDSPC.BTR | Špecifikácie dokladov | 12 | 1 |
| ISPDEF | ISPDEF.BTR | Definícia období splatnosti | 9 | 1 |
| ISRLST | ISRLST.BTR | Réžijné položky | 16 | 3 |
| ISHOLE | ISHOLE.BTR | Voľné poradové čísla | 7 | 1 |

### Kurzové prepočty
| Tabuľka | Súbor | Popis | Polí | Indexov |
|---------|-------|-------|------|---------|
| ISRCRH | ISRCRH.BTR | Hlavičky prekurzovania | 18 | 1 |
| ISRCRI | ISRCRI.BTR | Položky prekurzovania | 26 | 3 |

### Úhrady
| Tabuľka | Súbor | Popis | Polí | Indexov |
|---------|-------|-------|------|---------|
| PMI | PMIyyyy.BTR | Denník úhrad faktúr | 27 | 10 |
| PMQ | PMQyyyy.BTR | História prevodných príkazov | 13 | 4 |

## Sub-moduly (42 formulárov)

### Editačné formuláre
- `Isb_IshEdit_F.pas` - Hlavička faktúry
- `Isb_IsiLst_F.pas` - Položky faktúry
- `Isb_IsrEdit_F.pas` - Réžijná položka
- `Isb_IswEdit_F.pas` - Úprava upomienky
- `Isb_DocDel_F.pas` - Zrušenie faktúry
- `Isb_DocRev_F.pas` - Úprava tuzemskej faktúry
- `Isb_FgdRev_F.pas` - Úprava zahraničnej faktúry
- `Isb_DocCopy_F.pas` - Kopírovanie dokladu

### Zobrazenia a zoznamy
- `Isb_IsiDir_V.pas` - Položky všetkých faktúr
- `Isb_NpyIsd_V.pas` - Neuhradené faktúry
- `Isb_PmqLst_V.pas` - História prevodných príkazov
- `Isb_IswLst_V.pas` - Evidencia upomienok
- `Isb_IsrLst_V.pas` - Zoznam réžijných položiek
- `Isb_IsdLst_V.pas` - Zoznam faktúr
- `Isb_IsdFilt_V.pas` - Filtrované faktúry
- `Isb_DocSpc_V.pas` - Špecifikácie dokladov
- `Isb_IspDef_V.pas` - Obdobia splatnosti

### Nástroje
- `Isb_TsdPair_F.pas` - Párovanie s DDL
- `Isb_IsdLiq_F.pas` - Likvidácia faktúry
- `Isb_DocDsc_F.pas` - Zľava na doklad
- `Isb_DocRnd_F.pas` - Zaokrúhlenie
- `Isb_DocFlt_F.pas` - Filtrovanie dokladov
- `Isb_IsdFilt_F.pas` - Filtrovanie faktúr
- `Isb_IsdPay_F.pas` - Záväzky k dátumu
- `Isb_IspEvl_F.pas` - Záväzky podľa splatnosti
- `Isb_CrsChg_F.pas` - Kurzové prepočty
- `Isb_IsReCrs_F.pas` - Prekurzovanie

### Kontroly a údržba
- `Isb_IsdVer_F.pas` - Kontrola dokladov
- `Isb_IsnVer_F.pas` - Kontrola poznámok
- `Isb_PmiVer_F.pas` - Kontrola úhrad
- `Isb_IsdRen_F.pas` - Prečíslovanie
- `Isb_DocDate_F.pas` - Doplnenie dátumu
- `Isb_AccDate_F.pas` - Dátum účtovania

### Tlač
- `Isb_DocPrn_F.pas` - Tlač dokladu
- `Isb_IsdPrn_F.pas` - Zoznam dokladov
- `Isb_AccPrn.pas` - Hromadná tlač

### Pomocné
- `Isb_DocSpc_F.pas` - Špecifikácia dokladu
- `Isb_ExtNum_F.pas` - Externé číslo
- `Isb_IspDef_F.pas` - Definícia období
- `Isb_IsrLst_F.pas` - Zoznam réžií
- `Isb_BcSrch_F.pas` - Vyhľadávanie čiarového kódu

## Workflow

```
1. Príjem faktúry od dodávateľa
   ↓
2. Vytvorenie hlavičky (ISH)
   ↓
3. Zadanie/Import položiek (ISI)
   ↓
4. Párovanie s dodacími listami (TSH/TSI)
   ↓
5. Likvidácia faktúry
   ↓
6. Zaúčtovanie (JRN)
   ↓
7. Úhrada faktúry (PMI)
   ↓
8. Koncoročné prekurzovanie (ISRCRH/ISRCRI)
```

## Väzby na iné moduly

| Modul | Väzba | Popis |
|-------|-------|-------|
| TSB | ISI.TsdNum → TSH.DocNum | Párovanie s dodacími listami |
| PAB | ISH.PaCode → PAB.PaCode | Dodávateľ |
| STK | ISH.StkNum → STKLST.StkNum | Sklad |
| GSC | ISI.GsCode → GSCAT.GsCode | Tovar |
| JRN | ISH.DocNum → JRN.DocNum | Účtovné zápisy |

## Multi-mena architektúra

### Meny na faktúre
- **AcDvzName** - Účtovná mena (EUR)
- **FgDvzName** - Mena faktúry (cudzia mena)

### Hodnoty
- **Ac*** - Účtovná mena (AcCValue, AcEValue, AcPayVal, AcEndVal)
- **Fg*** - Mena faktúry (FgCValue, FgEValue, FgPayVal, FgEndVal)

### Kurzy
- **FgCourse** - Kurz faktúry k dňu vystavenia
- **EyCourse** - Koncoročný kurz pre prekurzovanie
- **EyCrdVal** - Kurzový rozdiel

## Stavy faktúry

### DstLck (Uzamknutie)
| Hodnota | Popis |
|---------|-------|
| 0 | Odomknutý |
| 1 | Uzamknutý |

### DstPair (Párovanie)
| Hodnota | Popis |
|---------|-------|
| N | Nevypárované |
| Q | Vypárované s DDL |

### DstAcc (Účtovanie)
| Hodnota | Popis |
|---------|-------|
| (prázdne) | Nezaúčtované |
| A | Zaúčtované |

### DstLiq (Likvidácia)
| Hodnota | Popis |
|---------|-------|
| (prázdne) | Nelikvidované |
| L | Likvidované |

## Stav migrácie

- [x] Analýza modulu
- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
