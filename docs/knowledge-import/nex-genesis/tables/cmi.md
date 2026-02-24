# CMI - Položky kompletizačného dokladu

## Kľúčové slová / Aliases

CMI, CMI.BTR, položky, kompletizačného, dokladu

## Popis

Položky (komponenty) kompletizačného dokladu. Každá položka reprezentuje jeden komponent alebo prácu spotrebovanú pri výrobe výrobku.

## Btrieve súbor

`CMIyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARyy\STK\CMIyynnn.BTR`

## Štruktúra polí (29 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocNum | Str12 | 13 | Číslo hlavičky dokladu - **FK** |
| ItmNum | word | 2 | Poradové číslo položky |
| ItmType | Str1 | 2 | Typ položky (C=komponent, W=práca) |

### Údaje komponentu

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CmGsCode | longint | 4 | Tovarové číslo komponentu (PLU) |
| CmGsName | Str30 | 31 | Názov komponentu |
| _CmGsName | Str20 | 21 | Vyhľadávacie pole názvu |
| CmBarCode | Str15 | 16 | Čiarový kód komponentu |

### Množstvá

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| NrmQnt | double | 8 | Normatívne množstvo (podľa receptúry) |
| RealQnt | double | 8 | Skutočné spotrebované množstvo |
| MuName | Str4 | 5 | Merná jednotka |

### Ceny a hodnoty

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Price | double | 8 | Jednotková cena komponentu |
| Value | double | 8 | Celková hodnota (RealQnt × Price) |

### Stav položky

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| StkStat | Str1 | 2 | Stav položky (N=zaevidované, S=naskladnené) |
| Sended | byte | 1 | Príznak odoslania (0=zmenený, 1=odoslaný) |

### Skladové údaje

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| StkNum | word | 2 | Číslo skladu |
| SmCode | word | 2 | Kód skladového pohybu |
| StmNum | Str12 | 13 | Číslo skladového pohybu |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |

## Indexy (5)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | DocNum, ItmNum | DocItm | Unikátny |
| 1 | CmGsCode | CmGsCode | Duplicit |
| 2 | _CmGsName | CmGsName | Duplicit, Case-insensitive |
| 3 | CmBarCode | CmBarCode | Duplicit |
| 4 | Sended | Sended | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| DocNum | CMH.DocNum | Hlavička dokladu |
| CmGsCode | GSCAT.GsCode | Katalóg produktov (komponent) |
| StkNum | STKLST.StkNum | Sklad |
| SmCode | STMLST.SmCode | Skladový pohyb |

## Použitie

- Evidencia komponentov v kompletizácii
- Sledovanie spotreby materiálu
- Porovnanie normatívnej vs. skutočnej spotreby
- Kalkulácia hodnoty výrobku

## Business pravidlá

- ItmType='C' = komponent (materiálová položka)
- ItmType='W' = práca (nákladová položka)
- NrmQnt = normatívne množstvo z receptúry (CMSPEC)
- RealQnt = skutočne spotrebované množstvo
- Value = RealQnt × Price
- StkStat='N' = položka čaká na odpočítanie zo skladu
- StkStat='S' = položka odpočítaná zo skladu

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
