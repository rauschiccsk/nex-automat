# ANDROS Server - Príručka pre servisného technika

**Pre:** Servisný technik (fyzická inštalácia)  
**Zákazník:** ANDROS s.r.o.  
**Dátum:** 2026-01-28

---

## 1. PREHĽAD

Tento dokument popisuje:
1. Fyzické pripojenie servera do serverovne
2. Nastavenie pracovných staníc pre pripojenie na server

**Poznámka:** Do operačného systému servera sa neprihlasujete. Všetky nastavenia OS vykoná vzdialene administrátor (Zoltán Rausch).

---

## 2. HARDVÉR

| Parameter | Hodnota |
|-----------|---------|
| Server | Dell PowerEdge R740XD |
| Rack | 2U |
| Napájanie | 2x 750W redundant (C13/C14) |
| Sieťové porty | 4x RJ45 (použije sa **eno4** - štvrtý port) |
| iDRAC port | Samostatný RJ45 port (označený "iDRAC") |
| Service Tag | GZ5L3N2 |

---

## 3. FYZICKÁ INŠTALÁCIA

### 3.1 Umiestnenie do racku

1. Server zasuňte do racku
2. Zaistite server skrutkami/kolejničkami
3. Pripojte obe napájacie káble (redundancia)

### 3.2 Sieťové pripojenie

Server má viacero sieťových portov. Pripojte tieto:

| Port | Kábel do | Poznámka |
|------|----------|----------|
| **eno4** (4. port zhora) | Switch/Router | Hlavná sieť |
| **iDRAC** (samostatný) | Switch/Router | Vzdialená správa |

**Schéma zadného panelu:**

```
┌──────────────────────────────────────────────────────────────┐
│  [PSU1]  [PSU2]    [eno1][eno2][eno3][eno4]  [iDRAC]        │
│                           sieť →  └──POUŽIŤ   └──POUŽIŤ      │
└──────────────────────────────────────────────────────────────┘
```

### 3.3 Zapnutie servera

1. Pripojte napájacie káble
2. Počkajte 30 sekúnd (iDRAC sa inicializuje)
3. Stlačte tlačidlo napájania na prednom paneli
4. Server sa spustí automaticky (boot trvá cca 3-5 minút)

---

## 4. IP ADRESY

Server má pridelené tieto IP adresy:

| Zariadenie | IP adresa | MAC adresa | Účel |
|------------|-----------|------------|------|
| Ubuntu Server | 192.168.55.250 | 84:16:0c:2a:16:b9 | Hlavný OS |
| iDRAC | 192.168.55.251 | *na štítku servera* | Vzdialená správa |
| Windows VM | *interná* | - | RDP server pre používateľov |

**Gateway:** 192.168.55.1

**Poznámka:** Ak router používa DHCP rezervácie, MAC adresa Ubuntu servera je **84:16:0c:2a:16:b9**. IP adresy .250 a .251 sú na konci rozsahu, aby nekolidovali s DHCP pre pracovné stanice.

---

## 5. OVERENIE FUNKČNOSTI

### 5.1 Test pripojenia (z akejkoľvek pracovnej stanice v sieti)

Otvorte príkazový riadok (cmd) a zadajte:

```
ping 192.168.55.250
```

Očakávaný výstup:
```
Reply from 192.168.55.250: bytes=32 time<1ms TTL=64
```

### 5.2 Informovať administrátora

Po úspešnom ping teste kontaktujte:

| Meno | Email | Telefón |
|------|-------|---------|
| Zoltán Rausch | rausch@icc.sk | +421 905 354 536 |

Administrátor vzdialene dokončí konfiguráciu servera.

---

## 6. NASTAVENIE PRACOVNÝCH STANÍC

### 6.1 Požiadavky na pracovnú stanicu

- Windows 10/11
- Pripojenie do rovnakej siete ako server
- Remote Desktop Client (štandardne súčasťou Windows)

### 6.2 Vytvorenie RDP pripojenia

