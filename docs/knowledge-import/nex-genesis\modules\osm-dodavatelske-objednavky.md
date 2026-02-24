# OSM - Dodávateľské objednávky

## Popis modulu

Modul pre evidenciu a spracovanie dodávateľských objednávok (nákup). Zabezpečuje vytváranie objednávok pre dodávateľov, sledovanie dodávok, správu termínov a integráciu s príjmom tovaru.

## Hlavný formulár

**Súbor:** `NexModules\Osm_F.pas`
**Trieda:** `TOsmF`
**Mark modulu:** `OSM`

## Funkcie modulu

### Správa dokladov
- Nový doklad (A_DocAdd) - vytvorenie novej objednávky
- Vymazanie dokladu (A_DocDel) - zrušenie prázdnej objednávky
- Uzatvorenie dokladu (A_DocCls)
- Otvorenie dokladu (A_DocOpn)
- Prepočet dokladu (A_DocClc)

### Položky
- Zoznam položiek (A_ItmLst) - Osm_OsiLst
- Editor položky (Osm_ItmEd1)

### Generovanie objednávok
- Automatické generovanie (A_OsdGen) - Osm_OsdGen
- Výkaz stavu objednávok (A_OsdRep) - Osm_OsdRep

### Odosielanie
- Odoslanie objednávky (A_OsdSnd) - Osm_OsdSnd
- Elektronický prenos (DocSnd)

### Termíny dodávok
- Správa termínov (A_RatAdm) - Osm_TrmAdm
- História zmien termínov (A_OsrHis) - Osm_OsrHis
- Zmena termínu (Osm_ChgTrm)

### Výber dodávateľa
- Výber partnera (Osm_ParSlc)

### Tlač
- Tlač objednávky (A_DocPrn)

## Prístupové práva (gAfc.Osb.*)

### Úpravy
| Právo | Popis |
|-------|-------|
| DocAdd | Pridanie dokladu |
| DocDel | Vymazanie dokladu |
| DocMod | Úprava dokladu |
| DocLck | Uzamknutie dokladu |
| DocUnl | Odomknutie dokladu |
| VatChg | Zmena DPH sadzieb |
| DocRnd | Zaokrúhlenie dokladu |
| DocDsc | Zľava na doklad |

### Zobrazenie
| Právo | Popis |
|-------|-------|
| SitLst | Zoznam položiek |
| OspLst | Zoznam dodávateľov |
| StaOut | Výstupné štatistiky |

### Tlač
| Právo | Popis |
|-------|-------|
| PrnDoc | Tlač dokladu |

### Nástroje
| Právo | Popis |
|-------|-------|
| OsdGen | Generovanie objednávok |
| SnfDbf | Export do DBF |
| DlvRea | Príjem dodávky |
| OsiDlv | Sledovanie dodávok |
| OsiNat | Národné položky |
| OssMov | Skladové pohyby |
| DocSnd | Odoslanie dokladu |
| OitSnd | Odoslanie položiek |
| OsiNar | Nedodané položky |
| BcsGen | Generovanie čiarových kódov |
| OsdSnd | Odoslanie objednávky |
| OsdDdm | Správa DDM |

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
| OSH | OSHyynnn.BTR | Hlavičky objednávok | 79 | 15 |
| OSI | OSIyynnn.BTR | Položky objednávok | 56 | 9 |
| OSN | OSNyynnn.BTR | Poznámky | 4 | 2 |
| OST | OSTyynnn.BTR | Väzby na DDL | 13 | 2 |

### LIST tabuľky (agregované)
| Tabuľka | Súbor | Popis | Polí | Indexov |
|---------|-------|-------|------|---------|
| OSHLST | OSHLST.BTR | Hlavičky objednávok LIST | 119 | 24 |
| OSILST | OSILST.BTR | Položky objednávok LIST | 64 | 17 |
| OSNLST | OSNLST.BTR | Poznámky LIST | 5 | 3 |

### Konfiguračné a pomocné tabuľky
| Tabuľka | Súbor | Popis | Polí | Indexov |
|---------|-------|-------|------|---------|
| OSBLST | OSBLST.BTR | Zoznam kníh | 27 | 1 |
| OSHOLE | OSHOLE.BTR | Voľné poradové čísla | 5 | 1 |
| OSRHIS | OSRHIS.BTR | História zmien termínov | 19 | 7 |
| OSPLST | OSPLST.BTR | Zoznam dodávateľov | 5 | 2 |
| OSGELIM | OSGELIM.BTR | Vylúčené položky | 11 | 1 |
| OSIMFS | OSIMFS.BTR | Výberový zoznam MFS | 79 | 5 |
| OSGREM | OSGREM.BTR | Presun tovaru medzi skladmi | 11 | 3 |
| OSSMOV | OSSMOV.BTR | Skladové pohyby pre objednávky | 10 | 3 |

