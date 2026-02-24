# TPC - Evidencia terminovaných cien

## Popis modulu

Modul pre správu terminovaných (plánovaných) cien. Umožňuje definovať budúce zmeny predajných cien s presným dátumom a časom začiatku a konca platnosti. Slúži na plánovanie cenových zmien pred ich aktiváciou v pokladniach.

## Hlavný súbor

`NexModules\Tpc_F.pas`

## Tabuľky modulu

| Tabuľka | Súbor | Popis | Polí | Indexov |
|---------|-------|-------|------|---------|
| TPC | TPCnnnnn.BTR | Položky terminovaných cien | 21 | 5 |

**Celkom: 1 tabuľka, 21 polí, 5 indexov**

## Sub-moduly (2)

### Editácia
| Súbor | Popis |
|-------|-------|
| Tpc_ItmEdi_F.pas | Editor položky terminovanej ceny |

### Nástroje
| Súbor | Popis |
|-------|-------|
| Tpc_CasSnd_F.pas | Odoslanie údajov do pokladní |

## Prístupové práva

Modul TPC používa štandardný mechanizmus kníh cez BOKLST:
- `gBok.BokName('TPC', BookNum)` - názov knihy
- `gBok.BokFirst('TPC')` - prvá kniha modulu

## Kľúčové vlastnosti

### Časové plánovanie
- **BegDate / BegTime** = dátum a čas začiatku platnosti ceny
- **EndDate / EndTime** = dátum a čas ukončenia platnosti ceny
- Terminovaná cena sa aktivuje automaticky v pokladni podľa BegDate/BegTime

### Cenové údaje
- **APrice** = terminovaná predajná cena bez DPH
- **BPrice** = terminovaná predajná cena s DPH
- **VatPrc** = sadzba DPH v %
- Vzťah: `APrice = BPrice / (1 + VatPrc/100)`

### Stavy položky (Status)
- **(prázdny)** = aktívna terminovaná cena
- **D** = zrušená položka

### Synchronizácia s pokladňami
- **SndNum** = číslo odoslania do pokladní
- Export do súboru `TPCnnnnn.REF` vo formáte CSV (oddeľovač `;`)

## Integrácie

| Závislosť | Popis |
|-----------|-------|
| GSCAT | Katalóg produktov (zdrojové údaje o tovare) |
| PLS | Predajný cenník (aktuálne ceny) |
| BARCODE | Čiarové kódy |
| CABLST | Zoznam pokladní (pre export) |
| BOKLST | Zoznam kníh modulu |

## Rozdiel TPC vs PLS vs APL

| Vlastnosť | TPC (Terminované) | PLS (Predajné) | APL (Akciové) |
|-----------|-------------------|----------------|---------------|
| Účel | Plánovaná zmena ceny | Aktuálna cena | Promocionálna cena |
| Časové obmedzenie | BegDate-EndDate | Nie | BegDate-EndDate |
| Aktivácia | Automatická podľa dátumu | Okamžitá | Podľa pravidiel akcie |
| Periodicita | Nie | Nie | Áno (dni v týždni) |
| Minimálne množstvo | Nie | Nie | Áno (MinQnt) |
| Cenové hladiny | Nie | D1, D2, D3 | Nie |

## Workflow

```
1. Plánovanie zmeny ceny
   ┌─────────────────────────────────────────────────────────────┐
   │ TPC: BegDate=15.2.2025, BPrice=5.99 EUR (teraz: 4.99 EUR) │
   └─────────────────────────────────────────────────────────────┘
                            │
                            ▼
2. Export do pokladní (Tpc_CasSnd_F)
   ┌─────────────────────────────────────────────────────────────┐
   │ TPCnnnnn.REF → CasPath pre každú pokladňu                  │
   └─────────────────────────────────────────────────────────────┘
                            │
                            ▼
3. Aktivácia v pokladni (automaticky 15.2.2025)
   ┌─────────────────────────────────────────────────────────────┐
   │ Pokladňa použije BPrice=5.99 EUR od BegDate/BegTime        │
   └─────────────────────────────────────────────────────────────┘
```

## Export formát

CSV súbor s oddeľovačom `;`:
```
GsCode;GsName;BarCode;BegDate;BegTime;EndDate;EndTime;VatPrc;APrice;BPrice;SndNum
12345;Tovar ABC;8590001234;15.02.2025;08:00;31.12.2025;23:59;20;4.99;5.99;1
```

## Business pravidlá

- Položka so Status='D' nie je editovateľná
- Pri ukladaní sa APrice vypočíta z BPrice a VatPrc
- Pri výbere tovaru sa načítajú údaje z GSCAT a PLS (aktuálna cena)
- Export prebieha do všetkých pokladní v CABLST
- Súbor sa najprv uloží ako .TMP, potom premenuje na .REF

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
