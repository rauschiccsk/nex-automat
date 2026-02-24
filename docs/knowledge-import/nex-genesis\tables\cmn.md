# CMN - Poznámky ku kompletizačným dokladom

## Kľúčové slová / Aliases

CMN, CMN.BTR, poznámky, kompletizačným, dokladom

## Popis

Poznámky k hlavičkám kompletizačných dokladov. Umožňuje pridať neobmedzené množstvo textových poznámok ku každému dokladu.

## Btrieve súbor

`CMNyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARyy\STK\CMNyynnn.BTR`

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
| DocNum | CMH.DocNum | Hlavička dokladu |

## Použitie

- Pridávanie poznámok k dokladom
- Záznam špeciálnych inštrukcií
- Dokumentácia výrobného procesu

## Business pravidlá

- Viacej poznámok na jeden doklad
- NoteNum určuje poradie poznámok
- Poznámky sa tlačia spolu s dokladom

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
