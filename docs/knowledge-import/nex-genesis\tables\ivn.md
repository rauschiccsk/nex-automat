# IVN - Poznámky k inventúrnym dokladom

## Kľúčové slová / Aliases

IVN, IVN.BTR, poznámky, inventúrnym, dokladom

## Popis

Poznámky k hlavičkám inventúrnych dokladov. Umožňuje pridať neobmedzené množstvo textových poznámok ku každej inventúre.

## Btrieve súbor

`IVNyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARyy\STK\IVNyynnn.BTR`

## Štruktúra polí (4 polia)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocNum | Str12 | 13 | Číslo hlavičky dokladu - **FK** |
| NoteNum | word | 2 | Poradové číslo poznámky |

### Obsah

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Note | Str80 | 81 | Text poznámky |
| NoteType | Str1 | 2 | Typ poznámky |

## Indexy (2)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | DocNum, NoteNum | DocNote | Unikátny |
| 1 | DocNum | DocNum | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| DocNum | IVH.DocNum | Hlavička inventúry |

## Použitie

- Pridávanie poznámok k inventúram
- Záznam zistení pri inventúre
- Dokumentácia príčin rozdielov

## Business pravidlá

- Viacej poznámok na jeden doklad
- NoteNum určuje poradie poznámok
- Poznámky sa tlačia spolu s dokladom

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
