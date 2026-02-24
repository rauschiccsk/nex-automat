# TSN - Poznámky k dodávateľským DL

## Kľúčové slová / Aliases

TSN, TSN.BTR, pokladničné poznámky, cash notes, poznámky k dokladom

## Popis

Tabuľka poznámok a príloh k dodávateľským dodacím listom. Umožňuje ukladať dlhé texty a prílohy k dokladom.

## Btrieve súbor

`TSNyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\TSNyynnn.BTR`

## Polia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocNum | Str12 | 13 | Interné číslo DDL - **FK → TSH** |
| NotType | Str1 | 2 | Typ poznámky (T=text, P=príloha) |
| LinNum | word | 2 | Poradové číslo riadku |
| Notice | Str250 | 251 | Text poznámky |

## Indexy

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | DocNum, NotType, LinNum | DoNtLn | Duplicit (Composite PK) |
| 1 | DocNum | DocNum | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| DocNum | TSH.DocNum | Hlavička dokladu |

## Typy poznámok

| NotType | Popis |
|---------|-------|
| T | Textová časť faktúry |
| P | Príloha |

## Použitie

- Poznámky k dodávke
- Reklamačné informácie
- Prílohy (názvy súborov)
- Špeciálne inštrukcie

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
