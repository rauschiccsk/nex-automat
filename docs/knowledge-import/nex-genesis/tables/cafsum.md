# CAFSUM - Kumulatívny stav financií podľa pokladníkov

## Kľúčové slová / Aliases

CAFSUM, CAFSUM.BTR, kumulatívny, stav, financií, podľa, pokladníkov

## Popis

Tabuľka kumulatívneho finančného stavu podľa jednotlivých pokladníkov. Sleduje aktuálny stav všetkých typov platidiel pre každého pokladníka. Globálny súbor.

## Btrieve súbor

`CAFSUM.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DATA\CAFSUM.BTR`

## Štruktúra polí (22 polí)

### Identifikácia pokladníka

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CasUsrc | Str10 | 11 | Identifikátor pokladníka (login) |
| CasUsrn | Str30 | 31 | Meno a priezvisko pokladníka |
| _CasUsrn | Str30 | 31 | Meno - vyhľadávacie pole |

### Finančný stav (10 typov platidiel)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ActVal0 | double | 8 | Finančný stav - platidlo 0 (hotovosť) |
| ActVal1 | double | 8 | Finančný stav - platidlo 1 (karta) |
| ActVal2 | double | 8 | Finančný stav - platidlo 2 (strav. lístky) |
| ActVal3 | double | 8 | Finančný stav - platidlo 3 |
| ActVal4 | double | 8 | Finančný stav - platidlo 4 |
| ActVal5 | double | 8 | Finančný stav - platidlo 5 |
| ActVal6 | double | 8 | Finančný stav - platidlo 6 |
| ActVal7 | double | 8 | Finančný stav - platidlo 7 |
| ActVal8 | double | 8 | Finančný stav - platidlo 8 |
| ActVal9 | double | 8 | Finančný stav - platidlo 9 |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModNum | longint | 4 | Počítadlo modifikácií |
| ModUser | Str8 | 9 | Používateľ poslednej zmeny |
| ModDate | DateType | 4 | Dátum poslednej zmeny |
| ModTime | TimeType | 4 | Čas poslednej zmeny |

## Indexy (2)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | CasUsrc | CasUsrc | Unikátny |
| 1 | _CasUsrn | CasUsrn | Duplicit, Case-insensitive |

## Príklad

```
CasUsrc  = "JAN.KOVAC"
CasUsrn  = "Ján Kováč"
─────────────────────────────────────────────────────────────────
ActVal0  = 1,250.00 EUR (hotovosť)
ActVal1  =   850.00 EUR (platobné karty)
ActVal2  =   420.00 EUR (stravovacie lístky)
ActVal3  =     0.00 EUR
...
─────────────────────────────────────────────────────────────────
Celkom   = 2,520.00 EUR
```

## Použitie

- Sledovanie finančného stavu pokladníkov
- Kontrola odovzdania tržby
- Manko/prebytok pri zmene smeny
- Reporting podľa pokladníkov

## Business pravidlá

- CasUsrc = login pokladníka
- ActValX sa aktualizuje pri každej transakcii
- Pri odovzdaní smeny sa hodnoty vynulujú

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
