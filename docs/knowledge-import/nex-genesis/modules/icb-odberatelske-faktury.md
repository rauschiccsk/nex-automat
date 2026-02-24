# ICB - Odberateľské faktúry

## Popis modulu

Modul pre evidenciu a spracovanie odberateľských faktúr (pohľadávok). Zabezpečuje vystavovanie faktúr, sledovanie úhrad, správu upomienok, penalizáciu a integráciu s účtovníctvom.

## Hlavný formulár

**Súbor:** `NexModules\Icb_F.pas`
**Trieda:** `TF_Icb`
**Mark modulu:** `ICB`

## Funkcie modulu

### Správa dokladov
- Nový doklad (A_DocAdd) - vytvorenie novej faktúry
- Vymazanie dokladu (A_DocDel) - zrušenie prázdnej faktúry
- Uzamknutie dokladu (A_DocLck)
- Odomknutie dokladu (A_UnLock)
- Kopírovanie faktúry (A_DocCopy)
- Zľava na doklad (A_DocDsc)
- Zaokrúhlenie dokladu (A_DocRnd)
- Prepočet dokladu (A_IchCalc)
- Presun do inej knihy (A_MovDoc)
- Filtrovanie dokladov (A_DocFlt, A_IcdFilt)
- Špecifikácia dokladu (A_DocSpc)

### Položky
- Zoznam položiek (A_SitLst, A_ItmInfo)
- Doplnenie údajov položiek (A_IciRef)
- Kontrola DPH položiek (A_ItmVer)
- Výpis fakturovaného tovaru (A_IcdPer)
- Kumulovaný výpis (A_IciSum)

### Párovanie s DL
- Generovanie DL (A_TcdGen)
- Párovanie DL (A_TcdPair)
- Kontrola párovania (A_IciTci)
- Prepojenie na DL (A_TchCon)

### Úhrady
- Denník úhrad (A_PmiLst)
- História úhrad (A_PayLst)
- Prepočet úhrady (A_PayCalc)
- Neuhradené faktúry (A_NpyIcd)
- Pohľadávky k dátumu (A_IcdPay)
- Úhrada cez ERP (A_EcsPay)
- Platba kartou (A_CrdPay)

### Zálohy
- Zoznam záloh (A_SpeLst)
- Príjem zálohy (A_SpeInc)
- Čerpanie zálohy (A_SpeExp)

### Upomienky a penále
- Generovanie upomienok (A_IcdWrn)
- História upomienok (A_IcwLst)
- Generovanie penále (A_PenGen)

### Účtovanie
- Rozúčtovanie dokladu (A_AccDoc)
- Zrušenie rozúčtovania (A_AccDel)
- Rozúčtovanie za obdobie (A_AccPer)
- Zoznam rozúčtovania (A_AccLst)
- Kontrola úhrad (A_PmiVer)

### Tlač
- Tlač faktúry (A_PrnIcd, A_DocPrn)
- Tlač pre zákazníka (A_PrnIcd_E)
- Tlač pre účtovníctvo (A_PrnIcd_I)
- Hromadná tlač (A_PrnDocs)
- Tlač likvidačného listu (A_LiqPrn, A_PrnLiqDoc)
- Tlač súhrnná (A_PrnSumI)
- Tlač obálok (A_PrnEnvelope)

### Komunikácia
- Odoslanie emailom (A_IcdEml)
- Online prenos (A_DocSnd)

### Import/Export
- Export do textového súboru (A_TxtExp)
- Export pre dopravu (A_TraExp)
- Import zásielkových údajov (A_ImpCsg)

### Opravné doklady
- Generovanie dobropisu (A_CorGen)

### Kontroly a údržba
- Kontrola interného čísla (A_IcnVer)
- Kontrola hlavičiek (A_HedVer)
- Obnova tovarových skupín (A_MgRef)
- Doplnenie merných jednotiek (A_MsnRef)
- Prenos NC z ODL (A_CprRef)
- Prepočet vyúčtovacej meny (A_FgCalc, A_AcvClc)
- Zrušenie factoringového dokladu (A_FacDel)
- Zoznam chýbajúcich dokladov (A_MisNum)

## Prístupové práva (gAfc.Icb.*)

### Úpravy
| Právo | Popis |
|-------|-------|
| DocAdd | Pridanie dokladu |
| DocDel | Vymazanie dokladu |
| DocMod | Úprava dokladu |
| DocLck | Uzamknutie dokladu |
| DocUnl | Odomknutie dokladu |
| DocDsc | Zľava na doklad |
| DocRnd | Zaokrúhlenie dokladu |
| DocCpy | Kopírovanie dokladu |
| VatChg | Zmena DPH sadzieb |
| DocSpc | Špecifikácia dokladu |

