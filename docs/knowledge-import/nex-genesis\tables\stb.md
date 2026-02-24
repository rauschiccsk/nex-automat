# STB - Počiatočné stavy

## Kľúčové slová / Aliases

STB, STB.BTR, stavy zásob podľa miest, stock by location, pozičná evidencia

## Popis

Tabuľka počiatočných stavov skladových položiek. Obsahuje záznamy pre prenos zásob z minulého roka a počiatočné zostatky FIFO kariet.

## Btrieve súbor

`STBxxxxx.BTR` (x = číslo skladu)

## Umiestnenie

`C:\NEX\YEARACT\STORES\STBxxxxx.BTR`

## Polia

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| GsCode | longint | 4 | Tovarové číslo (PLU) |
| FifNum | longint | 4 | Číslo FIFO karty |
| StmNum | longint | 4 | Poradové číslo skladového pohybu |
| GsName | Str30 | 31 | Názov tovaru |
| BarCode | Str15 | 16 | Identifikačný kód |

### Doklad

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocNum | Str12 | 13 | Interné číslo skladového dokladu |
| ItmNum | longint | 4 | Poradové číslo položky |
| DocDate | DateType | 4 | Dátum skladového dokladu |
| BegDate | DateType | 4 | Dátum počiatočného stavu |
| SmCode | word | 2 | Kód skladového pohybu |

### Množstvá a hodnoty

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocQnt | double | 8 | Pôvodné množstvo |
| BegQnt | double | 8 | Množstvo počiatočného stavu |
| CPrice | double | 8 | Nákupná cena bez DPH |
| CValue | double | 8 | Hodnota v NC bez DPH |

### Partner a presun

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PaCode | longint | 4 | Kód partnera |
| SpaCode | longint | 4 | Kód dodávateľa |
| ConStk | word | 2 | Protisklad |
| OcdNum | Str12 | 13 | Číslo zákazky |
| OcdItm | longint | 4 | Číslo riadku zákazky |

### Stav

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| AcqStat | Str1 | 2 | Príznak obstarania (R/K) |
| BegStat | Str1 | 2 | Príznak počiatočného stavu (B) |
| Sended | byte | 1 | Príznak odoslania zmien |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ModUser | Str8 | 9 | Používateľ poslednej zmeny |
| ModDate | DateType | 4 | Dátum poslednej zmeny |
| ModTime | TimeType | 4 | Čas poslednej zmeny |

## Indexy

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | GsCode, FifNum | GcFn | Duplicit |
| 1 | PaCode | PaCode | Duplicit |
| 2 | Sended | Sended | Duplicit |

## Použitie

- Prenos zásob z predchádzajúceho účtovného obdobia
- Nastavenie počiatočných stavov pri implementácii
- Inventúrne rozdiely ako počiatočný stav

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
