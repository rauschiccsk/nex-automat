# PKB - Prebalenie tovaru

## Popis modulu

Modul pre správu prebaľovacích dokladov. Umožňuje transformáciu skladových položiek - prebalenie zdrojového tovaru na cieľový tovar s rôznymi koeficientmi. Používa sa pri rozbalovaní paliet, prepočte množstiev medzi mernými jednotkami a zmene balení.

## Hlavný súbor

`NexModules\Pkb_F.pas`

## Tabuľky modulu

| Tabuľka | Súbor | Popis | Polí | Indexov |
|---------|-------|-------|------|---------|
| PKH | PKHyynnn.BTR | Hlavičky prebaľovacích dokladov | 38 | 6 |
| PKI | PKIyynnn.BTR | Položky prebaľovacích dokladov | 47 | 15 |
| PKBLST | PKBLST.BTR | Zoznam kníh prebalenia | 18 | 1 |
| PKHOLE | PKHOLE.BTR | Voľné poradové čísla | 5 | 1 |
| PKCLST | PKCLST.BTR | Zoznam koeficientov prebalenia (predpisy) | 19 | 7 |

**Celkom: 5 tabuliek, 127 polí, 30 indexov**

## Sub-moduly (11)

### Editácia
| Súbor | Popis |
|-------|-------|
| Pkb_PkhEdit_F.pas | Editor hlavičky prebaľovacieho dokladu |
| Pkb_PkiEdit_F.pas | Editor položky dokladu |
| Pkb_PkiLst_F.pas | Zoznam položiek dokladu |

### Prebaľovacie predpisy
| Súbor | Popis |
|-------|-------|
| Pkb_PkcLst_V.pas | Prebaľovací predpis - pohľad |
| Pkb_PkcLst_F.pas | Prebaľovací predpis - formulár |

### Tlač
| Súbor | Popis |
|-------|-------|
| Pkb_DocPrn_F.pas | Tlač prebaľovacieho dokladu |

### Nástroje
| Súbor | Popis |
|-------|-------|
| Pkb_PckDoc_F.pas | Prebalenie položiek dokladu |
| Pkb_StmPki_F.pas | Skladové pohyby položiek |

### Servis
| Súbor | Popis |
|-------|-------|
| Pkb_PkiToN_F.pas | Zmena dokladov na neodpočítané |
| Pkb_PkiRef_F.pas | Obnova položiek podľa hlavičiek |

### Konfigurácia
| Súbor | Popis |
|-------|-------|
| Key_PkbEdi_F.pas | Nastavenie vlastností knihy |

## Prístupové práva (gAfc.PKB.*)

Modul používa štandardný prístupový mechanizmus cez gAfc.PKB s 255 úrovňami prístupov (gafc.PKB.WriteData).

## Kľúčové vlastnosti

### Zdroj a Cieľ Pattern
- **Sc*** = zdrojový tovar (Source) - tovar, ktorý sa prebaľuje
- **Tg*** = cieľový tovar (Target) - výsledný tovar po prebalení

### Stavy dokladu
- **DstStk** = 'N' - neprebalený (červená farba)
- **DstStk** = 'S' - prebalený
- **StkStat** = 'N'/'S' - stav položky

### Skladové pohyby
- **ScSmCode** - kód skladového pohybu výdaja (vydanie zdrojového tovaru)
- **TgSmCode** - kód skladového pohybu príjmu (príjem cieľového tovaru)

### Koeficienty prebalenia (PKCLST)
- **ScGsKfc** - koeficient zdrojového tovaru
- **TgGsKfc** - koeficient cieľového tovaru
- Príklad: 1 paleta (zdroj) = 100 kusov (cieľ)

## Integrácie

| Závislosť | Popis |
|-----------|-------|
| GSCAT | Katalóg produktov (zdrojový aj cieľový tovar) |
| BARCODE | Čiarové kódy produktov |
| STKLST | Zoznam skladov |
| STM | Skladové pohyby |
| BOK | Správa kníh |

## Business pravidlá

- Prebalenie vytvára dva skladové pohyby: výdaj zdroja + príjem cieľa
- InMov + OutMov = DifVal (hodnota rozdielu)
- Doklad môže byť prepojený na zákazkový doklad (OcdNum)
- Podporuje internetový prenos (SndStat, Sended)

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
