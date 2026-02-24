# PANOTI - Poznámky k partnerom

## Kľúčové slová / Aliases

PANOTI, PANOTI.BTR, poznámky k partnerom, partner notes, interné poznámky

## Popis

Tabuľka poznámkových riadkov evidenčnej karty obchodných partnerov. Umožňuje ukladať dlhé textové poznámky rozdelené do riadkov.

## Btrieve súbor

`PANOTI.BTR`

## Umiestnenie

`C:\NEX\YEARACT\FIRMS\PANOTI.BTR`

## Polia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PaCode | longint | 4 | Číselný kód partnera - **FK → PAB** |
| LinNum | word | 2 | Poradové číslo poznámkového riadku |
| Notice | Str250 | 251 | Text poznámky |

## Indexy

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | PaCode, LinNum | PaLn | Duplicit (Composite PK) |
| 1 | PaCode | PaCode | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| PaCode | PAB.PaCode | Partner |

## Business pravidlá

- Partner môže mať viac poznámkových riadkov
- Composite PK: (PaCode, LinNum)
- LinNum je sekvenčné (1, 2, 3, ...)
- Maximálna dĺžka jedného riadku je 250 znakov
- Pre dlhšie poznámky sa použije viac riadkov

## Príklad použitia

| PaCode | LinNum | Notice |
|--------|--------|--------|
| 1001 | 1 | Preferovaný dodávateľ kancelárskych potrieb. |
| 1001 | 2 | Kontakt: Ing. Novák, tel. 02/1234567 |
| 1001 | 3 | Pozor: Vyžaduje platbu vopred pri prvých 3 objednávkach. |

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model (TEXT pole namiesto riadkov)
- [ ] API endpoint
