# BKGRGHT - Prístupové práva kníh podľa skupín

## Kľúčové slová / Aliases

BKGRGHT, BKGRGHT.BTR, práva kníh, book rights, oprávnenia kníh

## Popis

Tabuľka definujúca prístupové práva k jednotlivým knihám (IMB, OMB, ICB, ...) podľa skupín používateľov. Umožňuje jemnú granularitu oprávnení na úrovni konkrétnych kníh. Globálny súbor.

## Btrieve súbor

`BKGRGHT.BTR`

## Umiestnenie

`C:\NEX\SYSTEM\BKGRGHT.BTR`

## Štruktúra polí (7 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| RghtGrp | word | 2 | Skupina prístupových práv |
| BookType | Str3 | 4 | Typové označenie knihy (IMB, OMB, ICB, ...) |
| BookNum | Str5 | 6 | Číslo knihy (00001, 00002, ...) |
| BookRight | Str30 | 31 | Reťazec prístupových práv |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ModUser | Str8 | 9 | Používateľ poslednej zmeny |
| ModDate | DateType | 4 | Dátum poslednej zmeny |
| ModTime | TimeType | 4 | Čas poslednej zmeny |

## Indexy (3)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | RghtGrp | RghtGrp | Duplicit |
| 1 | RghtGrp, BookType | RgBt | Duplicit |
| 2 | RghtGrp, BookType, BookNum | RgBtBn | Unikátny |

## Prístupové práva (BookRight)

| Znak | Právo | Popis |
|------|-------|-------|
| E | Enable | Vstup do knihy |
| I | Insert | Pridávanie nových záznamov |
| D | Delete | Mazanie záznamov |
| M | Modify | Úprava existujúcich záznamov |
| P | Print | Tlač zostáv a dokladov |
| V | Property | Nastavenie vlastností knihy |
| L | DocLock | Automatické uzatváranie dokladov po tlači |
| O | OwnOpen | Otvoriť vlastné uzatvorené doklady |
| A | AllOpen | Otvoriť všetky uzatvorené doklady |

## Typy kníh (BookType)

### Skladové knihy

| Typ | Popis |
|-----|-------|
| IMB | Príjemky |
| OMB | Výdajky |
| RMB | Medziskladové presuny |
| CPB | Kalkulácie |
| CMB | Kompletizácia |

### Odbytové knihy

| Typ | Popis |
|-----|-------|
| MCB | Cenové ponuky |
| OCB | Zákazky |
| TCB | Dodacie listy |
| ICB | Faktúry |
| SCB | Servisné zákazky |

### Účtovné knihy

| Typ | Popis |
|-----|-------|
| IDB | Interné doklady |
| ISB | Dodávateľské faktúry |
| CSB | Hotovostné pokladne |
| SOB | Bankové výpisy |

## Príklad

```
Skupina 3: Skladníci - práva na príjemky
─────────────────────────────────────────────────────────────────
RghtGrp   = 3
BookType  = "IMB"
BookNum   = "00001"  (Hlavný sklad)
BookRight = "EIMP"   (Vstup, Vkladanie, Úprava, Tlač)
─────────────────────────────────────────────────────────────────
RghtGrp   = 3
BookType  = "IMB"
BookNum   = "00002"  (Reklamačný sklad)
BookRight = "EP"     (Len vstup a tlač - read only)
```

## Algoritmus kontroly práv

```pascal
function GetBookRight(pBookType: Str3; pBookNum: Str5): Str30;
begin
  // Predvolené práva z INI
  If not gIni.ValueExists('SYSTEM','Rights') then
    gIni.WriteString('SYSTEM','Rights','EIDMPVLOA');
  Result := gIni.ReadString('SYSTEM','Rights','EIDMPVCOA');

  // Alternatívne: z BKGRGHT tabuľky
  // dmSYS.btBKGRGHT.IndexName := 'RgBtBn';
  // If dmSYS.btBKGRGHT.FindKey([RghtGrp, pBookType, pBookNum]) then
  //   Result := dmSYS.btBKGRGHT.FieldByName('BookRght').AsString
  // else
  //   Result := dmSYS.btUSRLST.FieldByName('GlobRght').AsString;
end;

function BookModify(pBookType: Str3; pBookNum: Str5; pMsgEnab: boolean): boolean;
begin
  Result := Pos('M', GetBookRight(pBookType, pBookNum)) > 0;
  If pMsgEnab and not Result then
    ShowMsg(ecSysUsrNotModifyRight, '');
end;
```

## Použitie

- Kontrola práv pri otváraní knihy
- Kontrola práv pri pridávaní dokladu
- Kontrola práv pri mazaní dokladu
- Kontrola práv pri tlači
- Konfigurácia prístupov na úrovni jednotlivých kníh

## Business pravidlá

- Ak záznam neexistuje, použijú sa globálne práva z USRLST.GlobRght
- Práva sa kontrolujú pri každej operácii
- 'A' (AllOpen) je najvyššia úroveň pre prácu s uzatvorenými dokladmi
- BookNum = '*' môže znamenať všetky knihy daného typu

## Príklady kombinácií práv

| Práva | Popis |
|-------|-------|
| EIDMPVLOA | Plný prístup (administrátor) |
| EIMP | Štandardný používateľ (bez mazania) |
| EP | Read-only s tlačou |
| E | Len prezeranie |
| EIMPLO | Používateľ s právom otvárať vlastné doklady |

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
