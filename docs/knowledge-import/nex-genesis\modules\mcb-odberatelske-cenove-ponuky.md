# MCB - Odberateľské cenové ponuky

## Popis modulu

Modul pre správu odberateľských cenových ponúk (predpredajná fáza). Umožňuje vytvárať a spravovať cenové ponuky pre zákazníkov s podporou viacerých mien, zliav, príloh a následným generovaním objednávok či dodacích listov.

## Hlavný súbor

`NexModules\Mcb_F.pas`

## Účel

- Vytváranie cenových ponúk pre odberateľov
- Sledovanie platnosti a akceptácie ponúk
- Podpora tuzemských a valutových ponúk
- Generovanie odberateľských zákaziek a dodacích listov
- Export cenových ponúk
- Správa príloh k ponukám
- Sledovanie úspešnosti (vybavenosti) ponúk

## Architektúra

### Multi-book systém
```
MCBnnnnn.BTR     - Kniha cenových ponúk
  └── MCHyynnn.BTR  - Hlavičky (yy=rok, nnn=číslo knihy)
  └── MCIyynnn.BTR  - Položky
  └── MCNyynnn.BTR  - Poznámky
```

### Dátové tabuľky

| Tabuľka | Súbor | Popis |
|---------|-------|-------|
| MCH | MCHyynnn.BTR | Hlavičky cenových ponúk |
| MCI | MCIyynnn.BTR | Položky cenových ponúk |
| MCN | MCNyynnn.BTR | Poznámky k ponukám |
| MCBLST | MCBLST.BTR | Zoznam kníh ponúk |
| MCHOLE | MCHOLE.BTR | Voľné poradové čísla |

## Workflow

```
1. Vytvorenie cenovej ponuky (A_DocAdd)
   ↓
2. Pridanie položiek s cenami a množstvami
   ↓
3. Aplikácia zliav (DocDsc) a zaokrúhlenia (DocRnd)
   ↓
4. Tlač a odoslanie zákazníkovi
   ↓
5. Sledovanie odozvy (Accept=1 ak akceptovaná)
   ↓
6. Generovanie zákazky (OcdGen) alebo DDL (TcdGen)
   ↓
7. Sledovanie vybavenosti (EquPrc, EquVal)
```

## Špecifické funkcie

### Duálne meny
Každá ponuka podporuje dve meny:
- **Účtovná mena (Ac*)** - základná mena účtovníctva
- **Vyúčtovacia mena (Fg*)** - mena fakturovania (foreign)

### Sledovanie vybavenosti
- **EquVal** - Kumulatívna hodnota vybavených položiek
- **EquPrc** - Percentuálna úspešnosť vybavenosti
- **NeqNum** - Dôvod nevybavenosti

### Zálohové platby
- **DstSpi** - Príznak zálohovej platby
- **AcPValue/FgPValue** - Hodnota zálohy
- **PrfPrc** - Percentuálna záloha

## Stavy dokladu

| Pole | Hodnota | Význam |
|------|---------|--------|
| DstLck | 0 | Otvorený doklad |
| DstLck | 1 | Uzatvorený doklad |
| Accept | 0 | Čaká na odpoveď |
| Accept | 1 | Akceptovaná zákazníkom |
| DcCode | >0 | Dôvod odmietnutia |
| EquPrc | 100 | Plne vybavená |

## Pod-moduly (30 súborov)

### Úpravy
| Súbor | Popis |
|-------|-------|
| Mcb_MchEdit_F.pas | Editácia hlavičky ponuky |
| Mcb_DocEdi.pas | Editácia dokumentu (nová verzia) |
| Mcb_DocDsc_F.pas | Zľava na celý doklad |
| Mcb_DocDsc.pas | Modul zliav |
| Mcb_DocRnd_F.pas | Zaokrúhlenie dokladu |

### Zobrazenie
| Súbor | Popis |
|-------|-------|
| Mcb_MciLst_F.pas | Zoznam položiek ponuky |
| Mcb_ItmLst_F.pas | Zoznam položiek (alternatívny) |
| Mcb_MciEdit_F.pas | Editácia položky |
| Mcb_McdLst_V.pas | Zoznam dokladov |
| Mcb_OciHis.pas | História objednávok |

### Tlač
| Súbor | Popis |
|-------|-------|
| Mcb_PrnMcd_F.pas | Tlač cenovej ponuky |
| Mcb_McrFrc_F.pas | Výkaz podľa platnosti |
| Mcb_McrStk_F.pas | Výkaz podľa zásob |
| Mcb_McrFit_F.pas | Výkaz voľných položiek |

