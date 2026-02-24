# RMB - Medziskladové presuny

## Popis modulu

Modul pre správu medziskladových presunov (transfer medzi skladmi). Zabezpečuje simultánny výdaj z jedného skladu a príjem na druhý sklad v rámci jedného dokladu.

## Hlavný súbor

`NexModules\Rmb_F.pas`

## Účel

- Presun tovaru medzi skladmi v rámci organizácie
- Simultánny výdaj a príjem v jednej transakcii
- Sledovanie výrobných čísel pri presune
- Účtovanie medziskladových pohybov
- Import váhových dokladov

## Architektúra

### Multi-book systém
```
RMBnnnnn.BTR     - Kniha medziskladových presunov
  └── RMHyynnn.BTR  - Hlavičky (yy=rok, nnn=číslo knihy)
  └── RMIyynnn.BTR  - Položky
  └── RMNyynnn.BTR  - Poznámky
  └── RMPyynnn.BTR  - Výrobné čísla
```

### Dátové tabuľky

| Tabuľka | Súbor | Popis |
|---------|-------|-------|
| RMH | RMHyynnn.BTR | Hlavičky medziskladových presunov |
| RMI | RMIyynnn.BTR | Položky medziskladových presunov |
| RMN | RMNyynnn.BTR | Poznámky k dokladom |
| RMP | RMPyynnn.BTR | Výrobné/sériové čísla |
| RMBLST | RMBLST.BTR | Zoznam kníh presunov |
| RMHOLE | RMHOLE.BTR | Voľné poradové čísla |

## Workflow

```
1. Vytvorenie dokladu presunu (A_DocNew)
   ↓
2. Nastavenie zdrojového skladu (ScStkNum) a cieľového skladu (TgStkNum)
   ↓
3. Pridanie položiek (RMI) s množstvom
   ↓
4. Vykonanie presunu (StkStat: N→S)
   - Výdaj zo zdrojového skladu (ScStkNum, ScSmCode)
   - Príjem na cieľový sklad (TgStkNum, TgSmCode)
   ↓
5. Uzatvorenie dokladu (DstLck=1)
   ↓
6. Zaúčtovanie (DstAcc='A')
```

## Špecifiká medziskladového presunu

### Duálne sklady
Každý doklad má dva sklady:
- **ScStkNum** - Zdrojový sklad (Source) - odkiaľ sa vydáva
- **TgStkNum** - Cieľový sklad (Target) - kam sa prijíma

### Duálne skladové pohyby
- **ScSmCode** - Pohyb výdaja (Source Movement)
- **TgSmCode** - Pohyb príjmu (Target Movement)

### Pozičné kódy
Pre WMS systémy:
- **SrcPos** - Pozícia v zdrojovom sklade
- **TrgPos** - Pozícia v cieľovom sklade

## Stavy dokladu

| Pole | Hodnota | Význam |
|------|---------|--------|
| DstLck | 0 | Otvorený doklad |
| DstLck | 1 | Uzatvorený doklad |
| DstStk | 'N' | Nepresúva (položky nezrealizované) |
| DstStk | 'S' | Presúva (položky zrealizované) |
| DstAcc | 'A' | Zaúčtovaný |
| Sended | 1 | Odoslaný (synchronizácia) |

## Pod-moduly (12 súborov)

### Úpravy
| Súbor | Popis |
|-------|-------|
| Rmb_RmhEdit_F.pas | Editácia hlavičky presunu |
| Rmb_ItmEdi0_F.pas | Editácia položky |
| Rmb_PndEdit_F.pas | Editácia čakajúcich položiek |

### Zobrazenie
| Súbor | Popis |
|-------|-------|
| Rmb_RmiLst_F.pas | Zoznam položiek vybraného presunu |

### Tlač
| Súbor | Popis |
|-------|-------|
| Rmb_DocPrn_F.pas | Tlač vybraného dokladu |
| Rmb_RmdPrn_F.pas | Zoznam dokladov za obdobie |

### Nástroje
| Súbor | Popis |
|-------|-------|
| Rmb_MovDoc_F.pas | Vykonanie presunu vybraného dokladu |
| Rmb_MovBook_F.pas | Hromadný presun celej knihy |

### Údržba
| Súbor | Popis |
|-------|-------|
| Rmb_RmdVer.pas | Verifikácia dokladu |

### Servis
| Súbor | Popis |
|-------|-------|
| Rmb_RmiToN_F.pas | Položky do poznámok |
| Rmb_SndTxt_F.pas | Odoslanie textového exportu |

## Prístupové práva (gAfc.Rmb.*)

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
| NsuItm | Nenaskladnené položky |

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
| DocStp | Vykonanie presunu |
| AccDoc | Zaúčtovanie dokladu |
| AccDel | Zrušenie zaúčtovania |
| AccMas | Hromadné zaúčtovanie |
| MovLst | Zoznam pohybov |
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
- **STK** - Skladové karty a pohyby (dva sklady súčasne)
- **GSC** - Katalóg tovaru (GsCode, BarCode)
- **JRN** - Účtovné zápisy
- **OCH** - Zákazky (OcdNum)

### Účtovanie
Medziskladový presun generuje dva účtovné zápisy:
1. Výdaj zo zdrojového skladu
2. Príjem na cieľový sklad

## Konfigurácia knihy (RMBLST)

| Parameter | Popis |
|-----------|-------|
| ScStkNum | Predvolený zdrojový sklad |
| TgStkNum | Predvolený cieľový sklad |
| ScSmCode | Predvolený pohyb výdaja |
| TgSmCode | Predvolený pohyb príjmu |
| Online | Priamy presun (1=zapnutý) |
| AutoAcc | Automatické rozúčtovanie |
| Shared | Zdieľanie pre iné prevádzky |

## Rozdiel oproti IMB+OMB

| Aspekt | RMB | IMB+OMB |
|--------|-----|---------|
| Doklady | 1 doklad | 2 doklady (výdajka + príjemka) |
| Transakcia | Atomická | Možná nekonzistencia |
| Účtovanie | Jednoduchšie | Komplikovanejšie |
| Audit | Jednoduchší | Vyžaduje prepojenie |

## Štatistiky

- **Tabuľky**: 6
- **Polí celkom**: 184
- **Indexov celkom**: 39
- **Pod-modulov**: 12

## Stav migrácie

- [x] Analýza modulu
- [x] BDF dokumentácia
- [ ] Btrieve modely (nexdata)
- [ ] PostgreSQL modely
- [ ] API endpointy
- [ ] Migračné skripty
