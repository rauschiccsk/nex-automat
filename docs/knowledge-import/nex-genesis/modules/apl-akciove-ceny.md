# APL - Evidencia akciových cien

## Popis modulu

Modul pre správu akciových (promocionálnych) cien. Umožňuje definovať časovo obmedzené cenové akcie s dátumom začiatku a konca, percentuálnu zľavu, periodicitu (dni v týždni), minimálne množstvo a synchronizáciu s pokladňami.

## Hlavný súbor

`NexModules\Apl_F.pas`

## Tabuľky modulu

| Tabuľka | Súbor | Popis | Polí | Indexov |
|---------|-------|-------|------|---------|
| APLLST | APLLST.BTR | Zoznam akciových cenníkov | 16 | 1 |
| APLITM | APLITM.BTR | Položky akciových cenníkov | 31 | 8 |
| APL | APLnnnnn.BTR | Zoznam akciových tovarov (legacy) | 18 | 4 |

**Celkom: 3 tabuľky, 65 polí, 13 indexov**

## Sub-moduly (6)

### Editácia
| Súbor | Popis |
|-------|-------|
| Apl_AplLst_F.pas | Vlastnosti akciového cenníka |
| Apl_AplItm_F.pas | Položka akciového cenníka |

### Nástroje
| Súbor | Popis |
|-------|-------|
| Apl_CasSnd_F.pas | Poslanie údajov do pokladne |
| Sys_ImpApl_F.pas | Import akciového cenníka |

### Údržba
| Súbor | Popis |
|-------|-------|
| Apl_EndDel_F.pas | Zrušenie neplatných akcií |

## Prístupové práva

Modul APL nepoužíva samostatný súbor Usd_AfcApl.pas. Servisné funkcie (A_DifClc) sú obmedzené cez `gRgh.Service`.

## Kľúčové vlastnosti

### Farebné rozlíšenie položiek
- **Červená** (clRed) - aktuálne prebiehajúca akcia (BegDate ≤ dnes ≤ EndDate)
- **Čierna** (clBlack) - neaktívna akcia

### Ceny v položke
- **PcAPrice / PcBPrice** = cenníková cena (pôvodná)
- **AcAPrice / AcBPrice** = akciová cena (zľavnená)
- **DifPrc** = percentuálny rozdiel = (1 - AcBPrice/PcBPrice) * 100

### Časové nastavenia
- **BegDate / EndDate** = dátumový interval akcie
- **BegTime / EndTime** = časový interval (ak TimeInt=1)
- **Period** = periodicita (7 znakov pre dni v týždni, napr. "1100011")
- **TimeInt** = 0=terminovaný čas počas obdobia, 1=časový interval

### Typy akcií (AcType)
- **V** = výpredaj
- (prázdny) = bežná akcia

## Integrácie

| Závislosť | Popis |
|-----------|-------|
| PLSLST | Zoznam predajných cenníkov (PlsNum) |
| PLS | Predajný cenník (zdrojové ceny) |
| GSCAT | Katalóg produktov |
| BARCODE | Čiarové kódy |
| Pokladne | Synchronizácia cez Apl_CasSnd_F |

## Business pravidlá

- DifPrc = (1 - AcBPrice/PcBPrice) * 100 (zľava v %)
- Akcia je aktívna ak: BegDate ≤ aktuálny dátum ≤ EndDate
- MinQnt definuje minimálne množstvo pre uplatnenie akcie
- Sended=0 po zmene, 1 po odoslaní do pokladne
- ScdNum prepája položku so zdrojovým dokladom

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
