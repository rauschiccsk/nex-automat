# OCB - Odberateľské objednávky (Zákazky)

## Popis modulu

Modul pre evidenciu a spracovanie odberateľských objednávok (zákaziek). Poskytuje kompletnú funkcionalitu od prijatia objednávky cez rezerváciu, expedíciu až po fakturáciu. Podporuje import z e-shopov a plánovanie rozvozu.

## Hlavný formulár

**Súbor:** `NexModules\Ocm_F.pas`
**Trieda:** `TOcmF`
**Mark modulu:** `OCB`

## Funkcie modulu

### Správa dokladov
- Nový doklad (A_DocAdd) - vytvorenie novej zákazky
- Vymazanie dokladu (A_DocDel) - zrušenie prázdnej zákazky
- Kopírovanie dokladu (A_DocCop)
- Zľava na doklad (A_DocDsc)
- Prepočet dokladu (A_DocClc)
- Tlač dokladu (A_DocPrn)

### Položky a rezervácie
- Zoznam položiek (A_ItmLst) - editor položiek
- Zmena termínu dodávky (A_OcrChg)
- Obnova rezervácií (A_RocRef)
- Nedodané položky (A_UndOci)
- Stornované položky (A_CncOci)

### Generovanie nadväzných dokladov
- Expedičné príkazy (A_ExdGen)
- Dodacie listy a faktúry (A_TcdGen)
- Okamžitá platba (A_CpdGen) - hotovostné vyúčtovanie
- Odložená platba (A_WpdGen) - fakturácia na faktúru

### Zálohy a platby
- Príjem zálohy (A_DepRcv)
- História záloh (DpzLst)

### Komunikácia
- Odoslanie emailom (A_EmlOcd)
- História emailov (A_EmlHis)
- Import z e-shopu (A_ShpImp)

### Doprava a rozvoz
- Plánovací kalendár rozvozu (A_TrsPln)
- Zoznam smerov rozvozu (A_TrsLin)
- Kontrola dodania (A_OcmDlv)

## Prístupové práva (gAfc.Ocb.*)

### Úpravy
| Právo | Popis |
|-------|-------|
| DocAdd | Pridanie dokladu |
| DocDel | Vymazanie dokladu |
| DocMod | Úprava dokladu |
| DocDsc | Zľava na doklad |
| DocLck | Uzamknutie dokladu |
| DocUnl | Odomknutie dokladu |
| DocRnd | Zaokrúhlenie dokladu |
| VatChg | Zmena DPH sadzieb |
| SerMod | Zmena poradového čísla |
| DatMod | Zmena dátumu |
| DocCpy | Kopírovanie dokladu |

### Zobrazenie
| Právo | Popis |
|-------|-------|
| SitLst | Zoznam položiek |
| OciDel | Zrušené položky |
| SpdLst | Zoznam záloh |
| OccDoc | Obchodné zmluvy |
| AttLst | Prílohy |

### Tlač
| Právo | Popis |
|-------|-------|
| PrnOcd | Tlač zákazky |
| PrnRat | Tlač potvrdenia termínu |
| PrnMas | Hromadná tlač |
| ExpLst | Export zoznamu |

### Nástroje - Generovanie dokladov
| Právo | Popis |
|-------|-------|
| TcdGen | Generovanie dodacieho listu |
| IcdGen | Generovanie faktúry |
| PcdGen | Generovanie zálohovej faktúry |
| CadGen | Generovanie pokladničného dokladu |
| ExdGen | Generovanie expedičných príkazov |
| FmdGen | Generovanie výrobnej zákazky |
| OmdGen | Generovanie internej výdajky |
| ImdGen | Generovanie internej príjemky |
| RmdGen | Generovanie prevodky |

### Nástroje - Rezervácie a stavy
| Právo | Popis |
|-------|-------|
| OciRes | Rezervácia položiek |
| ResFre | Uvoľnenie rezervácií |
| ResOsd | Rezervácia z objednávky |
| ChgTrm | Zmena termínu |
| OcdSta | Zmena stavu dokladu |
| ShpImp | Import z e-shopu |

