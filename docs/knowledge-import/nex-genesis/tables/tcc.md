# TCC - Komponenty výrobkov ODL

## Kľúčové slová / Aliases

TCC, TCC.BTR, dodacie listy potvrdenia, delivery confirmations

## Popis

Tabuľka komponentov výrobkov na odberateľských dodacích listoch. Umožňuje rozpad výrobkov na komponenty pri predaji súprav alebo výrobkov zložených z viacerých komponentov.

## Btrieve súbor

`TCCnnnnn.BTR` (nnnnn=číslo skladu)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\TCCnnnnn.BTR`

## Štruktúra polí (37 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| TcdNum | Str12 | 13 | Číslo DL - **FK → TCH.DocNum** |
| TcdItm | word | 2 | Číslo položky DL |
| TccItm | longint | 4 | Číslo položky komponentu |
| Parent | longint | 4 | Nadradená položka |

### Výrobok a komponent

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PdCode | longint | 4 | Tovarové číslo výrobku |
| CpCode | longint | 4 | Tovarové číslo komponentu |
| MgCode | longint | 4 | Tovarová skupina |
| CpName | Str30 | 31 | Názov komponentu |
| BarCode | Str15 | 16 | Identifikačný kód |
| ItmType | Str1 | 2 | Typ položky (P=výrobok, C=komponent, W=práca) |
| GsType | Str1 | 2 | Typ tovaru (T=riadny, W=váhový, O=obal) |
| MsName | Str10 | 11 | Merná jednotka |

### Množstvá

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PdGsQnt | double | 8 | Množstvo vyrobeného výrobku |
| RcGsQnt | double | 8 | Množstvo komponentov na výrobok (čisté) |
| LosPrc | double | 8 | Strata v % |
| CpSeQnt | double | 8 | Množstvo na odpočítanie |
| CpSuQnt | double | 8 | Množstvo už odpočítané |

### Ceny

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| VatPrc | byte | 1 | Sadzba DPH % |
| CPrice | double | 8 | NC/MJ bez DPH |
| CValue | double | 8 | NC bez DPH |
| AcCValue | double | 8 | NC bez DPH v účtovnej mene |
| FgCPrice | double | 8 | NC/MJ bez DPH vo vyúčtovacej mene |
| FgCValue | double | 8 | NC bez DPH vo vyúčtovacej mene |

### Skladové údaje

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| StkStat | Str1 | 2 | Stav položky (N=neodpočítaný, S=vyskladnený) |
| StkNum | longint | 4 | Číslo skladu výdaja |
| PaCode | longint | 4 | Kód odberateľa |
| DocDate | DateType | 4 | Dátum dokladu |
| DlvDate | DateType | 4 | Dátum vyskladnenia |
| DrbDate | DateType | 4 | Dátum ukončenia trvanlivosti |
| DlvUser | Str8 | 9 | Skladník |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModNum | word | 2 | Poradové číslo modifikácie |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |

## Indexy (6)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | TcdNum, TccItm | TdTc | Unique |
| 1 | TcdNum, TcdItm | TdTi | Duplicit |
| 2 | TcdNum, Parent | TdPa | Duplicit |
| 3 | TcdNum | TcdNum | Duplicit |
| 4 | StkStat | StkStat | Duplicit |
| 5 | CpCode | CpCode | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| TcdNum | TCH.DocNum | Hlavička DL |
| TcdNum, TcdItm | TCI.DocNum, TCI.ItmNum | Položka DL |
| PdCode | GSCAT.GsCode | Výrobok |
| CpCode | GSCAT.GsCode | Komponent |
| PaCode | PAB.PaCode | Odberateľ |
| StkNum | STKLST.StkNum | Sklad |

## Typy položiek (ItmType)

| Hodnota | Popis |
|---------|-------|
| P | Výrobok (Product) |
| C | Komponent |
| W | Práca (Work) |

## Stavy položky (StkStat)

| Hodnota | Popis |
|---------|-------|
| N | Neodpočítaný |
| S | Vyskladnený |

## Príklad použitia

```
DL položka: PC zostava (výrobok)
  ↓
TCC komponenty:
  - Základná doska
  - Procesor
  - RAM pamäť
  - HDD/SSD
  - Skrinka
  - Zdroj
  - Práca (montáž)
```

## Workflow

```
1. Predaj výrobku (TCI)
   ↓
2. Rozpad na komponenty (TCC)
   ↓
3. Vyskladnenie komponentov (StkStat: N → S)
   ↓
4. Odpočet zo skladu
```

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
