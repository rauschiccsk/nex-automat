# USRMON - Monitorovanie prihlásených používateľov

## Kľúčové slová / Aliases

USRMON, USRMON.BTR, monitorovanie používateľov, user monitoring, sessions, relácie

## Popis

Tabuľka monitorovania aktuálne prihlásených používateľov. Sleduje kto je prihlásený, kedy sa prihlásil a aký modul práve používa. Globálny súbor.

## Btrieve súbor

`USRMON.BTR`

## Umiestnenie

`C:\NEX\SYSTEM\USRMON.BTR`

## Štruktúra polí (8 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| LoginName | Str8 | 9 | Prihlasovacie meno používateľa |
| FullName | Str30 | 31 | Celé meno používateľa |
| UserCode | word | 2 | Číselný kód používateľa |

### Časové údaje

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| LoginDate | DateType | 4 | Dátum prihlásenia do systému |
| LoginTime | TimeType | 4 | Čas prihlásenia do systému |
| RefrTime | TimeType | 4 | Čas poslednej kontroly/refresh |

### Stav

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| UseModul | Str40 | 41 | Aktuálne používaný programový modul |
| Coommand | Str5 | 6 | Príkaz pre daného používateľa |

## Indexy (1)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | LoginName | LoginName | Unikátny, Case-insensitive |

## Príkazy (Coommand)

| Hodnota | Popis |
|---------|-------|
| (prázdne) | Žiadny príkaz |
| LOGOF | Odhlásenie používateľa |
| CLOSE | Zatvorenie aktuálneho modulu |
| REFR | Obnovenie dát |
| MSG | Zobrazenie správy |

## Príklad

```
LoginName = "JAN.KOV"
FullName  = "Ján Kováč"
UserCode  = 1234
LoginDate = 15.01.2024
LoginTime = 08:30:00
RefrTime  = 14:25:32
UseModul  = "ICB - Odberateľské faktúry"
Coommand  = ""
```

## Workflow

```
1. Prihlásenie používateľa
   ↓
   USRMON.Insert(LoginName, LoginDate, LoginTime)
   ↓
2. Vstup do modulu
   ↓
   USRMON.UseModul := 'GSC - Evidencia tovaru'
   ↓
3. Periodický refresh (každých 60s)
   ↓
   USRMON.RefrTime := Now
   ↓
4. Odhlásenie
   ↓
   USRMON.Delete(LoginName)
```

## Použitie

- Prehľad prihlásených používateľov
- Detekcia "mŕtvych" session (RefrTime starší ako threshold)
- Vzdialené odhlásenie používateľov (Coommand = 'LOGOF')
- Sledovanie využitia modulov
- Licenčná kontrola (počet súčasných používateľov)

## Business pravidlá

- Jeden záznam = jeden prihlásený používateľ
- Záznam sa vymaže pri korektnom odhlásení
- RefrTime sa aktualizuje periodicky
- Ak RefrTime > 5 minút starý, session je považovaná za neaktívnu
- Pri núdzovom ukončení môže ostať "osirelý" záznam

## Čistenie osirelých záznamov

```
// Pseudo-kód
DELETE FROM USRMON
WHERE RefrTime < (NOW - 10 minút)
  AND Coommand = ''
```

## Súvisiace funkcie

```pascal
// Registrácia prihlásenia
procedure RegisterLogin;
begin
  dmSYS.btUSRMON.Insert;
  dmSYS.btUSRMON.FieldByName('LoginName').AsString := gvSys.LoginName;
  dmSYS.btUSRMON.FieldByName('FullName').AsString := gvSys.UserName;
  dmSYS.btUSRMON.FieldByName('LoginDate').AsDateTime := Date;
  dmSYS.btUSRMON.FieldByName('LoginTime').AsDateTime := Time;
  dmSYS.btUSRMON.Post;
end;

// Aktualizácia modulu
procedure UpdateModule(pModuleName: string);
begin
  If dmSYS.btUSRMON.FindKey([gvSys.LoginName]) then begin
    dmSYS.btUSRMON.Edit;
    dmSYS.btUSRMON.FieldByName('UseModul').AsString := pModuleName;
    dmSYS.btUSRMON.FieldByName('RefrTime').AsDateTime := Time;
    dmSYS.btUSRMON.Post;
  end;
end;
```

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint (WebSocket pre real-time monitoring)
