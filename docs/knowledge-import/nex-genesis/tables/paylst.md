# PAYLST - Formy úhrady

## Kľúčové slová / Aliases

PAYLST, PAYLST.BTR, spôsoby platby, payment methods, platobné podmienky

## Popis

Číselník foriem úhrady faktúr. Definuje spôsoby platby používané v obchodných vzťahoch.

## Btrieve súbor

`PAYLST.BTR`

## Umiestnenie

`C:\NEX\YEARACT\FIRMS\PAYLST.BTR`

## Polia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PayCode | Str3 | 4 | Kód formy úhrady - **PRIMARY KEY** |
| PayName | Str20 | 21 | Názov formy úhrady |
| _PayName | Str20 | 21 | Vyhľadávacie pole názvu |
| ModUser | Str8 | 9 | Používateľ poslednej zmeny |
| ModDate | DateType | 4 | Dátum poslednej zmeny |
| ModTime | TimeType | 4 | Čas poslednej zmeny |

## Indexy

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | PayCode | PayCode | Case-insensitive, Duplicit |
| 1 | _PayName | PayName | Case-insensitive, Duplicit |

## Príklady dát

| PayCode | PayName | Popis |
|---------|---------|-------|
| HOT | Hotovosť | Platba v hotovosti |
| PRE | Prevodom | Bankový prevod |
| DOB | Dobierka | Platba pri prevzatí |
| KAR | Kartou | Platobná karta |
| ZAL | Záloha | Platba vopred |
| INK | Inkaso | Inkaso z účtu |
| FAC | Faktoring | Factoringová platba |

## Použitie

Forma úhrady sa priraďuje partnerom:
- `PAB.IsPayCode` - preferovaná forma úhrady od dodávateľa
- `PAB.IcPayCode` - preferovaná forma úhrady pre odberateľa
- Používa sa aj na dokladoch (faktúry, objednávky)

## Business pravidlá

- PayCode je krátka skratka (max 3 znaky)
- _PayName je uppercase pre case-insensitive vyhľadávanie
- Forma úhrady ovplyvňuje účtovanie a workflow spracovania

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
