# CSB - Hotovostná pokladňa

## Popis modulu

Modul pre správu hotovostných pokladníc. Eviduje príjmové a výdajové pokladničné doklady, úhrady faktúr, duálne meny (účtovná a pokladničná), počiatočné a konečné stavy, DPH členenie a pokladničné knihy.

## Hlavný súbor

`NexModules\Csb_F.pas`

## Tabuľky modulu

| Tabuľka | Súbor | Popis | Polí | Indexov |
|---------|-------|-------|------|---------|
| CSH | CSHyynnn.BTR | Hlavičky pokladničných dokladov | 82 | 13 |
| CSI | CSIyynnn.BTR | Položky pokladničných dokladov | 47 | 7 |
| CSN | CSNyynnn.BTR | Poznámky k dokladom | 4 | 2 |
| CSBLST | CSBLST.BTR | Zoznam kníh hotovostných pokladní | 45 | 1 |
| CSHOLE | CSHOLE.BTR | Voľné poradové čísla | 5 | 1 |
| CSOINC | CSOINC.BTR | Číselník príjmových operácií | 16 | 3 |
| CSOEXP | CSOEXP.BTR | Číselník výdajových operácií | 16 | 3 |
| CSYLST | CSYLST.BTR | Zoznam konštantných symbolov | 6 | 1 |

**Celkom: 8 tabuliek, 221 polí, 31 indexov**

## Sub-moduly (26)

### Editácia
| Súbor | Popis |
|-------|-------|
| Csb_CshEdit_F.pas | Editor hlavičky pokladničného dokladu |
| Csb_CsiEdit_F.pas | Editor položky dokladu |
| Csb_DocCop.pas | Kopírovanie dokladu |
| Csb_DocSpc_F.pas | Špecifikácia dokladu |

### Špeciálne položky
| Súbor | Popis |
|-------|-------|
| Csb_CsiIcd_F.pas | Položka - úhrada odberateľskej FA |
| Csb_CsiIsd_F.pas | Položka - úhrada dodávateľskej FA |
| Csb_CsiTsd_F.pas | Položka - dodávateľský DDL |

### Zobrazenie
| Súbor | Popis |
|-------|-------|
| Csb_CsdSum_F.pas | Kumulatívne údaje pokladne |
| Csb_CsiDir_V.pas | Položky všetkých dokladov |
| Csb_CsoInc_F.pas | Príjmové operácie - formulár |
| Csb_CsoInc_V.pas | Príjmové operácie - pohľad |
| Csb_CsoExp_F.pas | Výdajové operácie - formulár |
| Csb_CsoExp_V.pas | Výdajové operácie - pohľad |

### Tlač
| Súbor | Popis |
|-------|-------|
| Csb_DocPrn_F.pas | Tlač pokladničného dokladu |
| Csb_MtbPrn_F.pas | Mesačná pokladničná kniha |

### Nástroje
| Súbor | Popis |
|-------|-------|
| Csb_DocFlt_F.pas | Filtrovanie dokladov |
| Csb_CsfRep_F.pas | Výkaz platieb fyzickým osobám |
| Csb_AccPer_F.pas | Zaúčtovanie dokladov za obdobie |
| Csb_AccRef_F.pas | Obnova predkontácie faktúr |

### Údržba
| Súbor | Popis |
|-------|-------|
| Csb_EndCalc_F.pas | Prepočet konečného stavu |
| Csb_CntClc_F.pas | Prepočet počítadiel |
| Csb_PmiVer_F.pas | Kontrola úhrady faktúr |

### Servis
| Súbor | Popis |
|-------|-------|
| Csb_CshRen_F.pas | Prečíslovanie dokladov |
| Csb_CsiRef_F.pas | Doplnenie údajov do položiek |
| Csb_PacRef_F.pas | Doplnenie kódu firmy |

## Prístupové práva (gAfc.Csb.*)

### Úpravy
| Právo | Popis |
|-------|-------|
| DocAdd | Pridanie dokladu |
| DocDel | Zmazanie dokladu |
| DocMod | Úprava dokladu |
| DocLck | Uzatvorenie dokladu |
| DocUnl | Odomknutie dokladu |
| DocSpc | Špecifikácia dokladu |

### Položky
| Právo | Popis |
|-------|-------|
| ItmAdd | Pridanie položky |
| ItmDel | Zmazanie položky |
| ItmMod | Úprava položky |

### Zobrazenie
| Právo | Popis |
|-------|-------|
| SitLst | Položky dokladu |
| AccLst | Účtovné zápisy dokladu |
| CsoInc | Príjmové operácie |
| CsoExp | Výdajové operácie |
| OrgDoc | Kópia originálneho dokladu (sken) |
| PmiLst | Denník úhrad faktúr |

