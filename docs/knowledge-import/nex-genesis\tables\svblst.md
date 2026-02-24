# SVBLST - Knihy faktúr zálohových platieb

## Kľúčové slová / Aliases

SVBLST, SVBLST.BTR, knihy, faktúr, zálohových, platieb

## Popis

Konfiguračná tabuľka kníh faktúr zálohových platieb. Každá kniha definuje nastavenia účtovania a organizácie pre skupinu daňových dokladov k zálohovým platbám.

## Btrieve súbor

`SVBLST.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\SVBLST.BTR`

## Štruktúra polí (23 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| BookNum | Str5 | 6 | Číslo knihy - **PRIMARY KEY** |
| BookName | Str30 | 31 | Názov knihy |
| BookYear | Str4 | 5 | Rok, na ktorý je založená kniha |
| SerNum | word | 2 | Poradové číslo knihy |

### Prevádzka

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| WriNum | word | 2 | Číslo prevádzkové jednotky - **FK WRILST** |
| DvzName | Str3 | 4 | Skratka meny |

### Účtovanie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocSnt | Str3 | 4 | Syntetický účet zálohy |
| DocAnl | Str6 | 7 | Analytický účet zálohy |
| VatSnt | Str3 | 4 | Syntetický účet DPH |
| VatAnl | Str6 | 7 | Analytický účet DPH |
| AutoAcc | byte | 1 | Automatické účtovanie (1=zapnuté) |

### Číslovanie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ExnFrm | Str12 | 13 | Formát generovania variabilného symbolu |

### Štatistiky

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocQnt | word | 2 | Počet dokladov v knihe |

### Synchronizácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Shared | byte | 1 | Príznak zdieľania (1=zdieľaný) |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModNum | word | 2 | Počítadlo modifikácií |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |

## Indexy (1)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | BookNum | BookNum | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| WriNum | WRILST.WriNum | Prevádzková jednotka |
| DocSnt + DocAnl | ACCANL | Účet zálohy |
| VatSnt + VatAnl | ACCANL | Účet DPH |

## Účtovné schéma

Pri účtovaní dokladu SPV sa použijú tieto účty:

```
MD: DocSnt + DocAnl (účet zálohy)      = BValue (hodnota s DPH)
D:  VatSnt + VatAnl (účet DPH)         = VatVal (hodnota DPH)
D:  Protiúčet (pokladňa/banka)         = AValue (hodnota bez DPH)
```

### Typické účty

| Účet | Popis |
|------|-------|
| 324 | Prijaté preddavky |
| 343 | DPH |
| 211/221 | Pokladňa/Banka |

## Formát variabilného symbolu (ExnFrm)

Podporované vzory:
- `RRNNNNNN` - Rok + poradové číslo
- `NNNNNNNN` - Len poradové číslo
- Vlastný formát s maskami

## Použitie

- Organizácia SPV dokladov podľa kníh
- Nastavenie účtov pre automatické účtovanie
- Konfigurácia generovania čísel

## Business pravidlá

- Jedna kniha = jeden rok + prevádzková jednotka
- BookNum formát typicky X-NNN (napr. A-001)
- SPV súbor: SPVyyNNN.BTR (yy=rok z BookYear, NNN z BookNum)
- AutoAcc=1 automaticky účtuje pri vytvorení SPV záznamu

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
