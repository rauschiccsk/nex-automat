# OMB - Interné skladové výdajky

## Popis modulu

Modul pre správu interných skladových výdajok (výdaj bez odberateľa). Používa sa pre inventúrne manká, likvidácie, spotreby, medziskladové presun a iné interné výdaje tovaru.

## Hlavný súbor

`NexModules\Omb_F.pas`

## Účel

- Evidencia interných výdajov zo skladu
- Výdaj tovaru bez priameho odberateľa (manká, likvidácie, spotreba)
- Medziskladové presuny s automatickým vytvorením príjemky
- Sledovanie výrobných čísel pri výdaji
- Účtovanie interných výdajov
- Import váhových dokladov

## Architektúra

### Multi-book systém
```
OMBnnnnn.BTR     - Kniha interných výdajok
  └── OMHyynnn.BTR  - Hlavičky (yy=rok, nnn=číslo knihy)
  └── OMIyynnn.BTR  - Položky
  └── OMNyynnn.BTR  - Poznámky
  └── OMPyynnn.BTR  - Výrobné čísla
```

### Dátové tabuľky

| Tabuľka | Súbor | Popis |
|---------|-------|-------|
| OMH | OMHyynnn.BTR | Hlavičky interných výdajok |
| OMI | OMIyynnn.BTR | Položky interných výdajok |
| OMN | OMNyynnn.BTR | Poznámky k dokladom |
| OMP | OMPyynnn.BTR | Výrobné/sériové čísla |
| OMBLST | OMBLST.BTR | Zoznam kníh výdajok |
| OMHOLE | OMHOLE.BTR | Voľné poradové čísla |

## Workflow

```
1. Vytvorenie internej výdajky (A_DocNew)
   ↓
2. Pridanie položiek (OMI) s množstvom
   ↓
3. Vyskladnenie tovaru zo skladu (StkStat: N→S)
   ↓
4. [Voliteľne] Medziskladový presun → automatická príjemka (IMH/IMI)
   ↓
5. Uzatvorenie dokladu (DstLck=1)
   ↓
6. Zaúčtovanie (DstAcc='A')
```

## Typy výdajov

1. **Definitívny výdaj** (TrgStk=0)
   - Likvidácia, spotreba, manko
   - Tovar opúšťa skladové hospodárstvo

2. **Medziskladový presun** (TrgStk>0)
   - Presun na iný sklad
   - Automatické vytvorenie príjemky (IMH/IMI)
   - Kontrola konzistencie (Omb_RwmVer_F)

## Stavy dokladu

| Pole | Hodnota | Význam |
|------|---------|--------|
| DstLck | 0 | Otvorený doklad |
| DstLck | 1 | Uzatvorený doklad |
| DstStk | 'N' | Nevyskladnené |
| DstStk | 'S' | Vyskladnené |
| DstAcc | 'A' | Zaúčtovaný |
| ImdSnd | 'O' | Odoslaný medziprevádzkovo |

## Pod-moduly (30 súborov)

### Úpravy
| Súbor | Popis |
|-------|-------|
| Omb_OmhEdit_F.pas | Editácia hlavičky výdajky |
| Omb_ItmEdi_F.pas | Editácia položky |

### Zobrazenie
| Súbor | Popis |
|-------|-------|
| Omb_OmiLst_F.pas | Zoznam položiek vybranej výdajky |
| Omb_NosOmi_V.pas | Nevyskladnené položky výdajok |
| Omb_OmiDir_V.pas | Položky všetkých výdajok |
| Omb_OmpDir_V.pas | Zoznam všetkých výrobných čísel |

### Tlač
| Súbor | Popis |
|-------|-------|
| Omb_DocPrn_F.pas | Tlač vybraného dokladu |
| Omb_OmdPrn_F.pas | Zoznam dokladov za obdobie |

### Nástroje
| Súbor | Popis |
|-------|-------|
| Omb_OmdFilt_F.pas | Filtrovanie skladových výdajok |
| Omb_OmdFilt_V.pas | Zobrazenie filtra |
| Omb_OutDoc_F.pas | Výdaj všetkých položiek dokladu |
| Omb_OutBook_F.pas | Výdaj položiek celej knihy |
| Omb_ImdCrt_F.pas | Vystavenie skladovej príjemky |
| Omb_StkOut_F.pas | Výdaj všetkých položiek zo skladu |
| Omb_MgcStc_F.pas | Skladové karty podľa skupín |
| Omb_SlcStc_F.pas | Výber skladových kariet |
| Omb_WgdImp_F.pas | Import váhových dokladov |

