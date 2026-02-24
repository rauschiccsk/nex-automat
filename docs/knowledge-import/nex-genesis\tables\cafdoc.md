# CAFDOC - Pokladničné doklady podľa pokladníkov

## Kľúčové slová / Aliases

CAFDOC, CAFDOC.BTR, pokladničné, doklady, podľa, pokladníkov

## Popis

Tabuľka pokladničných dokladov evidovaných podľa jednotlivých pokladníkov. Sleduje účtenky, príjmy a výdaje s rozpisom platidiel. Globálny súbor.

## Btrieve súbor

`CAFDOC.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DATA\CAFDOC.BTR`

## Štruktúra polí (25 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CasUsrc | Str10 | 11 | Identifikátor pokladníka |
| DocDate | DateType | 4 | Dátum vystavenia dokladu |
| DocTime | TimeType | 4 | Čas vystavenia dokladu |
| DocType | Str1 | 2 | Typ dokladu (U/P/V) |
| CasNum | word | 2 | Číslo pokladne |
| CadNum | word | 2 | Číslo účtenky |

### Hodnoty podľa platidiel (10 typov)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocVal0 | double | 8 | Hodnota - platidlo 0 |
| DocVal1 | double | 8 | Hodnota - platidlo 1 |
| DocVal2 | double | 8 | Hodnota - platidlo 2 |
| DocVal3 | double | 8 | Hodnota - platidlo 3 |
| DocVal4 | double | 8 | Hodnota - platidlo 4 |
| DocVal5 | double | 8 | Hodnota - platidlo 5 |
| DocVal6 | double | 8 | Hodnota - platidlo 6 |
| DocVal7 | double | 8 | Hodnota - platidlo 7 |
| DocVal8 | double | 8 | Hodnota - platidlo 8 |
| DocVal9 | double | 8 | Hodnota - platidlo 9 |

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
| 0 | CasUsrc, DocDate, DocTime | CuDdDt | Duplicit |
| 1 | CasUsrc | CasUsrc | Duplicit |

## Typy dokladov (DocType)

| Hodnota | Popis |
|---------|-------|
| U | Účtenka (predaj) |
| P | Príjem do pokladne |
| V | Výdaj z pokladne |

## Príklad

```
CasUsrc = "JAN.KOVAC"
DocDate = 15.01.2024
DocTime = 14:35:22
DocType = "U" (účtenka)
CasNum  = 1
CadNum  = 1234
─────────────────────────────────────────────────────────────────
DocVal0 = 25.50 EUR (hotovosť)
DocVal1 =  0.00 EUR
DocVal2 =  0.00 EUR
...
```

## Použitie

- Detailná história dokladov pokladníka
- Kontrola zmeny
- Audit transakcií
- Sledovanie príjmov a výdajov

## Business pravidlá

- Jeden záznam = jeden doklad
- DocValX sa sčítava do CAFSUM.ActValX
- Pri type P (príjem) sú hodnoty kladné
- Pri type V (výdaj) sú hodnoty záporné

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
