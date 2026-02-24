# OSSMOV - Skladové pohyby pre objednávky

## Kľúčové slová / Aliases

OSSMOV, OSSMOV.BTR, pohyby skladov objednávok, PO stock movements

## Popis

Konfiguračná tabuľka skladových pohybov, ktoré sa započítavajú do výpočtu objednávok. Definuje, ktoré typy výdajov sa majú zohľadniť pri automatickom generovaní objednávok.

## Btrieve súbor

`OSSMOV.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\OSSMOV.BTR`

## Štruktúra polí (10 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| SmCode | longint | 4 | Kód skladového pohybu - **PRIMARY KEY** |
| SmName | Str30 | 31 | Názov skladového pohybu |
| _SmName | Str30 | 31 | Vyhľadávacie pole |

### Synchronizácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Sended | byte | 1 | Príznak odoslania zmien |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ModNum | word | 2 | Poradové číslo zmeny |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |

## Indexy (3)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | SmCode | SmCode | Duplicit |
| 1 | _SmName | SmName | Duplicit, Case insensitive |
| 2 | Sended | Sended | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| SmCode | SMLST.SmCode | Definícia skladového pohybu |

## Príklad použitia

| SmCode | SmName | Započítať |
|--------|--------|-----------|
| 10 | Predaj VO | Áno |
| 11 | Predaj MO | Áno |
| 20 | Výdaj na spotrebu | Áno |
| 30 | Inventúrny rozdiel - | Nie |
| 40 | Presun medzi skladmi | Nie |

## Workflow

```
1. Definícia skladových pohybov v OSSMOV
   ↓
2. Pri výpočte objednávacieho množstva:
   - Načítanie výdajov za sledované obdobie
   - Filtrovanie podľa OSSMOV.SmCode
   - Výpočet priemerného výdaja
   ↓
3. Porovnanie s aktuálnou zásobou
   ↓
4. Generovanie návrhu objednávky
```

## Použitie

- Konfigurácia výpočtu objednávacieho množstva
- Vylúčenie mimoriadnych pohybov z výpočtu
- Presné plánovanie nákupu

## Business pravidlá

- Len pohyby evidované v tejto tabuľke sa započítavajú do priemeru
- Umožňuje vylúčiť mimoriadne výdaje (inventúrne rozdiely, škody)
- Zohľadňuje len relevantné obchodné výdaje

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
