# DMPCLC - Kalkulácia cien komponentov

## Kľúčové slová / Aliases

DMPCLC, DMPCLC.BTR, kalkulácia, cien, komponentov

## Popis

Tabuľka kalkulácie cien prijatého tovaru pri rozobraní. Definuje pravidlá pre výpočet nákupnej ceny komponentov z hodnoty rozoberaného výrobku. Globálny súbor.

## Btrieve súbor

`DMPCLC.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DATA\DMPCLC.BTR`

## Štruktúra polí (15 polí)

### Identifikácia tovaru

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| GsCode | longint | 4 | Tovarové číslo komponentu - **FK GSCAT** |
| GsName | Str30 | 31 | Názov tovaru |
| _GsName | Str30 | 31 | Názov tovaru - vyhľadávacie pole |
| BarCode | Str15 | 16 | Identifikačný kód tovaru |

### Kalkulácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ClcKfc | double | 8 | Kalkulačný koeficient |
| LosPrc | double | 8 | Strata v % |
| OthPrc | double | 8 | Ostatné prídavné náklady v % |
| OthVal | double | 8 | Ostatné prídavné náklady v EUR |

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

## Indexy (3)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | GsCode | GsCode | Duplicit |
| 1 | _GsName | GsName | Duplicit, Case-insensitive |
| 2 | BarCode | BarCode | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| GsCode | GSCAT.GsCode | Katalógová karta komponentu |

## Výpočet ceny

```
CPrice_komponent = (CValue_výrobok × ClcKfc × (1 - LosPrc/100) × (1 + OthPrc/100) + OthVal) / GsQnt
```

### Príklad

```
Výrobok: CValue = 1000 EUR
Komponent: ClcKfc = 0.30, LosPrc = 5%, OthPrc = 2%, OthVal = 0

CPrice = 1000 × 0.30 × (1 - 0.05) × (1 + 0.02) + 0
       = 1000 × 0.30 × 0.95 × 1.02
       = 290.70 EUR
```

## Použitie

- Automatický výpočet nákupných cien komponentov pri rozobraní
- Zohľadnenie strát pri demontáži (LosPrc)
- Prídavné náklady na rozobranie (OthPrc, OthVal)
- Proporcionálne rozdelenie hodnoty výrobku medzi komponenty (ClcKfc)

## Business pravidlá

- Súčet ClcKfc všetkých komponentov výrobku by mal byť 1.0 (100%)
- LosPrc zohľadňuje straty pri demontáži (poškodenie, opotrebenie)
- OthPrc/OthVal pridáva náklady na prácu pri rozobraní
- Ak DMPCLC záznam neexistuje, cena sa počíta pomerovo z DMSPEC.CmQnt

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