## Sub-moduly (11 formulárov)

### Hlavné formuláre
- `Osm_F.pas` - Hlavný formulár modulu
- `Osm_OshEdi.pas` - Editor hlavičky objednávky
- `Osm_OsiLst.pas` - Zoznam položiek objednávky
- `Osm_ItmEd1.pas` - Editor položky

### Generovanie a odosielanie
- `Osm_OsdGen.pas` - Generovanie objednávok
- `Osm_OsdRep.pas` - Výkaz stavu objednávok
- `Osm_OsdSnd.pas` - Odoslanie objednávky

### Termíny dodávok
- `Osm_TrmAdm.pas` - Správa termínov dodávky
- `Osm_OsrHis.pas` - História zmien termínov
- `Osm_ChgTrm.pas` - Zmena termínu

### Výber
- `Osm_ParSlc.pas` - Výber dodávateľa

## Workflow

```
1. Identifikácia potreby objednať tovar
   ├→ Ručné vytvorenie objednávky
   └→ Automatické generovanie (A_OsdGen)
   ↓
2. Zadanie položiek (OSI)
   ↓
3. Výpočet súm a kontrola
   ↓
4. Tlač objednávky
   ↓
5. Odoslanie dodávateľovi (email/fax/EDI)
   ↓
6. Sledovanie termínov dodávky
   ├→ Potvrdenie termínu dodávateľom
   └→ Zmeny termínov → OSRHIS
   ↓
7. Príjem tovaru na sklad (TSB modul)
   ↓
8. Párovanie s dodacím listom (OST)
   ↓
9. Uzatvorenie objednávky (DstCls = 'C')
```

## Filtrovanie dokladov

### Podľa roku
- Aktuálny rok (B_ActYer)
- Predchádzajúci rok (B_PrvYer)
- Všetky roky (B_AllYer)

### Podľa stavu
- Všetky doklady (B_AllDoc)
- Neodoslané (B_NotSnd) - PrnCnt=0, TsdPrq=0, OrdPrq>0
- Na dodanie (B_UndDoc) - UndPrq>0, PrnCnt>0
- Dodané (B_TsdDoc) - TsdPrq>=OrdPrq
- Meškajúce (B_DlvSlw) - UndPrq>0, ReqDte<Today
- Zmenené termíny (B_ModDoc) - DstRat='R'
- Ukončené (B_ClsDoc) - DstCls='C'

## Farebné kódovanie riadkov

| Farba | Stav |
|-------|------|
| Modrá | Objednávka čaká na odoslanie |
| Čierna | Objednávka je odoslaná |
| Zelená | Z objednávky už je rezervácia na zákazky |
| Červená | Nedodaný tovar na čas (meškajúce) |
| Sivá | Dodané |

## Väzby na iné moduly

| Modul | Väzba | Popis |
|-------|-------|-------|
| PAB | OSH.PaCode → PAB.PaCode | Dodávateľ |
| STK | OSH.StkNum → STKLST.StkNum | Cieľový sklad |
| GSC | OSI.GsCode → GSCAT.GsCode | Tovar |
| TSB | OST.TsdNum → TSH.DocNum | Dodací list príjmu |
| OCB | OSI.OcdNum → OCH.DocNum | Zdrojová zákazka |
| ISB | Fakturácia | Faktúra za dodávku |

## Stavy dokladu

### DstLck (Uzamknutie)
| Hodnota | Popis |
|---------|-------|
| (prázdne) | Odomknutá |
| L | Uzamknutá |
| R | Práve sa vytvára |

### DstCls (Ukončenie)
| Hodnota | Popis |
|---------|-------|
| (prázdne) | Aktívna |
| C | Ukončená |

### DstSnd (Odoslanie)
| Hodnota | Popis |
|---------|-------|
| (prázdne) | Neodoslaná |
| O | Odoslaná |

### DstRat (Zmena termínu)
| Hodnota | Popis |
|---------|-------|
| (prázdne) | Bez zmeny |
| R | Zmenený termín od dodávateľa |

### StkStat (Stav položky)
| Hodnota | Popis |
|---------|-------|
| O | Objednaný (nedodaný) |
| S | Dodaný na sklad |

## Stav migrácie

- [x] Analýza modulu
- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
