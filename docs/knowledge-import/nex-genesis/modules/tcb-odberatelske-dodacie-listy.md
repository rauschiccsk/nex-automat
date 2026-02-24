# TCB - Odberateľské dodacie listy

## Popis modulu

Modul pre evidenciu a spracovanie odberateľských dodacích listov (ODL). Zabezpečuje výdaj tovaru zo skladu odberateľom, sledovanie expedície, generovanie faktúr a integráciu s pokladničným systémom.

## Hlavný formulár

**Súbor:** `NexModules\Tcb_F.pas`
**Trieda:** `TF_Tcb`
**Mark modulu:** `TCB`

## Funkcie modulu

### Správa dokladov
- Nový doklad (A_DocAdd) - vytvorenie nového DL
- Vymazanie dokladu (A_DocDel) - zrušenie prázdneho DL
- Uzamknutie dokladu (A_DocLck)
- Odomknutie dokladu (A_DocUnl)
- Zľava na doklad (A_DocDsc)
- Zaokrúhlenie dokladu (A_DocRnd)
- Prepočet dokladu (A_DocClc)
- Presun dokladu (A_DocMov)
- Filtrovanie dokladov (A_DocFlt)
- Stornovanie dokladu (A_DocStr)

### Položky a expedícia
- Zoznam položiek (A_SitLst, A_ItmLst)
- Vyskladnenie položiek (A_OutTci, A_OutStk)
- Zrušenie vyskladnenia (A_CncOut)
- Expedičné príkazy (A_ExdGen)
- Uzatvorenie expedície (A_ExpCls)
- Terminálový výdaj (A_TrmOut)

### Generovanie faktúr
- Generovanie faktúry (A_IcgDoc)
- Hromadné generovanie faktúr (A_IcgMas)
- Nevyfakturované DL (A_NpyIcd)
- ERP vyúčtovanie (A_EcdGen)

### Komponenty a výrobky
- Zoznam komponentov (A_TccLst)
- Nevyskladnené komponenty (A_TccNsb)
- Súmrny zoznam komponentov (A_TccSum)
- Prepočet komponentov (A_TccClc)
- Konverzia na výrobky (A_TciTcc)

### Účtovanie
- Rozúčtovanie dokladu (A_AccDoc)
- Zrušenie rozúčtovania (A_AccDel)
- Hromadné rozúčtovanie (A_AccMas)
- Zoznam rozúčtovania (A_AccLst)

### Tlač
- Tlač dokladu (A_PrnDoc)
- Tlač skladovej výdajky (A_PrnStd)
- Tlač dodacieho listu (A_PrnTch)
- Hromadná tlač (A_DocsPrn)
- Tlač balíkov (A_PrnPck)
- Tlač za obdobie (A_TcdPrn)

### Kontroly a údržba
- Kontrola hlavičiek podľa položiek (A_TchVer)
- Kontrola vyúčtovania položiek (A_ItgVer)
- Kontrola interných čísel (A_DonVer)
- Obnova údajov hlavičiek (A_TchRef)
- Doplnenie údajov položiek (A_TciRef)
- Synchronizácia údajov (A_TciSyn)
- Zmena sadzieb DPH (A_VatChg)
- Prepočet vyúčtovacej meny (A_FgCalc, A_AcvClc)
- Prečíslovanie DL (A_TcdRen)

### Import/Export
- Import váhových dokladov (A_WgdImp, A_WgdDoc)
- Import elektronických dokladov (A_BciImp)
- Export do elektronického dokladu (A_TcdEdo)
- Medzifiremný prenos (A_TcdRcv)
- Odoslanie položiek online (A_OitSnd)

### Výrobné čísla
- Vydané výrobné čísla (A_TcpDir)

## Prístupové práva (gAfc.Tcb.*)

### Úpravy
| Právo | Popis |
|-------|-------|
| DocAdd | Pridanie dokladu |
| DocDel | Vymazanie dokladu |
| DocMod | Úprava dokladu |
| DocDsc | Zľava na doklad |
| DocRnd | Zaokrúhlenie dokladu |
| DocLck | Uzamknutie dokladu |
| DocUnl | Odomknutie dokladu |
| VatChg | Zmena DPH sadzieb |

### Zobrazenie
| Právo | Popis |
|-------|-------|
| SitLst | Zoznam položiek |
| AccLst | Zoznam rozúčtovania |
| NpaTcd | Nevypárované DL |
| NoiLst | Neodpočítané položky |
| NpyIcd | Nevyfakturované DL |

