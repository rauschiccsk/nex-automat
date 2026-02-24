# ICW - História upomienok k OF

## Kľúčové slová / Aliases

ICW, ICW.BTR, faktúry zálohy, invoice advances, zálohové faktúry

## Popis

Tabuľka histórie upomienok k odberateľským faktúram. Sleduje jednotlivé upomienky vystavené pre neuhradené faktúry.

## Btrieve súbor

`ICWbbbbb.BTR` (bbbbb=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\ICWbbbbb.BTR`

## Štruktúra polí (11 polí)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| IcdNum | Str12 | 13 | Interné číslo faktúry - **FK → ICH.DocNum** |
| WrnNum | byte | 1 | Číslo upomienky |
| WrnVal | double | 8 | Hodnota, na ktorú bola vystavená upomienka |
| WrnDate | DateType | 4 | Dátum vystavenia upomienky |
| WrnUser | Str10 | 11 | Prihlasovacie meno vystaviteľa |
| WrnName | Str30 | 31 | Meno a priezvisko vystaviteľa |
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |

## Indexy (2)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | IcdNum | IcdNum | Duplicit |
| 1 | IcdNum, WrnNum | InWn | Unique |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| IcdNum | ICH.DocNum | Hlavička faktúry |

## Workflow

```
1. Faktúra po splatnosti
   ↓
2. Generovanie 1. upomienky (WrnNum=1)
   ↓
3. Zápis do ICW
   ↓
4. Tlač a odoslanie upomienky
   ↓
5. Aktualizácia ICH.WrnNum, ICH.WrnDate
   ↓
6. Pri opakovanom omeškaní - ďalšie upomienky (WrnNum=2,3...)
```

## Business pravidlá

- Jedna faktúra môže mať viac upomienok
- Upomienky sa číslujú sekvenčne
- Sleduje sa hodnota zostatku pri vystavení upomienky
- História upomienok pre analýzu platobnej disciplíny

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