### Položky
| Právo | Popis |
|-------|-------|
| ItmAdd | Pridanie položky |
| ItmDel | Vymazanie položky |
| ItmMod | Úprava položky |

### Prílohy
| Právo | Popis |
|-------|-------|
| AttAdd | Pridanie prílohy |
| AttDel | Vymazanie prílohy |
| AttMod | Úprava prílohy |
| AttShw | Zobrazenie prílohy |
| AttFid | Vyhľadanie prílohy |

### Administrácia
| Právo | Popis |
|-------|-------|
| MntFnc | Údržbové funkcie |
| SerFnc | Servisné funkcie |

## Tabuľky modulu

### Hlavné dátové tabuľky (staršia štruktúra)
| Tabuľka | Súbor | Popis | Polí | Indexov |
|---------|-------|-------|------|---------|
| OCH | OCHyynnn.BTR | Hlavičky zákaziek | 117 | 20 |
| OCI | OCIyynnn.BTR | Položky zákaziek | 80 | 10 |
| OCN | OCNyynnn.BTR | Poznámky | 6 | 2 |

### Hlavné dátové tabuľky (nová štruktúra LIST)
| Tabuľka | Súbor | Popis | Polí | Indexov |
|---------|-------|-------|------|---------|
| OCHLST | OCHLST.BTR | Hlavičky zákaziek (LIST) | 119 | 18 |
| OCILST | OCILST.BTR | Položky zákaziek (LIST) | 95 | 19 |
| OCNLST | OCNLST.BTR | Poznámky (LIST) | 7 | 3 |

### Pomocné tabuľky
| Tabuľka | Súbor | Popis | Polí | Indexov |
|---------|-------|-------|------|---------|
| OCBLST | OCBLST.BTR | Zoznam kníh | 45 | 1 |
| OCHOLE | OCHOLE.BTR | Voľné poradové čísla | 7 | 1 |
| OCC | OCCyynnn.BTR | Obchodné zmluvy | 36 | 3 |
| OCZ | OCZyynnn.BTR | Zálohy | 12 | 4 |
| OCD | OCDyynnn.BTR | Zrušené položky | 68 | 6 |
| OCT | OCTyynnn.BTR | Odkazy na DDL | 13 | 3 |
| OCPDEF | OCPDEF.BTR | Definície spracovania | 4 | 1 |

## Sub-moduly (30 formulárov)

### Editačné formuláre
- `Ocm_OchEdi.pas` - Hlavička zákazky
- `Ocm_OciLst.pas` - Zoznam položiek
- `Ocm_ItmEd1.pas` - Editor položky (verzia 1)
- `Ocm_ItmEd2.pas` - Editor položky (verzia 2)
- `Ocm_DocCop.pas` - Kopírovanie dokladu
- `Ocm_DocDsc.pas` - Zľava na doklad
- `Ocm_OcrChg.pas` - Zmena termínu dodávky
- `Ocm_OciCnc.pas` - Stornovanie položky

### Generovanie dokladov
- `Ocm_ExdGen.pas` - Expedičné príkazy
- `Ocm_TcdGen.pas` - Dodacie listy a faktúry
- `Ocm_CpdGen.pas` - Okamžitá platba
- `Ocm_WpdGen.pas` - Odložená platba
- `Ocm_FmdGen.pas` - Výrobná zákazka
- `Ocm_FmdMov.pas` - Pohyb výrobnej zákazky

### Rezervácie
- `Ocm_RocRef.pas` - Obnova rezervácií
- `Ocm_OciRos.pas` - Rezervácia z objednávky
- `Ocm_ResOpt.pas` - Možnosti rezervácie

### Prehľady
- `Ocm_UndOci.pas` - Nedodané položky
- `Ocm_CncOci.pas` - Stornované položky
- `Ocm_OsiUnd.pas` - Nedodané objednávky
- `Ocm_OciDlv.pas` - Dodanie položiek
- `Ocm_DlvVer.pas` - Kontrola dodania
- `Ocm_OcrDet.pas` - Detail objednávky
- `Ocm_DocSlc.pas` - Výber dokladov
- `Ocm_ImgLst.pas` - Zoznam obrázkov

