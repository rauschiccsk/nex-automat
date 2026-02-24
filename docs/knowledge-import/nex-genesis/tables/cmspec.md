# CMSPEC - Špecifikácia výrobku (receptúra/BOM)

## Kľúčové slová / Aliases

CMSPEC, CMSPEC.BTR, špecifikácia, výrobku, receptúra, bom

## Popis

Receptúra (Bill of Materials) pre kompletizáciu. Definuje normatívne zloženie výrobku - aké komponenty a v akom množstve sú potrebné na výrobu jednotky výrobku.

## Btrieve súbor

`CMSPEC.BTR`

## Umiestnenie

`C:\NEX\YEARACT\STK\CMSPEC.BTR`

## Štruktúra polí (9 polí)

### Identifikácia výrobku

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PdGsCode | longint | 4 | Tovarové číslo výrobku (PLU) - **FK** |

### Identifikácia komponentu

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CmGsCode | longint | 4 | Tovarové číslo komponentu (PLU) - **FK** |
| CmGsName | Str30 | 31 | Názov komponentu |
| ItmNum | word | 2 | Poradové číslo v receptúre |

### Množstvo

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| NrmQnt | double | 8 | Normatívne množstvo komponentu |
| MuName | Str4 | 5 | Merná jednotka |

### Typ

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ItmType | Str1 | 2 | Typ položky (C=komponent, W=práca) |

## Indexy (1)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | PdGsCode, ItmNum | PdItm | Unikátny |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| PdGsCode | GSCAT.GsCode | Katalóg produktov (výrobok) |
| CmGsCode | GSCAT.GsCode | Katalóg produktov (komponent) |

## Príklady receptúr

| Výrobok (PdGsCode) | Komponent | NrmQnt | Popis |
|--------------------|-----------|--------|-------|
| 1001 (Stôl) | 2001 (Doska) | 1 | 1 doska na stôl |
| 1001 (Stôl) | 2002 (Nohy) | 4 | 4 nohy na stôl |
| 1001 (Stôl) | 2003 (Skrutky) | 16 | 16 skrutiek na stôl |
| 1001 (Stôl) | PRÁCA | 0.5 | 0.5 hodiny práce |

## Použitie

- Definícia zloženia výrobkov
- Automatické naplnenie položiek kompletizačného dokladu
- Kalkulácia nákladov
- Plánovanie materiálu

## Business pravidlá

- NrmQnt = množstvo komponentu potrebné na 1 jednotku výrobku
- Pri vytvorení CMH sa položky CMI naplnia podľa CMSPEC × PdQnt
- ItmType='C' = materiálový komponent
- ItmType='W' = práca (časové náklady)
- Skutočná spotreba v CMI môže byť odlišná od normatívnej

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
