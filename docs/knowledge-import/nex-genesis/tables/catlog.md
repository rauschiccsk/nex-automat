# CATLOG - Evidencia prenosov do ERP

## Kľúčové slová / Aliases

CATLOG, CATLOG.BTR, evidencia, prenosov, erp

## Popis

Tabuľka evidencie prenosov údajov do elektronických registračných pokladníc. Sleduje odoslanie a prijatie dát až pre 20 pokladníc. Globálny súbor.

## Btrieve súbor

`CATLOG.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DATA\CATLOG.BTR`

## Štruktúra polí (70 polí)

### Identifikácia prenosu

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| SndType | Str1 | 2 | Typ prenosu (P/A/T/K) |
| SndNum | word | 2 | Číslo prenosu daného typu |
| SndDate | DateType | 4 | Dátum vyhotovenia prenosu |
| SndTime | TimeType | 4 | Čas vyhotovenia prenosu |

### Stav prijatia (pre 20 pokladníc, XX=01-20)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| RcvDaXX | DateType | 4 | Dátum prijatia pokladňou XX |
| RcvTiXX | TimeType | 4 | Čas prijatia pokladňou XX |
| RcvStXX | Str1 | 2 | Stav prijatia pokladňou XX |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |

## Indexy (2)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | SndType, SndNum | StSn | Unikátny |
| 1 | SndDate | SndDate | Duplicit |

## Typy prenosov (SndType)

| Hodnota | Popis |
|---------|-------|
| P | Predajné ceny (PLS) |
| A | Akciové ceny (APL) |
| T | Terminované ceny |
| K | Zákaznícke karty (CRD) |

## Stavy prijatia (RcvStXX)

| Hodnota | Popis |
|---------|-------|
| (prázdne) | Neodoslané / Čaká |
| O | Prijaté (OK) |
| E | Chyba prenosu |

## Príklad

```
SndType = "P" (predajné ceny)
SndNum  = 125
SndDate = 15.01.2024
SndTime = 08:00:00
─────────────────────────────────────────────────────────────────
Pokladňa 01:
  RcvDa01 = 15.01.2024
  RcvTi01 = 08:05:32
  RcvSt01 = "O" (prijaté)

Pokladňa 02:
  RcvDa02 = 15.01.2024
  RcvTi02 = 08:07:15
  RcvSt02 = "O" (prijaté)

Pokladňa 03:
  RcvDa03 = (prázdne)
  RcvTi03 = (prázdne)
  RcvSt03 = (prázdne) - ešte neprijaté
```

## Workflow

```
1. Zmena cien v PLS / APL
   ↓
2. Generovanie prenosového súboru
   - SndDate, SndTime = teraz
   - SndNum = poradové číslo
   ↓
3. Distribúcia na pokladne
   ↓
4. Pokladňa prijme údaje
   - RcvDaXX, RcvTiXX = čas prijatia
   - RcvStXX = "O"
   ↓
5. Kontrola stavu všetkých pokladníc
```

## Použitie

- Sledovanie distribúcie cien na pokladne
- Kontrola prijatia aktualizácií
- Diagnostika problémov s prenosom
- Audit zmien cien

## Business pravidlá

- Maximálne 20 pokladníc (01-20)
- Prenos sa považuje za dokončený keď všetky pokladne majú RcvSt="O"
- Pri chybe (RcvSt="E") je potrebný manuálny zásah
- Typy P, A, T, K majú samostatné číslovanie (SndNum)

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
