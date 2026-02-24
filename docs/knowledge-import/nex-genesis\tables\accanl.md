# ACCANL - Obratová predvaha analytických účtov

## Kľúčové slová / Aliases

ACCANL, ACCANL.BTR, obratová, predvaha, analytických, účtov

## Popis

Analytické účty s mesačnými obratmi. Obsahuje detailné členenie syntetických účtov a agregované obraty za každý mesiac účtovného obdobia.

## Btrieve súbor

`ACCANL.BTR`

## Umiestnenie

`C:\NEX\YEARyy\DOCS\ACCANL.BTR`

## Štruktúra polí (49 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| AccSnt | Str3 | 4 | Syntetická časť účtu - **FK** |
| AccAnl | Str6 | 7 | Analytická časť účtu |
| AnlName | Str30 | 31 | Názov analytického účtu |
| _AnlName | Str30 | 31 | Vyhľadávacie pole názvu |

### Počiatočné a konečné stavy

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CBegVal | double | 8 | Počiatočný stav - MD |
| DBegVal | double | 8 | Počiatočný stav - Dal |
| CTurnVal | double | 8 | Celkový obrat - MD |
| DTurnVal | double | 8 | Celkový obrat - Dal |
| CEndVal | double | 8 | Konečný stav - MD |
| DEndVal | double | 8 | Konečný stav - Dal |
| DiffVal | double | 8 | Konečný zostatok (rozdiel) |

### Mesačné obraty - MD (CTurn01-12)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CTurn01 | double | 8 | Obrat za mesiac 01 - MD |
| CTurn02 | double | 8 | Obrat za mesiac 02 - MD |
| CTurn03 | double | 8 | Obrat za mesiac 03 - MD |
| CTurn04 | double | 8 | Obrat za mesiac 04 - MD |
| CTurn05 | double | 8 | Obrat za mesiac 05 - MD |
| CTurn06 | double | 8 | Obrat za mesiac 06 - MD |
| CTurn07 | double | 8 | Obrat za mesiac 07 - MD |
| CTurn08 | double | 8 | Obrat za mesiac 08 - MD |
| CTurn09 | double | 8 | Obrat za mesiac 09 - MD |
| CTurn10 | double | 8 | Obrat za mesiac 10 - MD |
| CTurn11 | double | 8 | Obrat za mesiac 11 - MD |
| CTurn12 | double | 8 | Obrat za mesiac 12 - MD |

### Mesačné obraty - Dal (DTurn01-12)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DTurn01 | double | 8 | Obrat za mesiac 01 - Dal |
| DTurn02 | double | 8 | Obrat za mesiac 02 - Dal |
| DTurn03 | double | 8 | Obrat za mesiac 03 - Dal |
| DTurn04 | double | 8 | Obrat za mesiac 04 - Dal |
| DTurn05 | double | 8 | Obrat za mesiac 05 - Dal |
| DTurn06 | double | 8 | Obrat za mesiac 06 - Dal |
| DTurn07 | double | 8 | Obrat za mesiac 07 - Dal |
| DTurn08 | double | 8 | Obrat za mesiac 08 - Dal |
| DTurn09 | double | 8 | Obrat za mesiac 09 - Dal |
| DTurn10 | double | 8 | Obrat za mesiac 10 - Dal |
| DTurn11 | double | 8 | Obrat za mesiac 11 - Dal |
| DTurn12 | double | 8 | Obrat za mesiac 12 - Dal |

### Nastavenia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| AccType | Str1 | 2 | Typ analytického účtu (A/P/N/V) |
| Balance | Str1 | 2 | Saldokontný účet (S) / skupina (1-4) |
| NoTaxMod | byte | 1 | Príznak neovplyvnenia základu dane (1=zapnutý) |
| FjrRow | Str2 | 3 | Číslo stĺpca v peňažnom denníku |
| StaStk | Str1 | 2 | Príznak skladového účtu (S=skladový účet) |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtName | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |

## Indexy (7)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | AccSnt, AccAnl | SnAn | Duplicit |
| 1 | AccSnt | AccSnt | Duplicit |
| 2 | _AnlName | AnlName | Duplicit |
| 3 | CTurnVal | CTurnVal | Duplicit |
| 4 | DTurnVal | DTurnVal | Duplicit |
| 5 | DiffVal | DiffVal | Duplicit |
| 6 | StaStk | StaStk | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| AccSnt | ACCSNT.AccSnt | Syntetický účet |

## Príklady analytických účtov

| AccSnt | AccAnl | AnlName |
|--------|--------|---------|
| 321 | 001 | Dodávatelia tuzemskí |
| 321 | 002 | Dodávatelia zahraniční |
| 311 | 001 | Odberatelia tuzemskí |
| 311 | 002 | Odberatelia zahraniční |
| 343 | 001 | DPH - daň na vstupe |
| 343 | 002 | DPH - daň na výstupe |
| 221 | 001 | Bežný účet VÚB |
| 221 | 002 | Bežný účet SLSP |

## Výpočtové vzťahy

```
CTurnVal = CTurn01 + CTurn02 + ... + CTurn12
DTurnVal = DTurn01 + DTurn02 + ... + DTurn12
CEndVal = CBegVal + CTurnVal
DEndVal = DBegVal + DTurnVal
DiffVal = CEndVal - DEndVal (pre A/N) alebo DEndVal - CEndVal (pre P/V)
```

## Použitie

- Obratová predvaha
- Mesačné zostatky účtov
- Podklad pre súvahu a výsledovku
- Sledovanie vývoja účtov v čase

## Business pravidlá

- Obraty sa aktualizujú pri každom zápise do JOURNAL
- AccType sa dedí z ACCSNT.SntType ak nie je zadané
- Balance='S' označuje saldokontný účet (sledovanie pohľadávok/záväzkov)
- StaStk='S' označuje účet skladových zásob

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
