# APMDEF - Prístup k programovým modulom

## Kľúčové slová / Aliases

APMDEF, APMDEF.BTR, práva modulov, module permissions, oprávnenia, prístup

## Popis

Tabuľka definujúca prístup skupín používateľov k jednotlivým programovým modulom. Určuje ktoré moduly sú dostupné pre danú skupinu práv. Globálny súbor.

## Btrieve súbor

`APMDEF.BTR`

## Umiestnenie

`C:\NEX\SYSTEM\APMDEF.BTR`

## Štruktúra polí (5 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| GrpNum | word | 2 | Číslo skupiny práv |
| PmdMark | Str6 | 7 | Typové označenie programového modulu |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ModUser | Str8 | 9 | Používateľ poslednej zmeny |
| ModDate | DateType | 4 | Dátum poslednej zmeny |
| ModTime | TimeType | 4 | Čas poslednej zmeny |

## Indexy (2)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | GrpNum | GrpNum | Duplicit |
| 1 | GrpNum, PmdMark | GrPm | Unikátny |

## Programové moduly (PmdMark)

### Bázová evidencia

| Kód | Modul | Popis |
|-----|-------|-------|
| GSC | cGsc | Evidencia tovaru |
| PAB | cPab | Evidencia partnerov |
| WGH | cWgh | Elektronické váhy |

### Obchodná činnosť

| Kód | Modul | Popis |
|-----|-------|-------|
| PLS | cPls | Tvorba predajných cien |
| APL | cApl | Akciové ceny |
| TPC | cTpc | Terminované ceny |
| ACB | cAcb | Akciové precenenie |
| BCI | cBci | Obchodné podmienky |
| CRD | cCrd | Zákaznícke karty |
| AGL | cAgl | Zmluvné podmienky |

### Zásobovanie

| Kód | Modul | Popis |
|-----|-------|-------|
| PSB | cPsb | Plánovanie objednávok |
| OSB | cOsb | Dodávateľské objednávky |
| TSB | cTsb | Dodacie listy dodávateľov |
| KSB | cKsb | Komisionálne vyúčtovanie |
| BSB | cBsb | Obchodné podmienky dodávok |
| TIB | cTim | Terminálové príjemky |

### Sklad

| Kód | Modul | Popis |
|-----|-------|-------|
| STK | cStk | Skladové karty |
| IMB | cImb | Príjemky |
| OMB | cOmb | Výdajky |
| RMB | cRmb | Medziskladové presuny |
| CPB | cCpb | Kalkulácie |
| CMB | cCmb | Kompletizácia |
| DMB | cDmb | Rozoberanie |
| IVB | cIvd | Inventarizácia |

### Odbyt

| Kód | Modul | Popis |
|-----|-------|-------|
| UDB | cUdb | Univerzálne doklady |
| MCB | cMcb | Cenové ponuky |
| OCB | cOcb | Zákazky |
| TCB | cTcb | Dodacie listy |
| ICB | cIcb | Faktúry |
| SCB | cScb | Servisné zákazky |

### Registračné pokladnice

| Kód | Modul | Popis |
|-----|-------|-------|
| CAB | cCab | Knihy pokladníc |
| SAB | cSab | Skladové výdajky MO |
| CAI | cCai | Informácie predaja |
| CAC | cCac | Výkaz uzávierok |

### Účtovníctvo

| Kód | Modul | Popis |
|-----|-------|-------|
| JRN | cJrn | Denník účtovných zápisov |
| ACT | cAct | Obratová predvaha |
| IDB | cIdb | Interné doklady |
| ISB | cIsb | Dodávateľské faktúry |
| CSB | cCsb | Hotovostné pokladne |
| SOB | cSob | Bankové výpisy |
| VTR | cVtb | Evidencia DPH |

### Systém

| Kód | Modul | Popis |
|-----|-------|-------|
| SYS | cSys | Systémové nastavenia |
| USD | cUsr | Evidencia používateľov |
| DBS | cDbs | Údržba databáz |
| KEY | cKey | Riadiace parametre |

## Príklad

```
Skupina 2: Účtovníctvo
─────────────────────────────────────────────────────────────────
GrpNum = 2, PmdMark = "GSC"   (Evidencia tovaru - read only)
GrpNum = 2, PmdMark = "PAB"   (Evidencia partnerov)
GrpNum = 2, PmdMark = "ISB"   (Dodávateľské faktúry)
GrpNum = 2, PmdMark = "CSB"   (Hotovostné pokladne)
GrpNum = 2, PmdMark = "SOB"   (Bankové výpisy)
GrpNum = 2, PmdMark = "JRN"   (Denník účtovných zápisov)
GrpNum = 2, PmdMark = "ACT"   (Obratová predvaha)
```

## Algoritmus kontroly práv

```pascal
function TNexRight.Enabled(pModul: byte): boolean;
begin
  Result := FALSE;
  // 1. Kontrola licencie
  If LicModEnabled(GetPmdMark(pModul)) then begin
    // 2. Kontrola skupiny (0 = admin má všetko)
    If gvSys.LoginGroup = 0 then
      Result := TRUE
    else
      // 3. Hľadanie v APMDEF
      Result := ohAPMDEF.LocateGrPm(gvSys.LoginGroup, GetPmdMark(pModul));
  end;
end;
```

## Použitie

- Nastavenie viditeľnosti položiek menu
- Kontrola pri spustení modulu
- Konfigurácia prístupov skupín
- Audit zmien oprávnení

## Business pravidlá

- GrpNum = 0 znamená administrátorskú skupinu (všetky práva)
- Záznam existuje = skupina má prístup k modulu
- Neexistencia záznamu = skupina nemá prístup
- Zmeny auditované cez ModUser/ModDate/ModTime
- Musí existovať aj licencia pre daný modul

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