### Zobrazenie
| Právo | Popis |
|-------|-------|
| SitLst | Zoznam položiek |
| AccLst | Zoznam rozúčtovania |
| PayLst | História úhrad |
| NopIch | Nevypárované faktúry |
| SpeLst | Zoznam záloh |
| NpyIcd | Neuhradené faktúry |
| PmiLst | Denník úhrad |
| IcwLst | História upomienok |

### Tlač
| Právo | Popis |
|-------|-------|
| PrnDoc | Tlač dokladu |
| PrnAcc | Tlač účtovného dokladu |
| PrnMas | Hromadná tlač |
| PrnLst | Tlač zoznamu |
| PrnIcd | Tlač faktúry |
| PrnLiq | Tlač likvidačného listu |
| PrnSum | Tlač súhrnná |

### Nástroje
| Právo | Popis |
|-------|-------|
| DocFlt | Filter dokladov |
| GscSrc | Vyhľadávanie tovaru |
| AccDoc | Rozúčtovanie dokladu |
| AccDel | Zrušenie rozúčtovania |
| AccPer | Rozúčtovanie za obdobie |
| TcdGen | Generovanie DL |
| TcdPar | Párovanie DL |
| TcdCon | Prepojenie na DL |
| CsdGen | Generovanie pokladničného dokladu |
| CrdPay | Platba kartou |
| SpeInc | Príjem zálohy |
| SpeExp | Čerpanie zálohy |
| NpaIcd | Nevypárované DL |
| IcdPay | Pohľadávky k dátumu |
| IcdPer | Výpis fakturovaného tovaru |
| IcdWrn | Generovanie upomienok |
| PenGen | Generovanie penále |
| NopIci | Nevypárované položky |
| IciRep | Report položiek |
| IciSum | Súhrnný report |
| IcdEml | Odoslanie emailom |
| ExpImp | Export/Import |

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
| CasFnc | Funkcie pokladne |

## Tabuľky modulu

### Hlavné dátové tabuľky
| Tabuľka | Súbor | Popis | Polí | Indexov |
|---------|-------|-------|------|---------|
| ICH | ICHyynnn.BTR | Hlavičky faktúr | 149 | 23 |
| ICI | ICIyynnn.BTR | Položky faktúr | 80 | 10 |
| ICN | ICNyynnn.BTR | Poznámky | 4 | 2 |

### Pomocné tabuľky
| Tabuľka | Súbor | Popis | Polí | Indexov |
|---------|-------|-------|------|---------|
| ICBLST | ICBLST.BTR | Zoznam kníh | 75 | 1 |
| ICHOLE | ICHOLE.BTR | Voľné poradové čísla | 5 | 1 |
| ICW | ICWbbbbb.BTR | História upomienok | 11 | 2 |
| ICR | ICRyynnn.BTR | Upomienky | 17 | 3 |
| ICP | ICPyynnn.BTR | Penalizačné faktúry | 3 | 2 |
| ICDSPC | ICDSPC.BTR | Špecifikácie faktúr | 17 | 1 |
| ICPDEF | ICPDEF.BTR | Definície období splatnosti | 9 | 1 |
| ICDPEN | ICDPEN.BTR | Penále k faktúram | 21 | 4 |

## Sub-moduly (85 formulárov)

### Editačné formuláre
- `Icb_IchEdit_F.pas` - Editor hlavičky faktúry
- `Icb_IciEdit_F.pas` - Editor položky faktúry
- `Icb_IciLst_F.pas` - Zoznam položiek
- `Icb_NewDoc_F.pas` - Nový doklad
- `Icb_NewItm_F.pas` - Nová položka
- `Icb_DocDsc_F.pas` - Zľava na doklad
- `Icb_DocRnd_F.pas` - Zaokrúhlenie dokladu
- `Icb_DocMov_F.pas` - Presun dokladu
- `Icb_DocFlt_F.pas` - Filter dokladov
- `Icb_DocCopy_F.pas` - Kopírovanie faktúry
- `Icb_DocSpc_F.pas` - Špecifikácia dokladu
- `Icb_DocNot_F.pas` - Poznámky k dokladu

### Párovanie a DL
- `Icb_TcdGen_F.pas` - Generovanie DL
- `Icb_TcdPair_F.pas` - Párovanie DL
- `Icb_IciTci_F.pas` - Kontrola párovania

### Úhrady
- `Icb_NoPayIc_F.pas` - Neuhradené faktúry
- `Icb_IcdPay_F.pas` - Pohľadávky k dátumu
- `Icb_PmiVer_F.pas` - Kontrola úhrad
- `Icb_EcdGen_F.pas` - ERP vyúčtovanie

### Zálohy
- `Icb_IcrLst_F.pas` - Zoznam záloh
- `Icb_IcrEdit_F.pas` - Editor zálohy

