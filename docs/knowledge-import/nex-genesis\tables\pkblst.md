# PKBLST - Zoznam kníh prebalenia tovaru

## Kľúčové slová / Aliases

PKBLST, PKBLST.BTR, zoznam, kníh, prebalenia, tovaru

## Popis

Konfiguračná tabuľka kníh prebaľovacích dokladov. Definuje sklad, predvolené skladové pohyby a nastavenia pre každú knihu prebalenia.

## Btrieve súbor

`PKBLST.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\PKBLST.BTR`

## Štruktúra polí (18 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| BookNum | Str5 | 6 | Číslo knihy dokladov - **PRIMARY KEY** |
| BookName | Str30 | 31 | Názov knihy dokladov |
| BookYear | Str4 | 5 | Rok založenia knihy |
| SerNum | word | 2 | Poradové číslo knihy |

### Nastavenie skladu

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| StkNum | longint | 4 | Číslo skladu pre prebalenie |
| PlsNum | longint | 4 | Číslo cenníka |

### Skladové pohyby

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ScSmCode | word | 2 | Kód skladového pohybu výdaja |
| TgSmCode | word | 2 | Kód skladového pohybu príjmu |

### Zdieľanie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Shared | byte | 1 | Príznak zdieľania cez FTP (1=zdieľaný) |

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
| StkNum | STKLST.StkNum | Sklad |
| ScSmCode | STMLST.SmCode | Skladový pohyb výdaja |
| TgSmCode | STMLST.SmCode | Skladový pohyb príjmu |
| PlsNum | PLSLST.PlsNum | Cenník |

## Použitie

- Konfigurácia kníh prebalenia
- Predvolený sklad a skladové pohyby
- Nastavenie cenníka

## Business pravidlá

- Jedna kniha = jeden sklad pre prebalenie
- ScSmCode a TgSmCode sa dedia do nových dokladov
- Shared=1 aktivuje FTP synchronizáciu

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
