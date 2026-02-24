# BANKLST - Zoznam bankových ústavov

## Kľúčové slová / Aliases

BANKLST, BANKLST.BTR, zoznam bánk, bank list, SWIFT kódy, peňažné ústavy

## Popis

Číselník bankových ústavov. Obsahuje smerové kódy, názvy a kontaktné údaje bánk.

## Btrieve súbor

`BANKLST.BTR`

## Umiestnenie

`C:\NEX\YEARACT\FIRMS\BANKLST.BTR`

## Polia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| BankCode | Str15 | 16 | Smerový kód banky - **PRIMARY KEY** |
| BankName | Str30 | 31 | Názov banky |
| _BankName | Str15 | 16 | Vyhľadávacie pole názvu |
| BankAddr | Str30 | 31 | Adresa banky |
| BankCtn | Str30 | 31 | Sídlo banky (mesto) |
| BankZip | Str15 | 16 | PSČ banky |
| BankIno | Str15 | 16 | IČO banky |
| IbanCode | Str34 | 35 | IBAN kód (prefix) |
| SwftCode | Str20 | 21 | SWIFT kód banky |
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModNum | word | 2 | Poradové číslo modifikácie |
| ModUser | Str8 | 9 | Používateľ poslednej zmeny |
| ModDate | DateType | 4 | Dátum poslednej zmeny |
| ModTime | TimeType | 4 | Čas poslednej zmeny |

## Indexy

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | BankCode | BankCode | Duplicit |
| 1 | _BankName | BankName | Case-insensitive, Duplicit |

## Príklady dát (SR)

| BankCode | BankName | SwftCode | BankCtn |
|----------|----------|----------|---------|
| 0200 | VÚB, a.s. | SUBASKBX | Bratislava |
| 0900 | Slovenská sporiteľňa | GIBASKBX | Bratislava |
| 1100 | Tatra banka | TATRSKBX | Bratislava |
| 0720 | Národná banka Slovenska | NBSBSKBX | Bratislava |
| 3100 | Sberbank Slovensko | LUBASKBX | Bratislava |
| 5600 | Prima banka | KOMASK2X | Žilina |
| 8330 | Fio banka | FIOZSKBA | Bratislava |

## Použitie

Banka sa priraďuje:
- `PAB.BankCode` - banka hlavného účtu partnera
- `PABACC.BankCode` - banka konkrétneho účtu partnera
- Používa sa pri generovaní príkazov na úhradu

## Business pravidlá

- BankCode je 4-miestny smerový kód (SR) alebo dlhší (zahraničie)
- SWIFT kód je povinný pre medzinárodné platby
- _BankName je uppercase pre case-insensitive vyhľadávanie
- IBAN prefix sa používa pri automatickom generovaní IBAN

## Formát čísla účtu (SR)

```
Číslo účtu: XXXXXX-YYYYYYYYYY/ZZZZ
                              └── BankCode (smerový kód)

IBAN: SKCC ZZZZ 0000 00XX XXXX YYYY YYYY
          └── BankCode
```

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
