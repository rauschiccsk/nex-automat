# IDB - Interné účtovné doklady

## Popis modulu

Modul pre správu interných účtovných dokladov v NEX Genesis. Umožňuje vytváranie účtovných zápisov bez externých dokladov (interné preúčtovania, kurzové rozdiely, otváranie/zatváranie účtov, zápočty).

## Hlavný súbor

`NexModules\Idb_F.pas`

## Tabuľky modulu

| Tabuľka | Súbor | Popis | Polí | Indexov |
|---------|-------|-------|------|---------|
| IDH | IDHyynnn.BTR | Hlavičky interných účtovných dokladov | 49 | 10 |
| IDI | IDIyynnn.BTR | Položky interných účtovných dokladov | 35 | 6 |
| IDN | IDNyynnn.BTR | Poznámky k dokladom | 3 | 2 |
| IDBLST | IDBLST.BTR | Zoznam kníh interných dokladov | 13 | 2 |
| IDHOLE | IDHOLE.BTR | Voľné poradové čísla | 5 | 1 |
| IDMLST | IDMLST.BTR | Zoznam pohybov (predkontácie) | 13 | 3 |

**Celkom: 6 tabuliek, 118 polí, 24 indexov**

## Sub-moduly (21)

### Editácia
| Súbor | Popis |
|-------|-------|
| Idb_IdhEdit_F.pas | Editor hlavičky dokladu |
| Idb_IdiEdit_F.pas | Editor položky dokladu |
| Idb_IdiLst_F.pas | Zoznam položiek dokladu |
| Idb_DelDoc_F.pas | Zmazanie dokladu |
| Idb_DocCopy_F.pas | Kopírovanie dokladu |

### Zobrazenie
| Súbor | Popis |
|-------|-------|
| Idb_IdiDir_V.pas | Položky všetkých dokladov |
| Idb_IddFilt_F.pas | Filtrovanie dokladov |
| Idb_IddFilt_V.pas | Filtrovaný pohľad na doklady |

### Tlač
| Súbor | Popis |
|-------|-------|
| Idb_DocPrn_F.pas | Tlač vybraného dokladu |

### Účtovné operácie
| Súbor | Popis |
|-------|-------|
| Idb_AccClose_F.pas | Uzatvorenie analytických účtov |
| Idb_AccOpen_F.pas | Otvorenie súvahových účtov |
| Idb_CrdAcc_F.pas | Zaúčtovanie kurzových rozdielov |
| Idb_CrdDif_F.pas | Dodatočne pridané položky kurzových rozdielov |
| Idb_IsdIcd.pas | Zápočet záväzkov a pohľadávok |

### Pohyby a predkontácie
| Súbor | Popis |
|-------|-------|
| Idb_IdmLst_F.pas | Zoznam pohybov - formulár |
| Idb_IdmLst_V.pas | Zoznam pohybov - pohľad |

### Údržba a servis
| Súbor | Popis |
|-------|-------|
| Idb_IdhRen_F.pas | Prečíslovanie dokladov |
| Idb_ImpItm_F.pas | Import položiek dokladu |
| Idb_PacRef_F.pas | Doplnenie kódu firmy |
| Idb_PmiVer_F.pas | Verifikácia úhrad |

## Prístupové práva (gAfc.Idb.*)

### Úpravy
| Právo | Popis |
|-------|-------|
| DocAdd | Pridanie nového dokladu |
| DocDel | Zmazanie dokladu |
| DocMod | Úprava dokladu |
| DocLck | Uzatvorenie dokladu |
| DocUnl | Odomknutie dokladu |
| DocCpy | Kopírovanie dokladu |

### Položky
| Právo | Popis |
|-------|-------|
| ItmAdd | Pridanie položky |
| ItmDel | Zmazanie položky |
| ItmMod | Úprava položky |

### Zobrazenie
| Právo | Popis |
|-------|-------|
| SitLst | Zobrazenie položiek |
| AccLst | Účtovné zápisy dokladu |
| PmiLst | Zoznam úhrad |