### Tlač
| Právo | Popis |
|-------|-------|
| PrnDoc | Tlač dokladu |
| PrnStd | Tlač skladovej výdajky |

### Nástroje
| Právo | Popis |
|-------|-------|
| DocFlt | Filter dokladov |
| DocStp | Skladové pohyby |
| DocStr | Stornovanie dokladu |
| AccDoc | Rozúčtovanie dokladu |
| AccDel | Zrušenie rozúčtovania |
| AccMas | Hromadné rozúčtovanie |
| IcgDoc | Generovanie faktúry |
| IcgMas | Hromadné generovanie faktúr |
| FmdGen | Generovanie výrobnej zákazky |
| OutStk | Vyskladnenie |
| ExdGen | Expedičné príkazy |
| DocClc | Prepočet dokladu |
| OitSnd | Online odoslanie položiek |
| TrmOut | Terminálový výdaj |
| TrdCpr | Porovnanie s treťou stranou |
| DocMov | Presun dokladu |
| OmiFxa | Fixácia cien |
| WgdImp | Import váhových dokladov |

### Pokladňa
| Právo | Popis |
|-------|-------|
| CasFnc | Funkcie pokladne |

### Položky
| Právo | Popis |
|-------|-------|
| ItmAdd | Pridanie položky |
| ItmDel | Vymazanie položky |
| ItmMod | Úprava položky |
| PckItm | Balíky |

### Administrácia
| Právo | Popis |
|-------|-------|
| MntFnc | Údržbové funkcie |
| SerFnc | Servisné funkcie |

## Tabuľky modulu

### Hlavné dátové tabuľky
| Tabuľka | Súbor | Popis | Polí | Indexov |
|---------|-------|-------|------|---------|
| TCH | TCHyynnn.BTR | Hlavičky ODL | 125 | 20 |
| TCI | TCIyynnn.BTR | Položky ODL | 79 | 10 |
| TCN | TCNyynnn.BTR | Poznámky | 4 | 2 |

### Pomocné tabuľky
| Tabuľka | Súbor | Popis | Polí | Indexov |
|---------|-------|-------|------|---------|
| TCBLST | TCBLST.BTR | Zoznam kníh | 45 | 1 |
| TCHOLE | TCHOLE.BTR | Voľné poradové čísla | 5 | 1 |
| TCP | TCPyynnn.BTR | Výrobné čísla | 12 | 6 |
| TCC | TCCnnnnn.BTR | Komponenty výrobkov | 37 | 6 |

## Sub-moduly (53 formulárov)

### Editačné formuláre
- `Tcb_TchEdit_F.pas` - Editor hlavičky DL
- `Tcb_TciEdit_F.pas` - Editor položky DL
- `Tcb_TciLst_F.pas` - Zoznam položiek
- `Tcb_DocDsc_F.pas` - Zľava na doklad
- `Tcb_DocRnd_F.pas` - Zaokrúhlenie dokladu
- `Tcb_DocClc_F.pas` - Prepočet dokladu
- `Tcb_DocMov_F.pas` - Presun dokladu
- `Tcb_DocFlt_F.pas` - Filter dokladov

### Generovanie faktúr
- `Tcb_IcdGen_F.pas` - Generovanie faktúry
- `Tcb_IcdMog_F.pas` - Hromadné generovanie faktúr
- `Tcb_EcdGen_F.pas` - ERP vyúčtovanie

### Vyskladnenie a expedícia
- `Tcb_OutDoc_F.pas` - Vyskladnenie dokladu
- `Tcb_OutStk_F.pas` - Vyskladnenie zo skladu
- `Tcb_OutBook_F.pas` - Výber položiek zo všetkých dokladov
- `Tcb_CncOut_F.pas` - Zrušenie vyskladnenia
- `Tcb_ExpCls.pas` - Uzatvorenie expedície
- `Tcb_PckLst.pas` - Zoznam balíkov
- `Tcb_PckItm.pas` - Položky balíka

### Komponenty
- `Tcb_TciTcc.pas` - Konverzia na výrobky
- `Tcb_TomCmp_F.pas` - Porovnanie komponentov

### Kontroly a údržba
- `Tcb_TchVer_F.pas` - Kontrola hlavičiek
- `Tcb_TcdVer_F.pas` - Kontrola DL
- `Tcb_ItgVer_F.pas` - Kontrola vyúčtovania
- `Tcb_TcnVer_F.pas` - Kontrola poznámok
- `Tcb_TchRef_F.pas` - Obnova hlavičiek
- `Tcb_TciRef_F.pas` - Obnova položiek
- `Tcb_TciSyn_F.pas` - Synchronizácia údajov
- `Tcb_TciToN_F.pas` - Zmena položiek na neodpočítané
- `Tcb_MsnRef_F.pas` - Doplnenie merných jednotiek

