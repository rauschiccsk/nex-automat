# CMH - Hlavičky kompletizačných dokladov

## Kľúčové slová / Aliases

CMH, CMH.BTR, hlavičky, kompletizačných, dokladov

## Popis

Hlavičky kompletizačných dokladov. Každý doklad reprezentuje jednu operáciu montáže/výroby výrobku z komponentov na sklade.

## Btrieve súbor

`CMHyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARyy\STK\CMHyynnn.BTR`

## Štruktúra polí (34 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| StkNum | word | 2 | Sklad kompletizácie |
| SerNum | longint | 4 | Poradové číslo dokladu |
| DocNum | Str12 | 13 | Interné číslo dokladu - **PRIMARY KEY** |
| Year | Str2 | 3 | Rok dokladu |

### Údaje výrobku

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PdGsCode | longint | 4 | Tovarové číslo výrobku (PLU) |
| PdGsName | Str30 | 31 | Názov výrobku |
| PdBarCode | Str15 | 16 | Čiarový kód výrobku |
| PdQnt | double | 8 | Množstvo výrobku |
| PdMuName | Str4 | 5 | Merná jednotka výrobku |

### Údaje dokladu

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Describe | Str30 | 31 | Popis dokladu |
| DocDate | DateType | 4 | Dátum vystavenia dokladu |
| OcdNum | Str20 | 21 | Číslo pripojeného zákazkového dokladu |

### Stav dokladu

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DstStk | Str1 | 2 | Príznak dokladu (N=pripravený, S=naskladnený) |
| DstLck | byte | 1 | Príznak uzamknutia |
| SndStat | Str1 | 2 | Stav internetového prenosu (S/O/E) |
| Sended | byte | 1 | Príznak odoslania zmien (0=zmenený, 1=odoslaný) |

### Skladové pohyby

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PdSmCode | word | 2 | Kód skladového pohybu príjmu výrobku |
| CmSmCode | word | 2 | Kód skladového pohybu výdaja komponentov |

### Štatistiky

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ItmQnt | word | 2 | Počet položiek (komponentov) |
| TotVal | double | 8 | Celková hodnota kompletizácie |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |

## Indexy (10)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | Year, SerNum | YearSerNum | Unikátny |
| 1 | StkNum, SerNum | StSn | Duplicit |
| 2 | DocNum | DocNum | Duplicit |
| 3 | DocDate | DocDate | Duplicit |
| 4 | PdGsCode | PdGsCode | Duplicit |
| 5 | PdBarCode | PdBarCode | Duplicit |
| 6 | OcdNum | OcdNum | Duplicit |
| 7 | Sended | Sended | Duplicit |
| 8 | DstStk | DstStk | Duplicit |
| 9 | SndStat | SndStat | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| StkNum | STKLST.StkNum | Sklad |
| PdGsCode | GSCAT.GsCode | Katalóg produktov (výrobok) |
| PdSmCode | STMLST.SmCode | Skladový pohyb príjmu |
| CmSmCode | STMLST.SmCode | Skladový pohyb výdaja |

## Použitie

- Evidencia kompletizačných operácií
- Sledovanie stavu výroby
- Prepojenie na zákazkové doklady
- Farebné rozlíšenie nepripravených dokladov

## Business pravidlá

- DstStk='N' = pripravený (zobrazí sa červenou farbou)
- DstStk='S' = naskladnený (dokončený)
- PdSmCode = kód pohybu pre príjem hotového výrobku
- CmSmCode = kód pohybu pre výdaj komponentov
- PdQnt = vyrobené množstvo hotového výrobku

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
