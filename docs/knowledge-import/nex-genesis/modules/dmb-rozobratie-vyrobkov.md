# DMB - Rozobratie výrobkov (Disassembly)

## Popis modulu

Modul pre správu dokladov rozobrania výrobkov. Umožňuje demontáž/rozobratie hotových výrobkov späť na komponenty. Je to opak modulu CMB (kompletizácia). Používa sa pri reklamáciách, opravách, recyklácii alebo zmene výrobnej dávky.

## Hlavný súbor

`NexModules\Dmb_F.pas`

## Vzťah CMB vs DMB

| Modul | Operácia | Vstup (výdaj) | Výstup (príjem) |
|-------|----------|---------------|-----------------|
| CMB | Kompletizácia (výroba) | Komponenty | Výrobok |
| DMB | Rozobratie (demontáž) | Výrobok | Komponenty |

## Tabuľky modulu

| Tabuľka | Súbor | Popis | Polí | Indexov |
|---------|-------|-------|------|---------|
| DMH | DMHyynnn.BTR | Hlavičky dokladov rozobrania | 34 | 12 |
| DMI | DMIyynnn.BTR | Položky dokladu (komponenty) | 28 | 5 |
| DMN | DMNyynnn.BTR | Poznámky ku dokladom | 3 | 2 |
| DMBLST | DMBLST.BTR | Zoznam kníh rozobrania | 17 | 1 |
| DMSPEC | DMSPEC.BTR | Špecifikácia výrobku (BOM) | 9 | 1 |
| DMPCLC | DMPCLC.BTR | Kalkulácia cien komponentov | 15 | 3 |

**Celkom: 6 tabuliek, 106 polí, 24 indexov**

## Sub-moduly (10)

### Editácia
| Súbor | Popis |
|-------|-------|
| Dmb_DmhEdit_F.pas | Editor hlavičky dokladu rozobrania |
| Dmb_DmiLst_F.pas | Zoznam položiek (komponentov) dokladu |

### Tlač
| Súbor | Popis |
|-------|-------|
| Dmb_DocPrn_F.pas | Tlač dokladu rozobrania |
| Dmb_DmdPrn_F.pas | Tlač zoznamu dokladov za obdobie |

### Nástroje
| Súbor | Popis |
|-------|-------|
| Dmb_DmpDoc_F.pas | Spracovanie rozobrania (príjem komponentov) |
| Dmb_DmpClc_F.pas | Definícia výpočtu nákupných cien |
| Dmb_DmpClc_V.pas | Zobrazenie kalkulácie cien |

### Údržba
| Súbor | Popis |
|-------|-------|
| Dmb_DmiToN_F.pas | Zmena položiek na neodpočítané |
| Dmb_StmDmi_F.pas | Porovnanie so skladovými pohybmi |
| Key_DmbEdi_F.pas | Nastavenie vlastností knihy |

## Skladové operácie

### Smer pohybov (opak CMB)

| Operácia | Sklad | Tovar | Pohyb |
|----------|-------|-------|-------|
| Výdaj výrobku | OuStkNum | GsCode (hlavička) | VÝDAJ |
| Príjem komponentov | InStkNum | GsCode (položky) | PRÍJEM |

### Konfigurácia knihy

| Parameter | Popis |
|-----------|-------|
| gKey.DmbStkNuO | Číslo skladu pre výdaj výrobku |
| gKey.DmbStkNuI | Číslo skladu pre príjem komponentov |
| gKey.DmbSmCodO | Kód skladového pohybu výdaja |
| gKey.DmbSmCodI | Kód skladového pohybu príjmu |
| gKey.DmbPlsNum | Číslo cenníka |

## Stavy dokladu

### DstStk - Stav výrobku

| Hodnota | Farba | Popis |
|---------|-------|-------|
| N | Červená | Pripravený - výrobok ešte nie je vydaný |
| S | Čierna | Vyskladnený - výrobok vydaný na rozobranie |

### StkStat - Stav komponentov

| Hodnota | Popis |
|---------|-------|
| N | Zaevidované - komponenty ešte nie sú prijaté |
| S | Naskladnené - komponenty prijaté na sklad |

## Workflow

