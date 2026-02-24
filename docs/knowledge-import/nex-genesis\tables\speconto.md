# SPECONTO - Zjednodušené zálohové účty

## Kľúčové slová / Aliases

SPECONTO, SPECONTO.BTR, zjednodušené, zálohové, účty

## Popis

Zjednodušená tabuľka zálohových účtov odberateľov bez rozdelenia podľa DPH skupín. Používa sa pre základnú evidenciu zostatkov.

## Btrieve súbor

`SPECONTO.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\SPECONTO.BTR`

## Štruktúra polí (13 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PaCode | word | 2 | Kód odberateľa - **PRIMARY KEY, FK PAB** |
| PaName | Str30 | 31 | Názov odberateľa |
| _PaName | Str30 | 31 | Vyhľadávacie pole názvu |

### Súhrnné hodnoty

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| IncVal | double | 8 | Celkový príjem |
| ExpVal | double | 8 | Celkový výdaj |
| EndVal | double | 8 | Konečný zostatok |

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
```

## Porovnanie so SPBLST

| Vlastnosť | SPECONTO | SPBLST |
|-----------|----------|--------|
| DPH skupiny | Nie | Áno (6 skupín) |
| Rozdelenie príjmov | Nie | IncVal1-6 |
| Rozdelenie výdajov | Nie | ExpVal1-6 |
| Vyúčtované hodnoty | Nie | PrfVal1-6 |
| Počet polí | 13 | 38 |

## Použitie

- Zjednodušená evidencia zálohových účtov
- Rýchly prehľad zostatkov
- Alternatíva k SPBLST pre jednoduchšie scenáre

## Business pravidlá

- Jeden partner = jeden zálohový účet
- Nesleduje DPH skupiny
- EndVal > 0 znamená nevyčerpanú zálohu

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
