# IVI - Položky inventúrneho dokladu

## Kľúčové slová / Aliases

IVI, IVI.BTR, inventúry položky, inventory items, inventúrne položky

## Popis

Položky inventúrneho dokladu. Každá položka obsahuje porovnanie účtovného a skutočného stavu pre jednu skladovú kartu.

## Btrieve súbor

`IVIyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARyy\STK\IVIyynnn.BTR`

## Štruktúra polí (38 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocNum | Str12 | 13 | Číslo hlavičky dokladu - **FK** |
| ItmNum | word | 2 | Poradové číslo položky |

### Údaje tovaru

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| GsCode | longint | 4 | Tovarové číslo (PLU) - **FK** |
| GsName | Str30 | 31 | Názov tovaru |
| _GsName | Str20 | 21 | Vyhľadávacie pole názvu |
| BarCode | Str15 | 16 | Čiarový kód |
| MuName | Str4 | 5 | Merná jednotka |

### Účtovný stav (zo STK)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| AccQnt | double | 8 | Účtovné množstvo (z STK.ActQnt) |
| AccVal | double | 8 | Účtovná hodnota |
| AvgPrice | double | 8 | Priemerná NC (z STK.AvgPrice) |

### Skutočný stav (zadaný)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| RealQnt | double | 8 | Skutočné množstvo (fyzický stav) |
| RealVal | double | 8 | Skutočná hodnota |

### Rozdiel

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DifQnt | double | 8 | Rozdiel množstva (RealQnt - AccQnt) |
| DifVal | double | 8 | Hodnota rozdielu |
| DifPrc | double | 8 | Percentuálny rozdiel |
| DifType | Str1 | 2 | Typ rozdielu (M=manko, P=prebytok, prázdne=bez rozdielu) |

### Stav spracovania

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| StkStat | Str1 | 2 | Stav položky (N=zadané, S=spracované) |
| GenStat | Str1 | 2 | Stav generovania (prázdne=negenerované, G=vygenerované) |
| Sended | byte | 1 | Príznak odoslania (0=zmenený, 1=odoslaný) |

### Pozičné údaje

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PosCode | Str15 | 16 | Skladová pozícia |

### Prepojenie na vyrovnávacie položky

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| OmiDocNum | Str12 | 13 | Číslo výdajky (manko) |
| OmiItmNum | word | 2 | Číslo položky výdajky |
| ImiDocNum | Str12 | 13 | Číslo príjemky (prebytok) |
| ImiItmNum | word | 2 | Číslo položky príjemky |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |

## Indexy (12)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | DocNum, ItmNum | DocItm | Unikátny |
| 1 | DocNum, GsCode | DocGs | Duplicit |
| 2 | GsCode | GsCode | Duplicit |
| 3 | _GsName | GsName | Duplicit, Case-insensitive |
| 4 | BarCode | BarCode | Duplicit |
| 5 | DifType | DifType | Duplicit |
| 6 | DifQnt | DifQnt | Duplicit |
| 7 | StkStat | StkStat | Duplicit |
| 8 | GenStat | GenStat | Duplicit |
| 9 | Sended | Sended | Duplicit |
| 10 | OmiDocNum | OmiDocNum | Duplicit |
| 11 | ImiDocNum | ImiDocNum | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| DocNum | IVH.DocNum | Hlavička inventúry |
| GsCode | GSCAT.GsCode | Katalóg produktov |
| GsCode | STK.GsCode | Skladová karta |
| OmiDocNum | OMI.DocNum | Položka výdajky (manko) |
| ImiDocNum | IMI.DocNum | Položka príjemky (prebytok) |

## Farebné kódovanie

| Farba | Podmienka | Popis |
|-------|-----------|-------|
| Čierna | DifQnt = 0 | Bez rozdielu |
| Červená | DifQnt < 0 | Manko |
| Zelená | DifQnt > 0 | Prebytok |

## Použitie

- Evidencia inventarizovaných položiek
- Porovnanie účtovného a skutočného stavu
- Výpočet mánk a prebytkov
- Prepojenie na vyrovnávacie doklady

## Business pravidlá

- AccQnt sa načíta zo STK.ActQnt v momente vytvorenia položky
- RealQnt sa zadáva manuálne alebo importuje
- DifQnt = RealQnt - AccQnt
- DifVal = DifQnt × AvgPrice
- DifPrc = (DifQnt / AccQnt) × 100 (ak AccQnt > 0)
- DifType = 'M' ak DifQnt < 0, 'P' ak DifQnt > 0
- GenStat = 'G' po vygenerovaní vyrovnávacieho dokladu
- Jedna položka STK môže byť v inventúre len raz

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
