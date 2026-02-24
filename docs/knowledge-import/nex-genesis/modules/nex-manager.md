# NEX Manager - Centrum riadenia NEX Genesis

## Popis

NEX Manager je hlavný riadiaci modul celého NEX Genesis systému. Slúži ako centrálny bod pre:
- Prihlásenie používateľov do systému
- Kontrolu licencií a prístupových práv
- Navigáciu medzi všetkými programovými modulmi
- Správu používateľských nastavení a session

## Hlavný formulár

**Súbor:** `AppModules\NexManager\Nex_F.pas`

```
TF_NexF (Main Form)
├── Menu Bar (M_xxx)
│   ├── M_Bam - Bázová evidencia
│   ├── M_Biz - Obchodná činnosť
│   ├── M_Spm - Zásobovanie
│   ├── M_Stm - Sklad
│   ├── M_Whm - Odbyt
│   ├── M_Sem - Servis
│   ├── M_Cam - Registračné pokladnice
│   ├── M_Lgm - Logistika
│   ├── M_Acm - Účtovníctvo
│   ├── M_Fxm - Majetok
│   ├── M_Eco - Ekonomika
│   ├── M_Adm - Administratíva
│   └── M_Mgm - Manažment
├── Action List (100+ akcií A_xxx)
├── ListView (rýchly prístup)
├── Status Bar (verzia, používateľ, rok)
└── E_Mod (rýchle vyhľadávanie modulov)
```

## Architektúra SDI

NEX Manager používa **SDI (Single Document Interface)** vzor s modálnymi oknami:

```pascal
procedure TF_NexF.A_GscExecute(Sender: TObject);
begin
  SrchHide;                                    // Skryť vyhľadávanie
  If F_Gsc=nil then F_Gsc:=TF_Gsc.Create(Application);
  F_Gsc.ShowModal;                             // Modálne zobrazenie
  FreeAndNil (F_Gsc);                          // Uvoľnenie pamäte
  SrchVisible;                                 // Zobraziť vyhľadávanie
end;
```

**Výhody:**
- Jednoduchá správa pamäte (FreeAndNil po zatvorení)
- Zabránenie duplicitným oknám
- Jasný stav aplikácie (jeden modul aktívny)

## Systém prístupových práv

### Trojúrovňová kontrola

```
1. LICENCIA (gNEXLic.ModLst)
   └── Má zákazník zakúpený modul?

2. SKUPINA PRÁV (APMDEF tabulka)
   └── Má skupina používateľa prístup k modulu?

3. KNIHA PRÁV (BKGRGHT tabulka)
   └── Má používateľ prístup ku konkrétnej knihe?
```

### Kontrola pri štarte (ModuleSetting)

```pascal
procedure TF_NexF.ModuleSetting;
begin
  // Základná evidencia
  A_GSC.Enabled:=gNexRight.Enabled(cGsc);  A_GSC.Visible:=A_GSC.Enabled;
  A_PAB.Enabled:=gNexRight.Enabled(cPab);  A_PAB.Visible:=A_PAB.Enabled;

  // Sklad
  A_IMB.Enabled:=gNexRight.Enabled(cImb);  A_IMB.Visible:=A_IMB.Enabled;
  A_OMB.Enabled:=gNexRight.Enabled(cOmb);  A_OMB.Visible:=A_OMB.Enabled;

  // ... pre všetky moduly

  // Nastavenie viditeľnosti menu skupín
  M_Stm.Visible:=M_Stc.Visible or M_Imb.Visible or M_Omb.Visible or ...;
end;
```

### Práva na úrovni kníh (BookRight.pas)

```pascal
// Typy práv
E - Enable    // Vstup do knihy
I - Insert    // Pridávanie záznamov
D - Delete    // Mazanie záznamov
M - Modify    // Úprava záznamov
P - Print     // Tlač zostáv
V - Property  // Nastavenie vlastností
L - DocLock   // Automatické uzatváranie dokladov
O - OwnOpen   // Otvoriť vlastné uzatvorené doklady
A - AllOpen   // Otvoriť všetky uzatvorené doklady

// Príklad kontroly
If BookModify('IMB','00001',TRUE) then
  // Používateľ môže upravovať záznamy v knihe IMB 00001
```

