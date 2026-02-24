# FXBLST - Knihy investičného majetku

## Kľúčové slová / Aliases

FXBLST, FXBLST.BTR, knihy, investičného, majetku

## Popis

Konfiguračná tabuľka kníh dlhodobého investičného majetku. Každá kniha obsahuje skupinu evidenčných kariet majetku v samostatných súboroch FXAyynnn.BTR, FXTyynnn.BTR, FXLyynnn.BTR atď.

## Btrieve súbor

`FXBLST.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\FXBLST.BTR`

## Štruktúra polí (23 polí)

### Identifikácia knihy

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| BookNum | Str5 | 6 | Číslo knihy - **PRIMARY KEY** |
| BookName | Str30 | 31 | Názov knihy |
| _BookName | Str30 | 31 | Vyhľadávacie pole názvu |
| BookSymb | Str2 | 3 | Symbol knihy |
| BookYear | word | 2 | Rok, na ktorý je kniha založená |
| SerNum | word | 2 | Poradové číslo knihy v rámci roka |

### Prevádzka

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| WriNum | word | 2 | Číslo prevádzkovej jednotky - **FK WRILST** |

### Číslovanie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| BegNum | longint | 4 | Počiatočné poradové číslo pre danú knihu |
| ModNum | byte | 1 | Počet modifikácií |

### Nastavenia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| LSuCalc | byte | 1 | Spôsob výpočtu účtovných odpisov |
| ActYear | Str4 | 5 | Aktuálny rok (pre spätné zadávanie) |

### Štatistiky

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocQnt | longint | 4 | Počet evidenčných kariet v knihe |
| ActPos | longint | 4 | Aktuálna pozícia |

### Rezervované

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Reserve | Str74 | 75 | Rezervované pole |
| Mark | Str1 | 2 | Príznak |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtName | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |

## Indexy (2)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | BookNum | BookNum | Duplicit |
| 1 | _BookName | BookName | Duplicit, Case-insensitive |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| WriNum | WRILST.WriNum | Prevádzková jednotka |
| BookNum | FXAyynnn (súbor) | Karty majetku |
| BookNum | FXTyynnn (súbor) | Daňové odpisy |
| BookNum | FXLyynnn (súbor) | Účtovné odpisy |

## Vzťah k FXA/FXT/FXL súborom

Každá kniha má priradené súbory s údajmi:

```
FXBLST.BookNum = "A001" → FXA-A001.BTR (karty majetku)
                        → FXT-A001.BTR (daňové odpisy)
                        → FXL-A001.BTR (účtovné odpisy)
                        → FXC-A001.BTR (technické zhodnotenie)
                        → FXM-A001.BTR (korekcia ceny)
                        → FXN-A001.BTR (poznámky)
```

## Použitie

- Organizácia majetku do logických skupín (kníh)
- Oddelenie majetku podľa prevádzok
- Nastavenie číslovacích sekvencií
- Správa roku pre spätné zadávanie

## Business pravidlá

- Jedna kniha = obvykle jedna prevádzka alebo typ majetku
- BookNum formát typicky X-NNN alebo podobný
- Mazanie knihy možné len ak DocQnt = 0
- ActYear umožňuje zadávať majetok do minulého roka

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
