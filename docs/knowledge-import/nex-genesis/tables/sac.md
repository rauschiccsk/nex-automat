# SAC - Komponenty výrobkov MO predaja

## Kľúčové slová / Aliases

SAC, SAC.BTR, komponenty, výrobkov, predaja

## Popis

Tabuľka komponentov (surovín) výrobkov z maloobchodného predaja. Používa sa pri predaji výrobkov s receptúrou, kde sa automaticky rozpadajú na jednotlivé komponenty pre správne vyskladnenie.

## Btrieve súbor

`SACnnnnn.BTR` (nnnnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\SACnnnnn.BTR`

## Štruktúra polí (31 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocNum | Str12 | 13 | Interné číslo dokladu |
| ItmNum | longint | 4 | Číslo položky dokladu (GsCode výrobku) |
| SacNum | longint | 4 | Číslo položky komponenty |
| Parent | longint | 4 | Číslo nadradenej položky |
| DocDate | DateType | 4 | Dátum predaja |

### Výrobok a komponent

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PdCode | longint | 4 | Tovarové číslo výrobku |
| CpCode | longint | 4 | Tovarové číslo komponentu |
| MgCode | longint | 4 | Tovarová skupina |
| CpName | Str30 | 31 | Názov komponentu |
| BarCode | Str15 | 16 | Identifikačný kód komponentu |

### Sklad

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| StkNum | longint | 4 | Číslo skladu výdaja |
| StkStat | Str1 | 2 | Stav položky (N=neodpočítaný, S=vyskladnený) |

### Množstvá z receptúry

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PdGsQnt | double | 8 | Množstvo vyrobeného výrobku (min. výrobné množstvo) |
| RcGsQnt | double | 8 | Množstvo komponentov na zadané množstvo výrobku (čisté) |
| LosPrc | double | 8 | Strata v % |
| MsName | Str10 | 11 | Merná jednotka |

### Množstvá skutočné

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CpSeQnt | double | 8 | Množstvo komponentov na odpočítanie |
| CpSuQnt | double | 8 | Množstvo komponentov už odpočítané |

### Hodnoty

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| VatPrc | byte | 1 | Sadzba DPH (%) |
| CPrice | double | 8 | NC/MJ bez DPH komponentu |
| CValue | double | 8 | NC bez DPH komponentu |

### Typ položky

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ItmType | Str1 | 2 | Typ položky (C=komponent, W=práca) |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |
| ModNum | word | 2 | Počítadlo modifikácií |

## Indexy (7)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | DocNum, SacNum | DnSn | Unique |
| 1 | DocNum, ItmNum, StkNum | DnInSt | Duplicit |
| 2 | DocNum, Parent | DnPa | Duplicit |
| 3 | DocNum | DocNum | Duplicit |
| 4 | PdCode | PdCode | Duplicit |
| 5 | CpCode | CpCode | Duplicit |
| 6 | StkStat | StkStat | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| DocNum | SAH.DocNum | Hlavička dokladu |
| ItmNum | SAI.GsCode | Výrobok v SAI |
| PdCode | GSCAT.GsCode | Výrobok |
| CpCode | GSCAT.GsCode | Komponent |
| StkNum | STKLST.StkNum | Sklad |

## Typy položiek (ItmType)

| Hodnota | Popis |
|---------|-------|
| C | Komponent (surovina) |
| W | Práca (výrobná operácia) |

## Použitie

- Rozpad výrobkov na komponenty
- Vyskladnenie surovín pri predaji hotových výrobkov
- Gastronómia - receptúry jedál
- Výroba - kusovníky

## Business pravidlá

- Vytvárajú sa automaticky z receptúr (CPI)
- ItmNum = GsCode výrobku z SAI
- CpSeQnt = množstvo na odpočítanie (s LosPrc)
- CpSuQnt = už odpočítané zo skladu
- StkStat='S' po vyskladnení

## Príklad

Pri predaji 2ks hamburgeru (GsCode=1001):
- SAI: GsCode=1001, SeQnt=2, StkStat='C'
- SAC: DocNum, ItmNum=1001, CpCode=2001 (mäso), CpSeQnt=0.3
- SAC: DocNum, ItmNum=1001, CpCode=2002 (žemľa), CpSeQnt=2
- SAC: DocNum, ItmNum=1001, CpCode=2003 (šalát), CpSeQnt=0.1

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
