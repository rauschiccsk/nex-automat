# IMPDEF - Definícia parametrov importu

## Kľúčové slová / Aliases

IMPDEF, IMPDEF.BTR, definícia, parametrov, importu

## Popis

Konfiguračná tabuľka pre definíciu parametrov importu. Ukladá nastavenia pre rôzne typy importov vo formáte sekcia-parameter-hodnota.

## Btrieve súbor

`IMPDEF.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\IMPDEF.BTR`

## Štruktúra polí (11 polí)

### Konfigurácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| SectionName | Str50 | 51 | Názov sekcie |
| IdentName | Str50 | 51 | Názov parametra |
| KeyValue | Str60 | 61 | Hodnota parametra |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |

## Indexy (2)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | SectionName, IdentName | SnIn | Duplicit |
| 1 | SectionName | SectionName | Duplicit |

## Príklad štruktúry

| SectionName | IdentName | KeyValue |
|-------------|-----------|----------|
| CSV_IMPORT | Delimiter | ; |
| CSV_IMPORT | Encoding | UTF-8 |
| CSV_IMPORT | SkipHeader | 1 |
| EDI_IMPORT | MessageType | DESADV |
| WEIGHT_IMPORT | DeviceType | METTLER |

## Použitie

- Konfigurácia CSV importu (oddeľovač, kódovanie)
- Nastavenia EDI importu
- Parametre importu z váh
- Mapovanie polí pri importe

## Business pravidlá

- Štruktúra podobná INI súborom
- Sekcia zoskupuje súvisiace parametre
- Umožňuje flexibilnú konfiguráciu bez zmeny kódu

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