### Tlač
| Právo | Popis |
|-------|-------|
| PrnDoc | Tlač dokladu |
| YebPrn | Ročná pokladničná kniha |
| MtbPrn | Mesačná pokladničná kniha |

### Nástroje
| Právo | Popis |
|-------|-------|
| DocFlt | Filtrovanie dokladov |
| CsfRef | Výkaz platieb FO |
| AccDoc | Zaúčtovanie dokladu |
| AccDel | Zrušenie zaúčtovania |
| AccMas | Hromadné zaúčtovanie |
| OitSnd | Medziprevádzkový presun |

### Údržba a servis
| Právo | Popis |
|-------|-------|
| MntFnc | Údržbové funkcie |
| SerFnc | Servisné funkcie |

## Typy dokladov (DocType)

| Hodnota | Popis | Farba |
|---------|-------|-------|
| I | Príjmový pokladničný doklad | Červená |
| E | Výdajový pokladničný doklad | Čierna |

## Stavové príznaky

| Pole | Hodnota | Popis |
|------|---------|-------|
| DstLck | 1 | Doklad je uzatvorený |
| DstAcc | A | Doklad je zaúčtovaný |
| DstLiq | L | Doklad je likvidovaný |
| Sended | 1 | Zmeny odoslané |
| SndStat | . | Odoslaný |
| SndStat | O | Potvrdený |
| SndStat | E | Chybný prenos |

## Duálne meny

Modul podporuje dve meny súčasne:

### Účtovná mena (Ac*)
- AcDvzName - Názov účtovnej meny
- AcAValue - Hodnota bez DPH
- AcVatVal - Hodnota DPH
- AcBValue - Hodnota s DPH

### Pokladničná mena (Py*)
- PyDvzName - Názov pokladničnej meny
- PyCourse - Kurz meny
- PyAValue - Hodnota bez DPH
- PyVatVal - Hodnota DPH
- PyBValue - Hodnota s DPH
- PyBegVal - Počiatočný stav
- PyIncVal - Príjmy
- PyExpVal - Výdaje
- PyEndVal - Konečný stav

## Väzby na iné moduly

| Modul | Popis väzby |
|-------|-------------|
| PAB | Obchodní partneri |
| ICB/ICD | Odberateľské faktúry - úhrady |
| ISB/ISD | Dodávateľské faktúry - úhrady |
| TSB/TSD | Dodacie listy |
| SAB | MO predaj - tržby |
| JRN | Hlavný denník - účtovné zápisy |
| WRILST | Prevádzkové jednotky |
| DRVLST | Vodiči |

## DPH členenie

Modul podporuje 5 sadzieb DPH:
- VatPrc1/AcAValue1/AcBValue1/PyAValue1/PyBValue1
- VatPrc2/AcAValue2/AcBValue2/PyAValue2/PyBValue2
- VatPrc3/AcAValue3/AcBValue3/PyAValue3/PyBValue3
- VatPrc4/AcAValue4/AcBValue4/PyAValue4/PyBValue4
- VatPrc5/AcAValue5/AcBValue5/PyAValue5/PyBValue5

## Číselníky operácií

### CSOINC - Príjmové operácie
Predkontácie pre príjmové pokladničné doklady (tržby, úhrady FA, zálohy).

### CSOEXP - Výdajové operácie
Predkontácie pre výdajové pokladničné doklady (výplaty, úhrady FA, odvody).

## Workflow

```
1. Vytvorenie pokladničného dokladu
   - Typ: I (príjem) alebo E (výdaj)
   - Nastavenie dátumu a partnera
   ↓
2. Pridanie položiek (CSI)
   - Výber operácie (CSOINC/CSOEXP)
   - Zadanie hodnoty a účtu
   - Prepojenie na faktúru (ConDoc)
   ↓
3. Prepočet hlavičky
   - CshRecalc aktualizuje súčty
   - Výpočet PyEndVal
   ↓
4. Kontrola zaokrúhlenia (RoundVerify)
   ↓
5. Automatické zaúčtovanie (ak AutoAcc=1)
   ↓
6. Uzatvorenie dokladu (DstLck=1)
```

## Použitie

- Hotovostné pokladne firmy
- Príjmy tržieb
- Úhrady dodávateľských faktúr
- Výplaty zamestnancom
- Cestovné príkazy
- Valutové pokladne

## Stav migrácie

- [x] Analýza modulu
- [x] BDF dokumentácia
- [ ] Btrieve modely (nexdata)
- [ ] PostgreSQL modely
- [ ] API endpointy
