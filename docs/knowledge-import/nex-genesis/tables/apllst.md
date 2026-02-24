# APLLST - Zoznam akciových cenníkov

## Kľúčové slová / Aliases

APLLST, APLLST.BTR, zoznam aplikácií, application list, moduly

## Popis

Konfiguračná tabuľka akciových cenníkov. Každý akciový cenník je prepojený s predajným cenníkom a obsahuje položky s časovo obmedzenými akciovými cenami.

## Btrieve súbor

`APLLST.BTR`

## Umiestnenie

`C:\NEX\YEARACT\STK\APLLST.BTR`

## Štruktúra polí (16 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| AplNum | word | 2 | Poradové číslo akciového cenníka - **PRIMARY KEY** |
| AplName | Str30 | 31 | Názov akciového cenníka |
| PlsNum | word | 2 | Číslo pripojeného predajného cenníka |

### Štatistiky

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ItmQnt | longint | 4 | Počet položiek v akciovom cenníku |
| Notice | Str60 | 61 | Textový popis - poznámka |

### Nastavenie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Delete | byte | 1 | Povolenie zrušiť cenník (0/1) |
| Shared | byte | 1 | Zdieľanie cez FTP (1=zdieľaný) |

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
| 0 | AplNum | AplNum | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| PlsNum | PLSLST.PlsNum | Predajný cenník |

## Použitie

- Správa akciových cenníkov
- Prepojenie s predajnými cenníkmi
- Štatistiky počtu akciových položiek

## Business pravidlá

- Jeden akciový cenník = jeden predajný cenník
- Delete=1 je potrebné pre zmazanie cenníka
- ItmQnt sa aktualizuje pri pridávaní/mazaní položiek
- Shared=1 aktivuje FTP synchronizáciu

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