### Účtovanie
- `Tcb_AccPer_F.pas` - Rozúčtovanie za obdobie
- `Tcm_DocAcc.pas` - Účtovanie dokladu
- `Tcb_CadGen_F.pas` - Generovanie pokladničného dokladu

### Tlač
- `Tcb_DocPrn_F.pas` - Tlač dokladu
- `Tcb_TcdPrn_F.pas` - Tlač DL za obdobie

### Import/Export
- `Tcb_WgdImp_F.pas` - Import váhových dokladov
- `Tcb_EdiRcv_F.pas` - Príjem EDI dokladov
- `Tcb_BonAdd_F.pas` - Pridanie bonusu

### Ostatné
- `Tcb_CaMark_F.pas` - Označenie pre ERP
- `Tcb_CrsChg_F.pas` - Zmena kurzu
- `Tcb_FgCalc_F.pas` - Prepočet vyúčtovacej meny
- `Tcb_AddHds_F.pas` - Logistická hlavičková zľava
- `Tcb_TcdRen_F.pas` - Prečíslovanie DL
- `Tcb_StmTcd_F.pas` - Porovnanie so skladovými pohybmi
- `Tcb_StmTca_F.pas` - Porovnanie so skladovými pohybmi (archív)
- `Tcb_NoeEdi.pas` - Editor poznámok
- `Tcb_EcdRnd.pas` - Zaokrúhlenie ERP dokladu
- `Tcb_PdnVer.pas` - Kontrola predajných dokladov

### Prehľady
- `Tcb_BookLst_V.pas` - Zoznam kníh
- `Tcb_TciDir_V.pas` - Prehľad položiek
- `Tcb_TcpDir_V.pas` - Prehľad výrobných čísel
- `Tcb_NosTci_V.pas` - Neodpočítané položky
- `Tcb_NopTch_V.pas` - Nevypárované DL

## Workflow

```
1. Vytvorenie DL (manuálne / z objednávky / z expedičného príkazu)
   ↓
2. Zadanie položiek (TCI)
   ↓
3. Kontrola skladových zásob
   ↓
4. Vyskladnenie tovaru (StkStat: N → S)
   ↓
5. Tlač dodacieho listu
   ↓
6. Potvrdenie prevzatia (RcvName, RcvCode)
   ↓
7. Generovanie faktúry (ICD)
   ↓
8. Rozúčtovanie (DstAcc = 'A')
   ↓
9. Uzatvorenie DL (DstCls = 1)
```

## Väzby na iné moduly

| Modul | Väzba | Popis |
|-------|-------|-------|
| PAB | TCH.PaCode → PAB.PaCode | Odberateľ |
| STK | TCH.StkNum → STKLST.StkNum | Sklad |
| GSC | TCI.GsCode → GSCAT.GsCode | Tovar |
| OCB | TCH.OcdNum → OCH.DocNum | Zákazka |
| ICB | TCH.IcdNum → ICH.DocNum | Faktúra |
| STM | Skladové pohyby | Výdaj zo skladu |

## Stavy dokladu

### DstPair (Párovanie)
| Hodnota | Popis |
|---------|-------|
| N | Nevypárované |
| Q | Vypárované |

### DstLck (Uzamknutie)
| Hodnota | Popis |
|---------|-------|
| 0 | Odomknutý |
| 1 | Uzamknutý |

### DstCls (Ukončenie)
| Hodnota | Popis |
|---------|-------|
| 0 | Aktívny |
| 1 | Ukončený |

### DstAcc (Účtovanie)
| Hodnota | Popis |
|---------|-------|
| (prázdne) | Neúčtované |
| A | Zaúčtované |

## Stavy položky

### StkStat (Skladový stav)
| Hodnota | Popis |
|---------|-------|
| N | Nerealizované |
| O | Objednané |
| R | Rezervované |
| P | Pripravené |
| S | Vyskladnené |
| E | Expedované |

### FinStat (Finančný stav)
| Hodnota | Popis |
|---------|-------|
| (prázdne) | Nevyfakturované |
| F | Vyfakturované |
| C | Vyúčtované cez ERP |

## Stav migrácie

- [x] Analýza modulu
- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