### Doprava
- `Ocm_TrsPln.pas` - Plánovací kalendár rozvozu

### Import
- `Ocm_ShpImp.pas` - Import z e-shopu

### Zálohy
- `Ocm_DepRcv.pas` - Príjem zálohy

### Špeciálne
- `Ocm_EcdRnd.pas` - Zaokrúhlenie ERP dokladu

## Workflow

```
1. Prijatie objednávky (manuálne / import z e-shopu)
   ↓
2. Vytvorenie zákazky (OCH/OCHLST)
   ↓
3. Zadanie položiek (OCI/OCILST)
   ↓
4. Rezervácia skladových zásob (STS)
   ↓
5. Príjem zálohy (OCZ) - voliteľné
   ↓
6. Expedícia tovaru
   ↓
7. Generovanie DL (TCD) / Faktúry (ICD)
   ↓
8. Ukončenie zákazky
```

## Väzby na iné moduly

| Modul | Väzba | Popis |
|-------|-------|-------|
| PAB | OCH.PaCode → PAB.PaCode | Odberateľ |
| STK | OCH.StkNum → STKLST.StkNum | Sklad |
| GSC | OCI.GsCode → GSCAT.GsCode | Tovar |
| TCD | OCI.TcdNum → TCH.DocNum | Odberateľský DL |
| ICD | OCI.IcdNum → ICH.DocNum | Odberateľská faktúra |
| OSD | OCI.OsdNum → OSH.DocNum | Dodávateľská objednávka |
| STS | Rezervácie | Skladové rezervácie |

## Stavy zákazky

### DstLck (Uzamknutie)
| Hodnota | Popis |
|---------|-------|
| (prázdne) | Odomknutý |
| L | Uzamknutý |
| R | Práve sa vytvára |

### DstCls (Ukončenosť)
| Hodnota | Popis |
|---------|-------|
| (prázdne) | Aktívna |
| C | Ukončená |

### DstMod (Modifikácia)
| Hodnota | Popis |
|---------|-------|
| (prázdne) | Bez zmien |
| M | Modifikovaná - treba informovať zákazníka |

### DstExd (Expedícia)
| Hodnota | Popis |
|---------|-------|
| (prázdne) | Nepripravuje sa |
| E | Prebieha expedícia |

## Stavy položky

### StkStat (Skladový stav)
| Hodnota | Popis |
|---------|-------|
| N | Nerezervované |
| O | Objednané u dodávateľa |
| R | Rezervované zo zásob |
| P | Pripravené na expedíciu |
| S | Vyskladnené |

### FinStat (Finančný stav)
| Hodnota | Popis |
|---------|-------|
| (prázdne) | Bez spracovania |
| F | Vyfakturované |
| C | Vyúčtované cez ERP |

## Kumulatívne množstvá

| Pole | Popis |
|------|-------|
| SalPrq | Celkové objednané množstvo |
| ReqPrq | Množstvo požiadaviek na objednanie |
| RstPrq | Množstvo rezervované zo zásob |
| RosPrq | Množstvo rezervované z objednávok |
| ExdPrq | Pripravené na expedíciu |
| TcdPrq | Dodané množstvo |
| CncPrq | Stornované množstvo |
| UndPrq | Nedodané množstvo |
| IcdPrq | Vyfakturované množstvo |

## Doprava

### TrsCod (Kód dopravy)
| Hodnota | Popis |
|---------|-------|
| C | Osobný odber (Customer) |
| V | Vlastný rozvoz |
| E | Externý prepravca |
| O | Iná forma dodávky |

### PayCod (Forma úhrady)
| Hodnota | Popis |
|---------|-------|
| H | Hotovosť |
| K | Platobná karta |
| B | Bankový prevod |
| D | Dobierka |
| O | Kompenzácia |

## Stav migrácie

- [x] Analýza modulu
- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
