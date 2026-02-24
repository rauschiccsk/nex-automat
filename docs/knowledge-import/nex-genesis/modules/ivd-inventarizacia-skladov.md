# IVD - Inventarizácia skladov

## Popis modulu

Modul pre správu skladových inventúr. Umožňuje porovnanie účtovného stavu (STK.ActQnt) so skutočným stavom na sklade, evidenciu rozdielov (manká a prebytky) a automatické generovanie vyrovnávacích dokladov (OMB pre manká, IMB pre prebytky).

## Hlavný súbor

`NexModules\Ivd_F.pas`

## Tabuľky modulu

| Tabuľka | Súbor | Popis | Polí | Indexov |
|---------|-------|-------|------|---------|
| IVH | IVHyynnn.BTR | Hlavičky inventúrnych dokladov | 32 | 8 |
| IVI | IVIyynnn.BTR | Položky inventúry | 38 | 12 |
| IVN | IVNyynnn.BTR | Poznámky k inventúre | 4 | 2 |
| IVBLST | IVBLST.BTR | Zoznam kníh inventúry | 22 | 1 |
| IVHOLE | IVHOLE.BTR | Voľné poradové čísla | 5 | 1 |

**Celkom: 5 tabuliek, ~101 polí, ~24 indexov**

## Sub-moduly (odhadované)

### Editácia
| Súbor | Popis |
|-------|-------|
| Ivd_IvhEdit_F.pas | Editor hlavičky inventúrneho dokladu |
| Ivd_IviLst_F.pas | Zoznam položiek inventúry |
| Ivd_ItmEdi_F.pas | Editor položky inventúry |

### Tlač
| Súbor | Popis |
|-------|-------|
| Ivd_DocPrn_F.pas | Tlač inventúrneho dokladu |
| Ivd_IvdPrn_F.pas | Tlač zoznamu inventúr za obdobie |
| Ivd_DifPrn_F.pas | Tlač zoznamu rozdielov (manká/prebytky) |

### Nástroje
| Súbor | Popis |
|-------|-------|
| Ivd_StkLoad_F.pas | Načítanie položiek zo skladu |
| Ivd_IviCalc_F.pas | Prepočet rozdielov |
| Ivd_DifGen_F.pas | Generovanie vyrovnávacích dokladov |
| Ivd_IvdFilt_F.pas | Filtrovanie inventúr |

### Import
| Súbor | Popis |
|-------|-------|
| Ivd_ImpCSV_F.pas | Import skutočných stavov z CSV |
| Ivd_ImpTrm_F.pas | Import z mobilného terminálu |

### Údržba
| Súbor | Popis |
|-------|-------|
| Ivd_IviToN_F.pas | Zmena položiek na neodpočítané |
| Ivd_IviRef_F.pas | Obnova položiek podľa hlavičky |

### Konfigurácia
| Súbor | Popis |
|-------|-------|
| Key_IvdEdi_F.pas | Nastavenie vlastností knihy |

## Prístupové práva (gAfc.Ivd.*)

### Úpravy dokladov
| Právo | Popis |
|-------|-------|
| DocAdd | Pridanie inventúrneho dokladu |
| DocDel | Zmazanie dokladu |
| DocMod | Úprava dokladu |
| DocLck | Uzamknutie dokladu |
| DocUnl | Odomknutie dokladu |

### Zobrazenie
| Právo | Popis |
|-------|-------|
| SitLst | Zoznam položiek |
| DifLst | Zoznam rozdielov |

### Tlač
| Právo | Popis |
|-------|-------|
| PrnDoc | Tlač dokladu |
| PrnMas | Hromadná tlač |
| PrnLst | Tlač zoznamu |
| PrnDif | Tlač rozdielov |

### Nástroje
| Právo | Popis |
|-------|-------|
| DocFlt | Filtrovanie dokladov |
| StkLod | Načítanie položiek zo skladu |
| DifGen | Generovanie vyrovnávacích dokladov |
| ImpCSV | Import z CSV |
| ImpTrm | Import z terminálu |

### Položky
| Právo | Popis |
|-------|-------|
| ItmAdd | Pridanie položky |
| ItmDel | Zmazanie položky |
| ItmMod | Úprava položky |

### Administrácia
| Právo | Popis |
|-------|-------|
| MntFnc | Funkcie údržby |
| SerFnc | Servisné funkcie |

## Kľúčové vlastnosti

### Stavy inventúry
- **DstStk** = 'N' - inventúra otvorená (červená farba)
- **DstStk** = 'S' - inventúra uzatvorená

### Porovnanie množstiev
- **AccQnt** = účtovné množstvo (z STK.ActQnt)
- **RealQnt** = skutočné množstvo (fyzický stav)
- **DifQnt** = rozdiel = RealQnt - AccQnt
- **DifType** = 'M' (manko) alebo 'P' (prebytok)

### Hodnoty
- **AccVal** = účtovná hodnota
- **RealVal** = hodnota skutočného stavu
- **DifVal** = hodnota rozdielu

### Farebné kódovanie položiek
| Farba | Stav |
|-------|------|
| Čierna | Bez rozdielu (DifQnt = 0) |
| Červená | Manko (DifQnt < 0) |
| Zelená | Prebytok (DifQnt > 0) |

## Workflow

```
1. Vytvorenie inventúrneho dokladu (IVH)
   ↓
2. Načítanie položiek zo skladu (Ivd_StkLoad_F)
   ├→ Všetky položky skladu
   ├→ Podľa tovarových skupín
   └→ Podľa pozičných miest
   ↓
3. Zadanie skutočných množstiev (RealQnt)
   ├→ Ručné zadanie
   ├→ Import z CSV
   └→ Import z mobilného terminálu
   ↓
4. Prepočet rozdielov (Ivd_IviCalc_F)
   ├→ DifQnt = RealQnt - AccQnt
   └→ DifVal = DifQnt × AvgPrice
   ↓
5. Kontrola a schválenie
   ↓
6. Generovanie vyrovnávacích dokladov (Ivd_DifGen_F)
   ├→ Manká → OMB (interná výdajka)
   └→ Prebytky → IMB (interná príjemka)
   ↓
7. Uzatvorenie inventúry (DstStk='S')
   ↓
8. Aktualizácia STK.InvDate
```

## Integrácie

| Závislosť | Popis |
|-----------|-------|
| STK | Skladové karty - zdrojové množstvá a ceny |
| STKLST | Zoznam skladov |
| GSCAT | Katalóg produktov |
| BARCODE | Čiarové kódy |
| MGLST | Tovarové skupiny |
| OMB | Interné výdajky (pre manká) |
| IMB | Interné príjemky (pre prebytky) |

## Business pravidlá

- Inventúra vždy pre jeden sklad (IVH.StkNum)
- AccQnt sa načíta zo STK.ActQnt v momente vytvorenia položky
- RealQnt sa zadáva manuálne alebo importuje
- DifQnt = RealQnt - AccQnt (kladné = prebytok, záporné = manko)
- Vyrovnávacie doklady sa generujú len pre nenulové rozdiely
- Po uzatvorení sa aktualizuje STK.InvDate pre inventarizované položky
- Inventúra môže byť čiastočná (vybrané položky) alebo úplná (celý sklad)

## Typy inventúr

1. **Úplná inventúra** - všetky položky skladu
2. **Čiastočná inventúra** - vybrané tovarové skupiny
3. **Pozičná inventúra** - podľa skladových pozícií
4. **Rotačná inventúra** - priebežná inventúra vybraných položiek

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
