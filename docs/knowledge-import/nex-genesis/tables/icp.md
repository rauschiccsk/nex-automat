# ICP - Penalizačné faktúry

## Kľúčové slová / Aliases

ICP, ICP.BTR, faktúry platobné podmienky, invoice payment terms

## Popis

Tabuľka prepojenia penalizačných faktúr s pôvodnými faktúrami. Sleduje väzbu medzi penalizačnými faktúrami (úroky z omeškania) a faktúrami, z ktorých boli vypočítané.

## Btrieve súbor

`ICPyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\ICPyynnn.BTR`

## Štruktúra polí (3 polia)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocNum | Str12 | 13 | Interné číslo penalizačnej faktúry - **FK → ICH.DocNum** |
| IcdNum | Str12 | 13 | Interné číslo pôvodnej faktúry - **FK → ICH.DocNum** |
| PenVal | double | 8 | Hodnota penále pre túto faktúru |

## Indexy (2)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | DocNum | DocNum | Duplicit |
| 1 | IcdNum | IcdNum | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| DocNum | ICH.DocNum | Penalizačná faktúra |
| IcdNum | ICH.DocNum | Pôvodná neuhradená faktúra |

## Workflow

```
1. Identifikácia neuhradených faktúr po splatnosti
   ↓
2. Výpočet úrokov z omeškania (ICDPEN)
   ↓
3. Vytvorenie penalizačnej faktúry (ICH)
   ↓
4. Zápis väzieb do ICP
   ↓
5. Jedna penalizačná FA môže obsahovať penále z viacerých pôvodných FA
```

## Business pravidlá

- Penalizačná faktúra môže obsahovať penále z viacerých pôvodných faktúr
- PenVal obsahuje čiastočnú hodnotu penále pripadajúcu na konkrétnu pôvodnú faktúru
- Suma PenVal pre jednu penalizačnú FA = celková hodnota penalizačnej FA
- Sledovanie pre účely reklamácií a dohadov

## Použitie

- Evidencia penalizačných faktúr
- Audit väzieb penále na pôvodné doklady
- Výkaz penalizácií podľa odberateľov
- Spätné dohľadanie zdrojových faktúr

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
