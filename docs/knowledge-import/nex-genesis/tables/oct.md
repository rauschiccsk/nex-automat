# OCT - Odkazy na dodacie listy

## Kľúčové slová / Aliases

OCT, OCT.BTR, objednávky termíny, order deadlines, termíny plnenia

## Popis

Väzobná tabuľka medzi položkami zákaziek a odberateľskými dodacími listami. Sleduje, ktoré položky zákazky boli dodané na ktorý DL.

## Btrieve súbor

`OCTyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\OCTyynnn.BTR`

## Štruktúra polí (13 polí)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| OciDoc | Str12 | 13 | Číslo zákazky - **FK → OCH.DocNum** |
| OciItm | word | 2 | Číslo položky zákazky |
| TcdDoc | Str12 | 13 | Číslo dodacieho listu - **FK → TCH.DocNum** |
| TcdItm | word | 2 | Číslo položky DL |
| TcdPrq | double | 8 | Dodané množstvo |
| TcdDate | DateType | 4 | Dátum dodania |
| IcdDoc | Str12 | 13 | Číslo faktúry |
| IcdPrq | double | 8 | Fakturované množstvo |
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |

## Indexy (3)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | OciDoc, OciItm, TcdDoc, TcdItm | Primary | Unique |
| 1 | TcdDoc, TcdItm | TcdDocItm | Case-insensitive, Duplicit |
| 2 | IcdDoc | IcdDoc | Case-insensitive, Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| OciDoc | OCH.DocNum | Hlavička zákazky |
| TcdDoc | TCH.DocNum | Hlavička DL |
| IcdDoc | ICH.DocNum | Hlavička faktúry |

## Workflow

```
1. Položka zákazky (OCI)
   ↓
2. Generovanie DL (A_TcdGen)
   ↓
3. Vytvorenie TCH/TCI
   ↓
4. Zápis väzby do OCT
   ↓
5. Aktualizácia OCI.TcdPrq
   ↓
6. Fakturácia DL
   ↓
7. Aktualizácia OCT.IcdDoc/IcdPrq
```

## Business pravidlá

- Jedna položka zákazky môže byť dodaná viacerými DL (čiastkové dodávky)
- Sleduje sa množstvo na každom DL
- Prepojenie na faktúru pre kontrolu fakturácie
- Umožňuje spätnú dohľadateľnosť

## Príklad

```
Zákazka OC24001, položka 1: 100 ks
  → OCT záznam 1: TCD24001/1 = 60 ks
  → OCT záznam 2: TCD24005/1 = 40 ks
Celkom dodané: 100 ks (OCI.TcdPrq = 100)
```

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
