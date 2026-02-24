# WireGuard VPN - Návod na pripojenie k ANDROS serveru

## 1. Inštalácia WireGuard klienta

### Windows
1. Stiahni WireGuard z https://www.wireguard.com/install/
2. Spusti inštalátor a nainštaluj aplikáciu
3. Po inštalácii sa WireGuard spustí automaticky

### Android
1. Otvor Google Play Store
2. Vyhľadaj "WireGuard"
3. Nainštaluj aplikáciu od WireGuard Development Team

### iOS (iPhone/iPad)
1. Otvor App Store
2. Vyhľadaj "WireGuard"
3. Nainštaluj aplikáciu

---

## 2. Import konfigurácie

### Windows
1. Spusti WireGuard aplikáciu
2. Klikni na **Import tunnel(s) from file** (alebo Ctrl+O)
3. Vyber súbor `andros.conf` ktorý si dostal
4. Tunel sa zobrazí v zozname ako "andros"

### Android
1. Otvor WireGuard aplikáciu
2. Klikni na modré **+** tlačidlo
3. Vyber **Import from file or archive**
4. Nájdi a vyber súbor `andros.conf`

### Alternatíva - manuálne zadanie (ak nemôžeš importovať súbor)
1. Klikni na **+** → **Create from scratch** (alebo **Add empty tunnel**)
2. Zadaj názov: `andros`
3. Skopíruj celý obsah konfigurácie do textového poľa

---

## 3. Pripojenie k VPN

### Windows
1. V zozname tunelov vyber **andros**
2. Klikni na tlačidlo **Activate**
3. Status sa zmení na "Active" so zeleným indikátorom
4. V system tray uvidíš WireGuard ikonu

### Android
1. V zozname tunelov nájdi **andros**
2. Klikni na prepínač vedľa názvu tunela
3. Pri prvom pripojení potvrď povolenie VPN
4. V notifikačnej lište uvidíš kľúčik (VPN aktívna)

---

## 4. Overenie pripojenia

Po aktivácii VPN otestuj pripojenie:

### Test 1 - Ping na VPN server
Otvor príkazový riadok (cmd) alebo terminál a zadaj:
```
ping 10.10.0.1
```
Mal by si dostať odpovede.

### Test 2 - Ping na Ubuntu server
```
ping 192.168.100.23
```

### Test 3 - Ping na Windows VM
```
ping 192.168.122.75
```

---

## 5. Pripojenie na Windows Server cez Remote Desktop

1. Otvor **Remote Desktop Connection** (mstsc.exe)
2. Do poľa Computer zadaj: `192.168.122.75`
3. Klikni **Connect**
4. Zadaj prihlasovacie údaje (dostaneš od administrátora)

---

## 6. Odpojenie od VPN

### Windows
- Klikni na **Deactivate** v WireGuard aplikácii

### Android
- Vypni prepínač vedľa tunela "andros"

---

## Riešenie problémov

### VPN sa nepripája
- Over, že máš internetové pripojenie
- Skontroluj, či firewall neblokuje UDP port 51820
- Skús reštartovať WireGuard aplikáciu

### Ping nefunguje, ale VPN je aktívna
- Skontroluj, či je tunel skutočne v stave "Active"
- Over v WireGuard aplikácii, či sa zvyšuje hodnota "Data received"

### Remote Desktop nefunguje
- Over, že VPN je aktívna (ping 10.10.0.1 funguje)
- Skús ping 192.168.122.75
- Kontaktuj administrátora

---

## Kontakt

Pri problémoch kontaktuj: **Zoltán Rausch**

---

## Technické údaje (pre referenciu)

| Parameter | Hodnota |
|-----------|---------|
| VPN Server | andros-vpn.duckdns.org:51820 |
| Tvoja VPN IP | 10.10.0.2 |
| Ubuntu Server | 192.168.100.23 |
| Windows VM (RDP) | 192.168.122.75 |
| Protokol | WireGuard (UDP) |