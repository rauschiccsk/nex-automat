# CSN - Poznámky k hotovostným dokladom

## Kľúčové slová / Aliases

CSN, CSN.BTR, poznámky, hotovostným, dokladom

## Popis

Tabuľka poznámkových riadkov k hotovostným pokladničným dokladom. Podporuje textové a interné poznámky.

## Btrieve súbor

`CSNyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\CSNyynnn.BTR`

## Štruktúra polí (4 polia)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocNum | Str12 | 13 | Interné číslo dokladu - **FK → CSH.DocNum** |
| NotType | Str1 | 2 | Typ poznámky (T=textová, I=interná) |
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
| DocNum | CSH.DocNum | Hlavička dokladu |

## Typy poznámok (NotType)

| Hodnota | Popis |
|---------|-------|
| T | Textová časť - tlačí sa na doklade |
| I | Interná poznámka - len v systéme |

## Použitie

- Viacriadkové poznámky k dokladu
- Oddelenie tlačových a interných poznámok

## Business pravidlá

- Jeden doklad môže mať neobmedzený počet poznámkových riadkov
- NotType='T' sa tlačí na doklade
- NotType='I' je len interná

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
