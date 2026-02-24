# BSM - Bankové výpisy

## Popis modulu

Modul pre správu bankových výpisov. Eviduje bezhotovostné platby, príkazy na úhradu, elektronické bankovníctvo (SEPA, SLSP), úhrady faktúr, duálne meny (mena účtu a účtovná mena), denník úhrad faktúr a katalóg bankových operácií.

## Hlavný súbor

`NexModules\Bsm_F.pas`

## Tabuľky modulu

| Tabuľka | Súbor | Popis | Polí | Indexov |
|---------|-------|-------|------|---------|
| BSMDOC | BSMDOC.BTR | Hlavičky bankových výpisov | 29 | 9 |
| BSMITM | BSMITM.BTR | Položky bankových výpisov | 46 | 9 |
| BSMCAT | BSMCAT.BTR | Katalóg bankových operácií | 20 | 5 |
| PAYJRN | PAYJRN.BTR | Denník úhrad faktúr | 38 | 9 |

**Celkom: 4 tabuľky, 133 polí, 32 indexov**

## Sub-moduly (19)

### Editácia
| Súbor | Popis |
|-------|-------|
| Bsm_DocEdi.pas | Formulár hlavičky bankového výpisu |
| Bsm_ItmEdi.pas | Editor položky výpisu |
| Bsm_ItmLst.pas | Položky vybraného výpisu |
| Bsm_DocDel.pas | Formulár na zrušenie dokladu |

### Súhrnné platby
| Súbor | Popis |
|-------|-------|
| Bsm_CitLst.pas | Zoznam súhrnných platieb |
| Bsm_CitImp.pas | Import súhrnných platieb |
| Bsm_CitDel.pas | Zmazanie súhrnnej platby |

### Elektronické bankovníctvo
| Súbor | Popis |
|-------|-------|
| Bsm_EbaSep.pas | Elektronické bankovníctvo - SEPA |
| Bsm_EbaSls.pas | Elektronické bankovníctvo - SLSP |

### Katalóg operácií
| Súbor | Popis |
|-------|-------|
| Bsm_CatEdi.pas | Editor katalógu operácií |
| Bsm_CatSlc.pas | Výber z katalógu operácií |

### Účtovanie
| Súbor | Popis |
|-------|-------|
| Bsm_DocAcc.pas | Zaúčtovanie vybraného výpisu |
| Bsm_BokAcc.pas | Zaúčtovanie všetkých výpisov |
| Bsm_DocClc.pas | Prepočet vybraného výpisu |
| Bsm_BokClc.pas | Prepočet všetkých výpisov |

### Výkazy a tlač
| Súbor | Popis |
|-------|-------|
| Bsm_PayMov.pas | Výkaz pohybov za obdobie |
| Bsm_PayDet.pas | Detail platby |
| Bsm_InvLst.pas | Zoznam faktúr |

## Prístupové práva

Modul BSM nepoužíva samostatný súbor Usd_AfcBsm.pas. Prístupové práva sú spravované cez štandardný mechanizmus kníh (BokLst) a všeobecné nastavenia programu.

## Kľúčové vlastnosti

### Dual Currency Pattern
- **PayXxx** = hodnoty v mene bankového účtu
- **AccXxx** = hodnoty v účtovnej mene
- PayCrs = kurz pre prepočet

### Farebné rozlíšenie dokladov
- **oClrEmp** - Prázdny bankový výpis (bez položiek)
- **oClrErr** - Nedokončený výpis (DstDif='!')
- **oClrNac** - Nezaúčtovaný výpis (DstAcc='')
- **oClrAcc** - Zaúčtovaný výpis (DstAcc='A')

### Document State Flags
- **DstLck** = 'L' - uzamknutý doklad
- **DstDif** = '!' - rozdiel konečného stavu
- **DstAcc** = 'A' - zaúčtovaný doklad

### Integrácie
- ISB (Dodávateľské faktúry) - úhrady
- ICB (Odberateľské faktúry) - úhrady
- PAB (Katalóg partnerov) - ParNum
- JRN (Účtovný denník) - zaúčtovanie
- BOK (Knihy) - správa bankových kníh

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
