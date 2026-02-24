# USRSET - Nastavenia formulárov používateľov

## Kľúčové slová / Aliases

USRSET, USRSET.BTR, nastavenia používateľov, user settings, osobné nastavenia

## Popis

Tabuľka uchovávania používateľských nastavení jednotlivých formulárov a komponentov. Umožňuje persistenciu pozícií okien, šírky stĺpcov, filtrov a ďalších používateľských preferencií. Globálny súbor.

## Btrieve súbor

`USRSET.BTR`

## Umiestnenie

`C:\NEX\SYSTEM\USRSET.BTR`

## Štruktúra polí (4 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| LoginName | Str8 | 9 | Prihlasovacie meno používateľa |
| FormName | Str20 | 21 | Názov formulára |
| CompName | Str20 | 21 | Názov komponentu |
| Setting | blob | variabilný | Uložené nastavenie (serializované) |

## Indexy (1)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | LoginName, FormName, CompName | LnFnCn | Unikátny, Case-insensitive |

## Typy nastavení

### Pozície okien

```
FormName = "F_Gsc"
CompName = "Form"
Setting  = "Left=100;Top=50;Width=800;Height=600;State=wsNormal"
```

### Šírky stĺpcov gridu

```
FormName = "F_Gsc"
CompName = "Grid"
Setting  = "Col0=100;Col1=200;Col2=80;Col3=120;Col4=150"
```

### Poradie stĺpcov

```
FormName = "F_Gsc"
CompName = "GridOrder"
Setting  = "0,2,1,3,4,5"
```

### Filtre

```
FormName = "F_Gsc"
CompName = "Filter"
Setting  = "GsType=1;GsState=A;GsCat=05"
```

### Zoradenie

```
FormName = "F_Icb"
CompName = "Sort"
Setting  = "IcDate DESC;IcNum ASC"
```

## Príklad

```
LoginName = "JAN.KOV"
FormName  = "F_Icb"
CompName  = "DBGrid1"
Setting   = "Col0=80;Col1=120;Col2=250;Col3=100;Col4=80;Col5=100"
─────────────────────────────────────────────────────────────────
LoginName = "JAN.KOV"
FormName  = "F_Icb"
CompName  = "Form"
Setting   = "Left=50;Top=30;Width=1200;Height=700"
─────────────────────────────────────────────────────────────────
LoginName = "JAN.KOV"
FormName  = "F_Gsc"
CompName  = "QuickFilter"
Setting   = "LastSearch=notebook;SearchField=GsName"
```

## Použitie

- Uloženie rozmerov a pozície okna
- Uloženie šírky stĺpcov v gridoch
- Uloženie poradia stĺpcov
- Uloženie posledných filtrov/vyhľadávaní
- Uloženie predvoleného zoradenia
- Uloženie používateľských preferencií komponentov

## Workflow

```
1. Otvorenie formulára
   ↓
   LoadSettings(FormName)
   ↓
   ApplySettings(Components)
   ↓
2. Práca používateľa (zmena rozmerov, stĺpcov, ...)
   ↓
3. Zatvorenie formulára
   ↓
   CollectSettings(Components)
   ↓
   SaveSettings(FormName)
```

## Implementácia

```pascal
procedure SaveFormSettings(pForm: TForm);
var mSetting: string;
begin
  mSetting := Format('Left=%d;Top=%d;Width=%d;Height=%d',
    [pForm.Left, pForm.Top, pForm.Width, pForm.Height]);

  SaveUserSetting(gvSys.LoginName, pForm.Name, 'Form', mSetting);
end;

procedure LoadFormSettings(pForm: TForm);
var mSetting: string;
begin
  mSetting := LoadUserSetting(gvSys.LoginName, pForm.Name, 'Form');
  If mSetting <> '' then begin
    pForm.Left := GetSettingValue(mSetting, 'Left');
    pForm.Top := GetSettingValue(mSetting, 'Top');
    pForm.Width := GetSettingValue(mSetting, 'Width');
    pForm.Height := GetSettingValue(mSetting, 'Height');
  end;
end;
```

## Business pravidlá

- Nastavenia sú viazané na LoginName (každý používateľ má svoje)
- Ak nastavenie neexistuje, použijú sa predvolené hodnoty
- Setting pole môže byť prázdne (= predvolené)
- Pri zmene štruktúry formulára môžu byť staré nastavenia nekompatibilné

## Čistenie nastavení

```
// Vymazanie nastavení pre formulár
DELETE FROM USRSET
WHERE LoginName = 'JAN.KOV'
  AND FormName = 'F_Gsc'

// Vymazanie všetkých nastavení používateľa
DELETE FROM USRSET
WHERE LoginName = 'JAN.KOV'
```

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model (JSON pre Setting)
- [ ] API endpoint
