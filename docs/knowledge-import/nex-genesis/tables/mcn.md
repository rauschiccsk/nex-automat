# MCN - Poznámky k odberateľským cenovým ponukám

## Kľúčové slová / Aliases

MCN, MCN.BTR, poznámky, odberateľským, cenovým, ponukám

## Popis

Tabuľka poznámkových riadkov k odberateľským cenovým ponukám. Podporuje interné aj externé poznámky.

## Btrieve súbor

`MCNyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\MCNyynnn.BTR`

## Štruktúra polí (4 polia)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocNum | Str12 | 13 | Interné číslo ponuky - **FK → MCH.DocNum** |
| NotType | Str1 | 2 | Typ poznámky (E=externé, I=interné) |
| LinNum | word | 2 | Poradové číslo riadku |
| Notice | Str250 | 251 | Poznámkový riadok |

## Indexy (2)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | DocNum, NotType, LinNum | DoNtLn | Duplicit |
| 1 | DocNum | DocNum | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| DocNum | MCH.DocNum | Hlavička ponuky |

## Typy poznámok (NotType)

| Hodnota | Popis |
|---------|-------|
| E | Externé - tlačia sa na doklade |
| I | Interné - viditeľné len v systéme |

## Použitie

- Viacriadkové poznámky k ponuke
- Oddelenie interných a externých poznámok
- Špeciálne podmienky ponuky

## Business pravidlá

- Jeden doklad môže mať neobmedzený počet poznámkových riadkov
- Externé poznámky (E) sa tlačia na doklade pre zákazníka
- Interné poznámky (I) sú len pre interné použitie

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