## Globálne objekty

### gvSys (TSysVar) - Systémové premenné

```pascal
TSysVar = record
  ActYear: Str4;           // Aktuálny účtovný rok (2025)
  LoginName: Str8;         // Prihlasovacie meno (JAN.KOV)
  LoginGroup: word;        // Skupina práv (0 = admin)
  UserName: Str30;         // Celé meno (Ján Kováč)
  UsrLev: byte;            // Úroveň prístupu (1=admin, 2=power, 3=user)
  UsrNum: word;            // Číselný kód používateľa
  Language: Str2;          // Jazyk (SK, CZ, HU, RU, UA)
  FirmaName: Str60;        // Názov firmy
  WriNum: word;            // Číslo prevádzky
  EasLdg: boolean;         // Jednoduché účtovníctvo
  Discret: boolean;        // Prístup k diskrétnym údajom (NC, zisk)
  AccDvz: Str3;            // Účtovná mena (EUR)
  RpcUse: boolean;         // Použitie požiadaviek na zmeny cien
end;
```

### gPath (TPaths) - Adresárová štruktúra

```pascal
TPaths = class
  NexPath: string;    // C:\NEX\
  ActPath: string;    // C:\NEX\YEARACT\     (aktuálny rok)
  SysPath: string;    // C:\NEX\SYSTEM\      (systémové súbory)
  StkPath: string;    // C:\NEX\YEARACT\STK\ (sklad)
  LdgPath: string;    // C:\NEX\YEARACT\LDG\ (účtovníctvo)
  TmpPath: string;    // Dočasné súbory
  PrivPath: string;   // Súkromné nastavenia používateľa
end;
```

### gNexRight (TNexRight) - Kontrola práv modulov

```pascal
TNexRight = class
  function Enabled(pModul: byte): boolean;     // Má prístup k modulu?
  function Registered(pModul: byte): boolean;  // Je modul licencovaný?
end;
```

### gRgh (TNexRgh) - Práva používateľa

```pascal
TNexRgh = class
  property Service: boolean;  // Servisné práva
end;
```

## Konštanty programových modulov

```pascal
// Bázová evidencia
cGsc = 10;   // Evidencia tovaru
cPab = 11;   // Evidencia partnerov
cPls = 12;   // Tvorba predajných cien
cWgh = 13;   // Elektronické váhy
cApl = 14;   // Akciové ceny

// Zásobovanie
cPsb = 20;   // Plánovanie objednávok
cOsb = 21;   // Dodávateľské objednávky
cTsb = 22;   // Dodávateľské dodacie listy
cKsb = 26;   // Komisionálne vyúčtovanie

// Sklad
cStk = 34;   // Skladové karty
cImb = 35;   // Príjemky
cOmb = 36;   // Výdajky
cRmb = 37;   // Medziskladové presuny
cCpb = 45;   // Kalkulácie

// Odbyt
cOcb = 61;   // Odberateľské zákazky
cTcb = 63;   // Dodacie listy
cIcb = 64;   // Faktúry
cScb = 65;   // Servisné zákazky

// Registračné pokladnice
cCab = 80;   // Knihy pokladníc
cCai = 81;   // Informácie predaja
cSab = 82;   // Skladové výdajky MO

// Účtovníctvo
cIdb = 92;   // Interné doklady
cCsb = 93;   // Hotovostné pokladne
cSob = 94;   // Bankové výpisy
cIsb = 97;   // Dodávateľské faktúry
cJrn = 99;   // Denník zápisov
```

## Inicializácia systému

### NexInitialize (NexInit.pas)

```pascal
procedure NexInitialize(pShowLogin: boolean);
begin
  // 1. Vytvorenie globálnych objektov
  gIni := TNexIni.Create;
  gSet := TNexSet.Create;
  gPath := TPaths.Create;
  gRgh := TNexRgh.Create;
  gBok := TBok.Create;
  gAfc := TAfc.Create;
  gKey := TKey.Create;
  gPlc := TPlc.Create;
  gNexRight := TNexRight.Create;

  // 2. Vytvorenie dátových modulov
  dmSYS := TdmSYS.Create(Application);
  dmSTK := TdmSTK.Create(Application);
  dmDLS := TdmDLS.Create(Application);
  dmCAB := TdmCAB.Create(Application);
  dmLDG := TdmLDG.Create(Application);
  // ...

  // 3. Načítanie nastavení
  gIni.LoadSettings;
  gSet.LoadSettings;
end;
```