```
1. Vytvorenie dokladu (Dmb_DmhEdit_F)
   ┌─────────────────────────────────────────────────────────────┐
   │ Výber výrobku na rozobranie (GsCode)                       │
   │ Množstvo na rozobranie (GsQnt)                             │
   │ DstStk='N', StkStat='N'                                    │
   └─────────────────────────────────────────────────────────────┘
                           │
                           ▼
2. Pridanie položiek/komponentov (Dmb_DmiLst_F)
   ┌─────────────────────────────────────────────────────────────┐
   │ Manuálne pridanie ALEBO                                    │
   │ Načítanie z DMSPEC (špecifikácia výrobku)                  │
   │ CmQnt = množstvo komponentu na jednotku výrobku            │
   └─────────────────────────────────────────────────────────────┘
                           │
                           ▼
3. Výdaj výrobku (B_SubtractClick)
   ┌─────────────────────────────────────────────────────────────┐
   │ F_DocHand.OutputDmPd - výdaj výrobku zo skladu OuStkNum   │
   │ Vytvorenie FIFO výdaja                                     │
   │ DstStk := 'S'                                              │
   └─────────────────────────────────────────────────────────────┘
                           │
                           ▼
4. Príjem komponentov (Dmb_DmpDoc_F)
   ┌─────────────────────────────────────────────────────────────┐
   │ Pre každú položku DMI:                                     │
   │   F_DocHand.InputDmItm - príjem komponentu na sklad InStkNum│
   │   Vytvorenie FIFO príjmu                                   │
   │   DMI.StkStat := 'S'                                       │
   └─────────────────────────────────────────────────────────────┘
                           │
                           ▼
5. Uloženie špecifikácie (SaveToDmSpec)
   ┌─────────────────────────────────────────────────────────────┐
   │ DMSPEC.PdCode = GsCode výrobku                             │
   │ DMSPEC.CmCode = GsCode komponentu                          │
   │ DMSPEC.CmQnt = DMI.GsQnt / DMH.GsQnt                       │
   └─────────────────────────────────────────────────────────────┘
```

## Špecifikácia výrobku (DMSPEC)

Definuje normatívne zloženie výrobku - koľko jednotiek každého komponentu obsahuje jedna jednotka výrobku.

| Pole | Typ | Popis |
|------|-----|-------|
| PdCode | longint | Tovarové číslo výrobku |
| CmCode | longint | Tovarové číslo komponentu |
| CmQnt | double | Množstvo komponentu na jednotku výrobku |

**Príklad:**
- Výrobok PLU=1001 (počítač)
- Komponenty: PLU=2001 (procesor, CmQnt=1), PLU=2002 (RAM, CmQnt=2), PLU=2003 (HDD, CmQnt=1)

## Kalkulácia cien (DMPCLC)

Definuje pravidlá pre výpočet nákupnej ceny komponentov z ceny výrobku.

| Pole | Typ | Popis |
|------|-----|-------|
| GsCode | longint | Tovarové číslo komponentu |
| ClcKfc | double | Kalkulačný koeficient |
| LosPrc | double | Strata v % |
| OthPrc | double | Ostatné náklady v % |
| OthVal | double | Ostatné náklady v EUR |

## FIFO logika

### Pri rozobraní výrobku:
1. **Výdaj výrobku** - odčíta sa z FIFO karty výrobku
2. **Príjem komponentov** - vytvorí sa nová FIFO karta pre každý komponent
3. **Cena komponentov** - vypočíta sa z ceny výrobku podľa DMPCLC alebo pomerne

### Výpočet ceny:
```
CPrice_komponent = (CValue_výrobok × ClcKfc) / GsQnt_komponent
```

## Dôvody rozobrania

- **Reklamácia** - vrátenie výrobku a využitie komponentov
- **Oprava/servis** - rozobranie na diagnostiku
- **Recyklácia** - využitie použiteľných komponentov
- **Zmena výrobnej dávky** - prebalenie/preznačenie
- **Kvalitativné problémy** - analýza chybnej série

## Integrácie

| Závislosť | Popis |
|-----------|-------|
| GSCAT | Katalóg produktov (výrobky aj komponenty) |
| BARCODE | Čiarové kódy produktov |
| STKLST | Zoznam skladov |
| STK | Skladové karty |
| STM | Skladové pohyby |
| FIF | FIFO karty |
| SMLST | Zoznam skladových pohybov |
| PAB | Obchodní partneri (zákazník pre reklamáciu) |
| CMB | Modul kompletizácie (opačný proces) |

## Business pravidlá

- Výrobok sa najprv musí vydať (DstStk='S'), až potom prijať komponenty
- Po príjme komponentov sa DMI.StkStat nastaví na 'S'
- Doklad možno zmazať len ak všetky FIFO karty majú OutQnt=0
- DMSPEC sa aktualizuje po každom rozobraní
- Hodnota komponentov by mala zodpovedať hodnote výrobku (mínus straty)
- Farebné rozlíšenie: DstStk='N' = červená, StkStat='N' = červená

## UI komponenty

| Komponent | Popis |
|-----------|-------|
| TV_Dmh | TableView - zoznam dokladov rozobrania |
| TV_Dmi | TableView - zoznam položiek (komponentov) |
| Nb_BokLst | Výber knihy dokladov |
| LB_Status | Zobrazenie stavu dokladu |

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
