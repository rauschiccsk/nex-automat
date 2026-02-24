# ACCSNT - Účtová osnova syntetických účtov

## Kľúčové slová / Aliases

ACCSNT, ACCSNT.BTR, účtová, osnova, syntetických, účtov

## Popis

Číselník syntetických účtov (účtová osnova). Definuje trojmiestne účty podľa slovenskej účtovej osnovy s typom účtu.

## Btrieve súbor

`ACCSNT.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\ACCSNT.BTR`

## Štruktúra polí (12 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| AccSnt | Str3 | 4 | Číslo syntetického účtu - **PRIMARY KEY** |
| SntName | Str30 | 31 | Názov syntetického účtu |
| _SntName | Str30 | 31 | Vyhľadávacie pole názvu |

### Typ účtu

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| SntType | Str1 | 2 | Typ účtu (N/V/A/P) |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtName | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModNum | word | 2 | Počítadlo modifikácií |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |

## Indexy (2)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | AccSnt | AccSnt | Duplicit |
| 1 | _SntName | SntName | Duplicit |

## Typy účtov (SntType)

| Hodnota | Popis | Zostatok |
|---------|-------|----------|
| A | Aktíva (súvaha - majetok) | MD - Dal |
| P | Pasíva (súvaha - zdroje) | Dal - MD |
| N | Náklady (výsledovka) | MD - Dal |
| V | Výnosy (výsledovka) | Dal - MD |

## Príklady účtov

| AccSnt | SntName | SntType |
|--------|---------|---------|
| 022 | Samostatné hnuteľné veci | A |
| 112 | Materiál na sklade | A |
| 132 | Tovar na sklade | A |
| 211 | Pokladnica | A |
| 221 | Bankové účty | A |
| 311 | Odberatelia | A |
| 321 | Dodávatelia | P |
| 343 | DPH | A/P |
| 411 | Základné imanie | P |
| 501 | Spotreba materiálu | N |
| 504 | Predaný tovar | N |
| 602 | Tržby z predaja služieb | V |
| 604 | Tržby za tovar | V |

## Použitie

- Definícia účtovej osnovy
- Validácia účtovania
- Podklad pre výkazy

## Business pravidlá

- AccSnt je 3-miestny kód podľa účtovej osnovy
- SntType určuje správanie účtu v súvahe/výsledovke
- Syntetický účet môže mať viacej analytických účtov (ACCANL)

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
