# PQBLST - Zoznam kníh prevodných príkazov

## Kľúčové slová / Aliases

PQBLST, PQBLST.BTR, zoznam, kníh, prevodných, príkazov

## Popis

Konfiguračná tabuľka kníh prevodných príkazov. Každá kniha je prepojená s jedným bankovým účtom a obsahuje nastavenia pre elektronické bankovníctvo.

## Btrieve súbor

`PQBLST.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\PQBLST.BTR`

## Štruktúra polí (22 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| BookNum | Str5 | 6 | Číslo knihy prevodných príkazov - **PRIMARY KEY** |
| BookName | Str20 | 21 | Názov knihy prevodných príkazov |
| SerNum | word | 2 | Posledné poradové číslo |

### Bankové spojenie platiteľa

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ContoNum | Str20 | 21 | Číslo bankového účtu |
| BankCode | Str4 | 5 | Numerický smerovací kód banky |
| BankName | Str15 | 16 | Názov peňažného ústavu |
| SeatName | Str20 | 21 | Sídlo banky |
| IbanCode | Str34 | 35 | IBAN kód bankového účtu |
| SwftCode | Str20 | 21 | SWIFT kód banky |
| DvzName | Str3 | 4 | Mena účtu |

### Elektronické bankovníctvo

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| AboType | byte | 1 | Typ ABO (0=žiadny, 1=OTP, 2=SLSP, 3=VUB, 4=Sberbank, 5=UniCredit) |
| AboPath | Str80 | 81 | Adresár pre export elektronických výpisov |

### Štatistiky

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocQnt | longint | 4 | Počet dokladov - prevodných príkazov |

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

## Indexy (2)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | BookNum | BookNum | Duplicit |
| 1 | SerNum | SerNum | Duplicit |

## Typy elektronického bankovníctva (AboType)

| Hodnota | Banka | Formát exportu |
|---------|-------|----------------|
| 0 | Žiadne | - |
| 1 | OTP Banka | OTP ABO |
| 2 | Slovenská sporiteľňa | SLSP formát |
| 3 | VÚB | VUB formát |
| 4 | Sberbank | Sberbank formát |
| 5 | UniCredit | UniCredit formát |

## Použitie

- Konfigurácia bankových účtov pre platby
- Nastavenie elektronického bankovníctva
- Správa číselných radov
- Prepojenie s modulom BSM (výpisy)

## Business pravidlá

- Jedna kniha = jeden bankový účet
- AboType určuje formát exportného súboru
- AboPath je cieľový adresár pre súbory
- IbanCode/SwftCode pre SEPA platby
- Kniha PQB zdieľa definíciu s BSM (SOB knihy)

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
