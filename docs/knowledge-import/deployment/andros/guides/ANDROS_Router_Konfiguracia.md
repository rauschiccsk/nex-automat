# ANDROS Server - Konfigurácia routera

**Pre:** Externá firma spravujúca internetové pripojenie  
**Zákazník:** ANDROS s.r.o.  
**Dátum:** 2026-02-03  
**Verejná IP:** 87.244.203.135

---

## 1. PREHĽAD

Žiadame o konfiguráciu port forwardingu pre nový server. Server bude pripojený do lokálnej siete s IP adresou **192.168.55.250**. Druhá IP adresa **192.168.55.251** je pre vzdialenú správu servera (iDRAC).

---

## 2. POŽADOVANÉ PORT FORWARDING PRAVIDLÁ

### 2.1 Základné služby (Ubuntu Server - 192.168.55.250)

| Služba | Externý port | Protokol | Interná IP | Interný port | Priorita |
|--------|--------------|----------|------------|--------------|----------|
| SSH (Ubuntu) | 22 | TCP | 192.168.55.250 | 22 | Vysoká |
| SSH (Windows VM) | 22122 | TCP | 192.168.55.250 | 22122 | Vysoká |
| RDP | 33389 | TCP | 192.168.55.250 | 33389 | Vysoká |
| HTTP | 80 | TCP | 192.168.55.250 | 80 | Vysoká |
| HTTPS | 443 | TCP | 192.168.55.250 | 443 | Vysoká |

**Poznámka:** RDP a SSH pre Windows VM používajú neštandardné porty z bezpečnostných dôvodov (ochrana pred automatizovanými útokmi).

### 2.2 Email Server - Stalwart (192.168.55.250)

| Služba | Externý port | Protokol | Interná IP | Interný port |
|--------|--------------|----------|------------|--------------|
| SMTP | 25 | TCP | 192.168.55.250 | 25 |
| SMTPS | 465 | TCP | 192.168.55.250 | 465 |
| Submission | 587 | TCP | 192.168.55.250 | 587 |
| IMAP | 143 | TCP | 192.168.55.250 | 143 |
| IMAPS | 993 | TCP | 192.168.55.250 | 993 |
| POP3 | 110 | TCP | 192.168.55.250 | 110 |
| POP3S | 995 | TCP | 192.168.55.250 | 995 |
| ManageSieve | 4190 | TCP | 192.168.55.250 | 4190 |
| Mail Admin HTTPS | 8443 | TCP | 192.168.55.250 | 8443 |

### 2.3 FTP Server (192.168.55.250)

| Služba | Externý port | Protokol | Interná IP | Interný port |
|--------|--------------|----------|------------|--------------|
| FTP Control | 21 | TCP | 192.168.55.250 | 21 |
| FTP Passive | 30000-30100 | TCP | 192.168.55.250 | 30000-30100 |
| SFTP | 22023 | TCP | 192.168.55.250 | 22 |

**Poznámka:** FTP Passive vyžaduje rozsah 101 portov (30000 až 30100 vrátane).

### 2.4 Vzdialená podpora - RustDesk (192.168.55.250)

| Služba | Externý port | Protokol | Interná IP | Interný port |
|--------|--------------|----------|------------|--------------|
| RustDesk TCP | 21115 | TCP | 192.168.55.250 | 21115 |
| RustDesk ID | 21116 | TCP + UDP | 192.168.55.250 | 21116 |
| RustDesk Relay | 21117 | TCP | 192.168.55.250 | 21117 |
| RustDesk Web | 21118 | TCP | 192.168.55.250 | 21118 |
| RustDesk API | 21119 | TCP | 192.168.55.250 | 21119 |

**Dôležité:** Port 21116 musí byť otvorený pre TCP aj UDP!

### 2.5 Jitsi Meet - Videokonferencie (192.168.55.250)

| Služba | Externý port | Protokol | Interná IP | Interný port |
|--------|--------------|----------|------------|--------------|
| Jitsi Video/Audio | 10000 | UDP | 192.168.55.250 | 10000 |

**Poznámka:** Jitsi Meet používa HTTPS (port 443) a HTTP (port 80) - tieto sú už definované v sekcii 2.1. Port 10000/UDP je kritický pre kvalitu video/audio prenosu.

**URL po konfigurácii:** https://meet.icc.sk

### 2.6 Vzdialená správa servera - iDRAC (192.168.55.251)

| Služba | Externý port | Protokol | Interná IP | Interný port |
|--------|--------------|----------|------------|--------------|
| iDRAC HTTPS | 9443 | TCP | 192.168.55.251 | 443 |
| iDRAC Virtual Console | 5900 | TCP | 192.168.55.251 | 5900 |
| iDRAC Virtual Media | 5901 | TCP | 192.168.55.251 | 5901 |

**Poznámka:** Port 8443 je použitý pre Stalwart Mail admin, preto iDRAC používa 9443.

### 2.7 Starý Windows Server 2012 (192.168.55.253) - EXISTUJÚCE

| Služba | Externý port | Protokol | Interná IP | Interný port |
|--------|--------------|----------|------------|--------------|
| RDP (starý) | 23389 | TCP | 192.168.55.253 | 3389 |

**Poznámka:** Toto pravidlo už existuje, ponechať bez zmeny.

---

## 3. SÚHRN PORTOV

### Celkový počet pravidiel: 26 + 1 existujúce

**TCP porty:** 21, 22, 25, 80, 110, 143, 443, 465, 587, 993, 995, 4190, 5900, 5901, 8443, 9443, 21115, 21116, 21117, 21118, 21119, 22023, 22122, 23389, 33389

**UDP porty:** 10000, 21116

**Rozsah portov:** 30000-30100 (101 portov)

---

## 4. REZERVÁCIE IP ADRIES (DHCP)

Ak router prideľuje IP cez DHCP, prosíme o rezerváciu týchto adries:

| MAC adresa | IP adresa | Poznámka |
|------------|-----------|----------|
| **84:16:0c:2a:16:b9** | 192.168.55.250 | Hlavný server (Ubuntu) |
| *zistí servisný technik z iDRAC* | 192.168.55.251 | iDRAC (správa) |

**Poznámka:** MAC adresu iDRAC zistí servisný technik z nálepky na serveri alebo z iDRAC web rozhrania.

---

## 5. KONTAKT

V prípade otázok kontaktujte:

| Meno | Email | Telefón |
|------|-------|---------|
| Zoltán Rausch | rausch@icc.sk | +421 905 354 536 |

---

## 6. TESTOVANIE

Po konfigurácii budeme testovať dostupnosť z internetu. Prosíme o potvrdenie, keď bude konfigurácia dokončená.

Testovacie príkazy (z externej siete):
```
telnet 87.244.203.135 22      # SSH Ubuntu
telnet 87.244.203.135 22122   # SSH Windows VM
telnet 87.244.203.135 33389   # RDP
telnet 87.244.203.135 443     # HTTPS
telnet 87.244.203.135 993     # IMAPS
```

Test Jitsi Meet:
```
# Z prehliadača otvoriť: https://meet.icc.sk
# UDP test (vyžaduje netcat s UDP podporou):
nc -u -v 87.244.203.135 10000
```