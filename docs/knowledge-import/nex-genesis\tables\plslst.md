# PLSLST - Zoznam predajných cenníkov

## Kľúčové slová / Aliases

PLSLST, PLSLST.BTR, zoznam, predajných, cenníkov

## Popis

Konfiguračná tabuľka predajných cenníkov. Definuje nastavenia cenníka, pripojený sklad, typ zaokrúhľovania, master cenník a pravidlá cenotvorby.

## Btrieve súbor

`PLSLST.BTR`

## Umiestnenie

`C:\NEX\YEARACT\STK\PLSLST.BTR`

## Štruktúra polí (17 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PlsNum | word | 2 | Poradové číslo cenníka - **PRIMARY KEY** |
| PlsName | Str30 | 31 | Názov predajného cenníka |

### Nastavenie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| StkNum | word | 2 | Číslo pripojeného skladu |
| WriNum | word | 2 | Číslo prevádzkovej jednotky |
| RndType | byte | 1 | Typ zaokrúhlenia predajnej ceny |
| AvgCalc | byte | 1 | Spôsob cenotvorby (1=priemerná NC, 0=posledná NC) |
| FrmNum | byte | 1 | Číslo formulára na tvorbu ceny |
| GrpTyp | Str1 | 2 | Typ skupiny (T=tovarová, F=finančná, S=špecifikačná) |

### Prepojenie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Master | word | 2 | Číslo hlavného cenníka (master) |
| DelPls | byte | 1 | Povolenie zrušiť cenník (0/1) |
| PrnLab | byte | 1 | Automatická tlač cenovky |
| Shared | byte | 1 | Zdieľanie cez FTP (1=zdieľaný) |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |

## Indexy (2)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | PlsNum | PlsNum | Duplicit |
| 1 | Master | Master | Duplicit |

## Typy zaokrúhlenia (RndType)

| Hodnota | Popis |
|---------|-------|
| 0 | Na 0.01 |
| 1 | Na 0.10 |
| 2 | Na 0.50 |
| 3 | Na 1.00 |
| 4 | Na 5.00 |
| 5 | Na 10.00 |
| 6 | Podľa tabuľky |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| StkNum | STKLST.StkNum | Pripojený sklad |
| WriNum | WRILST.WriNum | Prevádzková jednotka |
| Master | PLSLST.PlsNum | Hlavný cenník |

## Použitie

- Konfigurácia predajných cenníkov
- Prepojenie cenníka na sklad
- Master-detail vzťahy medzi cenníkmi
- Nastavenie zaokrúhľovania cien

## Business pravidlá

- AvgCalc=1 počíta zisk z priemernej NC, =0 z poslednej NC
- Master≠0 znamená závislosť na hlavnom cenníku
- DelPls=1 je potrebné pred zmazaním cenníka
- Shared=1 aktivuje FTP synchronizáciu

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
