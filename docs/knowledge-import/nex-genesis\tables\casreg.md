# CASREG - Globálny register pokladničných platidiel

## Kľúčové slová / Aliases

CASREG, CASREG.BTR, globálny, register, pokladničných, platidiel

## Popis

Tabuľka globálneho registra platobných prostriedkov. Obsahuje súhrnný stav všetkých typov platidiel naprieč všetkými pokladňami. Globálny súbor.

## Btrieve súbor

`CASREG.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DATA\CASREG.BTR`

## Štruktúra polí (8 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PayNum | byte | 1 | Kód platidla (0-9) |
| PayName | Str30 | 31 | Názov platidla |

### Hodnoty

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PayVal | double | 8 | Celková hodnota platidla |
| BegVal | double | 8 | Počiatočný stav |
| IncVal | double | 8 | Celkový príjem |
| TrnVal | double | 8 | Celková tržba |
| ExpVal | double | 8 | Celkový odvod |
| EndVal | double | 8 | Konečný stav |

## Indexy (1)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | PayNum | PayNum | Duplicit, Case-insensitive |

## Rozdiel oproti CAP

| Tabuľka | Rozsah | Súbor |
|---------|--------|-------|
| CAP | Jedna pokladňa | CAPnnnnn.BTR |
| CASREG | Všetky pokladne | CASREG.BTR |

## Príklad

```
PayNum  = 0
PayName = "Hotovosť"
─────────────────────────────────────────────────────────────────
BegVal  =  2,500.00 EUR (súčet zo všetkých pokladní)
TrnVal  = 15,250.00 EUR (celková tržba)
IncVal  =  1,000.00 EUR (vklady)
ExpVal  = 12,000.00 EUR (odvody)
EndVal  =  6,750.00 EUR (konečný stav)
```

## Výpočet

```
EndVal = BegVal + TrnVal + IncVal - ExpVal

CASREG.TrnVal = Σ CAP.TrnVal (všetky pokladne)
```

## Použitie

- Celkový prehľad stavu platidiel
- Reporting naprieč pokladňami
- Kontrola celkovej tržby
- Porovnanie s bankovou uzávierkou

## Business pravidlá

- CASREG = súčet hodnôt zo všetkých CAP tabuliek
- Aktualizuje sa pri dennej uzávierke
- Používa sa pre celkový reporting

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