### Nástroje
| Súbor | Popis |
|-------|-------|
| Mcb_TcdGen_F.pas | Generovanie dodacieho listu |
| Mcb_OcdGen.pas | Generovanie odberateľskej zákazky |
| Mcb_IcdGen_F.pas | Generovanie faktúry |
| Mcb_DocCopy_F.pas | Kopírovanie dokladu |
| Mcb_ExpDoc_F.pas | Export cenovej ponuky |
| Mcb_ExpTxt_F.pas | Export do textu |
| Mcb_MciClc_F.pas | Prepočet položiek |
| Mcb_MinAcq_F.pas | Minimalizácia vstupných nákladov |
| Mcb_MgcAdd.pas | Pridanie skupiny |
| Mcb_BcSrch_F.pas | Vyhľadávanie čiarovým kódom |

### Režijné položky
| Súbor | Popis |
|-------|-------|
| Mcb_McrLst_F.pas | Zoznam režijných položiek |
| Mcb_McrLst_V.pas | Zobrazenie režijných položiek |
| Mcb_McrEdit_F.pas | Editácia režijnej položky |

### Údržba
| Súbor | Popis |
|-------|-------|
| Mcb_DocFlt_F.pas | Filtrovanie dokladov |
| Mcb_McbEdit_F.pas | Editácia knihy |

## Prístupové práva (gAfc.Mcb.*)

### Úpravy dokladov
| Právo | Popis |
|-------|-------|
| DocAdd | Pridanie novej ponuky |
| DocDel | Zmazanie ponuky |
| DocMod | Úprava ponuky |
| DocDsc | Aplikácia zľavy |
| DocLck | Uzatvorenie ponuky |
| DocUnl | Odomknutie ponuky |
| DocRnd | Zaokrúhlenie |
| VatChg | Zmena sadzieb DPH |

### Zobrazenie
| Právo | Popis |
|-------|-------|
| SitLst | Zobrazenie položiek |
| PayLst | História platieb |
| BokPrp | Vlastnosti knihy |
| AttLst | Zoznam príloh |

### Tlač
| Právo | Popis |
|-------|-------|
| PrnMcd | Tlač cenovej ponuky |
| PrnMpd | Tlač zálohovej faktúry |

### Nástroje
| Právo | Popis |
|-------|-------|
| TcdGen | Generovanie DDL |
| OcdGen | Generovanie zákazky |
| DocCpy | Kopírovanie dokladu |
| MciClc | Prepočet položiek |
| CpyAgm | Uložiť do zmluvných podmienok |
| DocClc | Prepočet dokladu |
| PayClc | Prepočet úhrady |

### Položky
| Právo | Popis |
|-------|-------|
| ItmAdd | Pridanie položky |
| ItmDel | Zmazanie položky |
| ItmMod | Úprava položky |
| CphEdi | Editácia cenovej hlavičky |

### Prílohy
| Právo | Popis |
|-------|-------|
| AttAdd | Pridanie prílohy |
| AttDel | Zmazanie prílohy |
| AttMod | Úprava prílohy |
| AttShw | Zobrazenie prílohy |
| AttFid | Vyhľadanie prílohy |

## Integrácie

### Väzby na iné moduly
- **PAB** - Register obchodných partnerov (odberatelia)
- **GSC** - Katalóg tovaru
- **OCB** - Odberateľské zákazky (generovanie)
- **TCB** - Odberateľské dodacie listy (generovanie)
- **ICB** - Odberateľské faktúry (generovanie)
- **STK** - Kontrola skladových zásob
- **APL** - Akciové cenníky

### Konfigurácia knihy (MCBLST)

| Parameter | Popis |
|-----------|-------|
| DvzBook | Typ knihy (0=tuzemská, 1=valutová) |
| DvzName | Skratka meny |
| StkNum | Číslo skladu výdaja |
| PlsNum | Predvolený cenník |
| PabBook | Kniha obchodných partnerov |
| OcdBook | Kniha odberateľských zákaziek |
| TcdBook | Kniha dodacích listov |
| IcdBook | Kniha faktúr |
| PrnCls | Uzatvorenie po tlači |
| DsHide | Skryť diskrétne údaje (NC, zisk) |

## Štatistiky

- **Tabuľky**: 5
- **Polí celkom**: 238
- **Indexov celkom**: 24
- **Pod-modulov**: 30

## Stav migrácie

- [x] Analýza modulu
- [x] BDF dokumentácia
- [ ] Btrieve modely (nexdata)
- [ ] PostgreSQL modely
- [ ] API endpointy
- [ ] Migračné skripty