### Tlač
| Právo | Popis |
|-------|-------|
| PrnDoc | Tlač dokladu |
| PrnLst | Tlač zoznamu dokladov |
| TxtExp | Export textu |

### Nástroje - účtovanie
| Právo | Popis |
|-------|-------|
| CrdAcc | Zaúčtovanie kurzových rozdielov |
| AccDoc | Zaúčtovanie dokladu |
| AccDel | Zrušenie zaúčtovania |
| AccMas | Hromadné zaúčtovanie knihy |
| AccOpn | Otvorenie súvahových účtov |
| AccCls | Uzatvorenie analytických účtov |
| OitSnd | Odoslanie dokladu |
| ImpItm | Import položiek |

### Údržba a servis
| Právo | Popis |
|-------|-------|
| MntFnc | Údržbové funkcie |
| SerFnc | Servisné funkcie |

## Typy dokladov (DocType)

| Hodnota | Popis |
|---------|-------|
| 0 | Bežný účtovný doklad |
| 1 | Otvorenie účtov (počiatočné stavy) |
| 2 | Uzatvorenie účtov (záverečné stavy) |

## Stavové príznaky

| Pole | Hodnota | Popis |
|------|---------|-------|
| DstLck | 1 | Doklad je uzatvorený |
| DstAcc | A | Doklad je zaúčtovaný |
| DstDif | ! | Existuje rozdiel medzi hlavičkou a položkami |

## Väzby na iné moduly

| Modul | Popis väzby |
|-------|-------------|
| JRN (Journal) | Účtovné zápisy v hlavnom denníku |
| PAB | Obchodní partneri (PaCode) |
| Účtová osnova | Syntetické a analytické účty (AccSnt, AccAnl) |
| WRILST | Prevádzkové jednotky (WriNum) |

## Účtovné polia

### Hlavička (IDH)
- **CAccSnt/CAccAnl** - Účet strany Má dať
- **DAccSnt/DAccAnl** - Účet strany Dal
- **CredVal** - Hodnota strany MD
- **DebVal** - Hodnota strany Dal

### Položky (IDI)
- **AccSnt/AccAnl** - Účet položky
- **CredVal** - Hodnota MD
- **DebVal** - Hodnota Dal
- **FgDvzName** - Mena pre kurzové rozdiely
- **FgCourse** - Kurz meny

## Špeciálne funkcie

### Otvorenie účtov
Vytvorenie počiatočných stavov súvahových účtov na začiatku účtovného obdobia.

### Uzatvorenie účtov
Prevedenie konečných stavov analytických účtov do záverečného účtu.

### Kurzové rozdiely
Automatický výpočet a zaúčtovanie kurzových rozdielov z pohľadávok a záväzkov v cudzích menách.

### Zápočet záväzkov a pohľadávok
Vzájomné započítanie pohľadávok a záväzkov voči tomu istému partnerovi.

## Workflow

```
1. Vytvorenie hlavičky dokladu (DocAdd)
   ↓
2. Pridanie položiek (ItmAdd)
   - Každá položka = jeden účtovný zápis
   - CredVal ALEBO DebVal (MD alebo Dal)
   ↓
3. Kontrola bilancie (DstDif)
   - Suma MD musí rovnať sume Dal
   ↓
4. Uzatvorenie dokladu (DstLck=1)
   ↓
5. Zaúčtovanie do denníka (DstAcc='A')
   - Zápisy do JRN (JOURNAL)
```

## Použitie

- Interné preúčtovania medzi účtami
- Kurzové rozdiely
- Otváranie/zatváranie účtovného obdobia
- Zápočty pohľadávok a záväzkov
- Opravné zápisy
- Účtovanie odpisov

## Stav migrácie

- [x] Analýza modulu
- [x] BDF dokumentácia
- [ ] Btrieve modely (nexdata)
- [ ] PostgreSQL modely
- [ ] API endpointy
