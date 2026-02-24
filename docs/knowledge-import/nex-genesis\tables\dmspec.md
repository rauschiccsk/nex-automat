# DMSPEC - Špecifikácia výrobku (BOM pre rozobranie)

## Kľúčové slová / Aliases

DMSPEC, DMSPEC.BTR, špecifikácia, výrobku, bom, pre, rozobranie

## Popis

Tabuľka špecifikácie výrobku pre účely rozobrania. Definuje normatívne zloženie výrobku - koľko jednotiek každého komponentu obsahuje jedna jednotka výrobku. Zdieľaná s modulom CMB (kompletizácia). Globálny súbor.

## Btrieve súbor

`DMSPEC.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DATA\DMSPEC.BTR`

## Štruktúra polí (9 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PdCode | longint | 4 | Tovarové číslo výrobku (Product) - **FK GSCAT** |
| CmCode | longint | 4 | Tovarové číslo komponentu - **FK GSCAT** |
| CmQnt | double | 8 | Množstvo komponentu na jednotku výrobku |

### Synchronizácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Sended | byte | 1 | Príznak odoslania zmien (0=zmenený, 1=odoslaný) |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModNum | word | 2 | Poradové číslo modifikácie |
| ModUser | Str8 | 9 | Používateľ poslednej zmeny |
| ModDate | DateType | 4 | Dátum poslednej zmeny |
| ModTime | TimeType | 4 | Čas poslednej zmeny |

## Indexy (1)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | PdCode | PdCode | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| PdCode | GSCAT.GsCode | Katalógová karta výrobku |
| CmCode | GSCAT.GsCode | Katalógová karta komponentu |

## Príklad použitia

```
Výrobok: PLU=1001 (Počítač)
Komponenty:
- PLU=2001 (Procesor), CmQnt=1.0
- PLU=2002 (RAM 8GB), CmQnt=2.0
- PLU=2003 (HDD 1TB), CmQnt=1.0
- PLU=2004 (Skrinka), CmQnt=1.0

Pri rozobraní 5 ks počítačov:
- Procesor: 5 × 1.0 = 5 ks
- RAM: 5 × 2.0 = 10 ks
- HDD: 5 × 1.0 = 5 ks
- Skrinka: 5 × 1.0 = 5 ks
```

## Použitie

- Definícia normatívneho zloženia výrobku
- Automatické naplnenie položiek pri rozobraní
- Zdieľaná štruktúra pre CMB (kompletizácia) aj DMB (rozobranie)
- Aktualizuje sa po každom rozobraní (SaveToDmSpec)

## Business pravidlá

- CmQnt = množstvo komponentu na 1 jednotku výrobku
- Skutočné množstvo pri rozobraní = CmQnt × GsQnt (z hlavičky)
- Pri rozobraní sa DMSPEC aktualizuje podľa skutočného zloženia
- Rovnaká štruktúra sa používa v CMSPEC pre kompletizáciu

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
