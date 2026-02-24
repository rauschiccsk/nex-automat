# OCPDEF - Definície spracovania zákaziek

## Kľúčové slová / Aliases

OCPDEF, OCPDEF.BTR, predvolby objednávok, order defaults, šablóny

## Popis

Konfiguračná tabuľka definujúca spôsoby spracovania odberateľských zákaziek. Umožňuje preddefinovať kombinácie nastavení pre rôzne typy zákaziek.

## Btrieve súbor

`OCPDEF.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\OCPDEF.BTR`

## Štruktúra polí (4 polia)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DefNum | word | 2 | Číslo definície - **PRIMARY KEY** |
| DefName | Str30 | 31 | Názov definície |
| DefCode | Str10 | 11 | Kód definície |
| DefData | Text | var | Konfiguračné dáta (JSON/Binary) |

## Indexy (1)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | DefNum | DefNum | Unique |

## Obsah DefData

Konfiguračné dáta môžu obsahovať:

```
- AutoReserve: boolean     - automatická rezervácia
- AutoExpedition: boolean  - automatická expedícia
- RequireDeposit: boolean  - vyžadovať zálohu
- DepositPercent: double   - percento zálohy
- DefaultBook: word        - predvolená kniha
- DefaultWarehouse: word   - predvolený sklad
- GenerateTCD: boolean     - automaticky generovať DL
- GenerateICD: boolean     - automaticky generovať faktúru
- SendEmail: boolean       - odoslať email pri vytvorení
- EmailTemplate: string    - šablóna emailu
```

## Príklady definícií

| DefNum | DefName | Popis |
|--------|---------|-------|
| 1 | Štandardná | Bežná zákazka bez špeciálnych nastavení |
| 2 | E-shop | Automatická expedícia, email zákazníkovi |
| 3 | Veľkoobchod | Bez zálohy, odložená splatnosť |
| 4 | Cash&Carry | Okamžitá platba, ihneď expedícia |
| 5 | Záloha 50% | Vyžaduje 50% zálohu pred expedíciou |

## Použitie

- Rýchle nastavenie typu zákazky
- Štandardizácia procesov
- Redukcia chýb pri manuálnom nastavovaní
- Integrácia s e-shopom

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