### Upomienky a penále
- `Icb_IcdWrn_F.pas` - Generovanie upomienok
- `Icb_PenGen_F.pas` - Generovanie penále
- `Icb_PenCrt_F.pas` - Vytvorenie penále

### Účtovanie
- `Icb_AccPer_F.pas` - Rozúčtovanie za obdobie

### Tlač
- `Icb_DocPrn_F.pas` - Tlač dokladu
- `Icb_IcdPrn_F.pas` - Tlač faktúry
- `Icb_LiqPrn_F.pas` - Tlač likvidačného listu

### Kontroly a údržba
- `Icb_IciRef_F.pas` - Obnova položiek
- `Icb_MgRef_F.pas` - Obnova tovarových skupín
- `Icb_MsnRef_F.pas` - Doplnenie merných jednotiek
- `Icb_CprRef_F.pas` - Prenos NC z ODL
- `Icb_FgCalc_F.pas` - Prepočet vyúčtovacej meny
- `Icb_AcvClc_F.pas` - Prepočet účtovnej meny
- `Icb_IcnVer_F.pas` - Kontrola interných čísel
- `Icb_HedVer.pas` - Kontrola hlavičiek
- `Icb_ItmVer_F.pas` - Kontrola DPH položiek

### Import/Export
- `Icb_ExpTxt_F.pas` - Export do textu
- `Icb_TraExp_F.pas` - Export pre dopravu
- `Icb_ImpCsg.pas` - Import zásielok
- `Icb_IcdEml.pas` - Odoslanie emailom

### Prehľady
- `Icb_NopIch_V.pas` - Nevypárované faktúry
- `Icb_NpyIcd_V.pas` - Neuhradené faktúry
- `Icb_IcdLst_V.pas` - Zoznam faktúr
- `Icb_IcwLst_V.pas` - História upomienok
- `Icb_IciHis_V.pas` - História položiek
- `Icb_IccLst_V.pas` - Zoznam komponentov

### Špeciálne
- `Icb_DebCon.pas` - Odsúhlasenie pohľadávok
- `Icb_NicGen_F.pas` - Generovanie dobropisu
- `Icb_TypeIc_F.pas` - Typ faktúry
- `Icb_SaleLim_F.pas` - Limit predaja
- `Icm_ZipRep.pas` - Výkaz podľa PSČ

## Workflow

```
1. Generovanie faktúry z DL / manuálne vytvorenie
   ↓
2. Zadanie položiek (ICI)
   ↓
3. Výpočet súm a DPH
   ↓
4. Tlač faktúry
   ↓
5. Odoslanie zákazníkovi (email/pošta)
   ↓
6. Sledovanie splatnosti
   ↓
7. Úhrada faktúry
   ├→ Čiastočná úhrada → pokračuje sledovanie
   └→ Plná úhrada → DstPay = 1
   ↓
8. Pri omeškaní: Upomienka / Penále
   ↓
9. Rozúčtovanie (DstAcc = 'A')
   ↓
10. Uzatvorenie faktúry (DstCls = 1)
```

## Väzby na iné moduly

| Modul | Väzba | Popis |
|-------|-------|-------|
| PAB | ICH.PaCode → PAB.PaCode | Odberateľ |
| STK | ICH.StkNum → STKLST.StkNum | Sklad |
| GSC | ICI.GsCode → GSCAT.GsCode | Tovar |
| TCB | ICH.TcdNum → TCH.DocNum | Dodací list |
| OCB | ICH.OcdNum → OCH.DocNum | Zákazka |
| PMI | Úhrady | Denník úhrad pohľadávok |

## Stavy dokladu

### DstPair (Párovanie)
| Hodnota | Popis |
|---------|-------|
| N | Nevypárované |
| Q | Vypárované |

### DstPay (Úhrada)
| Hodnota | Popis |
|---------|-------|
| 0 | Neuhradená |
| 1 | Uhradená |

### DstLck (Uzamknutie)
| Hodnota | Popis |
|---------|-------|
| 0 | Odomknutá |
| 1 | Uzamknutá |

### DstCls (Ukončenie)
| Hodnota | Popis |
|---------|-------|
| 0 | Aktívna |
| 1 | Ukončená |

### DstAcc (Účtovanie)
| Hodnota | Popis |
|---------|-------|
| (prázdne) | Neúčtovaná |
| A | Zaúčtovaná |

## Multi-mena architektúra

- **Ac*** polia - Účtovná mena (EUR)
- **Fg*** polia - Vyúčtovacia mena (cudzia mena)
- EyCourse - Koncoročný kurz
- EyCrdVal - Kurzový rozdiel z prekurzovania

## Stav migrácie

- [x] Analýza modulu
- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
