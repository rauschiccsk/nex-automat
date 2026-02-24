# ICDPEN - Penále k odberateľským faktúram

## Kľúčové slová / Aliases

ICDPEN, ICDPEN.BTR, faktúry penále, invoice penalties, úroky z omeškania

## Popis

Tabuľka penále (úrokov z omeškania) k odberateľským faktúram. Obsahuje vypočítané penále za oneskorené platby pre jednotlivé faktúry.

## Btrieve súbor

`ICDPENyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\ICDPENyynnn.BTR`

## Štruktúra polí (21 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| IcdNum | Str12 | 13 | Interné číslo faktúry - **FK → ICH.DocNum** |
| PenNum | byte | 1 | Poradové číslo penále pre danú faktúru |

### Výpočet penále

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| BegDate | DateType | 4 | Začiatok obdobia výpočtu (deň po splatnosti) |
| EndDate | DateType | 4 | Koniec obdobia výpočtu |
| DayQnt | word | 2 | Počet omeškaných dní |
| PenRate | double | 8 | Úroková sadzba penále (% p.a.) |
| BaseVal | double | 8 | Základ pre výpočet (dlžná suma) |
| PenVal | double | 8 | Vypočítaná hodnota penále |

### Stav

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PenSts | byte | 1 | Stav penále (0=návrh, 1=vyfakturované, 2=storno) |
| PenDoc | Str12 | 13 | Číslo penalizačnej faktúry (ak bolo vyfakturované) |

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

## Indexy (4)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | IcdNum | IcdNum | Duplicit |
| 1 | IcdNum, PenNum | InPn | Unique |
| 2 | PenSts | PenSts | Duplicit |
| 3 | PenDoc | PenDoc | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| IcdNum | ICH.DocNum | Pôvodná faktúra |
| PenDoc | ICH.DocNum | Penalizačná faktúra |

## Stavy penále (PenSts)

| Hodnota | Popis |
|---------|-------|
| 0 | Návrh - vypočítané, nevyfakturované |
| 1 | Vyfakturované - vytvorená penalizačná FA |
| 2 | Storno - zrušené penále |

## Workflow

```
1. Faktúra je po splatnosti
   ↓
2. Spustenie výpočtu penále (Icb_F: IcHPenalF)
   ↓
3. Výpočet: PenVal = BaseVal × (PenRate/100) × (DayQnt/365)
   ↓
4. Zápis do ICDPEN so stavom PenSts=0
   ↓
5. Schválenie a vytvorenie penalizačnej FA
   ↓
6. Aktualizácia PenSts=1, PenDoc=číslo FA
```

## Vzorec výpočtu

```
Penále = Dlžná suma × Úroková sadzba × Počet dní / 365

Príklad:
- BaseVal = 1000 EUR
- PenRate = 9.25% (zákonná sadzba)
- DayQnt = 30 dní
- PenVal = 1000 × 0.0925 × 30/365 = 7.60 EUR
```

## Business pravidlá

- Pre jednu faktúru môže existovať viac záznamov penále (rôzne obdobia)
- Úroková sadzba sa preberá z nastavenia alebo zo zákonnej sadzby
- BegDate začína dňom po dátume splatnosti
- Penále sa počíta do dňa úhrady alebo do aktuálneho dátumu
- Pri čiastočných úhradách sa prepočítava BaseVal

## Použitie

- Výpočet úrokov z omeškania
- Generovanie penalizačných faktúr
- Reporting nedisciplinovaných odberateľov
- Podklad pre právne vymáhanie

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
