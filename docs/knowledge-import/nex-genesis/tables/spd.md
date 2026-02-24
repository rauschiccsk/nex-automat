# SPD - Zálohové platby odberateľa

## Kľúčové slová / Aliases

SPD, SPD.BTR, zálohové, platby, odberateľa

## Popis

Zálohové platby konkrétneho odberateľa. Každý súbor obsahuje pohyby na zálohovom účte jedného partnera - príjmy aj čerpania záloh.

## Btrieve súbor

`SPDnnnnn.BTR` (nnnnn=kód partnera)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\SPDnnnnn.BTR`

## Štruktúra polí (36 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| SerNum | word | 2 | Poradové číslo všetkých dokladov |
| IncNum | word | 2 | Poradové číslo príjmových dokladov |
| ExpNum | word | 2 | Poradové číslo výdajových dokladov |
| DocNum | Str12 | 13 | Interné číslo dokladu - **PRIMARY KEY** |
| DocDate | DateType | 4 | Dátum zaplatenia alebo čerpania zálohy |

### Popis

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Describe | Str30 | 31 | Popis dokladu |
| _Describe | Str20 | 21 | Vyhľadávacie pole popisu |

### Sadzby DPH

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| VatPrc1 | byte | 1 | Sadzba DPH - skupina 1 |
| VatPrc2 | byte | 1 | Sadzba DPH - skupina 2 |
| VatPrc3 | byte | 1 | Sadzba DPH - skupina 3 |

### Hodnoty dokladu

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocVal | double | 8 | Hodnota dokladu (+príjem/-výdaj) |
| DocVal1 | double | 8 | Hodnota dokladu - skupina 1 |
| DocVal2 | double | 8 | Hodnota dokladu - skupina 2 |
| DocVal3 | double | 8 | Hodnota dokladu - skupina 3 |

### Vyúčtované hodnoty

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PrfVal | double | 8 | Vyúčtovaná hodnota dokladu |
| PrfVal1 | double | 8 | Vyúčtovaná hodnota - skupina 1 |
| PrfVal2 | double | 8 | Vyúčtovaná hodnota - skupina 2 |
| PrfVal3 | double | 8 | Vyúčtovaná hodnota - skupina 3 |

### Kumulatívne hodnoty

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| IncVal | double | 8 | Celkový príjem po tomto doklade |
| ExpVal | double | 8 | Celkový výdaj po tomto doklade |
| EndVal | double | 8 | Konečný zostatok po tomto doklade |

### Prepojenia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ConDoc | Str12 | 13 | Číslo dokladu čerpania zálohy (OF/ER) |
| VatDoc | Str12 | 13 | Číslo daňového dokladu príjmu zálohy (DZ) |
| PayDoc | Str12 | 13 | Číslo dokladu úhrady |
| PayDate | DateType | 4 | Dátum poslednej úhrady zálohy |

### Forma platby

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PayMode | Str1 | 2 | Forma zaplatenia (H/K/B) |
| RspName | Str30 | 31 | Meno používateľa, ktorý vystavil doklad |

### Medzifiremný prenos

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PamCode | longint | 4 | Kód firmy pri medzifiremnom prenose |

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

## Indexy (10)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | SerNum | SerNum | Duplicit |
| 1 | IncNum | IncNum | Duplicit |
| 2 | ExpNum | ExpNum | Duplicit |
| 3 | DocNum | DocNum | Duplicit |
| 4 | DocDate | DocDate | Duplicit |
| 5 | _Describe | Describe | Duplicit, Case-insensitive |
| 6 | PayMode | PayMode | Duplicit |
| 7 | ConDoc | ConDoc | Duplicit |
| 8 | VatDoc | VatDoc | Duplicit |
| 9 | PayDoc | PayDoc | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| ConDoc | ICH.DocNum | Faktúra na ktorú sa čerpá |
| VatDoc | SPV.DocNum | Daňový doklad zálohy |

## Formy platby (PayMode)

| Hodnota | Popis |
|---------|-------|
| H | Hotovosť |
| K | Kreditná karta |
| B | Bankový prevod |

## Typy dokladov

| DocVal | Typ | Popis |
|--------|-----|-------|
| > 0 | Príjem | Prijatá záloha |
| < 0 | Výdaj | Čerpanie zálohy |

## Použitie

- Evidencia pohybov na zálohovom účte
- Prepojenie na daňové doklady
- Sledovanie kumulatívnych zostatkov

## Business pravidlá

- Jeden súbor na partnera (PaCode v názve súboru)
- DocVal > 0 = príjem zálohy (IncNum sa zvyšuje)
- DocVal < 0 = čerpanie zálohy (ExpNum sa zvyšuje)
- EndVal = IncVal + ExpVal (ExpVal je záporné)
- VatDoc obsahuje číslo daňového dokladu k zálohe
- ConDoc obsahuje číslo faktúry pri čerpaní

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