### Login proces (NexLgn.pas)

```pascal
function ExecuteNexLgn: boolean;
begin
  // 1. Načítanie zoznamu organizácií z INI
  LoadOrganizations(cOrgLstFile);

  // 2. Výber organizácie a pracoviska
  SelectOrganization;

  // 3. Overenie hesla
  If VerifyPassword then begin
    // 4. Nastavenie gvSys premenných
    SetLoginName(LoginName);
    SetUserName(UserName);
    gvSys.LoginGroup := GrpNum;
    gvSys.UsrLev := UsrLev;

    // 5. Nastavenie privátnych ciest
    SetPrivPathsVars;

    Result := TRUE;
  end;
end;
```

## Rýchle vyhľadávanie modulov

Pole E_Mod umožňuje rýchly prístup cez skratky:

```pascal
procedure TF_NexF.E_ModChange(Sender: TObject);
begin
  If UpString(E_Mod.AsString)='GSC' then A_GscExecute(Self);
  If UpString(E_Mod.AsString)='PAB' then A_PabExecute(Self);
  If UpString(E_Mod.AsString)='PLS' then A_PlsExecute(Self);
  If UpString(E_Mod.AsString)='IMB' then A_ImbExecute(Self);
  // ...
end;
```

## Prepnutie používateľa (bez reštartu)

```pascal
procedure TF_NexF.L_UserNameDblClick(Sender: TObject);
begin
  NexDestroy;                    // Zrušenie session
  NexLogined;                    // Nový login
  NexInitialize(TRUE);           // Reinicializácia
  ModuleSetting;                 // Nastavenie práv
  L_ActYear.Caption := gvSys.ActYear;
  L_UserName.Caption := gvSys.UserName;
end;
```

## Tabuľky používateľského systému

| Tabuľka | Popis | Kľúč |
|---------|-------|------|
| USRLST | Zoznam používateľov | LoginName |
| USRGRP | Skupiny používateľov | GrpNum |
| APMDEF | Práva modulov podľa skupín | GrpNum + PmdMark |
| BKGRGHT | Práva kníh podľa skupín | RghtGrp + BookType + BookNum |
| USRSET | Nastavenia formulárov | LoginName + FormName |
| USRMON | Monitorovanie prihlásených | LoginName |
| SYSTEM | Systémové údaje firmy | MyPaIno |

## Workflow prihlásenia

```
1. Spustenie NEX.exe
   ↓
2. Načítanie konfigurácie (cOrgLstFile)
   ↓
3. Výber organizácie a pracoviska
   ↓
4. Zadanie prihlasovacích údajov
   ↓
5. Overenie v USRLST
   ↓
6. Načítanie práv skupiny (APMDEF)
   ↓
7. NexInitialize - vytvorenie objektov
   ↓
8. ModuleSetting - nastavenie menu
   ↓
9. Zobrazenie hlavného okna
```

## Licenčný systém

```pascal
// gNEXLic.ModLst obsahuje zakúpené moduly
// Formát: ;MOD1;MOD2;MOD3;

// Príklady licenčných modulov
NEX - Základný systém (GSC, PAB, STK)
PLM - Predajné ceny
IMM - Príjemky
ICM - Faktúry
REM - Registračné pokladnice
```

## Súvisiace súbory

- `NexInit.pas` - Inicializácia systému
- `NexLgn.pas` - Login funkcionalita
- `NexPath.pas` - Správa ciest
- `NexRight.pas` - Práva modulov
- `BookRight.pas` - Práva kníh
- `NexRgh.pas` - Konštanty modulov
- `IcVariab.pas` - Globálne premenné

## Stav migrácie

- [x] Analýza hlavného formulára
- [x] Dokumentácia prístupových práv
- [x] Dokumentácia globálnych objektov
- [x] Dokumentácia tabuliek
- [ ] PostgreSQL model pre USRLST
- [ ] PostgreSQL model pre APMDEF
- [ ] API endpoint pre autentifikáciu
- [ ] API endpoint pre autorizáciu
