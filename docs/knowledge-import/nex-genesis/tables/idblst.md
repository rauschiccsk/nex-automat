# IDBLST - Zoznam kníh interných účtovných dokladov

## Kľúčové slová / Aliases

IDBLST, IDBLST.BTR, zoznam, kníh, interných, účtovných, dokladov

## Popis

Konfiguračná tabuľka kníh interných účtovných dokladov. Definuje základné nastavenia kníh.

## Btrieve súbor

`IDBLST.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\IDBLST.BTR`

## Štruktúra polí (13 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| BookNum | Str5 | 6 | Číslo knihy - **PRIMARY KEY** |
| BookName | Str30 | 31 | Názov knihy |
| _BookName | Str30 | 31 | Vyhľadávacie pole názvu |
| BookYear | Str4 | 5 | Rok založenia knihy |

### Nastavenia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| WriNum | word | 2 | Číslo prevádzkovej jednotky |
| WriAdd | byte | 1 | Povinné zadávanie PJ (1=zapnuté) |

### Štatistiky

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocQnt | longint | 4 | Počet dokladov v knihe |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |
| ModNum | longint | 4 | Počítadlo modifikácií |

## Indexy (2)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | BookNum | BookNum | Duplicit |
| 1 | _BookName | BookName | Duplicit, Case insensitive |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| WriNum | WRILST.WriNum | Prevádzková jednotka |

## Použitie

- Konfigurácia kníh interných dokladov
- Členenie podľa rokov
- Členenie podľa prevádzkových jednotiek

## Business pravidlá

- Kniha je vytvorená pre konkrétny rok (BookYear)
- WriAdd=1 vyžaduje zadanie PJ pri každom doklade
- DocQnt sa automaticky aktualizuje

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
