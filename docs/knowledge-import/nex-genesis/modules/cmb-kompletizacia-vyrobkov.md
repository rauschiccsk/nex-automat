# CMB - Kompletizácia výrobkov

## Popis modulu

Modul pre správu kompletizačných dokladov. Umožňuje montáž/výrobu hotových výrobkov z komponentov podľa receptúr (BOM). Sleduje spotrebu materiálu, práce a vytvára skladové pohyby pre príjem hotového výrobku a výdaj komponentov.

## Hlavný súbor

`NexModules\Cmb_F.pas`

## Tabuľky modulu

| Tabuľka | Súbor | Popis | Polí | Indexov |
|---------|-------|-------|------|---------|
| CMH | CMHyynnn.BTR | Hlavičky kompletizačných dokladov | 34 | 10 |
| CMI | CMIyynnn.BTR | Položky kompletizačného dokladu | 29 | 5 |
| CMN | CMNyynnn.BTR | Poznámky ku kompletizačným dokladom | 4 | 2 |
| CMBLST | CMBLST.BTR | Zoznam kníh kompletizačných dokladov | 20 | 1 |
| CMHOLE | CMHOLE.BTR | Voľné poradové čísla | 5 | 1 |
| CMSPEC | CMSPEC.BTR | Špecifikácia výrobku (receptúra/BOM) | 9 | 1 |

**Celkom: 6 tabuliek, 101 polí, 20 indexov**

## Sub-moduly (10)

### Editácia
| Súbor | Popis |
|-------|-------|
| Cmb_CmhEdit_F.pas | Editor hlavičky kompletizačného dokladu |
| Cmb_CmiLst_F.pas | Zoznam položiek (komponentov) dokladu |

### Tlač
| Súbor | Popis |
|-------|-------|
| Cmb_DocPrn_F.pas | Tlač kompletizačného dokladu |
| Cmb_CmdPrn_F.pas | Tlač príkazu na kompletizáciu |

### Nástroje
| Súbor | Popis |
|-------|-------|
| Cmb_CmpDoc_F.pas | Kompletizácia dokladu (spracovanie) |
| Cmb_CmiToN_F.pas | Zmena položiek na neodpočítané |
| Cmb_StmCmi_F.pas | Skladové pohyby položiek |
| Cmb_StmCma_F.pas | Skladové pohyby agregované |
| Cmb_ItmRev_F.pas | Revízia položiek |

### Konfigurácia
| Súbor | Popis |
|-------|-------|
| Key_CmbEdi_F.pas | Nastavenie vlastností knihy |

## Prístupové práva

Modul CMB nepoužíva samostatný súbor Usd_AfcCmb.pas. Prístup je riadený cez štandardný mechanizmus gAfc.CMB.

## Kľúčové vlastnosti

### Výrobok a Komponenty Pattern
- **Pd*** = výrobok (Product) - hotový produkt, ktorý sa vyrába
- **Cm*** = komponent (Component) - materiál spotrebovaný pri výrobe

### Stavy dokladu
- **DstStk** = 'N' - pripravený (červená farba)
- **DstStk** = 'S' - naskladnený (dokončený)

### Stavy položiek
- **StkStat** = 'N' - zaevidované
- **StkStat** = 'S' - naskladnené (odpísané zo skladu)

### Typy položiek (ItmType)
- **C** = komponent (materiál)
- **W** = práca (work - náklady na prácu)

### Receptúra (CMSPEC)
- Definuje zloženie výrobku
- Normatívne množstvá komponentov na jednotku výrobku
- Používa sa pre automatické naplnenie položiek

## Integrácie

| Závislosť | Popis |
|-----------|-------|
| GSCAT | Katalóg produktov (výrobky aj komponenty) |
| BARCODE | Čiarové kódy produktov |
| STKLST | Zoznam skladov |
| STM | Skladové pohyby |
| BOK | Správa kníh |

## Business pravidlá

- Kompletizácia vytvára skladové pohyby: príjem výrobku + výdaj komponentov
- Hodnota výrobku = súčet hodnoty komponentov + práce
- CMSPEC definuje normatívnu spotrebu (môže sa líšiť od skutočnej)
- Doklad môže byť prepojený na zákazkový doklad
- DstStk='N' = zatiaľ nekompletizovaný (červená farba)

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
