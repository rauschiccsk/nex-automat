# ICR - Upomienky k odberateľským faktúram

## Kľúčové slová / Aliases

ICR, ICR.BTR, faktúry úhrady, invoice payments, platby faktúr

## Popis

Tabuľka upomienok k odberateľským faktúram. Obsahuje sumárne údaje o upomienkach pre konkrétne faktúry a odberateľov.

## Btrieve súbor

`ICRyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\ICRyynnn.BTR`

## Štruktúra polí (17 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocNum | Str12 | 13 | Interné číslo upomienky - **PRIMARY KEY** |
| SerNum | word | 2 | Poradové číslo upomienky v knihe |
| DocDate | DateType | 4 | Dátum vystavenia upomienky |

### Odberateľ

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PaCode | longint | 4 | Kód odberateľa |
| PaName | Str30 | 31 | Názov odberateľa |
| _PaName | Str20 | 21 | Vyhľadávacie pole |
| PaINO | Str15 | 16 | IČO odberateľa |

### Upomínaná faktúra

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| RmdNum | byte | 1 | Poradové číslo upomienky pre danú faktúru |
| IcdNum | Str12 | 13 | Interné číslo faktúry |
| DayQnt | word | 2 | Počet omeškaných dní |
| EndVal | double | 8 | Neuhradená čiastka faktúry |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |

## Indexy (3)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | DocNum | DocNum | Duplicit |
| 1 | SerNum | SerNum | Duplicit |
| 2 | DocDate | DocDate | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| IcdNum | ICH.DocNum | Upomínaná faktúra |
| PaCode | PAB.PaCode | Odberateľ |

## Použitie

- Evidencia upomienok pre tlač
- Hromadné upomienky pre viacerých odberateľov
- Štatistiky omeškaných platieb
- Správa pohľadávok

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
