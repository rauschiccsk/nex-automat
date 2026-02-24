# CSOEXP - Výdajové hotovostné operácie

## Kľúčové slová / Aliases

CSOEXP, CSOEXP.BTR, výdajové, hotovostné, operácie

## Popis

Číselník výdajových hotovostných operácií (predkontácie). Definuje typy výdajov s prednastavenými účtami a sadzbami DPH.

## Btrieve súbor

`CSOEXP.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\CSOEXP.BTR`

## Štruktúra polí (16 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CsoNum | word | 2 | Kód operácie - **PRIMARY KEY** |
| CsoName | Str30 | 31 | Názov operácie |
| _CsoName | Str30 | 31 | Vyhľadávacie pole |

### Účtovanie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| AccSnt | Str3 | 4 | Syntetický účet |
| AccAnl | Str6 | 7 | Analytický účet |
| VatPrc | byte | 1 | Sadzba DPH (%) |

### Predvolená hodnota

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PayVal | double | 8 | Prednastavená čiastka úhrady |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtName | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |
| ModNum | word | 2 | Počítadlo modifikácií |

## Indexy (3)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | CsoNum | CsoNum | Duplicit |
| 1 | _CsoName | CsoName | Duplicit |
| 2 | AccSnt, AccAnl | SntAnl | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| AccSnt+AccAnl | ACCLST | Účet |

## Príklady operácií

| CsoNum | CsoName | AccSnt | Popis |
|--------|---------|--------|-------|
| 1 | Úhrada FA | 321 | Záväzky |
| 2 | Výplata mzdy | 331 | Zamestnanci |
| 3 | Cestovné | 512 | Cestovné |
| 4 | Odvod do banky | 261 | Peniaze na ceste |
| 5 | Nákup materiálu | 501 | Spotreba materiálu |

## Použitie

- Predkontácie pre výdajové doklady
- Rýchle zadávanie položiek
- Štandardizácia účtovania

## Business pravidlá

- Výber operácie automaticky doplní účet a DPH
- PayVal = predvolená suma (môže sa zmeniť)
- Zjednodušuje prácu pokladníkov

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