**Krok 1:** Otvoriť Remote Desktop Connection
- Stlačiť `Win + R`
- Napísať `mstsc`
- Stlačiť Enter

**Krok 2:** Nastaviť pripojenie

| Parameter | Hodnota |
|-----------|---------|
| Computer | 192.168.55.250:33389 |
| User name | *podľa zoznamu používateľov* |

**Dôležité:** Port **33389** je povinný! Bez portu sa pripojenie nepodarí.

**Krok 3:** Uložiť pripojenie
1. Kliknúť na "Show Options"
2. V záložke "General" kliknúť "Save As..."
3. Uložiť na plochu ako "ANDROS Server.rdp"

### 6.3 Prvé prihlásenie

Pri prvom prihlásení sa zobrazí bezpečnostné upozornenie o certifikáte. Kliknite **"Yes"** pre pokračovanie.

### 6.4 Zoznam používateľov

| Používateľ | Heslo | Poznámka |
|------------|-------|----------|
| *zoznam dodá administrátor* | | |

---

## 7. VYTVORENIE SKRATKY NA PLOCHE

### 7.1 Uložený RDP súbor

1. Pravý klik na plochu → Nový → Odkaz
2. Umiestnenie: `mstsc /v:192.168.55.250:33389`
3. Názov: `ANDROS Server`
4. Zmeniť ikonu (voliteľné): Pravý klik → Vlastnosti → Zmeniť ikonu

### 7.2 Alternatíva - .rdp súbor

Vytvoriť textový súbor `ANDROS Server.rdp` s obsahom:

```
full address:s:192.168.55.250:33389
username:s:
prompt for credentials:i:1
screen mode id:i:2
desktopwidth:i:1920
desktopheight:i:1080
```

---

## 8. RIEŠENIE PROBLÉMOV

### 8.1 Ping nefunguje

| Možná príčina | Riešenie |
|---------------|----------|
| Server nie je zapnutý | Skontrolovať LED na prednom paneli |
| Zlý sieťový kábel | Vymeniť kábel, skontrolovať LED na porte |
| Zlý port | Skúsiť iný port na switchi |
| IP konflikt | Overiť, že žiadne iné zariadenie nemá 192.168.55.250 |

### 8.2 RDP sa nepripojí

| Možná príčina | Riešenie |
|---------------|----------|
| Chýba port | Zadať **192.168.55.250:33389** (s portom!) |
| Server nie je plne naštartovaný | Počkať 5-10 minút po zapnutí |
| Firewall na stanici | Dočasne vypnúť Windows Firewall |
| Zlá IP adresa | Overiť IP: 192.168.55.250:33389 |

### 8.3 Certifikát upozornenie

Toto je normálne pri prvom pripojení. Kliknite "Yes" pre akceptovanie.

---

## 9. ČAKANIE NA ADMINISTRÁTORA

Po fyzickom pripojení servera a overení ping testu počkajte na administrátora, ktorý:

1. Vzdialene sa pripojí na server
2. Dokončí sieťovú konfiguráciu
3. Overí funkčnosť všetkých služieb
4. Potvrdí, že je možné nastavovať pracovné stanice

**Nepokúšajte sa prihlasovať na server** kým administrátor nepotvrdí pripravenosť.

---

## 10. KONTAKTY

| Rola | Meno | Email | Telefón |
|------|------|-------|---------|
| Administrátor | Zoltán Rausch | rausch@icc.sk | +421 905 354 536 |
| Zákazník | ANDROS s.r.o. | | |

---

## 11. POZNÁMKY PRE TECHNIKA

- Server automaticky spustí všetky služby po zapnutí
- Windows VM (virtuálny počítač) sa spustí automaticky s Ubuntu serverom
- Boot proces trvá 3-5 minút
- Ak sa server nespustí do 10 minút, kontaktujte administrátora
- **NEPOUŽÍVAJTE** fyzickú konzolu na serveri (klávesnica/monitor)
- **RDP port 33389** je zámerne neštandardný (bezpečnosť) - nezabudnite ho uviesť pri pripájaní!