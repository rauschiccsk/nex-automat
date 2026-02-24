# GSCKEY (GSCSRCH) - Vyhľadávacie kľúče

## Popis
Pomocná tabuľka pre rýchle vyhľadávanie tovarových kariet. Obsahuje indexované vyhľadávacie kľúče generované z názvov a kódov tovaru.

## Btrieve súbor
`GSCSRCH.BTR`

## Umiestnenie
`C:\NEX\YEARACT\STORES\GSCSRCH.BTR`

## Polia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| SrchKey | Str30 | 31 | Vyhľadávací kľúč |
| GsCode | longint | 4 | Číslo tovarovej karty (PLU) |

## Indexy

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | SrchKey | SrchKey | Duplicit |
| 1 | GsCode | GsCode | Duplicit |
| 2 | SrchKey, GsCode | SkGc | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| GsCode | GSCAT.GsCode | Tovarová položka |

## Generovanie kľúčov

Vyhľadávacie kľúče sa generujú z:
- Názvu tovaru (slová)
- Čiarového kódu
- Skladového kódu
- Doplnkového názvu

## Použitie

Rýchle vyhľadávanie v module Gsc_F.pas:
1. Používateľ zadá hľadaný text
2. Hľadá sa v GSCSRCH.SrchKey
3. Nájdené GsCode sa použijú na zobrazenie výsledkov z GSCAT

## Údržba

Kľúče sa regenerujú pomocou:
- `Gsc_KeyGen_F.pas` - Generovanie vyhľadávacích kľúčov
- `Gsc_GsnSrc_F.pas` - Vytvorenie názvového vyhľadávača

## Stav migrácie

- [ ] Model vytvorený
- [ ] PostgreSQL full-text search (alternatíva)
- [ ] Elasticsearch (pre veľké datasety)