### Účtovanie
| Súbor | Popis |
|-------|-------|
| Omb_DocAcc.pas | Zaúčtovanie vybraného dokladu |
| Omb_BokAcc.pas | Hromadné zaúčtovanie dokladov |

### Údržba
| Súbor | Popis |
|-------|-------|
| Omb_StmOmd_F.pas | Porovnávanie dokladu s pohybmi |
| Omb_StmOma_F.pas | Porovnávanie dokladov s pohybmi |
| Omb_StmOmi_F.pas | Porovnávanie položiek s pohybmi |
| Omb_RwmVer_F.pas | Kontrola medziprevádzkového presunu |
| Omb_ChckSrc_F.pas | Kontrola zdrojových dokladov |
| Omb_CrdDif_F.pas | Dodatočne pridané položky |

### Servis
| Súbor | Popis |
|-------|-------|
| Omb_OmiToN_F.pas | Položky do poznámok |
| Omb_OmiRef_F.pas | Obnova položiek podľa hlavičky |
| Omb_OmiFxa_F.pas | Oprava položiek |
| Omb_InpCor_F.pas | Oprava cien záporných výdajov |

## Prístupové práva (gAfc.Omb.*)

### Úpravy dokladov
| Právo | Popis |
|-------|-------|
| DocAdd | Pridanie nového dokladu |
| DocDel | Zmazanie dokladu |
| DocMod | Úprava dokladu |
| DocLck | Uzatvorenie dokladu |
| DocUnl | Odomknutie dokladu |
| VatChg | Zmena sadzieb DPH |

### Zobrazenie
| Právo | Popis |
|-------|-------|
| SitLst | Zobrazenie položiek |
| AccLst | Účtovné zápisy dokladu |

### Tlač
| Právo | Popis |
|-------|-------|
| PrnDoc | Tlač dokladu |
| PrnMas | Hromadná tlač |
| PrnLst | Tlač zoznamu |
| PrnLab | Tlač etikiet |

### Nástroje
| Právo | Popis |
|-------|-------|
| DocFlt | Filtrovanie dokladov |
| DocStp | Zastavenie dokladu |
| AccDoc | Zaúčtovanie dokladu |
| AccDel | Zrušenie zaúčtovania |
| AccMas | Hromadné zaúčtovanie |
| ImdGen | Generovanie príjemky |
| StkMgc | Skladové karty podľa skupín |
| OutStk | Výdaj zo skladu |
| WghRcv | Príjem váhových dokladov |
| OitSnd | Odoslanie položiek |
| TrmInc | Načítanie zo záznamníka |

### Údržba a servis
| Právo | Popis |
|-------|-------|
| MntFnc | Funkcie údržby |
| SerFnc | Servisné funkcie |

### Položky
| Právo | Popis |
|-------|-------|
| ItmAdd | Pridanie položky |
| ItmDel | Zmazanie položky |
| ItmMod | Úprava položky |

## Integrácie

### Väzby na iné moduly
- **IMB** - Automatické vytvorenie príjemky pri medziskladovom presune
- **GSC** - Katalóg tovaru (GsCode, BarCode)
- **STK** - Skladové karty a pohyby
- **JRN** - Účtovné zápisy
- **FTP** - Medziprevádzkové odosielanie

### Automatické operácie
- Medziskladový presun: OMI → IMI (Omb_ImdCrt_F)
- FTP odoslanie dokladu (B_ImdSndClick)
- Automatické zaúčtovanie po uzatvorení

## Konfigurácia knihy (OMBLST)

| Parameter | Popis |
|-----------|-------|
| ImdBook | Číslo knihy príjemok pre medziskladový presun |
| ImdStk | Sklad medziprevádzkového príjmu |
| ImdSmc | Skladový pohyb medziprevádzkového príjmu |
| SmCode | Základný skladový pohyb |
| StkNum | Základný sklad |
| Online | Priamy odpočet tovaru zo skladu |
| AutoAcc | Automatické rozúčtovanie |
| Shared | Zdieľanie cez FTP |

## Štatistiky

- **Tabuľky**: 6
- **Polí celkom**: 184
- **Indexov celkom**: 39
- **Pod-modulov**: 30

## Stav migrácie

- [x] Analýza modulu
- [x] BDF dokumentácia
- [ ] Btrieve modely (nexdata)
- [ ] PostgreSQL modely
- [ ] API endpointy
- [ ] Migračné skripty
