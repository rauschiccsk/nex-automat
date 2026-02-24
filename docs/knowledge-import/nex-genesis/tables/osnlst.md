# OSNLST - Poznámky k dodávateľským objednávkam LIST

## Kľúčové slová / Aliases

OSNLST, OSNLST.BTR, zoznam poznámok nákupných objednávok, PO notes list

## Popis

Agregovaná tabuľka poznámok k dodávateľským objednávkam. Rozšírená verzia OSN s možnosťou poznámok aj k položkám.

## Btrieve súbor

`OSNLST.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\OSNLST.BTR`

## Štruktúra polí (5 polí)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocNum | Str12 | 13 | Interné číslo objednávky - **FK → OSHLST.DocNum** |
| ItmNum | word | 2 | Poradové číslo riadku (0=hlavička, >0=položky) |
| NotTyp | Str1 | 2 | Typ poznámky (T=text, P=príloha) |
| LinNum | word | 2 | Poradové číslo riadku poznámky |
| Notice | Str250 | 251 | Text poznámky |

## Indexy (3)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | DocNum, ItmNum, NotTyp, LinNum | DnInNtLn | Unique |
| 1 | DocNum, ItmNum, NotTyp | DnInNt | Duplicit |
| 2 | DocNum | DocNum | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| DocNum | OSHLST.DocNum | Hlavička objednávky |

## Typy poznámok (NotTyp)

| Hodnota | Popis |
|---------|-------|
| T | Textová časť |
| P | Príloha (referencia na súbor) |

## Použitie

- Poznámky k hlavičke (ItmNum=0)
- Poznámky k položkám (ItmNum>0)
- Doplňujúce informácie na objednávke
- Špeciálne požiadavky

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
