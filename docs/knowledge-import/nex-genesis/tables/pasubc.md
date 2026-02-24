# PASUBC - Prevádzkové jednotky partnerov

## Kľúčové slová / Aliases

PASUBC, PASUBC.BTR, dodacie adresy, delivery addresses, shipping addresses, pobočky

## Popis

Tabuľka prevádzkových jednotiek (pobočiek) obchodných partnerov. Umožňuje evidovať viacero doručovacích adries pre jedného partnera.

## Btrieve súbor

`PASUBC.BTR`

## Umiestnenie

`C:\NEX\YEARACT\FIRMS\PASUBC.BTR`

## Polia

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PaCode | longint | 4 | Kód partnera - **FK → PAB** |
| WpaCode | word | 2 | Číslo prevádzkový jednotky |
| WpaName | Str60 | 61 | Názov prevádzky |

### Adresa

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| WpaAddr | Str30 | 31 | Ulica a číslo |
| WpaSta | Str2 | 3 | Kód štátu |
| WpaCty | Str3 | 4 | Kód obce |
| WpaCtn | Str30 | 31 | Názov mesta |
| WpaZip | Str15 | 16 | PSČ |

### Kontakty

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| WpaTel | Str20 | 21 | Telefón |
| WpaFax | Str20 | 21 | Fax |
| WpaEml | Str30 | 31 | Email |

### Doprava

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| TrsCode | Str3 | 4 | Kód spôsobu dopravy |
| TrsName | Str20 | 21 | Názov spôsobu dopravy |

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

## Indexy

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | PaCode | PaCode | Duplicit |
| 1 | PaCode, WpaCode | PaWp | Duplicit (Composite PK) |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| PaCode | PAB.PaCode | Partner |
| WpaSta | STALST.StaCode | Štát |
| WpaCty | CTYLST.CtyCode | Mesto |
| TrsCode | TRSLST.TrsCode | Spôsob dopravy |

## Business pravidlá

- Partner môže mať viac prevádzkových jednotiek
- Composite PK: (PaCode, WpaCode)
- Počet prevádzok sa ukladá do PAB.PasQnt
- Používa sa pri výbere doručovacej adresy na objednávkach/faktúrach

## Príklad použitia

| PaCode | WpaCode | WpaName | WpaAddr | WpaCtn |
|--------|---------|---------|---------|--------|
| 1001 | 1 | Centrála | Hlavná 1 | Bratislava |
| 1001 | 2 | Pobočka BA | Mlynská 5 | Bratislava |
| 1001 | 3 | Pobočka KE | Letná 10 | Košice |

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
