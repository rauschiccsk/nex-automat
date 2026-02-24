# PKH - Hlavičky prebaľovacích dokladov

## Kľúčové slová / Aliases

PKH, PKH.BTR, hlavičky, prebaľovacích, dokladov

## Popis

Hlavičky prebaľovacích dokladov. Každý doklad reprezentuje jednu operáciu prebalenia tovaru na sklade s definovanými skladovými pohybmi pre výdaj a príjem.

## Btrieve súbor

`PKHyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARyy\STK\PKHyynnn.BTR`

## Štruktúra polí (38 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| StkNum | word | 2 | Sklad prebalenia tovaru |
| SerNum | longint | 4 | Poradové číslo dokladu |
| DocNum | Str12 | 13 | Interné číslo dokladu - **PRIMARY KEY** |
| Year | Str2 | 3 | Rok dokladu |

### Údaje dokladu

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Describe | Str30 | 31 | Popis dokladu |
| DocDate | DateType | 4 | Dátum vystavenia dokladu |
| OcdNum | Str20 | 21 | Číslo pripojeného zákazkového dokladu |

### Stav dokladu

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DstStk | Str1 | 2 | Príznak dokladu (N=neprebalený, S=prebalený) |
| DstLck | byte | 1 | Príznak uzamknutia |
| SndStat | Str1 | 2 | Stav internetového prenosu (S/O/E) |
| Sended | byte | 1 | Príznak odoslania zmien (0=zmenený, 1=odoslaný) |

### Štatistiky

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ItmQnt | word | 2 | Počet položiek prebaľovacieho dokladu |
| ActPos | longint | 4 | Aktuálna pozícia |

### Skladové pohyby

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ScSmCode | word | 2 | Kód skladového pohybu výdaja |
| TgSmCode | word | 2 | Kód skladového pohybu príjmu |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |

### Nepoužívané polia (x_*)

| Pole | Typ | Popis |
|------|-----|-------|
| x_Status1-12 | Str1 | Rezervované statusy |
| x_SItemQnt, x_LItemQnt | word | Staré počítadlá |
| x_SSmName, x_DSmName | Str30 | Staré názvy pohybov |
| x_AccMth | Str4 | Stará účtovná metóda |

## Indexy (6)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | Year, SerNum | YearSerNum | Unikátny |
| 1 | StkNum, SerNum | StSn | Duplicit |
| 2 | DocNum | DocNum | Duplicit |
| 3 | DocDate | DocDate | Duplicit |
| 4 | OcdNum | OcdNum | Duplicit |
| 5 | Sended | Sended | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| StkNum | STKLST.StkNum | Sklad |
| ScSmCode | STMLST.SmCode | Skladový pohyb výdaja |
| TgSmCode | STMLST.SmCode | Skladový pohyb príjmu |

## Použitie

- Evidencia prebaľovacích operácií
- Sledovanie stavu prebalenia
- Prepojenie na zákazkové doklady
- Farebné rozlíšenie neprebalených dokladov

## Business pravidlá

- DstStk='N' = neprebalený (zobrazí sa červenou farbou)
- DstStk='S' = prebalený (dokončený)
- ScSmCode = kód pohybu pre výdaj zdrojového tovaru
- TgSmCode = kód pohybu pre príjem cieľového tovaru

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
