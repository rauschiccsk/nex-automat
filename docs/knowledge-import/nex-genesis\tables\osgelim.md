# OSGELIM - Vylúčené položky z objednávok

## Kľúčové slová / Aliases

OSGELIM, OSGELIM.BTR, eliminácia skupín objednávok, PO group elimination

## Popis

Tabuľka položiek vylúčených z automatického objednávania. Umožňuje definovať, ktoré tovary sa nemajú automaticky objednávať od konkrétneho dodávateľa.

## Btrieve súbor

`OSGELIM.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\OSGELIM.BTR`

## Štruktúra polí (11 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PaCode | longint | 4 | Číselný kód dodávateľa |
| GsCode | longint | 4 | Tovarové číslo (PLU) |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModNum | word | 2 | Poradové číslo zmeny |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |

## Indexy (1)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | PaCode, GsCode | PaGs | Unique |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| PaCode | PAB.PaCode | Dodávateľ |
| GsCode | GSCAT.GsCode | Tovar |

## Použitie

- Vylúčenie tovaru z automatického objednávania
- Dočasné pozastavenie objednávania konkrétnych položiek
- Správa výnimiek pre generovanie objednávok

## Business pravidlá

- Pri automatickom generovaní objednávok sa kontroluje táto tabuľka
- Ak existuje záznam pre kombináciu dodávateľ-tovar, položka sa neobjedná
- Môže byť použité pre dočasne nedostupné položky

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
