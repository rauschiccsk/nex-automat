# SPBLST - Zálohové účty odberateľov

## Kľúčové slová / Aliases

SPBLST, SPBLST.BTR, zálohové, účty, odberateľov

## Popis

Zálohové účty odberateľov. Každý záznam reprezentuje jeden zálohový účet partnera s kumulatívnymi hodnotami príjmov, výdajov a zostatku rozdelených podľa 6 skupín DPH.

## Btrieve súbor

`SPBLST.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\SPBLST.BTR`

## Štruktúra polí (38 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PaCode | word | 2 | Kód odberateľa - **PRIMARY KEY, FK PAB** |
| PaName | Str30 | 31 | Názov odberateľa |
| _PaName | Str30 | 31 | Vyhľadávacie pole názvu |

### Sadzby DPH (6 skupín)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| VatPrc1 | byte | 1 | Sadzba DPH - skupina 1 |
| VatPrc2 | byte | 1 | Sadzba DPH - skupina 2 |
| VatPrc3 | byte | 1 | Sadzba DPH - skupina 3 |
| VatPrc4 | byte | 1 | Sadzba DPH - skupina 4 |
| VatPrc5 | byte | 1 | Sadzba DPH - skupina 5 |
| VatPrc6 | byte | 1 | Sadzba DPH - skupina 6 |

### Súhrnné hodnoty

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| IncVal | double | 8 | Celkový príjem spolu |
| ExpVal | double | 8 | Celkový výdaj spolu |
| EndVal | double | 8 | Konečný stav zálohového účtu |
| PrfVal | double | 8 | Vyúčtovaná hodnota spolu |

### Príjmy podľa DPH skupín

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| IncVal1 | double | 8 | Celkový príjem - skupina 1 |
| IncVal2 | double | 8 | Celkový príjem - skupina 2 |
| IncVal3 | double | 8 | Celkový príjem - skupina 3 |
| IncVal4 | double | 8 | Celkový príjem - skupina 4 |
| IncVal5 | double | 8 | Celkový príjem - skupina 5 |
| IncVal6 | double | 8 | Celkový príjem - skupina 6 |

### Výdaje podľa DPH skupín

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ExpVal1 | double | 8 | Celkový výdaj - skupina 1 |
| ExpVal2 | double | 8 | Celkový výdaj - skupina 2 |
| ExpVal3 | double | 8 | Celkový výdaj - skupina 3 |
| ExpVal4 | double | 8 | Celkový výdaj - skupina 4 |
| ExpVal5 | double | 8 | Celkový výdaj - skupina 5 |
| ExpVal6 | double | 8 | Celkový výdaj - skupina 6 |

### Vyúčtované hodnoty podľa DPH skupín

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PrfVal1 | double | 8 | Vyúčtovaná hodnota - skupina 1 |
| PrfVal2 | double | 8 | Vyúčtovaná hodnota - skupina 2 |
| PrfVal3 | double | 8 | Vyúčtovaná hodnota - skupina 3 |
| PrfVal4 | double | 8 | Vyúčtovaná hodnota - skupina 4 |
| PrfVal5 | double | 8 | Vyúčtovaná hodnota - skupina 5 |
| PrfVal6 | double | 8 | Vyúčtovaná hodnota - skupina 6 |

### Synchronizácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Sended | byte | 1 | Príznak odoslania zmien (0=zmenený, 1=odoslaný) |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ModNum | word | 2 | Počítadlo modifikácií |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |

## Indexy (2)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | PaCode | PaCode | Duplicit |
| 1 | _PaName | PaName | Duplicit, Case-insensitive |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| PaCode | PAB.PaCode | Partner katalóg |

## Výpočtové pravidlá

```
EndVal = IncVal - ExpVal
IncVal = SUM(IncVal1..IncVal6)
ExpVal = SUM(ExpVal1..ExpVal6)
PrfVal = SUM(PrfVal1..PrfVal6)
```

## Použitie

- Evidencia zálohových účtov odberateľov
- Sledovanie zostatkov podľa DPH skupín
- Podklad pre čerpanie záloh

## Business pravidlá

- Jeden partner = jeden zálohový účet
- EndVal > 0 znamená nevyčerpanú zálohu
- EndVal = 0 znamená plne vyčerpanú zálohu
- IncVal sa zvyšuje pri príjme zálohy
- ExpVal sa znižuje (záporné) pri čerpaní

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
