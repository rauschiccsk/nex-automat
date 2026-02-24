# ANDROS Server - Tesne pred odpojením

**Pre:** Zoltán Rausch  
**Dátum:** 2026-01-28  
**Účel:** Finálne kroky TESNE PRED fyzickým odpojením servera

**⚠️ POZOR:** Po vykonaní týchto krokov server NEBUDE fungovať na pôvodnom mieste!

---

## 1. PREREKVIZITY

Pred pokračovaním overiť, že prípravné kroky sú dokončené:

```bash
# Overiť existenciu súborov
ls -la /etc/netplan/99-static.yaml
ls -la /root/switch-network.sh
ls -la /root/iptables-production.sh
ls -la /opt/rustdesk/docker-compose.yml
```

Ak niektorý súbor chýba, vrátiť sa k dokumentu **"Príprava TERAZ"**.

---

## 2. INFORMOVAŤ POUŽÍVATEĽOV

⏰ **Minimálne 1 hodinu pred odpojením:**

- [ ] Informovať všetkých používateľov o plánovanom výpadku
- [ ] Dohodnúť čas odpojenia
- [ ] Overiť, že nikto nepracuje na serveri

---

## 3. KONTROLA PRED VYPNUTÍM

### 3.1 Overiť stav služieb

```bash
# Docker kontajnery
docker ps

# Windows VM
sudo virsh list --all

# Disk usage
df -h
```

### 3.2 Uložiť aktuálny stav

```bash
# Aktuálne iptables pravidlá
sudo iptables-save > /root/iptables-before-shutdown.rules

# Aktuálna IP
ip addr show eno4 > /root/ip-before-shutdown.txt

# Timestamp
echo "Shutdown initiated: $(date)" >> /root/shutdown-log.txt
```

---

## 4. VYPNUTIE WINDOWS VM

```bash
# Graceful shutdown
sudo virsh shutdown win2025

# Počkať na vypnutie (max 2-3 minúty)
watch -n 5 'sudo virsh list --all'
```

Očakávaný výstup po vypnutí:
```
 Id   Name      State
--------------------------
 -    win2025   shut off
```

**Ak sa VM nevypne do 3 minút:**
```bash
# Force shutdown (len ak graceful nefunguje)
sudo virsh destroy win2025
```

---

## 5. ZASTAVENIE DOCKER KONTAJNEROV

```bash
# Zastaviť všetky kontajnery
cd /opt/nex-automat
sudo docker compose down

# Overiť
docker ps
```

Očakávaný výstup: žiadne bežiace kontajnery.

---

## 6. SYNC DISKOV

```bash
# Zabezpečiť, že všetky dáta sú zapísané na disk
sudo sync
sudo sync
sudo sync
```

---

## 7. VYPNUTIE UBUNTU SERVERA

```bash
# Finálne vypnutie
sudo shutdown -h now
```

---

## 8. FYZICKÉ ODPOJENIE

**Po úplnom vypnutí servera (LED zhasnú):**

1. [ ] Počkať 30 sekúnd po zhasnutí LED
2. [ ] Odpojiť sieťový kábel z **eno4**
3. [ ] Odpojiť sieťový kábel z **iDRAC**
4. [ ] Odpojiť **oba** napájacie káble
5. [ ] Označiť káble (ktorý je eno4, ktorý iDRAC)

---

## 9. TRANSPORT

### 9.1 Bezpečnostné opatrenia

- [ ] Server prepravovať vo vodorovnej polohe
- [ ] Chrániť pred nárazmi a vibráciami
- [ ] Neprepravovať v extrémnych teplotách

### 9.2 Čo zobrať so serverom

- [ ] Server Dell PowerEdge R740XD
- [ ] Oba napájacie káble
- [ ] Sieťové káble (2x - jeden pre eno4, jeden pre iDRAC)
- [ ] Dokumentáciu (vytlačené príručky)

---

## 10. ČASOVÝ PLÁN ODPOJENIA

| Čas | Akcia |
|-----|-------|
| T-60 min | Informovať používateľov |
| T-30 min | Kontrola, že nikto nepracuje |
| T-15 min | Záloha stavu, kontrola služieb |
| T-10 min | Vypnutie Windows VM |
| T-5 min | Zastavenie Docker, sync |
| T-0 | Vypnutie Ubuntu |
| T+1 min | Odpojenie káblov |

**Celkový čas: ~15-20 minút** (od začiatku vypínania po odpojenie)

---

## 11. KONTAKT NA SERVISNÉHO TECHNIKA

Pred odpojením overiť:

- [ ] Servisný technik je pripravený na novom mieste
- [ ] Router je nakonfigurovaný (port forwarding)
- [ ] IP adresy sú rezervované (192.168.55.250, 192.168.55.251)

---

## 12. ROLLBACK (AK TREBA ODLOŽIŤ)

Ak sa presun odloží a server treba znova spustiť:

1. Pripojiť napájacie káble
2. Pripojiť sieťové káble
3. Zapnúť server (tlačidlo na prednom paneli)
4. Počkať 5 minút na plný boot
5. Všetko by malo fungovať automaticky (DHCP, autostart VM)

---

## 13. PO ODPOJENÍ

**Nezabudnúť:**

- [ ] Hetzner VPS (46.224.229.55) **ZATIAĽ NEVYPÍNAŤ** - bude slúžiť ako fallback
- [ ] DNS záznamy **ZATIAĽ NEMENIŤ** - zmeniť až po overení funkčnosti na novom mieste