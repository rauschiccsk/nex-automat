# PLSADD - Rozširujúce údaje cenníka

## Kľúčové slová / Aliases

PLSADD, PLSADD.BTR, rozširujúce, údaje, cenníka

## Popis

Rozširujúce údaje položiek predajného cenníka. Obsahuje nastavenia, ktoré sa nezmestili do hlavnej tabuľky PLS, napríklad fixované cenové hladiny.

## Btrieve súbor

`PLSADD.BTR`

## Umiestnenie

`C:\NEX\YEARACT\STK\PLSADD.BTR`

## Štruktúra polí (5 polí)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PlsNum | word | 2 | Poradové číslo predajného cenníka |
| GsCode | longint | 4 | Tovarové číslo (PLU) |
| FixLevel | byte | 1 | Fixované cenové hladiny (bitová maska) |

## Indexy (3)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | PlsNum, GsCode | PnGc | Duplicit |
| 1 | PlsNum | PlsNum | Duplicit |
| 2 | GsCode | GsCode | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| PlsNum | PLSLST.PlsNum | Cenník |
| GsCode | PLS.GsCode | Položka cenníka |

## FixLevel bitová maska

| Bit | Hodnota | Cenová hladina |
|-----|---------|----------------|
| 0 | 1 | D1 (BPrice1) |
| 1 | 2 | D2 (BPrice2) |
| 2 | 4 | D3 (BPrice3) |
| 3 | 8 | Rezervované |

### Príklady FixLevel

| FixLevel | Fixované hladiny |
|----------|------------------|
| 0 | Žiadna (všetky sa prepočítavajú) |
| 1 | Len D1 |
| 3 | D1 + D2 |
| 7 | D1 + D2 + D3 |

## Použitie

- Nastavenie fixovaných cenových hladín
- Kontrola prepočtu cien
- Rozšírené nastavenia položiek

## Business pravidlá

- FixLevel určuje, ktoré cenové hladiny nepodliehajú prepočtu
- Ak bit je nastavený (1), hladina sa NEprepočítava
- Prepočet cenových hladín (Pls_LevClc_F) ignoruje fixované hladiny
- Štandardne FixLevel=0 (všetky hladiny sa prepočítavajú)

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
