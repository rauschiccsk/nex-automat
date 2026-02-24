# CABLST - Zoznam kníh registračných pokladníc

## Kľúčové slová / Aliases

CABLST, CABLST.BTR, zoznam, kníh, registračných, pokladníc

## Popis

Tabuľka zoznamu kníh registračných pokladníc. Obsahuje konfiguráciu jednotlivých pokladníc vrátane nastavenia cesty ku kontrolným páskam, skladu a cenníka. Globálny súbor.

## Btrieve súbor

`CABLST.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DATA\CABLST.BTR`

## Štruktúra polí (17 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| BookNum | Str5 | 6 | Číslo knihy registračnej pokladne (rrNNN) |
| BookName | Str30 | 31 | Pomenovanie pokladne |
| CasNum | word | 2 | Číslo pokladne |

### Konfigurácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CasPath | Str78 | 79 | Adresár kontrolných pások pokladne |
| PlsNum | word | 2 | Číslo cenníka (0=všetky) - **FK PLSLST** |
| StkNum | word | 2 | Číslo predvoleného skladu - **FK STKLST** |
| WriNum | word | 2 | Číslo prevádzkovej jednotky - **FK WRILST** |
| CasStk | byte | 1 | Zdroj čísla skladu (1=pokladňa, 0=kniha) |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModNum | word | 2 | Poradové číslo modifikácie |
| ModUser | Str8 | 9 | Používateľ poslednej zmeny |
| ModDate | DateType | 4 | Dátum poslednej zmeny |
| ModTime | TimeType | 4 | Čas poslednej zmeny |

## Indexy (2)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | BookNum | BookNum | Duplicit |
| 1 | CasNum | CasNum | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| PlsNum | PLSLST.PlsNum | Predajný cenník |
| StkNum | STKLST.StkNum | Predvolený sklad |
| WriNum | WRILST.WriNum | Prevádzková jednotka |

## Príklad

```
BookNum  = "24001"
BookName = "Pokladňa 1"
CasNum   = 1
CasPath  = "\\SERVER\NEX\CASSAS\CAS001\"
PlsNum   = 1
StkNum   = 10
WriNum   = 1
CasStk   = 0 (číslo skladu z knihy)
```

## Použitie

- Konfigurácia registračných pokladníc
- Nastavenie cesty k T-súborom (kontrolným páskam)
- Väzba pokladne na sklad a cenník
- Spracovanie denných uzávierok

## Business pravidlá

- BookNum = ActYear2 + StrIntZero(CasNum, 3) napr. "24001"
- Knihu možno zmazať len ak neobsahuje denné uzávierky
- CasPath musí obsahovať T-súbory pre spracovanie
- CasStk=1: číslo skladu sa berie z pokladne, CasStk=0: z knihy

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
